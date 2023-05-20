from odoo import models, fields


class User(models.Model):
    ''' cy_user model'''
    _name = 'cy.user'
    _description = ''' 用户账户信息 '''
    _sql_constraints = [('email_unique', 'UNIQUE(email)', 'email不可重复')]
    _rec_name = 'email'

    email = fields.Char(string='用户邮箱', required=True, size=127)
    email_verified = fields.Boolean(string='邮箱已验证')
    password = fields.Char(string='密码', required=True, size=127)
    nickname = fields.Char(string='昵称', size=63)
    state = fields.Selection(string='用户状态', selection=[('active', '激活'), ('frozen', '冻结')], default='active', index=True, size=31)


class UserLog(models.Model):
    ''' cy_user_log model'''
    _name = 'cy.user.log'
    _description = ''' 用户日志信息 '''

    user_id = fields.Many2one("cy.user", string="用户ID", required=True, index=True)
    content = fields.Char(string='日志内容', size=127)


class UserDevice(models.Model):
    ''' cy_user_device model'''
    _name = 'cy.user.device'
    _description = ''' 用户设备 '''
    _log_access = False
    _sql_constraints = [('device_id_unique', 'UNIQUE(device_id)', '设备不可重复')]

    user_id = fields.Many2one("cy.user", string="用户ID", index=True)
    device_id = fields.Char(string='设备ID', size=127)
    app_version = fields.Char(string='APP版本号', index=True, size=31)
    push_token = fields.Char(string='push token', size=63)
    create_date = fields.Datetime(string='创建时间')
    write_date = fields.Datetime(string='写入时间')
