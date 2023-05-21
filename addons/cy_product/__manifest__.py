{
    'name': 'CY Product',
    'version': '1.0',
    'summary': '商品管理',
    'category': '商品',
    'author': 'chuanmoon',
    'maintainer': 'yinshuwei',
    'website': "https://chuanmoon.com/",
    'category': 'Website/Website',
    'depends': [
            'cy_base', 'web', 'mail'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'view/product_spu.xml',
        'view/product_skc.xml',
        'view/search.xml',
        'view/product_color.xml',
        'view/product_size.xml',
        'view/product_sku.xml',
        'view/category.xml',
        'view/menu.xml'
    ],
    'sequence': 1,
    'installable': True,
    'auto_install': True,
    'application': True,
}
