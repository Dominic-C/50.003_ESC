<template>
  <v-container fluid>
    <v-layout wrap>
      <v-flex xs12>
        <vue-form-json-schema
      :model="model"
      :schema="schema"
      :ui-schema="uiSchema"
      :on-change="onChange"
      >
      </vue-form-json-schema>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Vue from 'vue';
import VueFormJsonSchema from 'vue-form-json-schema';

Vue.component('vue-form-json-schema', VueFormJsonSchema);

export default {
  name: 'FormSubmit',
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
          'courseDescription',
          'dayOfTheWeek',
          'startTime',
          'duration',
          'lecturer',
          'location'
        ],
        'properties': {
          'courseTitle' :{
            "type" : "string"
          },
          'courseDescription' : {
            "type" : "string"
          },
          'dayOfTheWeek' : {
            "type" : "string",
            "pattern" : "(((m|M)on|(T|t)ue(s)?|(w|W)ed(nes)?|(T|t)hur(s)?|(f|F)ri)(day)?)?"
          },
          'startTime' : {
            "type" : "string",
            "pattern" : "([0-2][0-9]){1}:([0-6][0-9]){1}(AM|PM)?"
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
      {"component": "div",
        "fieldOptions": {
          "class": ["form-group"]
        },
        "children": [{
          "component" : "label",
          "fieldOptions" : {
            "attrs" : {"for" : "course-description"},
            "class" : ["font-weight-bold"],
            "domProps" : {"innerHTML": "Course Description"}
            }
          },
        {"component": "input",
          "model": "courseDescription",
          "errorOptions": {
            "class": [
              "is-invalid"
              ]
            },
          "fieldOptions": {
            "attrs": {
              "id": "course-description"
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
              "innerHTML": "Please enter the Course description"
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
            "model": "courseDescription",
            "errorHandler": true,
            "displayOptions": {
              "model": "courseDescription",
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
      {"component": "div",
        "fieldOptions": {
          "class": ["form-group"]
        },
        "children": [{
          "component" : "label",
          "fieldOptions" : {
            "attrs" : {"for" : "the-date"},
            "class" : ["font-weight-bold"],
            "domProps" : {"innerHTML": "Day of the Week"}
            }
          },
        {"component": "input",
          "model": "dayOfTheWeek",
          "errorOptions": {
            "class": [
              "is-invalid"
              ]
            },
          "fieldOptions": {
            "attrs": {
              "id": "the-date",
              "type": "string",
              "pattern" : "(((m|M)on|(T|t)ue(s)?|(w|W)ed(nes)?|(T|t)hur(s)?|(f|F)ri)(day)?)?"
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
              "innerHTML": "Please enter which days of the week this session will be on."
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
            "model": "dayOfTheWeek",
            "errorHandler": true,
            "displayOptions": {
              "model": "dayOfTheWeek",
              "schema": {
                "not": {
                  "type": "string",
                  "pattern" : "(((m|M)on|(T|t)ue(s)?|(w|W)ed(nes)?|(T|t)hur(s)?|(f|F)ri)(day)?)?"
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
                  "innerHTML": "This field is required, and must be one of the five working weekdays of the week. (e.g. Monday)"
                  }
                }
              }]
            }
          ]
        },
      {"component": "div",
        "fieldOptions": {
          "class": ["form-group"]
        },
        "children": [{
          "component" : "label",
          "fieldOptions" : {
            "attrs" : {"for" : "start-time"},
            "class" : ["font-weight-bold"],
            "domProps" : {"innerHTML": "Starting Time"}
            }
          },
        {"component": "input",
          "model": "startTime",
          "errorOptions": {
            "class": [
              "is-invalid"
              ]
            },
          "fieldOptions": {
            "attrs": {
              "id": "start-time",
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
              "innerHTML": "Please enter the start time of the lesson in XX:XX format"
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
            "model": "startTime",
            "errorHandler": true,
            "displayOptions": {
              "model": "startTime",
              "schema": {
                "not": {
                  "type": "string",
                  "pattern" : "([0-2][0-9]){1}:([0-6][0-9]){1}(AM|PM)?"
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
                  "innerHTML": "Please enter a valid start time, either in the 24-hour format or with AM/PM. (e.g. 08:00 or 08:00AM)"
                  }
                }
              }]
            }
          ]
        },
      {"component": "div",
        "fieldOptions": {
          "class": ["form-group"]
        },
        "children": [{
          "component" : "label",
          "fieldOptions" : {
            "attrs" : {"for" : "duration-time"},
            "class" : ["font-weight-bold"],
            "domProps" : {"innerHTML": "Duration of Lesson in Minutes"}
            }
          },
        {"component": "input",
          "model": "duration",
          "errorOptions": {
            "class": [
              "is-invalid"
              ]
            },
          "fieldOptions": {
            "attrs": {
              "id": "duration-time",
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
              "innerHTML": "Please enter the duration of the lesson in minutes."
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
            "model": "duration",
            "errorHandler": true,
            "displayOptions": {
              "model": "duration",
              "schema": {
                "not": {
                  "type": "number"
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
                  "innerHTML": "This field is required."
                  }
                }
              }]
            },
          {"component": "div",
            "model": "duration",
            "errorHandler": true,
            "displayOptions": {
              "model": "duration",
              "schema": {
                "not": {
                  "type": "number",
                  "multipleOf": 1,
                  "minimum": 30
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
                  "innerHTML": "Lessons should at least be 30 minutes."
                  }
                }
              }]
            }
          ]
        },
      {"component": "div",
        "fieldOptions": {
          "class": ["form-group"]
        },
        "children": [{
          "component" : "label",
          "fieldOptions" : {
            "attrs" : {"for" : "the-lecturer"},
            "class" : ["font-weight-bold"],
            "domProps" : {"innerHTML": "Lecturer"}
            }
          },
        {"component": "input",
          "model": "lecturer",
          "errorOptions": {
            "class": [
              "is-invalid"
              ]
            },
          "fieldOptions": {
            "attrs": {
              "id": "the-lecturer",
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
              "innerHTML": "Who's teaching this?"
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
            "model": "lecturer",
            "errorHandler": true,
            "displayOptions": {
              "model": "lecturer",
              "schema": {
                "not": {
                  "type": "string",
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
                  "innerHTML": "This field is required."
                  }
                }
              }]
            }
          ]
        },
      {"component": "div",
        "fieldOptions": {
          "class": ["form-group"]
        },
        "children": [{
          "component" : "label",
          "fieldOptions" : {
            "attrs" : {"for" : "the-location"},
            "class" : ["font-weight-bold"],
            "domProps" : {"innerHTML": "Location"}
            }
          },
        {"component": "input",
          "model": "location",
          "errorOptions": {
            "class": [
              "is-invalid"
              ]
            },
          "fieldOptions": {
            "attrs": {
              "id": "the-location",
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
              "innerHTML": "Where is this being held?"
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
            "model": "location",
            "errorHandler": true,
            "displayOptions": {
              "model": "location",
              "schema": {
                "not": {
                  "type": "string",
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
                  "innerHTML": "This field is required."
                  }
                }
              }]
            }
          ]
        },
      ],
      methods: {
        onChange(value) {
          this.model = value;
      }
    },
    }
  }
}
</script>