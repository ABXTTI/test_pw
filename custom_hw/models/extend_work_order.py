import odoo.exceptions
from odoo import fields, models, api

class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    # Common for all sheets
    issue_no = fields.Char(string="Issue No.")
    revision_no = fields.Char(string="Revision No.")
    date_of_issue = fields.Date(string="Date of Issue")

    # //////////////////// Code For Granulation Sheet ///////////////////////////////////////////
    granulation_sheet_document_no = fields.Char(string="Document No.", compute='document_number')
    production_order_no = fields.Many2one("mrp.production", string="Production Order No.")
    production_order_date = fields.Date(string="Production Order Date")
    granulation_start_date = fields.Date(string="Granulation Date of Start")
    granulation_finish_date = fields.Date(string="Granulation Date of Finish")
    regn_no = fields.Integer(string="Regn. No.")
    batch_no = fields.Integer(string="Batch No.")
    batch_size = fields.Float(string="Batch Size", related="production_id.product_qty")
    mixing_wet_time_started = fields.Datetime(string="Mixing/Wet Time Started")
    mixing_wet_time_completed = fields.Datetime(string="Mixing/Wet Time Completed")
    mixing_wet_description = fields.Text(string="Mixing Wet Description")
    mixing_wet_lines = fields.One2many("granulation.line", "work_order_id", string="Mixing/Wet Lines")
    paste_solution_time_started = fields.Datetime(string="Paste/Solution Time Started")
    paste_solution_time_completed = fields.Datetime(string="Paste/Solution Time Completed")
    paste_solution_description = fields.Text(string="Paste Solution Description")
    paste_solution_lines = fields.One2many("granulation.line", "work_order_id", string="Paste/Solution Lines")
    drying_time_started = fields.Datetime(string="Drying Time Started")
    drying_time_completed = fields.Datetime(string="Drying Time Completed")
    drying_description = fields.Datetime(string="Drying Description")
    lubrication_time_started = fields.Datetime(string="Lubrication Time Started")
    lubrication_time_completed = fields.Datetime(string="Lubrication Time Completed")
    lubrication_description = fields.Datetime(string="Lubrication Description")
    lubrication_lines = fields.One2many("granulation.line", "work_order_id", string="lubrication Lines")
    mag_stearate_description = fields.Text(string="MAG. Stearate Description")

    @api.depends('name')
    def document_number(self):
        for rec in self:
            rec.granulation_sheet_document_no = "QR/PRO/" + str(rec.id)

#             Compression Sheet /////////////////////

    bulk_approval_no = fields.Char(string="Bulk Approval No.")
    bulk_approval_date = fields.Date(string="Approval Date")
    bulk_received = fields.Float(string="Bulk Received in mg.")
    comp_weight = fields.Float(string="Comp. Weight in mg")
    machine = fields.Char(string="Machine")
    punch_size = fields.Char(string="Punch Size")
    compression_starting_date = fields.Date(string="Starting Date")
    compression_completion_date = fields.Date(string="Completion Date")
    compression_lines = fields.One2many("compression.line", "work_order_id", string="Compression Lines")

    def fetch_lines(self):
        mixing_wet_granulation = self.env['mrp.routing.workcenter.line'].search([('sub_operation_id.name', '=', 'Mixing/Wet Granulation'), ('operation_id.bom_id', '=', self.production_id.bom_id.id)])
        if len(mixing_wet_granulation) > 1:
            raise odoo.exceptions.ValidationError("There is more than 1 BOM exists @@@ for this product")
        lines = [(5,0,0)]
        for product in mixing_wet_granulation.material_id:
            vals = {
                'material_id': product.id,
            }
            lines.append((0,0,vals))
        self.mixing_wet_lines = lines

class GranulationLine(models.Model):
    _name = "granulation.line"

    work_order_id = fields.Many2one("mrp.workorder", string="Work Order ID")
    qty = fields.Float(string="Quantity Kg.")
    material_id = fields.Many2one("product.template", string="Material")
    qc_no = fields.Char(string="Q.C. Number")
    performed_by = fields.Many2one("res.users", string="Performed By")
    checked_by = fields.Many2one("res.users", string="Checked By")

class CompressionLine(models.Model):
    _name = "compression.line"

    work_order_id = fields.Many2one("mrp.workorder", string="Work Order ID")
    date_time = fields.Datetime(string="Date & Time")
    weight_gm_1 = fields.Float(string="Weight of 10 tablets I gm")
    weight_gm_2 = fields.Float(string="Weight of 10 tablets II gm")
    col_height_mm_1 = fields.Float(string="Column Height mm I")
    col_height_mm_2 = fields.Float(string="Column Height mm II")
    hardness_kp_stockes_1 = fields.Char(string="Hardness-KP Stockes I")
    hardness_kp_stockes_2 = fields.Char(string="Hardness-KP Stockes II")
    dt = fields.Float(string="D.T")
    friability = fields.Float(string="D.T")
    initial = fields.Many2one("res.users", string="Initial")