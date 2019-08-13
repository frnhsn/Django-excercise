from django import forms
from .models import Topic


class NewTopicForm(forms.Form):
    subject = forms.CharField(
        widget = forms.TextInput(), 
        max_length=255, 
        required=True)

    message = forms.CharField(
        widget = forms.Textarea(), 
        max_length=4000, 
        required=True)

    class Meta:
        model = Topic
        fields = ['subject', 'message']

    def clean_subject(self):
        subject_input = self.cleaned_data.get('subject')
        if subject_input.lower() == 'new':
            raise forms.ValidationError('Please choose different subject name')
        return subject_input

class NewReplyForm(forms.Form):
    message = forms.CharField(
        widget = forms.Textarea(), 
        max_length=4000, 
        required=True)

    class Meta:
        model = Topic
        fields = ['message']
