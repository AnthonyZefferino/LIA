from django import forms
from .models import Company, Industry, Sector
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.utils.translation import gettext_lazy as _


class CompanyForm(forms.ModelForm):
    industry = forms.ModelChoiceField(
        queryset=Industry.objects.all(),
        required=False,
        label=_("Industry"),
        empty_label=_("Select Industry")  # o `None` per non avere un'opzione vuota
    )
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.all(),
        required=False,
        label=_("Sector"),
        empty_label=_("Select Sector")  # o `None` per non avere un'opzione vuota
    )

    class Meta:
        model = Company
        fields = '__all__'  # Nota che includendo 'all', non avrai bisogno di dichiarare esplicitamente ogni campo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Costruzione del layout del form con Crispy Forms se è richiesto
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = self.build_layout()
        self.helper.add_input(Submit('submit', _('Save')))

    def build_layout(self):
        layout = []
        for field_name, field in self.fields.items():
            layout.append(FloatingField(field_name))
        return layout
