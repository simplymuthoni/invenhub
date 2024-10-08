from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    address = fields.Str(required=True)

class AdminSchema(Schema):
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password= fields.Str(required=True)
    
    
user_schema = UserSchema()
users_schema = UserSchema(many=True) 

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)
