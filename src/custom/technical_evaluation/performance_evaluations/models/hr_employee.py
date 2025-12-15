from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    performance_review_ids = fields.One2many(
        "hr.performance.review",
        "employee_id",
        string="Performance Reviews"
    )