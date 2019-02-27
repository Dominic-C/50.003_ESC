module.exports = {
  title: 'Arrays',
  schema: {
    'id': 'https://example.com/arrays.schema.json',
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'description': 'A representation of a person, company, organization, or place',
    'type': 'object',
    'properties': {
      'fruits': {
        'type': 'array',
        description: 'This is a simple array of strings',
        'items': {
          'type': 'string'
        }
      },
      'sizes': {
        'type': 'array',
        'items': {
          'type': 'string',
          enum: ['small', 'medium', 'large']
        },
        minItems: 1
      },
      'vegetables': {
        'type': 'array',
        'description': 'A list of vegetables as editable objects.',
        'items': { '$ref': '#/definitions/veggie' }
      },
      coordinate: {
        type: 'array',
        title: 'Lat/lon coordinates as a tuple',
        items: [{type: 'number', title: 'Latitude'}, {type: 'number', title: 'Longitude'}]
      }
    },
    'definitions': {
      'veggie': {
        'type': 'object',
        'required': [ 'veggieName', 'veggieLike' ],
        'properties': {
          'veggieName': {
            'type': 'string',
            'description': 'The name of the vegetable.'
          },
          'veggieLike': {
            'type': 'boolean',
            'description': 'Do I like this vegetable?'
          }
        }
      }
    }
  },
  data: {
    'fruits': [ 'apple', 'orange', 'pear' ],
    'vegetables': [
      {
        'veggieName': 'potato',
        'veggieLike': true
      },
      {
        'veggieName': 'broccoli',
        'veggieLike': false
      }
    ]
  }
}
