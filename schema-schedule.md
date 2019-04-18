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

| Javascript Model      | Django Schedule Model | Covered | Computed Value |
|-----------------------|-----------------------|---------|----------------|
| data.courseName       | title -> courseName   | Y       |                |
| data.pillar           | None -> pillarType    | N       |                |
| data.ID               | None -> ID            | N       |                |
| data.title            | None -> eventName     | N       |                |
| data.color            | None                  | N       | Y              |
| data.location         | location              | Y       |                |
| data.professor        | lecturer              | Y       |                |
| data.classEnrolled    | None -> classEnrolled | N       |                |
| data.calendarType     | isEvent               | Y       | Y              |
| data.locked           | None                  | Y       | Y              |
| data.suggestedBy      | None -> initiatedBy   | N       | Y              |
| data.requestedBy      | None -> initiatedBy   | N       | Y              |
| schedule.dayOfWeek    | None -> dayOfWeek     | N       | Y              |
| schedule.times        | start_time            | Y       |                |
| schedule.duration     | None                  | Y       | Y              |
| schedule.durationType | None                  | Y       | Y              |
class Schedule(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(("Date"), default=datetime.date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lecturer = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    isEvent = models.BooleanField(default=False)