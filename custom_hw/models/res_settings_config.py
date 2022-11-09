import odoo.exceptions
from odoo import fields, models, api

class ResSettingsMrpCustom(models.Model):
    _name = "res.settings.mrp.custom"

    issue_number_granulation = fields.Char(string="Issue No. -- Granulation")
    date_of_issue_granulation = fields.Date(string="Date of Issue -- Granulation")
    revision_no_granulation = fields.Char(string="Revision No. -- Granulation")
    issue_number_compression = fields.Char(string="Issue No. -- Compression")
    date_of_issue_compression = fields.Date(string="Date of Issue -- Compression")
    revision_no_compression = fields.Char(string="Revision No. -- Compression")
