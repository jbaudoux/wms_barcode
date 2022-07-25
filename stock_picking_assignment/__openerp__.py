# Copyright 2016 Syvain Van Hoof (Okia sprl) <sylvainvh@okia.be>
# Copyright 2016-2019 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Picking Assignment',
    'version': '12.0.1.0.0',
    'category': 'Stock Management',
    'author': 'BCIM, Sylvain Van Hoof',
    'summary': "Assign operator on picking",
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_picking.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
