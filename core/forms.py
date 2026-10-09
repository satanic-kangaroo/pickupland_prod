from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # فیلد تله برای ربات‌ها: انسان‌ها آن را نمی‌بینند و پر نمی‌کنند
    website = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={
        "tabindex": "-1", "autocomplete": "off",
    }))

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        labels = {
            "name": "نام و نام خانوادگی",
            "email": "ایمیل",
            "phone": "تلفن (اختیاری)",
            "message": "پیام یا درخواست عضویت",
        }
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"dir": "ltr", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"dir": "ltr", "autocomplete": "tel"}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("درخواست نامعتبر است.")
        return ""
