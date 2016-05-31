from django import forms


class PdfForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
