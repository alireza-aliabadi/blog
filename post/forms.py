from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Comment
messages = {
    'required': 'لطفا فیلد مورد نظر را پر نمایید',
    'invalid': 'لطفا ایمیل صحیح را وارد نمایید',
    'max_length': 'تعداد کاراکتر های ورودی بیشتر از حد مجاز است',
    'min_length': 'تعداد کاراکتر های ورودی کمتر از حد مجاز است'
}


class EmailPostForm(forms.Form):
    name = forms.CharField(label=_("نام"), max_length=25, error_messages=messages)
    email = forms.EmailField(label=_("ایمیل فرستنده"), error_messages=messages)
    to = forms.EmailField(label=_("ایمیل گیرنده"), required=True, error_messages=messages)
    comment = forms.CharField(label=_("متن"), widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')
        labels = {
            "name": _("نام"),
            "email": _("ایمیل"),
            "text": _("متن")
        }
