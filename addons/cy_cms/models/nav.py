# -*- coding: utf-8 -*-
from odoo import fields, models, api, tools
import json


class Nav(models.Model):
    ''' cy_nav model'''
    _name = 'cy.nav'
    _inherit = 'cy.element.email.base'
    _order = 'sequence'
    _description = '导航'

    home_id = fields.Many2one('cy.home', string='首页', index=True)
    name = fields.Char(string='名称', required=True, size=63)
    mobile_items = fields.One2many('cy.nav.mobile.item', 'nav_id', '手机端楼层(m web,iOS,Android)')
    desktop_items = fields.One2many('cy.nav.desktop.item', 'nav_id', '桌面端列(pc web)')
    action = fields.Many2one('cy.action', string='点击动作', index=True)
    active = fields.Boolean(string='是否生效', default=True, tracking=True, required=True, index=True)
    sequence = fields.Integer(string='排序', index=True)


class NavMobileItem(models.Model):
    ''' cy_nav_mobile_item model'''
    _name = 'cy.nav.mobile.item'
    _inherit = 'cy.element.base'
    _order = 'sequence'
    _description = '导航楼层'

    nav_id = fields.Many2one('cy.nav', string='导航', index=True)
    item_type = fields.Selection([
        ('rotation_image', '轮播图'),
        ('row_image', '整行图'),
        ('column2_image', '两列图'),
        ('column3_image', '3列图'),
    ], string='楼层类型', required=True, size=31)
    images = fields.One2many('cy.nav.mobile.item.image', 'item_id', string='图片列表')
    images_text = fields.Char(compute='_compute_images_text', store=False, string='图片列表')

    @api.depends('images')
    def _compute_images_text(self):
        for record in self:
            if record.images:
                image_urls = list(filter(lambda x: x and True or False, [x.is_show and x.image_url for x in record.images]))
                record.images_text = ','.join(image_urls[:6])
            else:
                record.images_text = False


class NavMobileItemImage(models.Model):
    ''' cy_nav_mobile_item_image model'''
    _name = 'cy.nav.mobile.item.image'
    _inherit = 'cy.element.base'
    _order = 'sequence'
    _description = '导航楼层'

    item_id = fields.Many2one('cy.nav.mobile.item', string='楼层', index=True)
    image_url = fields.Char(string='图片', size=255)
    action = fields.Many2one('cy.action', string='点击动作', index=True)


class NavDesktopItem(models.Model):
    ''' cy_nav_desktop_item model'''
    _name = 'cy.nav.desktop.item'
    _inherit = 'cy.element.base'
    _order = 'sequence'
    _description = '导航楼层'

    nav_id = fields.Many2one('cy.nav', string='导航', index=True)
    item_type = fields.Selection([('row_image', '整行图'), ('text_link', '文本链接'), ('division_line', '分割线')], string='楼层类型', required=True, size=31)
    images = fields.One2many('cy.nav.desktop.item.image', 'item_id', string='图片列表')
    images_text = fields.Char(compute='_compute_images_text', store=False, string='图片列表')
    texts = fields.One2many('cy.nav.desktop.item.text', 'item_id', string='文本列表')
    texts_text = fields.Char(compute='_compute_texts_text', store=False, string='文本列表')

    @api.depends('images')
    def _compute_images_text(self):
        for record in self:
            if record.images:
                image_urls = list(filter(lambda x: x and True or False, [x.is_show and x.image_url for x in record.images]))
                record.images_text = ','.join(image_urls[:6])
            else:
                record.images_text = False

    @api.depends('texts')
    def _compute_texts_text(self):
        for record in self:
            if record.texts:
                texts = list(filter(lambda x: x and True or False, [x.is_show and x.text for x in record.texts]))
                record.texts_text = ','.join(texts[:3])+'...'
            else:
                record.texts_text = False


class NavDesktopItemImage(models.Model):
    ''' cy_nav_desktop_item_image model'''
    _name = 'cy.nav.desktop.item.image'
    _inherit = 'cy.element.base'
    _order = 'sequence'
    _description = '导航楼层图片'

    item_id = fields.Many2one('cy.nav.desktop.item', string='楼层', index=True)
    image_url = fields.Char(string='图片', size=255)
    action = fields.Many2one('cy.action', string='点击动作', index=True)


class NavDesktopItemText(models.Model):
    ''' cy_nav_desktop_item_text model'''
    _name = 'cy.nav.desktop.item.text'
    _inherit = 'cy.element.base'
    _order = 'sequence'
    _description = '导航楼层文本'

    item_id = fields.Many2one('cy.nav.desktop.item', string='楼层', index=True)
    text = fields.Char(string='文本', size=63)
    font_weight = fields.Selection([('normal', '正常'), ('bold', '粗体，顶部有间距')], string='文本类型', required=True, default='normal', size=31)
    color = fields.Char(string='文字颜色', default='#000000', size=15)
    action = fields.Many2one('cy.action', string='点击动作', index=True)


class NavBottom(models.Model):
    ''' cy_nav_bottom model'''
    _name = 'cy.nav.bottom'
    _inherit = 'cy.mail.thread'
    _order = 'sequence'
    _description = '底部导航'

    name = fields.Char(string='名字', size=63)
    nav_type = fields.Selection([
        ('home', '首页'),
        ('nav', '分类导航'),
        ('cart', '购物车'),
        ('mine', '我的'),
        ('page', '页面'),
    ], string='导航类型', required=True, size=31)
    page_id = fields.Many2one('cy.page', string='页面')
    icon = fields.Char(string='正常图标(wh>132px)', size=255)
    icon_active = fields.Char(string='选中图标(wh>132px)', size=255)
    is_show = fields.Boolean(string='是否显示', default=True, index=True)
    sequence = fields.Integer(string='排序', index=True)

    def action_release_navbottom(self):
        inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
        for record in self:
            bizContent = {}
            data = {
                'module': 'cms',
                'version': '2.0',
                'method': 'CmsApi.NavBottomRelease',
                'bizContent': json.dumps(bizContent)
            }
            result = self.env['cy.base'].request_has_sign(inside_gateway_link, data)

            if result and result.get('errorCode', 5001) == 0:
                record.message_post(body='底部导航发布成功')
            else:
                record.message_post(body='底部导航发布失败，'+result.get('errorMsg', ''))
