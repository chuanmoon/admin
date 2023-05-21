from odoo import models, fields, api


class ProductCategoryVariant(models.Model):
    ''' cy_product_category_variant 品类变体属性定义 '''
    _name = 'cy.product.category.variant'
    _description = '''品类变体属性定义'''

    name = fields.Char(string="属性名称", size=255)
    select_values = fields.One2many('cy.product.category.variant.value', 'variant_id', string="属性值列表")
    active = fields.Boolean(string='是否有效', default=True, tracking=True)
    

class ProductCategoryVariantRel(models.Model):
    ''' cy_product_category_variant_rel 品类变体属性关系定义 '''
    _name = 'cy.product.category.variant.rel'
    _description = '''品类变体属性关系定义'''
    _order = 'sequence'

    category_id = fields.Many2one('cy.product.category', string="品类", index=True)
    variant_id = fields.Many2one('cy.product.category.variant', string="属性", index=True)
    sequence = fields.Integer(string="排序", index=True)


class ProductCategoryVariantValue(models.Model):
    ''' cy_product_category_variant_value 品类变体属性值定义 '''
    _name = 'cy.product.category.variant.value'
    _description = '''品类变体属性值定义'''
    _order = 'sequence'

    variant_id = fields.Many2one('cy.product.category.variant', string="属性", index=True)
    name = fields.Char(string="属性值", size=255)
    image_url = fields.Char(string="图片地址", size=255, help="当有图片时，显示在选择按钮上，没有图片时，显示属性值")
    sequence = fields.Integer(string="排序", index=True)
    active = fields.Boolean(string='是否有效', default=True, tracking=True)


class ProductCategoryAttr(models.Model):
    ''' cy_product_category_attr 品类普通属性定义 '''
    _name = 'cy.product.category.attr'
    _description = '''品类普通属性定义'''
    _order = 'sequence'

    name = fields.Char(string="属性名称", size=255)
    active = fields.Boolean(string='是否有效', default=True, tracking=True)

class ProductCategoryAttrRel(models.Model):
    ''' cy_product_category_attr_rel 品类普通属性关系定义 '''
    _name = 'cy.product.category.attr.rel'
    _description = '''品类普通属性关系定义'''
    _order = 'sequence'

    category_id = fields.Many2one('cy.product.category', string="品类", index=True)
    attr_id = fields.Many2one('cy.product.category.attr', string="属性", index=True)
    sequence = fields.Integer(string="排序", index=True)
    