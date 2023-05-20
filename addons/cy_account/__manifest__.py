{
    'name': 'CY Account',
    'version': '1.0.0',
    'summary': '用户账户',
    'category': '商城',
    'author': 'chuanmoon',
    'maintainer': 'yinshuwei',
    'website': 'https://chuanmoon.com',
    'depends': [
            'cy_public', "web"
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/user_group.xml',
        'views/shipping.xml',
        'views/shipping_rule.xml',
        'views/mailing_list.xml',
        'views/country.xml',
        'views/user.xml',
        'views/menu.xml',
    ],
    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': True
}
