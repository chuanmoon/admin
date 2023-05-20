from odoo import models, fields, api


class BrowseHistory(models.Model):
    _name = 'cy.product.browse.history'
    _description = '商品浏览记录'
    _sql_constraints = [('spu_id_owner_unique', 'UNIQUE(owner,spu_id)', 'spu_id不可重复')]
    _order = 'id desc'

    owner = fields.Char(string='拥有者', required=True, index=True, size=128)
    spu_id = fields.Integer(string='spu_id', required=True)
