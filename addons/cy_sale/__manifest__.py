# -*- coding: utf-8 -*-
{
    'name': "CY Sale",
    'summary': 'chuanmoon sale',
    'description': """ CY 销售中心 """,
    'author': '尹术伟',
    'website': "https://chuanmoon.com/",
    'category': 'Website/Website',
    'depends': ['base', 'mail', 'web', 'cy_public', 'cy_product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/coupon_rule.xml',
        'views/promotion.xml',
        'views/menu.xml'
    ],
    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': True,
}
