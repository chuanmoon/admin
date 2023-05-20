# -*- coding: utf-8 -*-
{
    'name': "CY Public",
    'summary': 'chuanmoon public',
    'description': """ CY 公共组件 """,
    'author': '尹术伟',
    'website': "https://chuanmoon.com/",
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'view/records.xml',
        'view/public.xml',
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
