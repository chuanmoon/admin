{
    'name': "CY Orders",
    'summary': 'chuanmoon order manager',
    'description': """ CY 订单管理 """,
    'author': 'yinshuwei',
    'website': "https://chuanmoon.com/",
    'depends': ['base', 'mail', 'web', 'cy_public', 'cy_product'],
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
