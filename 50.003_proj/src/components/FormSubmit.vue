<template>
  <vue-form-json-schema
    :model="model"
    :schema="schema"
    :ui-schema="uiSchema"
    :on-change="onChange"
  >
  </vue-form-json-schema>
</template>

<script>
export default {
  data() {
    return {
      model: {
      },
      options: {
        "castToSchemaType": true
      },
      // Some valid JSON Schema Object
      schema: {
        'type' : 'object',
        'required' : [
          'courseTitle',
          'description',
          'date',
          'startTime',
          'duration',
          'lecturer',
          'location'
        ],
        'properties': {
          'courseTitle' :{
            "type" : "string"
          },
          'description' : {
            "type" : "string"
          },
          'date' : {
            "type" : "string",
            "format" : "date"
          },
          'startTime' : {
            "type" : "string",
            "pattern" : "([0-2][0-9]){1}:([0-6][0-9]){1}"
          },
          'duration' : {
            "type" : "number",
            "multipleOf" : 1,
            "minimum" : 30,
          },
          'lecturer' : {
            "type" : "string"
          },
          'location' : {
            "type" : "string"
          }
        }
      },
      uiSchema : [
      {"component": "div",
        "fieldOptions": {
          "class": ["form-group"]
        },
        "children": [{
          "component" : "label",
          "fieldOptions" : {
            "attrs" : {"for" : "course-title"},
            "class" : ["font-weight-bold"],
            "domProps" : {"innerHTML": "Course Title"}
            }
          },
        {"component": "input",
          "model": "courseTitle",
          "errorOptions": {
            "class": [
              "is-invalid"
              ]
            },
          "fieldOptions": {
            "attrs": {
              "id": "course-title"
            },
            "class": [
              "form-control"
            ],
            "on": [
              "input"
            ]}
          },
        {"component": "small",
          "fieldOptions": {
            "class": [
              "text-muted"
            ],
            "domProps": {
              "innerHTML": "Please enter the Course Title"
            }
          }
        }]
        },
      {"component": "transition",
        "fieldOptions": {
        "props": {"name": "fade"}
        },
        "children": [
          {"component": "div",
            "model": "courseTitle",
            "errorHandler": true,
            "displayOptions": {
              "model": "courseTitle",
              "schema": {
                "not": {
                  "type": "string"
                }
              }
            },
            "fieldOptions": {
              "class": [
                "alert alert-danger"
                ]
            },
            "children": [
            {"component": "div",
              "fieldOptions": {
                "domProps": {
                  "innerHTML": "This field is required"
                  }
                }
              }]
            }
          ]
        },
      ]
    }
  }
}
</script>