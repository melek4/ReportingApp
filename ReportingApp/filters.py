from django import forms
import django_filters
from django_filters import NumberFilter
from .models import *
from bootstrap_datepicker_plus.widgets import DatePickerInput

class DateInput(forms.DateInput):
    input_type = 'date'

sex_choices = (
        ('M', 'Homme'),
        ('F', 'Femme')
    )
cet_choices = (
        ('0', 'Actif'),
        ('1', 'Inactif temporaire'),
        ('2', 'Inactif')
    )
cat_choices = (
        ('4', 'Cadre'),
        ('1', 'Execution'),
        ('2', 'Maitrise'),
        ('5', 'Execution Maitrise')
    )
nat_choices = (
        ('1', 'Gestion'),
        ('2', 'Technique')
    )
class personnelFilter(django_filters.FilterSet):

    pers_mat_95 = NumberFilter(field_name='pers_mat_95', label='Matricule')
    # pers_sexe_x = django_filters.ChoiceFilter(choices=sex_choices, label='Sexe')
    # pers_date_nais = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), label='Date de naissance')
    pers_cet_9 = django_filters.ChoiceFilter(choices=cet_choices, label='Etat')
    # date_rec = DateFilter(field_name='pers_date_rec', label='Date recrutement')
    # date_nais = DateFilter(field_name='pers_date_nais', label='Date naissance')
    pers_date_rec = django_filters.DateFilter(widget=DatePickerInput(), label='Date de récrutement')
    pers_affect_92 = django_filters.ModelChoiceFilter(label='Direction',queryset=Direction.objects.all())
    # pers_naturagent_93 = django_filters.ModelChoiceFilter(
        # queryset=Natureagent.objects.all(), label='Nature agent')
    # pers_qualif_x45 = CharFilter(field_name='pers_qualif_x45',
                        # lookup_expr='icontains', label='Qualification')
    pers_catpers_9 = django_filters.ChoiceFilter(
        choices=cat_choices, label='Catégorie')
    pers_natpers_9 = django_filters.ChoiceFilter(
        choices=nat_choices, label='Nature')

    
    class Meta:
        model = Personnel
        # fields = 
        exclude = ['pers_mat_95','pers_date_rec','pers_date_nais','pers_affect_92','pers_naturagent_93','pers_qualif_x45','pers_catpers_9','pers_sexe_x','pers_cet_9','pers_natpers_9']

per_choices = (
        ('M', 'Matin'),
        ('A', 'Apres-midi')
    )

class absenceFilter(django_filters.FilterSet):

    abs_mat_95 = NumberFilter(field_name='abs_mat_95', label='Matricule personnel')
    abs_nat_9 = django_filters.ModelChoiceFilter(
        queryset=NatAbs.objects.all(), label='Nature absence')
    abs_date_deb = django_filters.DateFilter(widget=DatePickerInput(), label='Date début')
    abs_perdeb_x = django_filters.ChoiceFilter(choices=per_choices, label='Periode début')
    abs_date_fin = django_filters.DateFilter(widget=DatePickerInput(),label='Date fin')
    abs_perfin_x = django_filters.ChoiceFilter(choices=per_choices, label='Periode fin')
    abs_nbrjour_93 = NumberFilter(field_name='abs_nbrjour_93', label='Nombre de jours')
    

    class Meta:
        model = Absence
        # fields = ['abs_mat_95', 'abs_nat_9', 'abs_date_deb',
        #           'abs_date_fin']
        exclude=['abs_mat_95','abs_nat_9','abs_date_deb','abs_perdeb_x','abs_date_fin','abs_perfin_x','abs_nbrjour_93','abs_cumule_9','index_pk']

congnat_choices = (
        ('1', 'Annuel'),
        ('2', 'Recuperation'),
        ('3', 'Exceptionnel')
    )

class congeFilter(django_filters.FilterSet):
    cong_mat_95=NumberFilter(field_name='cong_mat_95', label='Matricule personnel')
    cong_nat_9 = django_filters.ChoiceFilter(choices=congnat_choices, label='Nature congé')
    cong_ancsold_93=NumberFilter(field_name='cong_ancsold_93', label='Ancien solde')
    cong_nbrjour_93=NumberFilter(field_name='cong_nbrjour_93', label='Nombre jours')
    cong_novsold_93=NumberFilter(field_name='cong_novsold_93', label='Nouveau solde')
    cong_date_deb = django_filters.DateFilter(widget=DatePickerInput(), label='Date début')
    cong_perdeb_x = django_filters.ChoiceFilter(choices=per_choices, label='Periode début')
    cong_date_fin = django_filters.DateFilter(widget=DatePickerInput(),label='Date fin')
    cong_perfin_x = django_filters.ChoiceFilter(choices=per_choices, label='Periode fin')
    class Meta:
        model = Conge
        # fields = ['cong_mat_95', 'cong_nat_9', 'cong_date_deb',
        #           'cong_date_fin']
        exclude=['cong_mat_95','cong_nat_9','cong_ancsold_93','cong_nbrjour_93','cong_novsold_93','cong_date_deb','cong_perdeb_x','cong_date_fin','cong_perfin_x','index_pk']

mois_choices= (
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
    )

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

type_choices = (
        ('0','0'),
        ('1','1'),
    )

class paieFilter(django_filters.FilterSet):
    mois = django_filters.ChoiceFilter(choices=mois_choices, label = 'Mois')
    anne = NumberFilter(field_name='anne', label='Année')
    class Meta:
        model = Paie
        exclude = ['mois', 'anne', 'jours_pres', 'matricule', 'nom_ligne', 'mnt_ligne', 'nbre_qte', 'type_ligne', 'num_ord', 'index_pk']


