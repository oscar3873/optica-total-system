from django import forms

from .models import Notifications

class NotificationsForm(forms.ModelForm):

    class Meta:
        model = Notifications
        fields = '__all__'