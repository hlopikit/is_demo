from django import forms
from allcompbizproc.models import BizprocModel


class BPForm(forms.ModelForm):
    class Meta:
        model = BizprocModel
        fields = []

    bp = forms.ModelChoiceField(
        queryset=BizprocModel.objects.all(),
        to_field_name='process_id',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Не выбрано',
        label='БП'
    )
