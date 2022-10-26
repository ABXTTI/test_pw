from odoo import models, fields, api

class MrpRoutingWorkcenter(models.Model):
    _inherit = "mrp.routing.workcenter"

    operation_line_ids = fields.One2many("mrp.routing.workcenter.line", "operation_id", string="Operation Lines")


class MrpRoutingWorkcenterSub(models.Model):
    _name = "mrp.routing.workcenter.sub"

    name = fields.Char(string="Sub Operation")
    description = fields.Text(string="Description")

class MrpRoutingWorkcenterLine(models.Model):
    _name = "mrp.routing.workcenter.line"

    operation_id = fields.Many2one("mrp.routing.workcenter", string="Operation")
    sub_operation_id = fields.Many2one("mrp.routing.workcenter.sub", string="Sub Operation")
    description = fields.Char(string="Description")
    material_id = fields.Many2many("product.template", string="Material")
    standard_duration = fields.Float(string="Standard Duration")

    @api.onchange('sub_operation_id')
    def onchange_sub_operation_id(self):
        for rec in self:
            if rec.sub_operation_id:
                rec.description = rec.sub_operation_id.description