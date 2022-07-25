# -*- coding: utf-8 -*-
# © 2017 Syvain Van Hoof (Okia sprl) <sylvainvh@okia.be>
# © 2018 Jacques-Etienne Baudoux (BCIM sprl) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class PickingZone(models.Model):
    _name = "picking.zone"

    name = fields.Char("Name", required=True, translate=True)
    code = fields.Char("Code", required=True)

    _sql_constraints = [
        ("unique_picking_zone", "unique (code)", "The picking zone code must be unique")
    ]
