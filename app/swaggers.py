from flasgger import Swagger, swag_from

def init_swagger(app):
    swagger = Swagger(app)
    
    @app.route('/register', methods=['POST'])
    @swag_from({
        'responses': {
            201: {
                'description': 'User registered successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string'
                        }
                    }
                }
            }
        },
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'phone_number': {'type': 'string'},
                        'email': {'type': 'string'},
                        'address': {'type': 'string'},
                        'username': {'type': 'string'}
                    },
                    'required': ['name', 'phone_number', 'email', 'address', 'username']
                }
            }
        ],
        'tags': ['Users']
    })
    def register():
        pass
