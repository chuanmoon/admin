{
    'name': "CY Orders",
    'version': '1.0.0',
    'summary': 'chuanmoon order manager',
    'description': """ CY 订单管理 """,
    'author': 'chuanmoon',
    'website': "https://chuanmoon.com/",
    'category': 'Website/Website',
    'depends': ['base', 'mail', 'web', 'cy_base', 'cy_product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/order.xml',
        'views/reason.xml',
        'views/menu.xml'
    ],
    'sequence': 2,
    'installable': True,
    'application': True,
    'auto_install': True,
}
