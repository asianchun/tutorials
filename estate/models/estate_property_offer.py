from odoo import fields, models, api
from odoo.exceptions import UserError
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
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be a positive number.'),
    ]
    
    def action_set_accepted(self):
        for record in self:
            accepted_offers = self.search([
                    ('property_id', '=', record.property_id.id),
                    ('status', '=', 'accepted'),
                    ('id', '!=', record.id)
                ])
            
            if accepted_offers:
                raise UserError('There is already an accepted offer!')
            
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
                    
        return True
    
    def action_set_rejected(self):
        for record in self:
            record.status = 'refused'
        
        return True
    
    @api.depends("validity", 'create_date')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
            
    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days