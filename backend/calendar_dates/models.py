from django.db import models
from calendars.models import Calendar

ExceptionType = (('a','Added'), ('r', 'Removed'))
class CalendarDate(models.Model):
    service= models.ForeignKey(to = Calendar, on_delete = models.CASCADE)
    date = models.DateField()
    exception_type = models.CharField(choices=ExceptionType, max_length=100)

    def __str__(self):
        return f'serv_id : {self.service} date : {self.date} type : {self.exception_type} id : {self.id}'
    

    

