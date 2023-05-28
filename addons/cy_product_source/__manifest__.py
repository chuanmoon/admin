{
    'name': 'CY Product Source',
    'version': '1.0.0',
    'summary': '商品来源',
    'category': '商品',
    'author': 'chuanmoon',
    'maintainer': 'yinshuwei',
    'website': "https://chuanmoon.com/",
    'category': 'Website/Website',
    'depends': [
            'cy_base', 'web', 'mail', 'cy_product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/product_source.xml',
        'view/menu.xml'
    ],
    'sequence': 1,
    'installable': True,
    'auto_install': True,
    'application': True,
}
