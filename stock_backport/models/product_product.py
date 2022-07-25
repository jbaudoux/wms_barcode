# Copyright 2022 Jacques-Etienne Baudoux (BCIM sprl) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    tracking = fields.Char(compute='_compute_tracking')

    @api.depends("track_all")
    def _compute_tracking(self):
        for rec in self:
            rec.tracking = rec.track_all and "lot" or "none"
