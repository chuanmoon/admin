from logging import StringTemplateStyle
from odoo import fields, models, api


class PtShare(models.Model):
    _name = "cy.share"

    _share_channels = [
        ("facebook", "Facebook"),
        ("whatsapp", "Whatsapp"),
        ("instagram", "Instagram"),
        ("message", "Message"),
        ("link", "Link"),
        ("default", "Default")
    ]

    name = fields.Char(string="名称", size=128)
    template = fields.Text(string="分享连接模板")
    active = fields.Boolean(string="时候生效", default=True)
    channel = fields.Selection(selection=_share_channels, string="渠道", default='link', size=64)
