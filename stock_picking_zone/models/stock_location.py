# -*- coding: utf-8 -*-
# Copyright 2017 Sylvain Van Hoof <svh@sylvainvh.be>
# Copyright 2018 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    picking_zone_id = fields.Many2one("picking.zone", string="Picking zone")
