# Required Data

## Calendar Event Data

- Course Name
- Pillar
- ID
- Title
- Color
- Location
- Professor
- Class Enrolled
- Calendar Type
- Locked
- Suggester
- Requester
- Is Selected

## Calendar Scheduling Data

- Day of the Week
- Times
- Duration
- Duration Type

## Mapping JS to Django Schema

| Django Schedule Model | Javascript Model      | Data Type         | Covered | Computed Value |
|-----------------------|-----------------------|-------------------|---------|----------------|
| title -> courseName   | data.courseName       | char[120]         | Y       |                |
| None -> pillarType    | data.pillar           | char[10]          | N       |                |
| None -> ID            | data.id               | int               | N       |                |
| None -> eventName     | data.title            | char[120]         | N       |                |
| None                  | data.color            | hexcode           | N       | Y              |
| location              | data.location         | char[50]          | Y       |                |
| lecturer              | data.professor        | char[50]          | Y       |                |
| None -> classEnrolled | data.classEnrolled    | char[4]           | N       |                |
| isEvent               | data.calendarType     | boolean -> string | Y       | Y              |
| None                  | data.locked           | boolean           | Y       | Y              |
| None -> initiatedBy   | data.suggestedBy      | int               | N       | Y              |
| None -> initiatedBy   | data.requestedBy      | int               | N       | Y              |
| None -> dayOfWeek     | schedule.dayOfWeek    | int[]             | N       | Y              |
| start_time            | schedule.times        | [char[5]]         | Y       |                |
| None                  | schedule.duration     | int               | Y       | Y              |
| None                  | schedule.durationType | char[7]           | Y       | Y              |
