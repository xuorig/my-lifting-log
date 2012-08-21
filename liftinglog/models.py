from django.db import models
from django.contrib.auth.models import User



class Log(models.Model):
    
    def __unicode__(self):
        return str(self.pub_date)
     
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('Date of workout')
    notes = models.CharField(max_length=500)
    bw = models.IntegerField()

class Lift(models.Model):
    
    def __unicode__(self):
        return self.name
        
    name = models.CharField(max_length=200)
    log = models.ForeignKey(Log)
    reps = models.IntegerField()
    sets = models.IntegerField()
    weight = models.IntegerField()


        


