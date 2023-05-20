# -*- coding: utf-8 -*-

{
    'name': 'CY Cms',
    'version': '1.0',
    'summary': 'chuanmoon cms',
    'sequence': 1,
    'author': 'chuanmoon',
    'description': """
        chuanmoon cms
        Home
        Nav
    """,
    'website': "https://chuanmoon.com/",
    'category': 'Website/Website',
    'depends': ['web', 'mail', 'cy_public', 'cy_product', 'web_notify'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/page.xml',
        'views/home.xml',
        'views/nav_bottom.xml',
        'views/nav.xml',
        'views/condition.xml',
        'views/flashsale.xml',
        'views/popup.xml',
        'views/setting.xml',
        'views/personal_center.xml',
        'views/home_top.xml',
        'views/share.xml',
        'views/page_banner.xml',
        'views/menu.xml',
    ],
    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': True
}
