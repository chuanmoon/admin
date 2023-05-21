{
    'name': "CY Payment",
    'summary': 'chuanmoon payment',
    'description': """ CY 支付配置 """,
    'author': 'yinshuwei',
    'website': "https://chuanmoon.com/",
    'category': 'Website/Website',
    'depends': ['base', 'mail', 'web', 'cy_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/channel.xml',
        'views/records.xml',
        'views/menu.xml'
    ],
    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': True,
}
