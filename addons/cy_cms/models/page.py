# -*- coding: utf-8 -*-
from odoo import fields, models, api, tools
import json


class Page(models.Model):
    ''' cy_page model'''
    _name = 'cy.page'
    _inherit = 'cy.mail.thread'
    _order = 'id desc'
    _description = '页面'

    name = fields.Char(string='名称', size=63, tracking=True, required=True)
    bg_color = fields.Char(string='背景颜色', default='#FFFFFF', size=15)
    waterfall_tabs = fields.One2many('cy.page.waterfall.tab', 'page_id', '瀑布流')
    active = fields.Boolean(string='是否生效', default=True, tracking=True, required=True, index=True)
    items = fields.One2many('cy.page.item', 'page_id', '楼层')

    def action_release_page(self):
        inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
        for record in self:
            bizContent = {
                'pageId': record.id,
            }
            data = {
                'module': 'cms',
                'version': '2.0',
                'method': 'CmsApi.PageRelease',
                'bizContent': json.dumps(bizContent)
            }
            result = self.env['cy.base'].request_has_sign(inside_gateway_link, data)

            if result and result.get('errorCode', 5001) == 0:
                record.message_post(body='页面发布成功')
            else:
                record.message_post(body='页面发布失败，'+result.get('errorMsg', ''))

    @api.model_create_multi
    def create(self, vals_list):
        result = super(Page, self).create(vals_list)
        for record in result:
            self.env['cy.action'].sync_action(record.name, 'page', str(record.id))
        return result

    def write(self, vals):
        result = super(Page, self).write(vals)
        for record in self:
            self.env['cy.action'].sync_action(record.name, 'page', str(record.id))
        return result


class PageWaterfallTab(models.Model):
    ''' cy_page_waterfall_tab model'''
    _name = 'cy.page.waterfall.tab'
    _inherit = 'cy.element.base'
    _order = 'sequence'
    _description = '瀑布流商品'

    name = fields.Char(string='名称', size=63, required=True)
    page_id = fields.Many2one('cy.page', string='页面', index=True)
    condition_id = fields.Many2one('cy.cms.condition', string='商品集合', index=True)


class PageItem(models.Model):
    ''' cy_page_item model'''
    _name = 'cy.page.item'
    _inherit = 'cy.element.base'
    _order = 'sequence'
    _description = '页面楼层'

    page_id = fields.Many2one('cy.page', string='页面', index=True)
    bg_color = fields.Char(string='背景颜色', default='#FFFFFF', size=15)
    item_type = fields.Selection([
        ('rotation_image', '轮播图'),
        ('slide_image', '横滑图'),
        ('row_image', '整行图'),
        ('flash_sale', '闪购'),
        ('slide_products', '横滑商品'),
        ('products', '商品列表'),
    ], string='楼层类型', required=True, size=31)
    has_margin = fields.Boolean(string='是否有左右边距', default=False)
    screen_count = fields.Float(string='每屏显示图片张数', default=2.2)
    indicator_style = fields.Selection([('in_image', '在图片上的'), ('out_image', '在图片外的'), ('none', '没有指示器')], string='轮播图指示器样式', default='none', size=31)
    flash_sale_id = fields.Many2one('cy.cms.flashsale', string='闪购', index=True)
    condition_id = fields.Many2one('cy.cms.condition', string='商品集合', index=True)
    images = fields.One2many('cy.page.item.image', 'item_id', string='图片列表')
    images_text = fields.Char(compute='_compute_images_text', store=False, string='图片列表')
    images_text_pc = fields.Char(compute='_compute_images_text', store=False, string='图片列表PC')
    product_count = fields.Integer(string='商品展示数量', default=14)

    @api.depends('images')
    def _compute_images_text(self):
        for record in self:
            if record.images:
                image_urls = list(filter(lambda x: x and True or False, [x.is_show and x.image_url for x in record.images]))
                record.images_text = ','.join(image_urls[:6])

                image_url_pc = list(filter(lambda x: x and True or False, [x.is_show and x.image_url_pc for x in record.images]))
                record.images_text_pc = ','.join(image_url_pc[:6])
            else:
                record.images_text = False
                record.images_text_pc = False


class PageItemImage(models.Model):
    ''' cy_page_item_image model'''
    _name = 'cy.page.item.image'
    _inherit = 'cy.element.base'
    _order = 'sequence'
    _description = '页面楼层'

    item_id = fields.Many2one('cy.page.item', string='楼层', index=True)
    image_url = fields.Char(string='图片', size=255)
    image_url_pc = fields.Char(string='PC图片', size=255)
