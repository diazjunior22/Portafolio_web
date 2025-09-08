from django  import forms
from django.core.validators import EmailValidator    #this is for validate the email


class ContactForm(forms.Form):
    nombre =  forms.CharField(max_length=50)
    email = forms.CharField(validators=[EmailValidator()])
    asunto = forms.CharField(max_length=50)
    mensaje = forms.CharField(widget=forms.Textarea)
    
    fields = [nombre , email , asunto , mensaje]
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={'class':'w-full px-4 py-3 bg-input border border-border rounded-lg focus:ring-2 focus:ring-ring focus:border-transparent',}
        self.fields['mensaje'].widget.attrs['rows'] = "5"


# class="">