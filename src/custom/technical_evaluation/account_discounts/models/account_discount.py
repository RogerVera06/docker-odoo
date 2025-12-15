from odoo import models, fields,_

class AccountDiscount(models.Model):
    _name = "account.discount"
    _description = "Invoice discount policies"
    _rec_name = "customer_type"

    #Fields
    customer_type = fields.Char(
        string="Customer type", 
        required=True,
        help='Name of the customer type')

    percentage = fields.Float(
        string="Discount (%)", 
        required=True,
        default=0.0,
        help='Discount percentage for customer type'
    )
    
    #Constrains
    _sql_constraints = [
        ('customer_type_unique','unique(customer_type)',_('The customer type already has a discount policy')),
        ('valid_percentage', 'CHECK(percentage >= 0 AND percentage <= 100)', _('The percentage must be between 0 and 100')),
        ]