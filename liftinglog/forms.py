from django import forms
from django.forms import ModelForm
from liftinglog.models import Log, Lift
from django.forms.models import inlineformset_factory


LiftFormSet = inlineformset_factory(Log, Lift, can_delete=False, extra = 6)


class LogForm(ModelForm):
    
    pub_date = forms.DateField(input_formats=['%d-%m-%Y', '%m-%d-%Y',], label=(u'Date'))
    notes = forms.CharField(label=(u'Notes'))
    bw = forms.IntegerField(label=(u'Bodyweight'))
    
    class Meta:
        model = Log
        exclude = ("user",)
        

class LiftForm(ModelForm):
    
    class Meta:
        
        model = Lift
        exclude = ("log",)   