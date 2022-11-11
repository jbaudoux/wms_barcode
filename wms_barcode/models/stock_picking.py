# -*- coding: utf-8 -*-
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
    def wms_start_picking(self, picking_type_id, operator_id):
        # FIXME: add picking progress (ongoing)
        self.env.cr.execute("""
            SELECT printed
            FROM stock_picking
            WHERE picking_type_id = %s
            FOR UPDATE
            """, (picking_type_id, ))

        picking_type = self.env["stock.picking.type"].browse(picking_type_id)
        nbr = picking_type.wms_wave_size

        picking = self._wms_select_recover_picking([
            ('operator_id', '=', operator_id),
            ('printed', '=', True),
            ('picking_type_id', '=', picking_type_id),
            ('state', 'in', ('partially_available', 'assigned'))],
            limit=nbr)

        if not picking:
            if len(picking) < nbr:
                picking |= self._wms_select_assigned_picking([
                    ('operator_id', '=', operator_id),
                    ('printed', '=', True),
                    ('picking_type_id', '=', picking_type_id),
                    ('state', 'in', ('partially_available', 'assigned'))],
                    limit=(nbr - len(picking)))

            if len(picking) < nbr:
                picking |= self._wms_select_new_picking([
                    ('operator_id', '=', False),
                    ('picking_type_id', '=', picking_type_id),
                    ('state', 'in', ('partially_available', 'assigned'))],
                    limit=(nbr - len(picking)))

        # Mark picking as started
        picking.filtered(lambda p: not p.printed or not p.operator_id)\
               .write({'operator_id': operator_id, 'printed': True})

        return picking.wms_picking_load()

    def wms_picking_load(self):
        pickings = []
        for p in self:
            if not p.pack_operation_ids:
                # Create the pack operations if they do not exist yet
                p.recheck_availability()
            ml = []
            for line in p.pack_operation_ids:
                d = {
                    'id': line.id,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.display_name,
                    'product_qty': line.product_qty,
                    'product_qty_done': line.qty_done,
                    'location_src': {
                        'id': line.location_id.id,
                        'name': line.location_id.name,
                        'corridor': line.location_id.corridor,
                        #'barcode': line.location_id.barcode,
                    },
                    'package_dest_id': line.result_package_id.id,
                }
                if line.lot_id:
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

    @api.multi
    def wms_picking_set_qty(self, pack_op_id, qty, lot_id, pack_id):
        self.ensure_one()
        line = self.pack_operation_ids.browse(pack_op_id)
        if not line:
            raise UserError(_('Operation not found'))
        if len(line) > 1:
            raise UserError(_('Multiple operations found'))
        # In v8, the lot is on the pack op line
        # if lot_id:
        #     lot = line.pack_lot_ids.filtered(lambda l: l.lot_id.id == lot_id)
        #     if not lot:
        #         line.pack_lot_ids = [(0, 0, {
        #             'lot_id': lot_id, 'qty': qty})]
        #     else:
        #         lot.qty += qty
        line.qty_done = qty
        line.result_package_id = pack_id

    def wms_put_in_pack(self):
        self.ensure_one()
        operations = any(x for x in self.pack_operation_ids if x.qty_done > 0 and (not x.result_package_id))
        if operations:
            pack = self.put_in_pack()  # result is a package and not JSON serializable
            return pack.name
        packs = self.pack_operation_ids.mapped('result_package_id')
        if packs:
            return packs[0].name

    @api.multi
    def wms_transfer(self):
        self.ensure_one()
        if self.state in ('cancel', 'done'):
            return
        self.do_transfer()
