# Copyright 2019 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def wms_version(self):
        return '1.0.0'

    def _wms_select_recover_picking(self, domain, limit):
        return self.search(domain, limit=limit)

    def _wms_select_assigned_picking(self, domain, limit):
        return self.search(domain, limit=limit)

    def _wms_select_new_picking(self, domain, limit):
        return self.search(domain, limit=limit)

    @api.model
    def wms_start_picking(self, picking_type_ids, operator_id, nbr=1):
        picking = self._wms_select_recover_picking([
            ('operator_id', '=', operator_id),
            ('printed', '=', True),
            ('picking_type_id', 'in', picking_type_ids),
            ('state', 'in', ('partially_available', 'assigned'))],
            limit=nbr)

        if len(picking) < nbr:
            picking |= self._wms_select_assigned_picking([
                ('operator_id', '=', operator_id),
                ('printed', '=', True),
                ('picking_type_id', 'in', picking_type_ids),
                ('state', 'in', ('partially_available', 'assigned'))],
                limit=(nbr - len(picking)))

        if len(picking) < nbr:
            picking |= self._wms_select_new_picking([
                ('operator_id', '=', False),
                ('picking_type_id', 'in', picking_type_ids),
                ('state', 'in', ('partially_available', 'assigned'))],
                limit=(nbr - len(picking)))

        # Mark picking as started
        picking.filtered(lambda p: not p.printed or not p.operator_id)\
               .write({'operator_id': operator_id, 'printed': True})

        return picking.wms_picking_load()

    def wms_picking_load(self):
        pickings = []
        for p in self:
            ml = []
            for line in p.move_line_ids:
                d = {
                    'id': line.id,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.display_name,
                    'product_qty': line.product_uom_qty,
                    'product_qty_done': line.qty_done,
                    'location_src': {
                        'id': line.location_id.id,
                        'name': line.location_id.name,
                        'corridor': line.location_id.corridor,
                        'barcode': line.location_id.barcode,
                    }
                }
                if not line.lot_id:
                    d.update({
                        'lot_id': line.lot_id.id,
                    })
                    ml.append(d)
            pickings.append({
                'id': p.id,
                'name': p.name,
                'partner': {
                    'id': p.partner_id.id,
                    'name': p.partner_id.display_name,
                },
                # 'delivery_round': {
                #     'name': p.delivery_round_id.display_name,
                # },
                'lines': ml,
            })
        return pickings

    def wms_picking_set_qty(self, line_id, qty, new_lot_id=False):
        self.ensure_one()
        line = self.move_line_ids.browse(line_id)
        if not line:
            raise UserError(_('Operation not found'))
        if line.lot_id and line.lot_id.id != new_lot_id:
            # Another lot has been picked
            line = line.copy(default={
                'product_uom_qty': 0,
                'lot_id': new_lot_id,
            })
        line.qty_done += qty

    def wms_put_in_pack(self, nbr_packages=1):
        self.ensure_one()
        operations = any(x for x in self.move_line_ids if x.qty_done > 0 and (not x.result_package_id))
        if operations:
            pack = self.with_context(
                default_nbr_packages=self.nbr_packages)._put_in_pack()
            return pack.name
        packs = self.move_line_ids.mapped('result_package_id')
        if packs:
            return packs[0].name

    def wms_transfer(self):
        self.action_done()
