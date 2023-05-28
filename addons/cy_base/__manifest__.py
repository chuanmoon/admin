# -*- coding: utf-8 -*-
{
    'name': "CY Base",
    'version': '1.0.0',
    'summary': 'chuanmoon base',
    'description': """ CY 公共组件 """,
    'author': 'chuanmoon',
    'website': "https://chuanmoon.com/",
    'category': 'Website/Website',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'view/records.xml',
        'view/base.xml',
        'view/action.xml',
        'view/lang.xml',
        'view/currency.xml',
        'view/menu.xml'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'sequence': 0,
    'installable': True,
    'application': True,
    'auto_install': True,
}
