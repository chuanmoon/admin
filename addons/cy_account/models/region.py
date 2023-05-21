from odoo import models, fields, api, tools


class Country(models.Model):
    ''' cy_country '''
    _name = 'cy.country'
    _description = '国家'
    _log_access = False
    _sql_constraints = [('region_id_unique', 'UNIQUE(region_id)', 'region_id不可重复')]

    region_id = fields.Many2one('cy.region', string='区域')

    code = fields.Char(string='二字码', index=True, size=7)
    phone_len = fields.Integer(string='手机号长度')
    phone_code = fields.Char(string='手机号区号', size=7)
    time_zone = fields.Char(string='时区', size=31)
    currency_code = fields.Char(string='币种', size=15)

    def apply_now(self):
        for record in self:
            inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
            data = {
                'subj': 'odoo_setting_release',
                'table': 'cy_country',
                'id': str(record.id),
            }
            result = self.env['cy.base'].request_has_sign(inside_gateway_link+'/publish', data)
            print(result)


class Region(models.Model):
    ''' cy_region '''
    _name = 'cy.region'
    _description = '区域'
    _order = 'sequence'
    _rec_name = 'full_name'
    _log_access = False

    name = fields.Char(string='名字', index=True, size=63)
    zh_name = fields.Char(string='中文名', size=63)
    parent_id = fields.Many2one('cy.region', string='父级', index=True)
    full_name = fields.Char(compute='_compute_full_name', store=True, string='全名', size=255)
    level = fields.Integer(string='级别', index=True)
    post_code = fields.Char(string='邮编', size=2047)
    is_remote = fields.Boolean(string='偏远地区')
    sequence = fields.Integer(string='排序', index=True)
    active = fields.Boolean(string='是否可用', default=True, tracking=True, required=True, index=True)
    write_date = fields.Datetime(string='修改时间')

    @api.depends('name', 'parent_id')
    def _compute_full_name(self):
        for record in self:
            if record.parent_id and record.parent_id.full_name:
                record.full_name = record.parent_id.full_name+'/' + (record.name or '')
            else:
                record.full_name = record.name or ''
