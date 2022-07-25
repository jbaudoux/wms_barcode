# Copyright 2022 Jacques-Etienne Baudoux (BCIM sprl) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_uom_id = fields.Many2one(
        'product.uom', string='Unit of Measure', related='product_id.uom_id',
        readonly=True)
