import odoo.exceptions
from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    regn_no = fields.Char(string="Regn No.")