# -*- coding: utf-8 -*-
# Copyright 2022 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    wms_wave_size = fields.Integer(
        string="WMS Wave Size",
        help="Amount of pickings performed at the same time",
        default=1,
    )
