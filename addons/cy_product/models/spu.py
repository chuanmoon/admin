from odoo import fields, models, api


class Spu(models.Model):
    ''' cy_product_spu 商品SPU '''
    _name = 'cy.product.spu'
    _rec_name = "spu_sn"
    _inherit = 'cy.mail.thread'
    _sql_constraints = [('spu_sn_unique', 'UNIQUE(spu_sn)', 'spu_sn不可重复')]
    _description = '''Standard Product Unit'''

    category_id = fields.Many2one('cy.product.category', string="分类", index=True)
    spu_sn = fields.Char(string="SPU SN", size=31)
    skus = fields.One2many('cy.product.sku', 'spu_id', string='SKU列表')
    sku_count = fields.Integer(compute="_compute_sku_count", store=False, string="sku数量")
    active = fields.Boolean(string="是否有效", default=True, tracking=True, index=True)

    @api.depends("skus")
    def _compute_sku_count(self):
        for record in self:
            record.sku_count = len(record.skus)

    @api.model_create_multi
    def create(self, vals_list):
        result = super(Spu, self).create(vals_list)
        if result.id:
            result.write({'spu_sn': 'SPU%010d' % result.id})
        return result
