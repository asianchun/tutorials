from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    
    name = fields.Char("Property Type", required=True)
    property_ids = fields.One2many("estate.property", 'property_type_id')
    
    _sql_constraints = [
        ('check_unique_type', 'UNIQUE(name)', 'The type name has to be unique.'),
    ]