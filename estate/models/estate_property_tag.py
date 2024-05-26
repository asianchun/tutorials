from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    
    name = fields.Char("Name", required=True)
    
    _sql_constraints = [
        ('check_unique_tag', 'UNIQUE(name)', 'The tag name has to be unique.'),
    ]