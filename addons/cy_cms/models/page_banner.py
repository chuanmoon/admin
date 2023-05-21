from odoo import fields, models, api, tools
import json


class PageBanner(models.Model):
    _name = 'cy.cms.page.banner'
    _rec_name = "name"
    _inherit = 'cy.element.email.base'

    _page_type = [
        ("whats_new", "新品"),
        ("flash_sale", "闪购"),
        ("user_center", "个人中心"),
        ("collection", "商品列表"),
        ("search", "搜索结果"),
    ]

    name = fields.Char(string='名称', required=True, size=255)
    page_type = fields.Selection(_page_type, string='页面类型', required=True)
    m_images = fields.Char(string='M图片', size=255)
    pc_images = fields.Char(string='PC图片', size=255)
    is_show = fields.Boolean(string='是否显示', default=True, required=True, index=True, copy=False)
    param = fields.Char(string='参数', size=255)  # 用于额外区分

    def action_release_page(self):
        inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
        for record in self:
            bizContent = {
                'pageType': record.page_type,
            }
            data = {
                'module': 'cms',
                'version': '2.0',
                'method': 'CmsApi.PageBannerRelease',
                'bizContent': json.dumps(bizContent)
            }
            result = self.env['cy.base'].request_has_sign(inside_gateway_link, data)

            if result and result.get('errorCode', 5001) == 0:
                record.message_post(body='页面发布成功')
            else:
                record.message_post(body='页面发布失败，'+result.get('errorMsg', ''))
