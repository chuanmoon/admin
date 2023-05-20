import random
import re
from datetime import datetime
import logging
from odoo import api, exceptions, fields, models


class FlashSale(models.Model):
    _name = 'cy.cms.flashsale'
    _description = '''
		闪购活动
	'''

    name = fields.Char(string="闪购名称", size=63)
    start_time = fields.Datetime(string='开始时间', default=fields.Datetime.now, required=True, index=True)
    end_time = fields.Datetime(string='结束时间', required=True, index=True)
    active = fields.Boolean(string="是否生效", index=True, default=True)
    skcs = fields.One2many('cy.cms.flashsale.skc', "flashsale_id", string="商品列表")  # domain=['|', ('active', '=', True), ('active', '=', False)], context={'active_test': False}

    @api.constrains('start_time', 'end_time', 'active')
    def _constrains_start_time(self):
        if not self.active:
            return

        if self.end_time < datetime.now():
            raise exceptions.UserError('结束时间不能是过去的时间')
        if self.end_time < self.start_time:
            raise exceptions.UserError('开始时间大于结束时间')
        sql = '''select name from cy_cms_flashsale where active = true and id != %(id)d and ((start_time > '%(start)s' and  end_time  < '%(end)s') or (start_time between '%(start)s' and '%(end)s') or (end_time between '%(start)s' and '%(end)s'))''' % {
            'id': self.id, 'start': self.start_time, 'end': self.end_time}

        logging.getLogger("info").info(sql)
        self.env.cr.execute(sql)
        count = self.env.cr.dictfetchone()
        logging.getLogger("info").info(count)
        if count and count.get('name', None):
            raise exceptions.UserError('当前时间段已经有闪购了:%s' % count.get('name'))

    @api.model_create_multi
    def create(self, vals_list):
        result = super(FlashSale, self).create(vals_list)
        for record in result:
            self.env['cy.action'].sync_action(record.name, 'flashsale', str(record.id))
        return result

    def write(self, vals):
        result = super(FlashSale, self).write(vals)
        for record in self:
            self.env['cy.action'].sync_action(record.name, 'flashsale', str(record.id))
        return result

    def open_cy_cms_flashsale_add_skc_wizard_form(self):
        ''' 批量添加或删除SKC向导 '''
        if len(self) > 0:
            record = self[0]
            return self.env['cy.cms.flashsale.add.skc.wizard'].open(record.id)
        return True

    def open_cy_cms_flashsale_price_wizard_form(self):
        ''' 批量设置价格向导 '''
        if len(self) > 0:
            record = self[0]
            return self.env['cy.cms.flashsale.price.wizard'].open(record.id)
        return True


class FlashsaleAddSkcWizard(models.TransientModel):
    _name = 'cy.cms.flashsale.add.skc.wizard'

    flashsale_id = fields.Many2one('cy.cms.flashsale', string="Flashsale", required=True, ondelete='cascade')
    skcs = fields.Text(string='请输入SKC_SN')

    @api.model
    def open(self, flashsale_id):
        record = self.create({'flashsale_id': flashsale_id})
        res = {
            'name': '批量添加&amp;删除',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env['ir.model.data'].xmlid_to_res_id('cy_cms.cy_cms_flashsale_add_skc_wizard_form'),
            'res_model': 'cy.cms.flashsale.add.skc.wizard',
            'domain': [],
            'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': record.id
        }
        return res

    def remove(self):
        for record in self:
            datas = [[x1 for x1 in re.split(',|\t| |，', x.strip()) if x1.strip() != ''] for x in re.split('\n', record.skcs)]
            skcs = []
            for data in datas:
                if data:
                    skcs.append(data[0])
            skc_list = self.env['cy.product.skc'].search([('skc_sn', 'in', skcs), '|', ('active', '=', True), ('active', '=', False)])
            skc_map = {}
            for skc in skc_list:
                skc_map[skc.skc_sn] = skc

            item_obj = self.env['cy.cms.flashsale.skc']
            for skc_sn in skcs:
                skc = skc_map.get(skc_sn)
                if not skc:
                    raise exceptions.ValidationError('批量删除SKC失败' + 'SKC:'+skc_sn+',不存在或已不可用！')
                item_obj.search([('skc_id', '=', skc.id), ('flashsale_id', '=', record.flashsale_id.id)]).write({'active': False})
            return self.env.user.notify_success(message='成功删除了'+str(len(skcs))+'个商品：'+(','.join(skcs))+'.')

    def save(self):
        for record in self:
            datas = [[x1 for x1 in re.split(',|\t| |，', x.strip()) if x1.strip() != ''] for x in re.split('\n', record.skcs)]
            skcs = []
            for data in datas:
                if data:
                    skcs.append(data[0])
            skc_list = self.env['cy.product.skc'].search([('skc_sn', 'in', skcs), '|', ('active', '=', True), ('active', '=', False)])
            skc_map = {}
            for skc in skc_list:
                skc_map[skc.skc_sn] = skc

            flashsale_id = record.flashsale_id.id
            self.env.cr.execute('''select max(sequence) from cy_cms_flashsale_skc where flashsale_id=%s''', (flashsale_id,))
            seqs = self.env.cr.fetchone()
            seq = seqs[0] or 0

            item_obj = self.env['cy.cms.flashsale.skc']
            for skc_sn in skcs:
                skc = skc_map.get(skc_sn)
                if not skc:
                    raise exceptions.ValidationError('批量添加SKC失败' + 'SKC:'+skc_sn+',不存在或已不可用！')

                items = item_obj.search([('skc_id', '=', skc.id), ('flashsale_id', '=', flashsale_id), '|', ('active', '=', True), ('active', '=', False)])
                if items:
                    items.write({'active': True})
                else:
                    seq = seq + 1
                    item_obj.create({'flashsale_id': flashsale_id, 'skc_id': skc.id, 'sequence': seq,
                                     'active': True, 'limit_qty': 2, 'stock': 200, 'sold_count': random.randint(1, 10),
                                     'price': skc.shop_price})

        return self.env.user.notify_success(message='成功导入了'+str(len(skcs))+'个商品：'+(','.join(skcs))+'.')


class FlashsalePriceWizard(models.TransientModel):
    _name = 'cy.cms.flashsale.price.wizard'

    flashsale_id = fields.Many2one('cy.cms.flashsale', string="Flashsale", required=True, ondelete='cascade')
    price_type = fields.Selection([('rate', '折扣(如9折输入90)'), ('price', '具体值，卖$9.9输入9.9')], string='价格类型', default='rate', size=7)
    rate = fields.Integer(string='折扣')
    price = fields.Float(string='金额')

    @api.model
    def open(self, flashsale_id):
        record = self.create({'flashsale_id': flashsale_id})
        res = {
            'name': '批量设置价格向导',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env['ir.model.data'].xmlid_to_res_id('cy_cms.cy_cms_flashsale_price_wizard_form'),
            'res_model': 'cy.cms.flashsale.price.wizard',
            'domain': [],
            'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': record.id
        }
        return res

    def save(self):
        for record in self:
            if not record.price_type:
                raise exceptions.ValidationError('设置失败: “价格类型”必填')
            if record.price_type == 'rate':
                if not record.rate:
                    raise exceptions.ValidationError('设置失败: “折扣”必填')
                if record.rate > 100 or record.rate < 0:
                    raise exceptions.ValidationError('设置失败: “折扣”必须在0~100之间')
            if record.price_type == 'price' and not record.price:
                raise exceptions.ValidationError('设置失败: “金额”必填')
            skcs = record.flashsale_id.skcs
            for skc in skcs:
                if record.price_type == 'rate':
                    skc.write({'price': skc.skc_id.shop_price*record.rate/100})
                else:
                    skc.write({'price': record.price})
            return self.env.user.notify_success(message='成功设置了'+str(len(skcs))+'个商品价格')


class FlashSaleProduct(models.Model):
    ''' cy_cms_flashsale_skc '''
    _name = 'cy.cms.flashsale.skc'
    _description = '''
		闪购商品SKC
	'''
    _rec_name = "skc_id"
    _order = "sequence desc"
    _sql_constraints = [('flashsale_skc_id_unique', 'UNIQUE(flashsale_id,skc_id)', '商品SKC不可重复')]

    flashsale_id = fields.Many2one('cy.cms.flashsale', string="闪购ID", ondelete="cascade", index=True)
    skc_id = fields.Many2one('cy.product.skc', string="商品SKC", index=True)
    product_images = fields.Char(string="商品图片", compute="_product_images", store=False)
    spu_id = fields.Integer(compute="_spu_id", store=True, string='SPU ID')
    sequence = fields.Integer(string="排序", default=0)
    stock = fields.Integer(string="活动库存", default=200)
    shop_price = fields.Float(string="售价", compute='_shop_price')
    price = fields.Float(string="活动价")
    sold_count = fields.Integer(string="卖出数量", default=0)
    active = fields.Boolean(string="是否生效", index=True, default=True)
    limit_qty = fields.Integer(string="购买上限数量(0不限制)", default=2)

    @ api.depends("skc_id")
    def _spu_id(self):
        for record in self:
            if record.skc_id:
                record.spu_id = record.skc_id.spu_id
            else:
                record.spu_id = 0

    @ api.depends("skc_id")
    def _product_images(self):
        for record in self:
            if record.skc_id:
                record.product_images = record.skc_id.image_urls.split(',')[0]
            else:
                record.product_images = ""

    @api.depends('skc_id')
    def _shop_price(self):
        for record in self:
            record.shop_price = record.skc_id.shop_price
