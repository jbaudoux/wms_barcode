# Copyright 2016-2019 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    subcode = fields.Char('Code')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    picking_type_subcode = fields.Char(
        related='picking_type_id.subcode', readonly=True
    )


class StockMove(models.Model):
    _inherit = 'stock.move'

    picking_type_subcode = fields.Char(
        related='picking_type_id.subcode', readonly=True
    )
