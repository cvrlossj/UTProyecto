from django import forms
from accounts.models import Region, Comuna, Perfiles
from .models import JuntaVecinos

class AddJuntaVecinos(forms.Form):
    nombreOrganizacion = forms.CharField(
        label="Nombre de la organización",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'nombreOrganizacion',
            'placeholder': 'Ingresar nombre',
            'name': 'nombreOrganizacion',
            'required': 'required',
            'autofocus': 'autofocus'
        })
    )
    fechaIntegracion = forms.DateField(
        label="Fecha integración",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'fechaIntegracion',
            'placeholder': 'Ingresar fecha',
            'name': 'fechaIntegracion',
            'required': 'required',
            'date': 'date',
            'autocomplete': 'off',
            'autofocus': 'autofocus'
        })
    )
    direccionOrganizacion = forms.CharField(
        label="Dirección de la organización",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'direccionOrganizacion',
            'placeholder': 'Ingresar la dirección',
            'name': 'direccionOrganizacion',
            'required': 'required',
            'autofocus': 'autofocus'
        })
    )
    regionOrganizacion = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        label="Región",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'region',
            'required': True
        }),
        empty_label="Selecciona una región"
    )
    comunaOrganizacion = forms.ModelChoiceField(
        queryset=Comuna.objects.none(),
        label="Comuna",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'comuna',
            'required': True
        })
    )
    
    direccionOrganizacion = forms.CharField(
        label="Dirección",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'direccionOrganizacion',
            'required': True
        })
    )
    
    perfilesOrganizacion = forms.ModelMultipleChoiceField(
        queryset=Perfiles.objects.none(),
        label="Administradores Junta Vecino",
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'perfilesOrganizacion'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = kwargs.get('data', None)
        if data:
            try:
                region_id = int(data.get('regionOrganizacion', 0))
                comuna_id = data.get('comunaOrganizacion', None)
                
                if region_id:
                    self.fields['comunaOrganizacion'].queryset = Comuna.objects.filter(
                        id_region=region_id
                    )
                
                if comuna_id:
                    self.fields['perfilesOrganizacion'].queryset = Perfiles.objects.filter(
                        id_comuna=comuna_id,
                        id_rol=2
                    ).exclude(juntavecinos__isnull=False)
            except (ValueError, TypeError):
                pass
        
    def clean(self):
        cleaned_data = super().clean()
        region = cleaned_data.get('regionOrganizacion')
        comuna = cleaned_data.get('comunaOrganizacion')

        if region and comuna:
            # Verificar que la comuna pertenece a la región
            if comuna.id_region != region:
                self.add_error(
                    'comunaOrganizacion',
                    'La comuna seleccionada no pertenece a la región elegida'
                )

        return cleaned_data
    

class EditJuntaVecinos(forms.Form):
    pass