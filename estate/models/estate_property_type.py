from odoo import fields, models, api

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = 'sequence, name'
    
    name = fields.Char("Property Type", required=True)
    property_ids = fields.One2many("estate.property", 'property_type_id')
    sequence = fields.Integer('Sequence', default=1)
    
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_count")
    
    _sql_constraints = [
        ('check_unique_type', 'UNIQUE(name)', 'The type name has to be unique.'),
    ]
    
    @api.depends('offer_ids')
    def _compute_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)