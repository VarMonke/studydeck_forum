from django import forms
from .models import Reply, Thread


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
        }

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "content", "category", "tags", "resources"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 6}),
            "tags": forms.CheckboxSelectMultiple()
        }

        