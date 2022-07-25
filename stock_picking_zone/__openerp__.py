# -*- coding: utf-8 -*-
# © 2016-2018 Jacques-Etienne Baudoux (BCIM)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Picking Zone",
    "version": "8.0.1.0.0",
    "author": "BCIM",
    "maintainer": "Camptocamp",
    "category": "Stock Management",
    "depends": ["stock"],
    "data": [
        "views/picking_zone.xml",
        "views/stock_location.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "application": False,
}
