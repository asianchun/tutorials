from odoo import fields, models, api
from datetime import timedelta

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    
    price = fields.Float("Price")
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    
    @api.depends("validity", 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)
            
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days