# Copyright 2022 Jacques-Etienne Baudoux (BCIM sprl) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    barcode = fields.Char(related="loc_barcode")
