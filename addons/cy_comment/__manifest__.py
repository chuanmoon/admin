{
    'name': "CY Comment",
    'version': '1.0.0',
    'summary': 'chuanmoon comment',
    'description': """ CY 评价管理 """,
    'author': 'chuanmoon',
    'website': "https://chuanmoon.com/",
    'category': 'Website/Website',
    'depends': ['base', 'mail', 'web', 'cy_base', 'cy_product', 'cy_account'],
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
