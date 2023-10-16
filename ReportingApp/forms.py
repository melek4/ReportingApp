# from django.contrib.auth.models import User
from asyncio.windows_events import NULL
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext, gettext_lazy as _

from Project import settings
from .models import *
from datetime import date

User = get_user_model()
# passwordChangeForm = AdminPasswordChangeForm()

# this is where the forms are defined


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href=\"password/\">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active',
                  'staff', 'admin', 'Direction']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RegisterForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

from bootstrap_datepicker_plus.widgets import DatePickerInput

class PersonnelForm(forms.ModelForm):
    thisyear = date.today().year
    pers_mat_95 = forms.IntegerField(label='Matricule')
    sex_choices = (
        ('M', 'Homme'),
        ('F', 'Femme')
    )
    pers_sexe_x = forms.ChoiceField(choices=sex_choices, label='Sexe')
    pers_date_nais = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label="Date naissance",widget=DatePickerInput)
    cet_choices = (
        ('0', 'Actif'),
        ('1', 'Inactif temporaire'),
        ('2', 'Inactif')
    )
    pers_cet_9 = forms.ChoiceField(choices=cet_choices, label='Etat')
    
    pers_date_rec = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label="Date recrutement",widget=DatePickerInput)
    
    pers_affect_92 = forms.ModelChoiceField(
        queryset=Direction.objects.all(), label='Direction')
    pers_naturagent_93 = forms.ModelChoiceField(
        queryset=Natureagent.objects.all(), label='Nature agent')
    pers_qualif_x45 = forms.CharField(label='Qualification')
    cat_choices = (
        ('4', 'Cadre'),
        ('1', 'Execution'),
        ('2', 'Maitrise'),
        ('5', 'Execution Maitrise')
    )
    pers_catpers_9 = forms.ChoiceField(
        choices=cat_choices, label='Catégorie')
    nat_choices = (
        ('1', 'Gestion'),
        ('2', 'Technique')
    )
    pers_natpers_9 = forms.ChoiceField(
        choices=nat_choices, label='Nature')
    
    field_order= ['pers_mat_95', 'pers_sexe_x', 'pers_date_nais', 'pers_cet_9', 'pers_date_rec', 'pers_affect_92', 'pers_naturagent_93', 'pers_qualif_x45', 'pers_catpers_9', 'pers_natpers_9']
    class Meta:
        model = Personnel
        fields = '__all__'
        

class AbsenceForm(forms.ModelForm):

    thisyear = date.today().year
    abs_mat_95 = forms.ModelChoiceField(
        queryset=Personnel.objects.all().order_by('-pers_mat_95'), label="Matricule du personnel")
    abs_nat_9 = forms.ModelChoiceField(
        queryset=NatAbs.objects.all(), label='abs_nat_9')
    abs_date_deb = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label="Date début",widget=DatePickerInput)
    per_choices = (
        ('M', 'Matin'),
        ('A', 'Apres-midi')
    )
    abs_perdeb_x = forms.ChoiceField(
        choices=per_choices, label='Période début')
    abs_date_fin = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label="Date fin",widget=DatePickerInput)
    abs_perfin_x = forms.ChoiceField(
        choices=per_choices, label='Période fin')
    abs_nbrjour_93 = forms.DecimalField(label='Nombre de jours')
    index_pk = forms.IntegerField(label="Matricule de l'absence")

    class Meta:
        model = Absence
        fields = '__all__'
        exclude = ['abs_cumule_9']


class CongeForm(forms.ModelForm):
    thisyear = date.today().year
    cong_mat_95 = forms.ModelChoiceField(
        queryset=Personnel.objects.all().order_by('-pers_mat_95'), label='Matricule du personnel')
    congnat_choices = (
        ('1', 'Annuel'),
        ('2', 'Recuperation'),
        ('3', 'Exceptionnel')
    )
    cong_nat_9 = forms.ChoiceField(
        choices=congnat_choices, label='Nature congé')
    cong_ancsold_93 = forms.DecimalField(label='Ancien solde')
    cong_nbrjour_93 = forms.DecimalField(label='Nombre de jours')
    cong_novsold_93 = forms.DecimalField(label='Nouveau solde')
    cong_date_deb = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label="Date début",widget=DatePickerInput)
    per_choices = (
        ('M', 'Matin'),
        ('A', 'Apres-midi')
    )
    cong_perdeb_x = forms.ChoiceField(
        choices=per_choices, label='Période début')
    cong_date_fin = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label="Date fin",widget=DatePickerInput)
    cong_perfin_x = forms.ChoiceField(
        choices=per_choices, label='Période fin')
    index_pk = forms.IntegerField(label='Matricule du congé')

    class Meta:
        model = Conge
        fields = '__all__'

mois_choices= [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ]

class PaieForm(forms.ModelForm):
    
    mois = forms.ChoiceField(choices=mois_choices, label = "Mois")
    anne = forms.IntegerField(label = "Année")
    jours_pres = forms.IntegerField(required=False, label = "Jours de présence")
    matricule = forms.ModelChoiceField(queryset=Personnel.objects.all().order_by('-pers_mat_95'), label="Matricule du personnel")
    nom_choices = (
        ('SALAIRE DE BASE','Saliare de Base'),
        ('Indemnite de Technicite','Indemnite de Technicite'),
        ('Indemnite de Representation','Indemnite de Representation'),
        ('Indemnite Specifique 2016-2017-2018','Indemnite Specifique 2016-2017-2018'),
        ('INDEMNITE DE FONCTION','Indemnite de Fonction'),
        ("Indemnite d'Exercice", "Indemnite d'Exercice"),
        ('Indemnite Majoration Kilometrique','Indemnite Majoration Kilometrique'),
        ('Indemnite Kilometrique','Indemnite Kilometrique'),
        ('SALAIRE BRUT','Saliare Brut'),
        ("Bons d'essence","Bons d'essence"),
        ('RETENUE RETRAITE','Retenue Retraite'),
        ('RETENUE PREVOYANCE SOCIALE','Retenue Prevoyance Sociale'),
        ('RETENUE CAPITAL DECES','Retenue Capital Décés'),
        ('SALAIRE IMPOSABLE','Saliare Imposable'),
        ('CONTRIBUTION SOCIALE DE SOLIDARITE','Contribution Sociale se Solidaité'),
        ('RETENUE IMPOT SUR LE REVENU','Retenue Impot Sur le Révenu'),
        ('RETENUE ASSURANCE GROUPE','Retenue Assurance Groupe'),
        ('RETENUE ASSURANCE RETRAITE','Retenue Assurance Retraite'),
        ('REMBOURS. PRET ORDINATEUR','Remboursement Pret Ordinateur'),
        ('MONTANT COTISATION UGTT','Montant Cotisation UGTT'),
        ('NET A PAYER','Net à Payer'),
    )
    nom_ligne = forms.ChoiceField(choices=nom_choices, label="Nom de la ligne")
    mnt_ligne = forms.DecimalField(required=False, label="Montant de la ligne")
    nbre_qte = forms.IntegerField(required=False, label="Quantité de la ligne")
    type_choices = (
        ('0','0'),
        ('1','1'),
    )
    type_ligne = forms.ChoiceField(choices=type_choices, label="Type de la ligne")
    num_ord = forms.IntegerField()
    index_pk = forms.IntegerField()

    class Meta:
        model = Paie
        fields = '__all__'


dir_choices = []
dirs = []
for i in Paie.objects.all():
    d = i.matricule.pers_affect_92.lib_direction
    if d not in dirs:
        dirs.append(d)
        t = (f'{d}', f'{d.title()}')
        dir_choices.append(t)

emp_choices = []
emps = []
for i in Paie.objects.all():
    m = i.matricule
    if m not in emps:
        emps.append(m)
        t = (f'{m}', f'{m}')
        emp_choices.append(t)

year_choices = []
years = []
for i in Paie.objects.all():
    y = i.anne
    if y not in years:
        years.append(y)
        t = (f'{y}', f'{y}')
        year_choices.append(t)
class FDPForm(forms.Form):
    direction = forms.MultipleChoiceField(choices=dir_choices, widget = forms.CheckboxSelectMultiple,required=False)
    all = forms.BooleanField(required=False)
    employees = forms.MultipleChoiceField(choices = emp_choices, widget = forms.CheckboxSelectMultiple,required=False)
    year = forms.ChoiceField(choices = year_choices)
    mois = forms.ChoiceField(choices = mois_choices)

def clean(self):
        cleaned_data = super(FDPForm, self).clean()
        direction = cleaned_data.get(direction)
        all = cleaned_data.get(all)
        employees = cleaned_data.get(employees)
        if (direction and all and employees) or (direction and all) or (direction and employees) or (all and employees):
            raise forms.ValidationError("Utiliser une seule méthode!")
        elif not direction and not all and not employees:
            raise forms.ValidationError("Choisir les employés concernés!")

        return cleaned_data
