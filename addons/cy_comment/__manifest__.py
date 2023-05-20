{
    'name': "CY Comment",
    'summary': 'chuanmoon comment',
    'description': """ CY 评价管理 """,
    'author': 'yinshuwei',
    'website': "https://chuanmoon.com/",
    'category': 'Website/Website',
    'depends': ['base', 'mail', 'web', 'cy_public', 'cy_product', 'cy_account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/comment_static.xml',
        'views/comment.xml',
        'views/menu.xml'
    ],
    'sequence': 2,
    'installable': True,
    'application': True,
    'auto_install': True
}
