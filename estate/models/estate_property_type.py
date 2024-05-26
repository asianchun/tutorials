from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    
    name = fields.Char("Property Type", required=True)
    
    _sql_constraints = [
        ('check_unique_type', 'UNIQUE(name)', 'The type name has to be unique.'),
    ]