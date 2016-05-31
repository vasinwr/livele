from django import forms


class PdfForm(forms.Form):
    pdffile = forms.FileField(label='Select a file')
