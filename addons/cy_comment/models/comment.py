from enum import Flag
from typing import Sequence
from odoo import fields, api, models


class Comment(models.Model):
    _name = 'cy.product.comment'
    _order = 'order_type,sequence desc,create_date desc'
    _description = '''用户对订单和商品的评价'''
    _sql_constraints = [('comment_product_unique', 'UNIQUE(order_id,sku_id)', '重复评论'), ('extend_id_unique', 'UNIQUE(extend_id)', '重复评论')]

    order_id = fields.Integer(string="订单ID", required=True, index=True)
    spu_id = fields.Integer(string="SPU ID", index=True)
    skc_id = fields.Integer(string="SKC ID", index=True)
    sku_id = fields.Integer(string="SKU ID", index=True)
    user_id = fields.Many2one('cy.user', string="用户ID")
    user_name = fields.Char(string='用户名称', compute="_user_name", store=True, size=63)

    score = fields.Float(string="用户评分", default=5)
    image_urls = fields.Text(string="评价图片")
    content = fields.Char(string="评价内容", size=500)
    fit_level = fields.Selection(selection=[('1', "Small"), ('2', 'True To Size'), ('3', 'Large')], default='2', size=31)
    sequence = fields.Integer(string='排序')
    order_type = fields.Selection(selection=[('1', '手动排序'), ('2', '高分有图'), ('3', '高分无图'), ('4', '低分')], default='1', size=31)
    color_name = fields.Char(string="颜色", size=63)
    size_name = fields.Char(string="尺寸", size=63)

    active = fields.Boolean(string='是否显示')
    extend_id = fields.Char(string='扩展ID', size=128, default=None)

    statics_id = fields.Many2one('cy.product.comment.statics', string="评论统计")

    @api.depends("user_id")
    def _user_name(self):
        for item in self:
            if item.user_id:
                item.user_name = item.user_id.email
            else:
                item.user_name = ""

    @api.depends("sku_id")
    def _skc_id(self):
        for item in self:
            if item.sku_id:
                item.skc_id = item.sku_id.skc_id
                item.spu_id = item.sku_id.spu_id
            else:
                item.skc_id = 0
                item.spu_id = 0

    def write(self, vals):
        sequence = vals.get('sequence', 0)
        if sequence > 0:
            vals['order_type'] = '1'
        return super(Comment, self).write(vals)


class CommentStatics(models.Model):
    _name = 'cy.product.comment.statics'
    _sql_constraints = [('spu_id_unique', 'UNIQUE(spu_id)', '重复评论')]

    spu_id = fields.Many2one('cy.product.spu', string="SPU ID", required=True, ondelete="cascade")

    total = fields.Integer(string='评论总数', default=0, store=False, compute="_cal_sum", readonly=True)
    star_sum = fields.Float(string='评分总数', default=0, store=False, compute="_cal_sum", readonly=True)
    small_sum = fields.Integer(string='偏小数量', default=0, store=False, compute="_cal_sum", readonly=True)
    fit_sum = fields.Integer(string='正好数量', default=0, store=False, compute="_cal_sum", readonly=True)
    big_sum = fields.Integer(string='偏大数量', default=0, store=False, compute="_cal_sum", readonly=True)

    comments = fields.One2many("cy.product.comment", "statics_id", string="评论列表", context={'active_test': False})

    @api.depends("comments")
    def _cal_sum(self):
        for record in self:
            total = 0
            small = 0
            fit = 0
            big = 0
            count = 0
            if record.comments:
                for comment in record.comments:
                    if not comment.active:
                        continue
                    count += 1
                    total += comment.score
                    record.star_sum += comment.score
                    if comment.fit_level == "1":
                        small += 1
                    if comment.fit_level == "2":
                        fit += 1
                    if comment.fit_level == "3":
                        big += 1

            record.small_sum = small
            record.fit_sum = fit
            record.big_sum = big
            record.star_sum = total
            record.total = count
