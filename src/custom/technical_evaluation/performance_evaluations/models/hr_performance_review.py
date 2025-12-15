from odoo import fields,models,api, _ 
from odoo.exceptions import ValidationError

class HrPerformanceReview(models.Model):
    _name = "hr.performance.review"
    _description = "Performance Reviews"
    _rec_name = "employee_id"
    
    status = fields.Selection([
        ("pending", "Pending"),
        ("completed", "Completed"),
        ], default="pending")
    
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
        help="Employee being evaluated"
    )
    
    review_date = fields.Date(
        string="Review Date",
        required=True,
        default=fields.Date.context_today,
        help="Date of performance review"
    )
    
    reviewer_id = fields.Many2one(
        "hr.employee",
        string="Reviewer",
        required=True,
        help="Employee who is doing the review"
    )
    
    score = fields.Float(
        string="Score",
        required=True,
        help="Numerical rating (1 to 10)",
        default=0.0,
    )
    
    comments = fields.Text(
        string="Comments",
        help="Qualitative feedback on the employee's performance"
    )
    
    goals_next_period = fields.Text(
        string="Goals for Next Period",
        help="Objectives to be achieved in the next review cycle"
    )
    
    strengths = fields.Text(
        string="Strengths",
        help="Key strengths observed during the review period"
    )
    
    weaknesses = fields.Text(
        string="Weaknesses",
        help="Areas for improvement identified during the review"
    )
    
    @api.constrains("score")
    def _check_score(self):
        for record in self:
            if record.score < 0 or record.score > 10:
                raise ValidationError(_("Score must be between 0 and 10."))

    @api.constrains("employee_id", "status")
    def _check_only_one_pending_review(self):
        for record in self:
            if record.status == "pending" and record.employee_id:
                #Busca reviews asociadas al empleado en estatus 'pending'
                pending_review = self.env['hr.performance.review'].search([
                    ('status','=','pending'),
                    ('employee_id','=',record.employee_id.id)])

                if len(pending_review) > 1:
                    raise ValidationError(_("An employee can only have one pending performance review."))
                
    def action_complete_review(self):
        if self.status != 'pending':
            raise ValidationError(_("Only pending reviews can be completed."))
        if self.reviewer_id != self.env.user.employee_id:
            raise ValidationError(_("Only the assigned reviewer can complete this review."))
        self.status = 'completed'