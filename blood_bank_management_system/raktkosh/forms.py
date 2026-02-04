from django import forms
# from django.contrib.auth.models import User
from . import models
from .models import Stock
from .models import Category
from .models import BloodRequest

class BloodForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['bloodgroup', 'unit']

    def __init__(self, *args, **kwargs):
        super(BloodForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        blood_group_choices = [(category.name, category.name) for category in categories]
        self.fields['bloodgroup'].choices = blood_group_choices

class DonationForm(forms.ModelForm):
    class Meta:
        model=models.BloodDonate
        fields=['age','bloodgroup','disease','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'patient_age', 'reason', 'bloodgroup', 'unit']

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['patient_name'].widget.attrs['readonly'] = True
        self.fields['patient_age'].widget.attrs['readonly'] = True
        self.fields['bloodgroup'].widget.attrs['readonly'] = True