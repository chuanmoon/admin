from odoo import fields, models


class AddressDefault(models.Model):
    ''' cy_address_default 默认地址 '''
    _name = 'cy.address.default'
    _log_access = False

    user_id = fields.Many2one("cy.user", string="用户ID", required=True, index=True)
    address_id = fields.Integer(string="默认地址")  # 不关联，不级联删除


class Address(models.Model):
    ''' cy_address 地址 '''
    _name = 'cy.address'

    user_id = fields.Many2one("cy.user", string="用户ID", required=True, index=True)

    first_name = fields.Char('First Name', size=63)
    last_name = fields.Char('Last Name', size=63)
    phone_number = fields.Char('Phone Number', size=31)
    address_line1 = fields.Char('Address Line 1', size=255)
    address_line2 = fields.Char('Address Line 2', size=255)
    post_code = fields.Char(string="Post/Zip Code", size=31)
    tax_number = fields.Char(string="Tax Number", size=63)
    country = fields.Char(string="Country/Region", size=63)
    state = fields.Char(string="State/Province", size=63)
    city = fields.Char(string="City", size=63)
    country_region_id = fields.Integer(string="Country/Region ID")
    state_region_id = fields.Integer(string="State/Province ID")
    city_region_id = fields.Integer(string="City ID")

    active = fields.Boolean(string='是否有用', index=True, default=True)

    is_for_bill = fields.Boolean(string='是否为账单地址', index=True, default=False)