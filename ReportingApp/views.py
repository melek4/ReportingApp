from copyreg import pickle
from django.shortcuts import render
from django.views import View
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO


import decimal
from re import S
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.http import HttpResponse, HttpRequest
from django.views.generic import View


from ReportingApp.forms import PersonnelForm, AbsenceForm, CongeForm, PaieForm, FDPForm
from .models import Direction, Natureagent, Personnel, Absence, NatAbs, YearData, Conge, Paie
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from .utils import get_Age_Genre_Barplot, get_Age_Category_Barplot, get_Abs_Repartition_Donut_Chart, get_Days_Sex_Barplot, get_Abs_Cat_Sex, get_Effectifs_Donut_Chart, get_Genre_Cat_Prof_Barchart, get_bar_chart_p4
from .filters import congeFilter, personnelFilter, absenceFilter, paieFilter
# Create your views here.

# this is where the views(functions) of the application are defined



@login_required(login_url='login_user')
def FDP_download(request):
    context = {}
    if request.method == "POST":
        form = FDPForm(request.POST)
        if form.is_valid():
            return HttpResponse('All Good!')
        else:
            return HttpResponse(form.errors.values()) 
    else:
        context['form'] = FDPForm()

    return render(request, 'fdp_download.html', context)


def FDP_data(id, year, month):
    paie_queryset = Paie.objects.filter(matricule=id).filter(anne=year).filter(mois=month)
    personne= get_object_or_404(Personnel, pers_mat_95=id)

    matricule = id
    qualification = personne.pers_qualif_x45
    direction = personne.pers_affect_92.lib_direction.upper()
    date_de_paie = str(month) + '/' + str(year)
    salaire_de_base = ''
    nb_jour = ''
    if paie_queryset.filter(nom_ligne__iexact="SALAIRE DE BASE "):
        salaire_de_base = paie_queryset.filter(nom_ligne__iexact="SALAIRE DE BASE ").values('mnt_ligne')[0]['mnt_ligne']
        nb_jour = paie_queryset.filter(nom_ligne__iexact="SALAIRE DE BASE ").values('jours_pres')[0]['jours_pres']
    indemnite_projet = ''
    if  paie_queryset.filter(nom_ligne__iexact="INDEMNITE DE PROJET"):
        indemnite_projet = paie_queryset.filter(nom_ligne__iexact="INDEMNITE DE PROJET").values('mnt_ligne')[0]['mnt_ligne']
    indemnite_representation = ''
    if paie_queryset.filter(nom_ligne__iexact="Indemnite de Representation"):
        indemnite_representation = paie_queryset.filter(nom_ligne__iexact="Indemnite de Representation").values('mnt_ligne')[0]['mnt_ligne']
    indemnite_kilometrique = ''
    if paie_queryset.filter(nom_ligne__iexact="Indemnite Kilometrique"):
        indemnite_kilometrique = paie_queryset.filter(nom_ligne__iexact="Indemnite Kilometrique").values('mnt_ligne')[0]['mnt_ligne']
    indemnite_majoration_kilometrique = ''
    if paie_queryset.filter(nom_ligne__iexact="Indemnite Majoration Kilometrique"):
        indemnite_majoration_kilometrique = paie_queryset.filter(nom_ligne__iexact="Indemnite Majoration Kilometrique").values('mnt_ligne')[0]['mnt_ligne']
    indemnite_specifique = ''
    if paie_queryset.filter(nom_ligne__iexact="Indemnite Specifique 2016-2017-2018"):
        indemnite_specifique = paie_queryset.filter(nom_ligne__iexact="Indemnite Specifique 2016-2017-2018").values('mnt_ligne')[0]['mnt_ligne']
    salaire_brut = ''
    if paie_queryset.filter(nom_ligne__iexact="SALAIRE BRUT"):
        salaire_brut = paie_queryset.filter(nom_ligne__iexact="SALAIRE BRUT").values('mnt_ligne')[0]['mnt_ligne']
    retenue_retraite = ''
    if paie_queryset.filter(nom_ligne__iexact="RETENUE RETRAITE"):
        retenue_retraite = paie_queryset.filter(nom_ligne__iexact="RETENUE RETRAITE").values('mnt_ligne')[0]['mnt_ligne']
    retenue_prevoyage_sociale = ''
    if paie_queryset.filter(nom_ligne__iexact="RETENUE PREVOYANCE SOCIALE"):
        retenue_prevoyage_sociale = paie_queryset.filter(nom_ligne__iexact="RETENUE PREVOYANCE SOCIALE").values('mnt_ligne')[0]['mnt_ligne']
    retenue_capital_decès = ''
    if paie_queryset.filter(nom_ligne__iexact="RETENUE CAPITAL DECES"):
        retenue_capital_decès = paie_queryset.filter(nom_ligne__iexact="RETENUE CAPITAL DECES").values('mnt_ligne')[0]['mnt_ligne']
    salaire_imposable = ''
    if paie_queryset.filter(nom_ligne__iexact="SALAIRE IMPOSABLE"):
        salaire_imposable = paie_queryset.filter(nom_ligne__iexact="SALAIRE IMPOSABLE").values('mnt_ligne')[0]['mnt_ligne']
    contribution_sociale = ''
    if paie_queryset.filter(nom_ligne__iexact="CONTRIBUTION SOCIALE DE SOLIDARITE"):
        contribution_sociale = paie_queryset.filter(nom_ligne__iexact="CONTRIBUTION SOCIALE DE SOLIDARITE").values('mnt_ligne')[0]['mnt_ligne']
    retenue_impot = ''
    if paie_queryset.filter(nom_ligne__iexact="RETENUE IMPOT SUR LE REVENU"):
        retenue_impot = paie_queryset.filter(nom_ligne__iexact="RETENUE IMPOT SUR LE REVENU").values('mnt_ligne')[0]['mnt_ligne']
    retenue_assurance_groupe = ''
    if paie_queryset.filter(nom_ligne__iexact="RETENUE ASSURANCE GROUPE"):
        retenue_assurance_groupe = paie_queryset.filter(nom_ligne__iexact="RETENUE ASSURANCE GROUPE").values('mnt_ligne')[0]['mnt_ligne']
    retenue_assurance_retraite = ''
    if paie_queryset.filter(nom_ligne__iexact="RETENUE ASSURANCE RETRAITE"):
        retenue_assurance_retraite = paie_queryset.filter(nom_ligne__iexact="RETENUE ASSURANCE RETRAITE").values('mnt_ligne')[0]['mnt_ligne']
    net_a_payer = ''
    if paie_queryset.filter(nom_ligne__iexact="NET A PAYER"):
        net_a_payer = paie_queryset.filter(nom_ligne__iexact="NET A PAYER").values('mnt_ligne')[0]['mnt_ligne']
    
    
    context={'matricule':matricule, 'qualification':qualification, 'direction':direction, 'date_de_paie':date_de_paie, 'salaire_de_base':salaire_de_base,
    'nb_jour':nb_jour, 'indemnite_projet':indemnite_projet, 'indemnite_representation':indemnite_representation, 'indemnite_kilometrique':indemnite_kilometrique,
    'indemnite_majoration_kilometrique':indemnite_majoration_kilometrique, 'indemnite_specifique':indemnite_specifique, 'salaire_brut':salaire_brut,
    'retenue_retraite':retenue_retraite, 'retenue_prevoyage_sociale':retenue_prevoyage_sociale, 'retenue_capital_decès':retenue_capital_decès,
    'salaire_imposable':salaire_imposable, 'contribution_sociale':contribution_sociale, 'retenue_impot':retenue_impot, 'retenue_assurance_groupe':retenue_assurance_groupe,
    'retenue_assurance_retraite':retenue_assurance_retraite, 'net_a_payer':net_a_payer}

    return context

@login_required(login_url='login_user')
def fiche_de_paie(request, id, year, month):
    context = FDP_data(id, year, month)

    
    return render (request , 'fiche_de_paie.html', context )

@login_required(login_url='login_user')
def list_Paie(request):
    
    context = {}
    paie_list = Paie.objects.all()
    paie_Filter = paieFilter(request.GET, queryset=paie_list)
    paie_list = paie_Filter.qs
    # add the dictionary during initialization
    context["paie_list"] = paie_list
    context['paie_Filter'] = paie_Filter
    


    return render(request, "CRUD_operations/Paie_view.html", context)

@login_required(login_url='login_user')
def create_Paie(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = PaieForm(request.POST or None)
    if form.is_valid():
        form.save()
        mat = form.cleaned_data.get("index_pk")
        sucess_message = ("Paie %d ajoutée avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        return HttpResponseRedirect("/list_Paie")

    context['form'] = form
    return render(request, "CRUD_operations/Paie_create.html", context)

@login_required(login_url='login_user')
def update_Paie(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Paie, index_pk=id)

    # pass the object as instance in form
    form = PaieForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        mat = form.cleaned_data.get("index_pk")
        form.save()
        sucess_message = ("Paie %d modifiée avec succés" % mat )
        messages.add_message(request, messages.INFO, sucess_message)
        return HttpResponseRedirect("/list_Paie/")

    # add form dictionary to context
    context["form"] = form

    return render(request, "CRUD_operations/Paie_update.html", context)


@login_required(login_url='login_user')
def delete_Paie(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Paie, index_pk=id)

    if request.method == "POST":
        mat = obj.index_pk
        sucess_message = ("Paie %d supprimée avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/list_Paie/")

    return render(request, "CRUD_operations/Paie_delete.html", context)

@login_required(login_url='login_user')
def pers_paie_detail_view(request, id, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["p"] = Paie.objects.filter(index_pk=pk).get(matricule=id)

    return render(request, "CRUD_operations/pers_paie_detail_view.html", context)

@login_required(login_url='login_user')
def view_pers_paie(request, id):
    context = {}
    paie_list = Paie.objects.filter(matricule=id)
    context["paie_list"] = paie_list
    return render(request, "CRUD_operations/view_pers_paie.html", context)

@login_required(login_url='login_user')
def create_Personnel(request):
    context = {}

    # add the dictionary during initialization
    form = PersonnelForm(request.POST or None)
    if form.is_valid():
        form.save()
        mat = form.cleaned_data.get("pers_mat_95")
        sucess_message = ("Personnel %d ajouté avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        return HttpResponseRedirect("/list_Personnel")

    context['form'] = form
    return render(request, "CRUD_operations/Personnel_create.html", context)
# class create_Personnel(View):
#     def get(self, request, *args, **kwargs):
#         form = PersonnelForm()
#         return render(request, 'CRUD_operations/Personnel_create.html',{'form': form})

#     def post(self, request, *args, **kwargs):
#         form = PersonnelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('list_Personnel')
#         return render(request, 'CRUD_operations/Personnel_create.html', {'form': form})

@login_required(login_url='login_user')
def list_Personnel(request):
    
    context = {}
    pers_list = Personnel.objects.all().order_by('-pers_mat_95')[:10]
    personnel_Filter = personnelFilter(request.GET, queryset=Personnel.objects.all().order_by('-pers_mat_95'))
    pers_list = personnel_Filter.qs
    # add the dictionary during initialization
    context["Person_list"] = pers_list
    context['personnel_Filter'] = personnel_Filter


    return render(request, "CRUD_operations/Personnel_view.html", context)

@login_required(login_url='login_user')
def update_Personnel(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Personnel, pers_mat_95=id)

    # pass the object as instance in form
    form = PersonnelForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        mat = form.cleaned_data.get("pers_mat_95")
        sucess_message = ("Personnel %d modifié avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        return HttpResponseRedirect("/list_Personnel/")

    # add form dictionary to context
    context["form"] = form

    return render(request, "CRUD_operations/Personnel_update.html", context)

@login_required(login_url='login_user')
def delete_Personnel(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Personnel, pers_mat_95=id)

    if request.method == "POST":
        mat = obj.pers_mat_95
        sucess_message = ("Personnel %d supprimé avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/list_Personnel/")

    return render(request, "CRUD_operations/Personnel_delete.html", context)

@login_required(login_url='login_user')
def create_Absence(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = AbsenceForm(request.POST or None)
    if form.is_valid():
        form.save()
        mat = form.cleaned_data.get("index_pk")
        sucess_message = ("Absence %d ajoutée avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        return HttpResponseRedirect("/list_Absence")

    context['form'] = form
    return render(request, "CRUD_operations/Absence_create.html", context)

@login_required(login_url='login_user')
def list_Absence(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    abs_list = Absence.objects.all().order_by('-abs_date_deb')[:10]
    absence_Filter = absenceFilter(request.GET, queryset=Absence.objects.all().order_by('-abs_date_deb'))
    abs_list = absence_Filter.qs

    # add the dictionary during initialization
    context["Abs_list"] = abs_list
    context['absence_Filter'] = absence_Filter

    return render(request, "CRUD_operations/Absence_view.html", context)

@login_required(login_url='login_user')
def update_Absence(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Absence, index_pk=id)

    # pass the object as instance in form
    form = AbsenceForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        mat = form.cleaned_data.get("index_pk")
        sucess_message = ("Absence %d modifiée avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        return HttpResponseRedirect("/list_Absence/")

    # add form dictionary to context
    context["form"] = form

    return render(request, "CRUD_operations/Absence_update.html", context)

@login_required(login_url='login_user')
def delete_Absence(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Absence, index_pk=id)

    if request.method == "POST":
        mat = obj.index_pk
        sucess_message = ("Absence %d supprimée avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/list_Absence/")

    return render(request, "CRUD_operations/Absence_delete.html", context)

@login_required(login_url='login_user')
def create_Conge(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = CongeForm(request.POST or None)
    if form.is_valid():
        mat = form.cleaned_data.get("index_pk")
        sucess_message = ("Congé %d ajouté avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        form.save()
        return HttpResponseRedirect("/list_Conge")

    context['form'] = form
    return render(request, "CRUD_operations/Conge_create.html", context)

@login_required(login_url='login_user')
def list_Conge(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    cong_list = Conge.objects.all().order_by('-cong_date_deb')[:10]
    conge_Filter = congeFilter(request.GET, queryset=Conge.objects.all().order_by('-cong_date_deb'))
    cong_list = conge_Filter.qs

    # add the dictionary during initialization
    context["Cong_list"] = cong_list
    context['conge_Filter'] = conge_Filter

    return render(request, "CRUD_operations/Conge_view.html", context)

@login_required(login_url='login_user')
def update_Conge(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Conge, index_pk=id)

    # pass the object as instance in form
    form = CongeForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        mat = form.cleaned_data.get("index_pk")
        sucess_message = ("Congé %d modifié avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        form.save()
        return HttpResponseRedirect("/list_Conge/")

    # add form dictionary to context
    context["form"] = form

    return render(request, "CRUD_operations/Conge_update.html", context)


@login_required(login_url='login_user')
def delete_Conge(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Conge, index_pk=id)

    if request.method == "POST":
        mat = obj.index_pk
        sucess_message = ("Congé %d supprimé avec succés" % mat )
        messages.add_message(request, messages.SUCCESS, sucess_message)
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/list_Conge/")

    return render(request, "CRUD_operations/Conge_delete.html", context)

@login_required(login_url='login_user')
def pers_abs_detail_view(request, id, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["p"] = Absence.objects.filter(index_pk=pk).get(abs_mat_95=id)

    return render(request, "CRUD_operations/pers_abs_detail_view.html", context)

@login_required(login_url='login_user')
def pers_cong_detail_view(request, id, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["p"] = Conge.objects.filter(index_pk=pk).get(cong_mat_95=id)

    return render(request, "CRUD_operations/pers_cong_detail_view.html", context)

@login_required(login_url='login_user')
def view_pers_cong_abs(request, id):
    context = {}
    Abs_list = Absence.objects.filter(abs_mat_95=id)
    context["Abs_list"] = Abs_list
    Cong_list = Conge.objects.filter(cong_mat_95=id)
    context["Cong_list"] = Cong_list
    return render(request, "CRUD_operations/view_pers_cong_abs.html", context)
# @login_required  # means that only looged in users can access this view
# Personnel.objects.all() reads all the objects(lines) of the personnel table
# .filter() is almost like "where" in sql u can see more of the options here
# and here https://docs.djangoproject.com/en/4.0/topics/db/aggregation/
# and a video here https://www.youtube.com/watch?v=WimXjp0ryOo&list1=LL&index=1&t=147s
# return render(request, 'first.html', {'Effectif_total': Effectif_total}) this line defines the template page associated with this view 'first.html'
# {'Effectif_total': Effectif_total} this means that Effectif_total of this function can be called in the html file associated ('first.html')
# using the name 'Effectif_total'


def Percent(group, total):
    percent = []
    for i in range(0, len(group)):
        percent.append((group[i]*100)/total)
        percent[i] = "{:.2f}".format(percent[i])
    return (percent)


def nb_cat_p7(cat):   #this function provides data of 2.3 and 2.4_par genre, par categorie et par profil(page 7)  for each categorie
    val_list2M = [0, 0, 0] #list to contain male data for the specified category  
    val_list2F = [0, 0, 0]  #female data
    val_list1 = [0, 0, 0] #data for category for table 2.3
    val_list2M[0] = Personnel.objects.filter(pers_cet_9=0).filter(
        pers_natpers_9=2).filter(pers_sexe_x__iexact='M').filter(pers_catpers_9=cat).count() #hommes dans directions techniques de la categorie specifié
    val_list2F[0] = Personnel.objects.filter(pers_cet_9=0).filter(
        pers_natpers_9=2).filter(pers_sexe_x__iexact='F').filter(pers_catpers_9=cat).count()
    val_list2M[1] = Personnel.objects.filter(pers_cet_9=0).exclude(
        pers_natpers_9=2).filter(pers_sexe_x__iexact='M').filter(pers_catpers_9=cat).count() #hommes dans directions de gestion de la categorie specifié
    val_list2F[1] = Personnel.objects.filter(pers_cet_9=0).exclude(
        pers_natpers_9=2).filter(pers_sexe_x__iexact='F').filter(pers_catpers_9=cat).count()
    val_list2M[2] = val_list2M[0]+val_list2M[1]  #total hommes dans la categorie specifié
    val_list2F[2] = val_list2F[0]+val_list2F[1]  #femmes
    val_list1[0] = val_list2M[0]+val_list2F[0]  #total par nature de personnel(techniche)
    val_list1[1] = val_list2M[1]+val_list2F[1]  #total par nature de personnel(gestion)
    val_list1[2] = val_list2M[2]+val_list2F[2]  #total de personnel(les deux)
    perc_list1 = Percent(val_list1, val_list1[2]) #% de personnel pr nature (tech/gestion/total)
    perc_list2M = Percent(val_list2M, val_list2M[2]) #% des hommes par nature pour la categorie specifié
    perc_list2F = Percent(val_list2F, val_list2F[2]) #% femmes ...........
    return(val_list1, perc_list1, val_list2M, perc_list2M, val_list2F, perc_list2F)


def Age_Calculator(i):
    today = date.today()
    return (today.year - i.pers_date_nais.year -
            ((today.month, today.day) < (i.pers_date_nais.month, i.pers_date_nais.day)))


def Age_Group(age, age_groupe):   #classification of employees per age group 
    if 25 <= age <= 29:
        age_groupe[0] += 1
    elif 30 <= age <= 34:
        age_groupe[1] += 1
    elif 35 <= age <= 39:
        age_groupe[2] += 1
    elif 40 <= age <= 44:
        age_groupe[3] += 1
    elif 45 <= age <= 49:
        age_groupe[4] += 1
    elif 50 <= age <= 54:
        age_groupe[5] += 1
    elif 55 <= age:
        age_groupe[6] += 1


def Age_query(Category):
    Age_Groupes = [0, 0, 0, 0, 0, 0, 0]
    count = 0
    Total = 0
    for i in Personnel.objects.all().filter(pers_cet_9=0).filter(pers_catpers_9=Category):  #for each employee of the corresponding category:
        age = Age_Calculator(i)   #calculate his age
        Age_Group(age, Age_Groupes)  #classification to age groups for the corresponding category
        count+=1  #count of people in the corresponding category
        Total += age   #sum of ages per category to use later for average
    return (Age_Groupes, count, Total)


def Average_Year(S, C):
    return(S//C)


def Average_Month(S, C):
    M = ((S/C) % 1)*12
    M = "{:.0f}".format(M)
    return(M)


def Anc_Calculator(i):
    today = date.today()
    return (today.year - i.pers_date_rec.year -
            ((today.month, today.day) < (i.pers_date_rec.month, i.pers_date_rec.day)))


def Anc_Group(anc, anc_groupe):
    if 0 <= anc < 5:
        anc_groupe[0] += 1
    elif 5 <= anc < 10:
        anc_groupe[1] += 1
    elif 10 <= anc < 15:
        anc_groupe[2] += 1
    elif 15 <= anc < 20:
        anc_groupe[3] += 1
    elif 20 <= anc < 25:
        anc_groupe[4] += 1
    elif 25 <= anc:
        anc_groupe[5] += 1


def Anc_query(Category):   # same as age for anciennete
    Anc_Groupes = [0, 0, 0, 0, 0, 0]
    count = 0
    Total = 0

    for i in Personnel.objects.all().filter(pers_cet_9=0).filter(pers_catpers_9=Category):
        anc = Anc_Calculator(i)
        Anc_Group(anc, Anc_Groupes)
        count += 1
        Total += anc
    return (Anc_Groupes, count, Total)


def Abs_query(mat_list, cat, list1, total_list):

    for i in Absence.objects.all().filter(abs_date_deb__year=2021).filter(abs_nat_9=cat).filter(
            abs_mat_95__pers_sexe_x__iexact='F'):  #for females
        if i.abs_mat_95 not in mat_list:   # mat list contains matricules of employees that have absence (this loop counts unique females for the specified abs nat)
            list1[3] += 1
            mat_list.append(i.abs_mat_95)
        list1[4] += 1   #count of nb. cas of the specified abs nat
        list1[5] += i.abs_nbrjour_93  # count of total days of absence of the specified abs nat
    for i in Absence.objects.all().filter(abs_date_deb__year=2021).filter(abs_nat_9=cat).filter(
            abs_mat_95__pers_sexe_x__iexact='M'):  #same as female but for male
        if i.abs_mat_95 not in mat_list:
            list1[6] += 1
            mat_list.append(i.abs_mat_95)
        list1[7] += 1
        list1[8] += i.abs_nbrjour_93
    list1[0] = list1[3]+list1[6]   #effectif total pour cet abs nat
    list1[1] = list1[4]+list1[7]   # nb. cas total .......
    list1[2] = list1[5]+list1[8]   #nb jours total .......
    for i in range(0, 9):
        total_list[i] += list1[i]   #adds the data of this nat abs to a list that contains the sum of data of all abs nats


def Abs_query2(cat, total_list, mat_list):
    list1 = [0, 0, 0]
    for i in Personnel.objects.filter(
            pers_sexe_x__iexact='F').filter(pers_catpers_9=cat):
        if i.pers_mat_95 in mat_list:
            list1[0] += 1        #count of female employees of the specified category that exist in the absence table

    for i in Personnel.objects.filter(
            pers_sexe_x__iexact='M').filter(pers_catpers_9=cat):
        if i.pers_mat_95 in mat_list:
            list1[1] += 1        #same for male
    list1[2] = list1[0]+list1[1]   #total of employees that exist in the absence table
    total_list[0] += list1[0]  #adding the previous data of the specified category to a list that will hold data for all categories combined
    total_list[1] += list1[1]
    total_list[2] += list1[2]
    return (list1)


def dir_query(label):
    val_list = []
    list2 = [4, 2, 1, 5]
    label_query_set = Personnel.objects.filter(
        pers_cet_9=0).filter(pers_affect_92=label) #select employees that work in the specified direction
    for i in list2:
        val_list.append(label_query_set.filter(pers_catpers_9=i).exclude(
            pers_natpers_9=2).filter(pers_sexe_x__iexact='M').count()) #number of males with the specified category that work in the direction
        val_list.append(label_query_set.filter(pers_catpers_9=i).exclude(
            pers_natpers_9=2).filter(pers_sexe_x__iexact='F').count())
        val_list.append(label_query_set.filter(pers_catpers_9=i).filter(
            pers_natpers_9=2).filter(pers_sexe_x__iexact='M').count())
        val_list.append(label_query_set.filter(pers_catpers_9=i).filter(
            pers_natpers_9=2).filter(pers_sexe_x__iexact='F').count())
    return(val_list)


def effectif_natureagent():
    val_list = []
    records = Personnel.objects.filter(pers_cet_9=0)
    act_etap = records.filter(pers_naturagent_93=1).count()      #personnel en activité à etap
    detaches = records.filter(pers_naturagent_93__in=[6, 7, 8]).count()      #personnel detaches
    disp = records.filter(pers_naturagent_93=14).count()         #personnel mis en disponibilite
    det_aupres = records.filter(pers_naturagent_93__in=[5, 15]).count()     #personnel detaches aupres d'etap
    contrac = records.filter(pers_naturagent_93__in=[2, 3]).count()       #effectifs contractuels
    val_list.append(act_etap+detaches+disp)
    val_list.append(act_etap)
    val_list.append(detaches)
    val_list.append(disp)
    val_list.append(det_aupres)
    val_list.append(contrac)
    return val_list


def natureagent_categorie(i):   #count of employees per natureagent per category
    val_list = []
    records = Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=i)
    act_etap = records.filter(pers_naturagent_93=1).count()
    detaches = records.filter(pers_naturagent_93__in=[6, 7, 8]).count()
    disp = records.filter(pers_naturagent_93=14).count()
    det_aupres = records.filter(pers_naturagent_93__in=[15, 5]).count()
    contrac = records.filter(pers_naturagent_93__in=[2, 3]).count()
    val_list.append(act_etap)
    val_list.append(detaches)
    val_list.append(disp)
    val_list.append(contrac)
    val_list.append(act_etap+detaches+disp+contrac)
    val_list.append(det_aupres)
    return val_list


def nat_cat_tech(i): #for each category (cadre, maitrise...): count of "personnel dans directions techniques", "personnel technique exercant a etap"
                                                              #"personnel technique hors etap" and "femmes dans directions techniques"
    val_list = []
    records = Personnel.objects.filter(pers_cet_9=0).filter(
        pers_affect_92__in=['EX', 'DE', 'ED', 'DO', 'OC', 'DI', 'PS', 'OI']).filter(pers_catpers_9=i)  #personnel dans directions techniques
    total = records.count()
    femmes = Personnel.objects.filter(pers_cet_9=0).filter(
        pers_affect_92__in=['EX', 'DE', 'ED', 'DO', 'OC', 'DI', 'PS', 'OI']).filter(pers_sexe_x__iexact='F').count()
    etap = records.filter(pers_naturagent_93__in=[1, 2, 3, 6, 7, 8]).count()  #personnel technique exercant a etap
    hors_etap = records.filter(pers_naturagent_93__in=[5, 14, 15]).count()    #personnel technique hors etap
    val_list.append(etap)
    val_list.append(hors_etap)
    val_list.append(total)
    val_list.append(femmes)
    return val_list


def nat_cat_gest(i):   #same as above but for gestion instead of technique
    val_list = []
    records = Personnel.objects.filter(pers_cet_9=0).exclude(
        pers_affect_92__in=['EX', 'DE', 'ED', 'DO', 'OC', 'DI', 'PS', 'OI']).filter(pers_catpers_9=i)
    total = records.count()
    femmes = Personnel.objects.filter(pers_cet_9=0).exclude(
        pers_affect_92__in=['EX', 'DE', 'ED', 'DO', 'OC', 'DI', 'PS', 'OI']).filter(pers_sexe_x__iexact='F').count()
    etap = records.filter(pers_naturagent_93__in=[1, 2, 3, 6, 7, 8]).count()
    hors_etap = records.filter(pers_naturagent_93__in=[5, 14, 15]).count()
    val_list.append(etap)
    val_list.append(hors_etap)
    val_list.append(total)
    val_list.append(femmes)
    return val_list

def retraite(y):
        cat = [4, 2, 1, 5]
        yr_data = []  #a list that contains the year and the estimated employees that will retire of each category in that year 
        yr_data.append(y)
        #personnel technique
        tech = Personnel.objects.filter(pers_cet_9=0).filter(pers_natpers_9=2)
        for i in cat: #for each category
            count = 0
            for j in tech.filter(pers_catpers_9=i):
                if (y - j.pers_date_nais.year) == 60:
                    count += 1
            yr_data.append(count)
        #personnel de gestion
        gest = Personnel.objects.filter(pers_cet_9=0).exclude(pers_natpers_9=2)
        for i in cat: #for each category
            count = 0
            for j in gest.filter(pers_catpers_9=i):
                if (y - j.pers_date_nais.year) == 60:
                    count += 1
            yr_data.append(count)

        #total for the specified year
        total = Personnel.objects.filter(pers_cet_9=0)
        count = 0
        for j in total:
            if (y - j.pers_date_nais.year) == 60:
                count += 1
        yr_data.append(count)
        return(yr_data)


def bilan_social_data(request):
    ################################################ comp #######################################################

    Effectif_total = Personnel.objects.filter(pers_cet_9=0).count()
    nb_hommes = Personnel.objects.filter(
        pers_cet_9=0).filter(pers_sexe_x__iexact='M').count()
    nb_femmes = Personnel.objects.filter(
        pers_cet_9=0).filter(pers_sexe_x__iexact='F').count()

    natureag = effectif_natureagent()     #list of values of the first part of the first table

    nat_cat4 = natureagent_categorie(4)   #cadres par natureagent
    nat_cat2 = natureagent_categorie(2)   #maitrise par natureagent
    nat_cat1 = natureagent_categorie(1)   #execution par natureagent
    nat_cat5 = natureagent_categorie(5)   #execution maitrise par natureagent

    nat_cat_tech4 = nat_cat_tech(4)   #cadres dans directions techniques exercant a etap, hors etap, total et femmes
    nat_cat_tech2 = nat_cat_tech(2)   #same as above but for other categories (maitrise, execution...)
    nat_cat_tech1 = nat_cat_tech(1)
    nat_cat_tech5 = nat_cat_tech(5)

    nat_cat_gest4 = nat_cat_gest(4)
    nat_cat_gest2 = nat_cat_gest(2)
    nat_cat_gest1 = nat_cat_gest(1)
    nat_cat_gest5 = nat_cat_gest(5)

    ################################################ comp #######################################################

    ################################################ ages #######################################################
    Age_Groupes_Hommes = [0, 0, 0, 0, 0, 0, 0]
    Age_Groupes_Femmes = [0, 0, 0, 0, 0, 0, 0]
    HTotal = 0
    FTotal = 0
    TAge = 0

    for i in Personnel.objects.all().filter(pers_cet_9=0).filter(pers_sexe_x__iexact='M'): #male employees 1 by 1 calculate their age and add each one to the corresponding age group
        age = Age_Calculator(i)
        Age_Group(age, Age_Groupes_Hommes)
        HTotal += 1  #count of male employees
        TAge += age # sum of male's ages to use later for the average age
    for i in Personnel.objects.all().filter(pers_cet_9=0).filter(pers_sexe_x__iexact='F'):
        age = Age_Calculator(i)
        Age_Group(age, Age_Groupes_Femmes)
        FTotal += 1
        TAge += age

    Age_Groupes_Cadres, CTotal_p13, CTAge = Age_query(4)
    Age_Groupes_Maitrises, MTotal_p13, MTAge = Age_query(2)
    Age_Groupes_Execution, ETotal_p13, ETAge = Age_query(1)
    Age_Groupes_EM, EMTotal_p13, EMTAge = Age_query(5)


    Category_Total_By_Group_p13 = [0, 0, 0, 0, 0, 0, 0]
    Genre_Total_By_Group = [0, 0, 0, 0, 0, 0, 0]
    Total_p13 = HTotal+FTotal
    CatTotal_p13 = CTotal_p13+MTotal_p13+ETotal_p13+EMTotal_p13
    for i in range(0, 7):
        Genre_Total_By_Group[i] = Age_Groupes_Hommes[i] + Age_Groupes_Femmes[i]    #sum of male and female for each group to get the total of each age group
        Category_Total_By_Group_p13[i] = Age_Groupes_Cadres[i] + \
            Age_Groupes_Maitrises[i] + \
            Age_Groupes_Execution[i] + Age_Groupes_EM[i]  
    HPercent = Percent(Age_Groupes_Hommes, HTotal)   #percentage of each age group of the total (for males)
    FPercent = Percent(Age_Groupes_Femmes, FTotal)
    TPercent_By_Group = Percent(Genre_Total_By_Group, Total_p13)  #percentage ...... (for total)
    CPercent_p13 = Percent(Age_Groupes_Cadres, CTotal_p13)  #percentage....... (for cadres)
    MPercent_p13 = Percent(Age_Groupes_Maitrises, MTotal_p13)
    EPercent_p13 = Percent(Age_Groupes_Execution, ETotal_p13)
    EMPercent_p13 = Percent(Age_Groupes_EM, EMTotal_p13)
    TCPercent_p13 = Percent(Category_Total_By_Group_p13, CatTotal_p13)

    Average_Age_years = Average_Year(TAge, Total_p13)   #average age for all employees (years)
    Average_Age_Months = Average_Month(TAge, Total_p13)  #same but months 
    Average_Age_Years_C = Average_Year(CTAge, CTotal_p13) #average age for cadres
    Average_Age_Months_C = Average_Month(CTAge, CTotal_p13)  # etc
    Average_Age_Years_M = Average_Year(MTAge, MTotal_p13)
    Average_Age_Months_M = Average_Month(MTAge, MTotal_p13)
    Average_Age_Years_E = Average_Year(ETAge, ETotal_p13)
    Average_Age_Months_E = Average_Month(ETAge, ETotal_p13)
    Average_Age_Years_EM = Average_Year(EMTAge, EMTotal_p13)
    Average_Age_Months_EM = Average_Month(EMTAge, EMTotal_p13)

    avrg_age = f"{Average_Age_years} ans et {Average_Age_Months} mois"

    today = date.today()
    chart = get_Age_Genre_Barplot(Age_Groupes_Hommes, Age_Groupes_Femmes)
    chart2 = get_Age_Category_Barplot(
        Age_Groupes_Cadres, Age_Groupes_Maitrises, Age_Groupes_Execution, Age_Groupes_EM)

    age_lt_40 = 0
    for i in range(0, 3):
        age_lt_40 += Genre_Total_By_Group[i]   #count of employees with age < 40 
    perc_age_lt_40 = (age_lt_40*100)/Effectif_total  #% of .......
    perc_age_lt_40 = "{:.2f}".format(perc_age_lt_40)
    age_gt_40 = 0
    for i in range(3, 7):
        age_gt_40 += Genre_Total_By_Group[i]   #count ...... > 40  
    perc_age_gt_40 = (age_gt_40*100)/Effectif_total #% ......
    perc_age_gt_40 = "{:.2f}".format(perc_age_gt_40)

    ################################################ ages #######################################################
    ################################################ anc #######################################################

    Anc_Groupes_Cadres, CTotal_p14, CTAnc = Anc_query(4)    #same as age everything
    Anc_Groupes_Maitrises, MTotal_p14, MTAnc = Anc_query(2)
    Anc_Groupes_Execution, ETotal_p14, ETAnc = Anc_query(1)
    Anc_Groupes_EM, EMTotal_p14, EMTAnc = Anc_query(5)

    CatTotal_p14 = CTotal_p14+MTotal_p14+ETotal_p14+EMTotal_p14
    Category_Total_By_Group_p14 = [0, 0, 0, 0, 0, 0]
    for i in range(0, 6):
        Category_Total_By_Group_p14[i] = Anc_Groupes_Cadres[i] + \
            Anc_Groupes_Maitrises[i] + \
            Anc_Groupes_Execution[i] + Anc_Groupes_EM[i]
    TAnc = CTAnc+MTAnc+ETAnc+EMTAnc
    half = [0, 0]
    half[0] = Category_Total_By_Group_p14[0] + \
        Category_Total_By_Group_p14[1]
    half[1] = Category_Total_By_Group_p14[2]+Category_Total_By_Group_p14[3] + \
        Category_Total_By_Group_p14[4]+Category_Total_By_Group_p14[5]
    CPercent_p14 = Percent(Anc_Groupes_Cadres, CTotal_p14)
    MPercent_p14 = Percent(Anc_Groupes_Maitrises, MTotal_p14)
    EPercent_p14 = Percent(Anc_Groupes_Execution, ETotal_p14)
    EMPercent_p14 = Percent(Anc_Groupes_EM, EMTotal_p14)
    TCPercent_p14 = Percent(Category_Total_By_Group_p14, CatTotal_p14)
    half_Percent = Percent(half, CatTotal_p14)

    Average_Anc_Years_C = Average_Year(CTAnc, CTotal_p14)
    Average_Anc_Months_C = Average_Month(CTAnc, CTotal_p14)
    Average_Anc_Years_M = Average_Year(MTAnc, MTotal_p14)
    Average_Anc_Months_M = Average_Month(MTAnc, MTotal_p14)
    Average_Anc_Years_E = Average_Year(ETAnc, ETotal_p14)
    Average_Anc_Months_E = Average_Month(ETAnc, ETotal_p14)
    Average_Anc_Years_EM = Average_Year(EMTAnc, EMTotal_p14)
    Average_Anc_Months_EM = Average_Month(EMTAnc, EMTotal_p14)
    Average_Anc_Years_T = Average_Year(TAnc, CatTotal_p14)
    Average_Anc_Months_T = Average_Month(TAnc, CatTotal_p14)

    avrg_anc = f"{Average_Anc_Years_T} ans et {Average_Anc_Months_T} mois"

    ################################################ anc #######################################################
    ################################################ abs #######################################################

    codes = []
    labels = []
    mat_list = [] #list to contain unique matricules of employees that exist in absence table

    for i in NatAbs.objects.all():

        codes.append(i.code_abs)   # get codes of natabs
        s = i.libelle_abs.title()  # get labels of natabs
        labels.append(s)
    list1 = []
    total = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    nat_nb = NatAbs.objects.all().count()
    for i in range(0, nat_nb):
        test = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        list1.append(test)    # initialization of the list that will contain data for 5.2-absenteisme
    forlist = []
    j = 0
    for i in range(0, nat_nb):
        forlist.append(j)
        j += 1
    for i in range(0, nat_nb):
        mat_list.append([])
        Abs_query(mat_list[i], codes[i], list1[i], total)

    disp_list = zip(list1, labels)
    nb_jrs = [total[5], total[8]]
    percent = Percent(nb_jrs, total[2])  #% of days for females and males of the total days
    motives_nb_jrs = []
    F_days = []
    H_days = []
    for i in range(0, nat_nb):
        motives_nb_jrs.append(list1[i][2])  #list that contains number of days of each abs nat
        F_days.append(list1[i][5]) #same as above for females
        H_days.append(decimal.Decimal(list1[i][8]))  #same as above for male

    for i in range(0, nat_nb):
        motives_percent = Percent(motives_nb_jrs, total[2])  #% of days of each abs nat of the total days
    graph = get_Abs_Repartition_Donut_Chart(
        labels, motives_percent, motives_nb_jrs)
    graph2 = get_Days_Sex_Barplot(labels, F_days, H_days)

    total_list = [0, 0, 0]
    tlist = []
    for i in Absence.objects.filter(abs_date_deb__year=2021).values('abs_mat_95'):
        if i['abs_mat_95'] not in tlist:
            tlist.append(i['abs_mat_95'])
    t = len(tlist)
    abs_cadres = Abs_query2(4, total_list, tlist)  #abs data for cadres
    abs_maitrise = Abs_query2(2, total_list, tlist)
    abs_execution = Abs_query2(1, total_list, tlist)
    abs_em = Abs_query2(5, total_list, tlist)

    graph3 = get_Abs_Cat_Sex(abs_cadres, abs_maitrise, abs_execution, abs_em)

    taux_abse = (total[2]*100)/(Effectif_total*298)
    taux_abse = "{:.2f}".format(taux_abse)  #taux d'absenteisme

    ################################################ abs #######################################################
    ################################################ Rep pers #######################################################
    p7_c_val, p7_c_per, p7_cm_val, p7_cm_per, p7_cf_val, p7_cf_per = nb_cat_p7(        
        4)   #data for cadres
    p7_m_val, p7_m_per, p7_mm_val, p7_mm_per, p7_mf_val, p7_mf_per = nb_cat_p7(
        2)   #data for maitrise
    p7_e_val, p7_e_per, p7_em_val, p7_em_per, p7_ef_val, p7_ef_per = nb_cat_p7(
        1)   #data for execution 
    p7_exm_val, p7_exm_per, p7_exmm_val, p7_exmm_per, p7_exmf_val, p7_exmf_per = nb_cat_p7(
        5)   #data for execution_maitrise

    p7_total_val = [0, 0, 0]
    for i in range(0, 3):
        p7_total_val[i] = p7_c_val[i]+p7_m_val[i]+p7_e_val[i]+p7_exm_val[i]
    p7_totat_per = Percent(p7_total_val, p7_total_val[2])

    def barchart_p8(ind):
        M = [0, 0, 0, 0]
        F = [0, 0, 0, 0]
        M[0] = p7_cm_val[ind]
        M[1] = p7_mm_val[ind]
        M[2] = p7_em_val[ind]
        M[3] = p7_exmm_val[ind]
        F[0] = p7_cf_val[ind]
        F[1] = p7_mf_val[ind]
        F[2] = p7_ef_val[ind]
        F[3] = p7_exmf_val[ind]
        return(M, F)

    bar_MT, bar_FT = barchart_p8(0)
    bar_MG, bar_FG = barchart_p8(1)

    g_p8 = get_Genre_Cat_Prof_Barchart(bar_MT, bar_FT, bar_MG, bar_FG)

    g = get_Effectifs_Donut_Chart(
        p7_c_val[2], p7_m_val[2], p7_e_val[2], p7_exm_val[2])

    ################################################ Rep pers #######################################################
    ################################################ Rep pers dir #######################################################
    total_v = []
    dir_val_list = []
    Dir_labels = []
    for i in Direction.objects.all():
        Dir_labels.append(i.code_direction)  #labels that will be displayed 
        total_v.append(Personnel.objects.filter(pers_cet_9=0).filter(
            pers_affect_92=i.code_direction).count()) #total employees working in each direction
        dir_val_list.append(dir_query(i.code_direction))  #the data of each direction
    template_list = zip(Dir_labels, dir_val_list, total_v)  #zipping lists to be able to iterate through all of the them at the same time

    ################################################ Rep pers dir #######################################################
    thisyear = YearData(year=today.year, eff_tot=Effectif_total, eff_perm=natureag[0], act_etap=natureag[1], detach=natureag[2], disp=natureag[3], det_aupres=natureag[4], contract=natureag[5], nb_c=p7_c_val[2],
                        nb_m=p7_m_val[2], nb_e=p7_e_val[2], nb_em=p7_exm_val[2], nb_ing=p7_c_val[0], nb_tech=p7_m_val[0], nb_ag_tech=p7_e_val[0]+p7_exm_val[0], nb_cg=p7_c_val[1], nb_ag_mg=p7_m_val[1], nb_admin=p7_e_val[1]+p7_exm_val[1],
                        nb_h=nb_hommes, nb_f=nb_femmes, age_moy=avrg_age, anc_moy=avrg_anc, taux_abs=taux_abse, nb_ptech=p7_total_val[
                            0], nb_pgest=p7_total_val[1],
                        age_inf_40=perc_age_lt_40, age_sup_40=perc_age_gt_40, abs_nb_jrs=total[2])  #storing all the necessary data of the current year to the database to be able to use it in the future reports
    thisyear.save()

    def yearperc(val, total):
        perc = (val*100)/total
        perc = "{:.2f}".format(perc)
        return(perc)

    def yearsdata(y):
        listvals = []
        listperc = []

        for i in YearData.objects.filter(year=y):
            #reading values of the specified year from the new table we created in the database
            listvals.append(i.year)
            listvals.append(i.eff_tot)
            listvals.append(i.eff_perm)
            listvals.append(i.act_etap)
            listvals.append(i.detach)
            listvals.append(i.disp)
            listvals.append(i.det_aupres)
            listvals.append(i.contract)
            listvals.append(i.nb_c)
            listvals.append(i.nb_m)
            listvals.append(i.nb_e)
            listvals.append(i.nb_em)
            listvals.append(i.nb_ing)
            listvals.append(i.nb_tech)
            listvals.append(i.nb_ag_tech)
            listvals.append(i.nb_cg)
            listvals.append(i.nb_ag_mg)
            listvals.append(i.nb_admin)
            listvals.append(i.nb_h)
            listvals.append(i.nb_f)
            listvals.append(i.age_moy)
            listvals.append(i.anc_moy)
            listvals.append(i.taux_abs)
            listvals.append(i.nb_ptech)
            listvals.append(i.nb_pgest)
            listvals.append(i.age_inf_40)
            listvals.append(i.age_sup_40)
            listvals.append(i.abs_nb_jrs)   
            #calculating the needed percentages as we read to optimize
            listperc.append(yearperc(i.nb_c, i.eff_tot))
            listperc.append(yearperc(i.nb_m, i.eff_tot))
            listperc.append(yearperc(i.nb_e, i.eff_tot))
            listperc.append(yearperc(i.nb_em, i.eff_tot))
            listperc.append(yearperc(i.nb_ing, i.eff_tot))
            listperc.append(yearperc(i.nb_tech, i.eff_tot))
            listperc.append(yearperc(i.nb_ag_tech, i.eff_tot))
            listperc.append(yearperc(i.nb_cg, i.eff_tot))
            listperc.append(yearperc(i.nb_ag_mg, i.eff_tot))
            listperc.append(yearperc(i.nb_admin, i.eff_tot))
            listperc.append(yearperc(i.nb_h, i.eff_tot))
            listperc.append(yearperc(i.nb_f, i.eff_tot))
            listperc.append(yearperc(i.nb_ptech, i.eff_tot))
            listperc.append(yearperc(i.nb_pgest, i.eff_tot))
            listperc.append(
                yearperc(i.act_etap+i.contract+i.det_aupres, i.eff_tot))
            listperc.append(yearperc(i.detach, i.eff_tot))
            listperc.append(yearperc(i.nb_ing, i.eff_tot))
            listperc.append(yearperc(i.nb_tech, i.eff_tot))
            listperc.append(yearperc(i.nb_ag_tech, i.eff_tot))
            listperc.append(yearperc(i.nb_cg, i.eff_tot))
            listperc.append(yearperc(i.nb_ag_mg, i.eff_tot))
            listperc.append(yearperc(i.nb_admin, i.eff_tot))  
        return(listvals, listperc)
    #reading data and calculating percentages of the current year and the 2 before it
    thisyearvals, thisyearperc = yearsdata(today.year)  
    thisyear1vals, thisyear1perc = yearsdata(today.year-1)
    thisyear2vals, thisyear2perc = yearsdata(today.year-2)

    g_p4 = get_bar_chart_p4(thisyearvals[8], thisyearvals[9], thisyearvals[10], thisyearvals[11], thisyear1vals[8], thisyear1vals[9],
                            thisyear1vals[10], thisyear1vals[11], thisyear2vals[8], thisyear2vals[9], thisyear2vals[10], thisyear2vals[11])

    ################################################## p11 ##############################################
    ################################################## departs #####################################################

    p15 = []
    #calculating retirement data for the current tear and 16 years ahead:
    for i in range(0, 16):
        p15.append(retraite(today.year+i))

    ################################################## departs #####################################################

    today = today.strftime("%d/%m/%Y")

    
    
    

    context = {'g': g, 'p7_c_val': p7_c_val, 'p7_m_val': p7_m_val, 'p7_e_val': p7_e_val, 'p7_exm_val': p7_exm_val, 'p7_c_per': p7_c_per,
               'p7_cm_val': p7_cm_val, 'p7_cm_per': p7_cm_per, 'p7_cf_val': p7_cf_val, 'p7_cf_per': p7_cf_per, 'p7_m_per': p7_m_per, 'p7_mm_val': p7_mm_val,
               'p7_mm_per': p7_mm_per, 'p7_mf_val': p7_mf_val, 'p7_mf_per': p7_mf_per, 'p7_e_per': p7_e_per, 'p7_em_val': p7_em_val, 'p7_em_per': p7_em_per,
               'p7_ef_val': p7_ef_val, 'p7_ef_per': p7_ef_per, 'p7_exm_per': p7_exm_per, 'p7_exmm_val': p7_exmm_val, 'p7_exmm_per': p7_exmm_per,
               'p7_exmf_val': p7_exmf_val, 'p7_exmf_per': p7_exmf_per, 'p7_total_val': p7_total_val, 'p7_totat_per': p7_totat_per, 'today': today,
               'Dir_labels': Dir_labels, 'Age_Groupes_Hommes': Age_Groupes_Hommes, 'Age_Groupes_Femmes': Age_Groupes_Femmes,
               'Genre_Total_By_Group': Genre_Total_By_Group, 'Total_p13': Total_p13, 'HTotal': HTotal, 'FTotal': FTotal, 'HPercent': HPercent,
               'FPercent': FPercent, 'TPercent_By_Group': TPercent_By_Group, 'Average_Age_years': Average_Age_years, 'Average_Age_Months': Average_Age_Months,
               'today': today, 'chart': chart, 'chart2': chart2, 'Age_Groupes_Cadres': Age_Groupes_Cadres, 'Age_Groupes_Maitrises': Age_Groupes_Maitrises,
               'Age_Groupes_Execution': Age_Groupes_Execution, 'Age_Groupes_EM': Age_Groupes_EM, 'CTotal_p13': CTotal_p13, 'MTotal_p13': MTotal_p13,
               'ETotal_p13': ETotal_p13, 'EMTotal_p13': EMTotal_p13, 'Category_Total_By_Group_p13': Category_Total_By_Group_p13,
               'CatTotal_p13': CatTotal_p13, 'CPercent_p13': CPercent_p13, 'MPercent_p13': MPercent_p13, 'EPercent_p13': EPercent_p13,
               'EMPercent_p13': EMPercent_p13, 'TCPercent_p13': TCPercent_p13, 'Average_Age_Years_C': Average_Age_Years_C,
               'Average_Age_Months_C': Average_Age_Months_C, 'Average_Age_Years_M': Average_Age_Years_M, 'Average_Age_Months_M': Average_Age_Months_M,
               'Average_Age_Years_E': Average_Age_Years_E, 'Average_Age_Months_E': Average_Age_Months_E, 'Average_Age_Years_EM': Average_Age_Years_EM,
               'Average_Age_Months_EM': Average_Age_Months_EM, 'EMTAge': EMTAge, 'Age_Groupes_Cadres': Age_Groupes_Cadres,
               'Anc_Groupes_Cadres': Anc_Groupes_Cadres, 'Anc_Groupes_Maitrises': Anc_Groupes_Maitrises, 'Anc_Groupes_Execution': Anc_Groupes_Execution,
               'Anc_Groupes_EM': Anc_Groupes_EM, 'Category_Total_By_Group_p14': Category_Total_By_Group_p14, 'CPercent_p14': CPercent_p14,
               'MPercent_p14': MPercent_p14, 'EPercent_p14': EPercent_p14, 'EMPercent_p14': EMPercent_p14, 'TCPercent_p14': TCPercent_p14,
               'CTotal_p14': CTotal_p14, 'MTotal_p14': MTotal_p14, 'ETotal_p14': ETotal_p14, 'EMTotal_p14': EMTotal_p14, 'CatTotal_p14': CatTotal_p14,
               'Average_Anc_Years_C': Average_Anc_Years_C, 'Average_Anc_Months_C': Average_Anc_Months_C, 'Average_Anc_Years_M': Average_Anc_Years_M,
               'Average_Anc_Months_M': Average_Anc_Months_M, 'Average_Anc_Years_E': Average_Anc_Years_E, 'Average_Anc_Months_E': Average_Anc_Months_E,
               'Average_Anc_Years_EM': Average_Anc_Years_EM, 'Average_Anc_Months_EM': Average_Anc_Months_EM, 'half_Percent': half_Percent,
               'Average_Anc_Years_T': Average_Anc_Years_T, 'Average_Anc_Months_T': Average_Anc_Months_T, 'disp_list': disp_list, 'nat_nb': nat_nb,
               'total': total, 'forlist': forlist, 'percent': percent, 'motives_percent': motives_percent, 'graph': graph, 'graph2': graph2,
               'abs_cadres': abs_cadres, 'abs_maitrise': abs_maitrise, 'abs_execution': abs_execution, 'abs_em': abs_em, 'total_list': total_list,
               'graph3': graph3, 'mat_list': mat_list, 't': t, 'g_p8': g_p8, 'bar_MT': bar_MT, 'thisyearvals': thisyearvals, 'thisyearperc': thisyearperc,
               'thisyear1vals': thisyear1vals, 'thisyear1perc': thisyear1perc, 'thisyear2vals': thisyear2vals, 'thisyear2perc': thisyear2perc, 'g_p4': g_p4,
               'template_list': template_list, 'p15': p15, 'nat_cat4': nat_cat4, 'nat_cat2': nat_cat2, 'nat_cat1': nat_cat1, 'nat_cat5': nat_cat5,
               'nat_cat_tech4': nat_cat_tech4, 'nat_cat_tech2': nat_cat_tech2, 'nat_cat_tech1': nat_cat_tech1, 'nat_cat_tech5': nat_cat_tech5,
               'nat_cat_gest4': nat_cat_gest4, 'nat_cat_gest2': nat_cat_gest2, 'nat_cat_gest1': nat_cat_gest1, 'nat_cat_gest5': nat_cat_gest5,
               }

    return(context)


@login_required(login_url='login_user')
def Principaux_indicateurs(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/Principaux_indicateurs.html', context)


@login_required(login_url='login_user')
def I_1(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_1.html', context)


@login_required(login_url='login_user')
def I_2_1(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_1.html', context)


@login_required(login_url='login_user')
def I_2_2(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_2.html', context)


@login_required(login_url='login_user')
def I_2_3(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_3.html', context)


@login_required(login_url='login_user')
def I_2_4(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_4.html', context)


@login_required(login_url='login_user')
def I_2_5_1(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_5_1.html', context)


@login_required(login_url='login_user')
def I_2_5_2(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_5_2.html', context)


@login_required(login_url='login_user')
def I_2_6(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_6.html', context)


@login_required(login_url='login_user')
def I_2_7_1(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_7_1.html', context)


@login_required(login_url='login_user')
def I_2_7_2(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_7_2.html', context)


@login_required(login_url='login_user')
def I_2_7(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_7.html', context)


@login_required(login_url='login_user')
def I_2_8_1(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_8_1.html', context)


@login_required(login_url='login_user')
def I_2_8(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_2_8.html', context)


@login_required(login_url='login_user')
def I_3(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_3.html', context)


@login_required(login_url='login_user')
def I_4(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_4.html', context)


@login_required(login_url='login_user')
def I_5_1(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_5_1.html', context)


@login_required(login_url='login_user')
def I_5_2(request):
    context = bilan_social_data(HttpRequest)
    return render(request, 'Bilan-social/I_5_2.html', context)


@login_required(login_url='login_user')
def bilan_social(request):
    context = bilan_social_data(HttpRequest)

    return render(request, 'bilan_social.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    result.close()
    return None


data = bilan_social_data(HttpRequest)

# Opens up page as PDF


class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        
        pdf = render_to_pdf('bilan_social_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
data2 = FDP_data(9857, 2022, 1)


class ViewFDPPDF(View):
    def get(self, request, *args, **kwargs):
        
        pdf = render_to_pdf('fdp_download.html', data2)
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file

class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        pdf = render_to_pdf('bilan_social_pdf.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Bilan_social_%s.pdf" % str(today)
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response

class DownloadFDPPDF(View):
    def get(self, request, *args, **kwargs):

        pdf = render_to_pdf('fdp_download.html', data2)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Fiche_de_paie_{data2['matricule']}_{data2['date_de_paie']}.pdf"  
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response

def login_user(request):
    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            return redirect('homepage')
        else:
            messages.success(
                request, ("Invalid email or password!"))
            return redirect('login_user')
    else:
        return render(request, 'login.html', {})


@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login_user')



def homepage(request):
    return render(request, 'home.html', {})



@login_required(login_url='login_user')
def personnelDashboard(request):
    context = {}
    labels=[]
    data1=[]
    dir_queryset=Direction.objects.all()
    pers_queryset=Personnel.objects.filter(pers_cet_9=0)
    for i in dir_queryset:
        labels.append(i.code_direction)
        data1.append(pers_queryset.filter(pers_affect_92=i.code_direction).count())

    context['labels']=labels
    context['data1']=data1

    dataDirectionM = []
    dataDirectionF = []

    for i in dir_queryset:
        dataDirectionM.append(pers_queryset.filter(pers_sexe_x='M').filter(pers_affect_92=i.code_direction).count())
        dataDirectionF.append(pers_queryset.filter(pers_sexe_x='F').filter(pers_affect_92=i.code_direction).count())

    context['dataDirectionM']=dataDirectionM
    context['dataDirectionF']=dataDirectionF

    dataDirectionCadre = []
    dataDirectionMaitrise = []
    dataDirectionExecution = []
    dataDirectionExecution_Maitrise = []


    for i in dir_queryset:
        dataDirectionCadre.append(pers_queryset.filter(pers_catpers_9=4).filter(pers_affect_92=i.code_direction).count())
        dataDirectionMaitrise.append(pers_queryset.filter(pers_catpers_9=2).filter(pers_affect_92=i.code_direction).count())
        dataDirectionExecution.append(pers_queryset.filter(pers_catpers_9=1).filter(pers_affect_92=i.code_direction).count())
        dataDirectionExecution_Maitrise.append(pers_queryset.filter(pers_catpers_9=5).filter(pers_affect_92=i.code_direction).count())

    context['dataDirectionCadre']=dataDirectionCadre
    context['dataDirectionMaitrise']=dataDirectionMaitrise
    context['dataDirectionExecution']=dataDirectionExecution
    context['dataDirectionExecution_Maitrise']=dataDirectionExecution_Maitrise

    labelsCategorie = ['Cadre' , 'Maitrise' , 'Execution' , 'Execution-maitrise' ]
    ListCat=[4,2,1,5]
    dataActif = []
    datainactif_Temporaire = []
    dataInactif = []
    pers_queryset_all=Personnel.objects.all()
    for i in ListCat:
        dataActif.append(pers_queryset_all.filter(pers_cet_9=0).filter(pers_catpers_9=i).count())
        datainactif_Temporaire.append(pers_queryset_all.filter(pers_cet_9=1).filter(pers_catpers_9=i).count())
        dataInactif.append(pers_queryset_all.filter(pers_cet_9=2).filter(pers_catpers_9=i).count())
    context['dataActif']=dataActif
    context['datainactif_Temporaire']=datainactif_Temporaire
    context['dataInactif']=dataInactif
    context['labelsCategorie']=labelsCategorie

    dataGestion = []
    dataTechnique = []
    for i in ListCat:
        dataGestion.append(pers_queryset.filter(pers_natpers_9=1).filter(pers_catpers_9=i).count())
        
        dataTechnique.append(pers_queryset.filter(pers_natpers_9=2).filter(pers_catpers_9=i).count())
    context['dataGestion']=dataGestion
    context['dataTechnique']=dataTechnique

    labelsNatureagent = []
    labelsNatureagentExplicit = []
    dataNatureagent= []
    dataNatureagentCadre= []
    dataNatureagentMaitrise= []
    dataNatureagentExecution= []
    dataNatureagentExecution_Maitrise =[]
    distinct_natureagent = Natureagent.objects.all()

    for i in distinct_natureagent:
        labelsNatureagent.append(str(i.natag_code_93))
        labelsNatureagentExplicit.append(i.natag_lib_x50.title())
        dataNatureagent.append(pers_queryset.filter(pers_naturagent_93 = i.natag_code_93).count())
        dataNatureagentCadre.append(pers_queryset.filter(pers_catpers_9=4).filter(pers_naturagent_93 = i.natag_code_93).count())
        dataNatureagentMaitrise.append(pers_queryset.filter(pers_catpers_9=2).filter(pers_naturagent_93 = i.natag_code_93).count())
        dataNatureagentExecution.append(pers_queryset.filter(pers_catpers_9=1).filter(pers_naturagent_93 = i.natag_code_93).count())
        dataNatureagentExecution_Maitrise.append(pers_queryset.filter(pers_catpers_9=5).filter(pers_naturagent_93 = i.natag_code_93).count())
    labelsNatureagent2=zip(labelsNatureagent,labelsNatureagentExplicit)
    context['labelsNatureagent']=labelsNatureagent
    context['labelsNatureagent2']=labelsNatureagent2
    context['dataNatureagentCadre']=dataNatureagentCadre
    context['dataNatureagentMaitrise']=dataNatureagentMaitrise
    context['dataNatureagentExecution']=dataNatureagentExecution
    context['dataNatureagentExecution_Maitrise']=dataNatureagentExecution_Maitrise
    context['dataNatureagent']=dataNatureagent

    def data_calulator(cat, nat, years):
        if nat == 'tech':
            query=Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=cat).filter(pers_natpers_9=2)
        elif nat == 'gest' :
            query=Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=cat).exclude(pers_natpers_9=2)
        elif nat == 'total' :
            query=Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=cat)

        cat_data=[]
        for y in years :
            count = 0
            for i in query:
                if y-i.pers_date_nais.year==60:
                    count += 1 
            cat_data.append(count)

        return cat_data
    today=datetime.today()
    dataCategorieNat = []
    labelsYear = []
    label = ['Cadre Tech', 'Maitrise Tech', 'Execution Tech', 'Execution-Maitrise Tech', 'Cadre Gest', 'Maitrise Gest', 'Execution Gest', 'Execution-Maitrise Gest']
    for i in range(0, 16):
        labelsYear.append(today.year+i)
    for nat in ['tech', 'gest']:
        for cat in [4,2,1,5]:
            dataCategorieNat.append(data_calulator(cat, nat, labelsYear))
    data_list=zip(dataCategorieNat, label)
    context['data_list']=data_list
    context['labelsYear']=labelsYear
    
    totalretr = []
    for y in labelsYear :
            countretr = 0
            for i in Personnel.objects.filter(pers_cet_9=0):
                if y-i.pers_date_nais.year==60:
                    countretr += 1 
            totalretr.append(countretr)
    context['totalretr']=totalretr

    labels2=[]
    queryset=Personnel.objects.all().order_by('pers_date_rec')
    for i in queryset:
        year=i.pers_date_rec.year
        if year not in labels2:
            labels2.append(year)
    context['labels2']=labels2
    totalrecr = []
    for y in labels2 :
            countrecr = 0
            for i in queryset:
                if i.pers_date_rec.year==y:
                    countrecr += 1
            totalrecr.append(countrecr)
    context['totalrecr']=totalrecr
    dataCadre=[]
    dataMaitrise=[]
    dataExecution=[]
    dataExecutionMaitrise=[]
    for y in labels2:
        dataCadre.append(Personnel.objects.filter(pers_date_rec__year=y).filter(pers_catpers_9=4).count())
        dataMaitrise.append(Personnel.objects.filter(pers_date_rec__year=y).filter(pers_catpers_9=2).count())
        dataExecution.append(Personnel.objects.filter(pers_date_rec__year=y).filter(pers_catpers_9=1).count())
        dataExecutionMaitrise.append(Personnel.objects.filter(pers_date_rec__year=y).filter(pers_catpers_9=5).count())
    context['dataCadre']=dataCadre
    context['dataMaitrise']=dataMaitrise
    context['dataExecution']=dataExecution
    context['dataExecutionMaitrise']=dataExecutionMaitrise

    cadre=[0,0,0,0,0,0]
    exec=[0,0,0,0,0,0]
    maitr=[0,0,0,0,0,0]
    exec_maitr=[0,0,0,0,0,0]
    for i in pers_queryset.filter(pers_catpers_9=4):
        anc = Anc_Calculator(i)
        Anc_Group(anc, cadre)
    for i in pers_queryset.filter(pers_catpers_9=2):
        anc = Anc_Calculator(i)
        Anc_Group(anc, exec)
    for i in pers_queryset.filter(pers_catpers_9=1):
        anc = Anc_Calculator(i)
        Anc_Group(anc, maitr)
    for i in pers_queryset.filter(pers_catpers_9=5):
        anc = Anc_Calculator(i)
        Anc_Group(anc, exec_maitr)

    labelsAnc=['0-5 ans', '5-10 ans', '10-15 ans', '15-20 ans','20-25 ans', 'plus de 25 ans']

    context['cadre']=cadre
    context['maitr']=maitr
    context['exec']=exec
    context['exec_maitr']=exec_maitr
    context['labelsAnc']=labelsAnc
    return render(request, 'dashboards/personnelDashboard.html', context)

@login_required(login_url='login_user')
def directionDashboard(request):
    context = {}
    dir_queryset=Direction.objects.all()
    pers_queryset=Personnel.objects.filter(pers_cet_9=0)
    labels=[]
    data1=[]
    for i in dir_queryset:
        labels.append(i.code_direction)
        data1.append(pers_queryset.filter(pers_affect_92=i.code_direction).count())
    context['labels']=labels
    context['data1']=data1

    dataDirectionM = []
    dataDirectionF = []

    for i in dir_queryset:
        dataDirectionM.append(pers_queryset.filter(pers_sexe_x='M').filter(pers_affect_92=i.code_direction).count())
        dataDirectionF.append(pers_queryset.filter(pers_sexe_x='F').filter(pers_affect_92=i.code_direction).count())

    context['dataDirectionM']=dataDirectionM
    context['dataDirectionF']=dataDirectionF

    dataDirectionCadre = []
    dataDirectionMaitrise = []
    dataDirectionExecution = []
    dataDirectionExecution_Maitrise = []


    for i in dir_queryset:
        dataDirectionCadre.append(pers_queryset.filter(pers_catpers_9=4).filter(pers_affect_92=i.code_direction).count())
        dataDirectionMaitrise.append(pers_queryset.filter(pers_catpers_9=2).filter(pers_affect_92=i.code_direction).count())
        dataDirectionExecution.append(pers_queryset.filter(pers_catpers_9=1).filter(pers_affect_92=i.code_direction).count())
        dataDirectionExecution_Maitrise.append(pers_queryset.filter(pers_catpers_9=5).filter(pers_affect_92=i.code_direction).count())

    context['dataDirectionCadre']=dataDirectionCadre
    context['dataDirectionMaitrise']=dataDirectionMaitrise
    context['dataDirectionExecution']=dataDirectionExecution
    context['dataDirectionExecution_Maitrise']=dataDirectionExecution_Maitrise

    return render(request, 'dashboards/directionDashboard.html', context)

@login_required(login_url='login_user')
def fluxDashboard(request):
    context = {}
    def retr_data_calulator(cat, nat, years):
        if nat == 'tech':
            query=Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=cat).filter(pers_natpers_9=2)
        elif nat == 'gest' :
            query=Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=cat).exclude(pers_natpers_9=2)
        elif nat == 'total' :
            query=Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=cat)

        cat_data=[]
        for y in years :
            count = 0
            for i in query:
                if y-i.pers_date_nais.year==60:
                    count += 1 
            cat_data.append(count)

        return cat_data

    def recr_data_calulator(cat, nat, years):
        if nat == 'tech':
            query=Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=cat).filter(pers_natpers_9=2)
        elif nat == 'gest' :
            query=Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=cat).exclude(pers_natpers_9=2)
        elif nat == 'total' :
            query=Personnel.objects.filter(pers_cet_9=0).filter(pers_catpers_9=cat)

        cat_data=[]
        for y in years :
            count = 0
            for i in query:
                if i.pers_date_rec.year==y:
                    count += 1 
            cat_data.append(count)

        return cat_data
    today=datetime.date.today()
    dataCategorieNat = []
    labelsYear = []
    label = ['Cadre Tech', 'Maitrise Tech', 'Execution Tech', 'Execution-Maitrise Tech', 'Cadre Gest', 'Maitrise Gest', 'Execution Gest', 'Execution-Maitrise Gest']
    for i in range(0, 16):
        labelsYear.append(today.year+i)
    for nat in ['tech', 'gest']:
        for cat in [4,2,1,5]:
            dataCategorieNat.append(retr_data_calulator(cat, nat, labelsYear))
    data_list=zip(dataCategorieNat, label)
    context['data_list']=data_list
    context['labelsYear']=labelsYear
    
    totalretr = []
    for y in labelsYear :
            countretr = 0
            for i in Personnel.objects.filter(pers_cet_9=0):
                if y-i.pers_date_nais.year==60:
                    countretr += 1 
            totalretr.append(countretr)
    context['totalretr']=totalretr

    labels2=[]
    queryset=Personnel.objects.all().order_by('pers_date_rec')
    for i in queryset:
        year=i.pers_date_rec.year
        if year not in labels2:
            labels2.append(year)
    context['labels2']=labels2
    dataCategorieNatRecr = []
    for nat in ['tech', 'gest']:
        for cat in [4,2,1,5]:
            dataCategorieNatRecr.append(recr_data_calulator(cat, nat, labels2))
    data_list_recr=zip(dataCategorieNatRecr, label)
    context['data_list_recr'] = data_list_recr
    totalrecr = []
    for y in labels2 :
            countrecr = 0
            for i in queryset:
                if i.pers_date_rec.year==y:
                    countrecr += 1
            totalrecr.append(countrecr)
    context['totalrecr']=totalrecr
    dataCadre=[]
    dataMaitrise=[]
    dataExecution=[]
    dataExecutionMaitrise=[]
    for y in labels2:
        dataCadre.append(Personnel.objects.filter(pers_date_rec__year=y).filter(pers_catpers_9=4).count())
        dataMaitrise.append(Personnel.objects.filter(pers_date_rec__year=y).filter(pers_catpers_9=2).count())
        dataExecution.append(Personnel.objects.filter(pers_date_rec__year=y).filter(pers_catpers_9=1).count())
        dataExecutionMaitrise.append(Personnel.objects.filter(pers_date_rec__year=y).filter(pers_catpers_9=5).count())
    

    context['dataCadre']=dataCadre
    context['dataMaitrise']=dataMaitrise
    context['dataExecution']=dataExecution
    context['dataExecutionMaitrise']=dataExecutionMaitrise

    labels3=[]
    for y in labelsYear:
        labels3.append(y-60)
    dataCadreRetr=[]
    dataMaitriseRetr=[]
    dataExecutionRetr=[]
    dataExecutionMaitriseRetr=[]
    for y in labels3:
        dataCadreRetr.append(Personnel.objects.filter(pers_date_nais__year=y).filter(pers_catpers_9=4).count())
        dataMaitriseRetr.append(Personnel.objects.filter(pers_date_nais__year=y).filter(pers_catpers_9=2).count())
        dataExecutionRetr.append(Personnel.objects.filter(pers_date_nais__year=y).filter(pers_catpers_9=1).count())
        dataExecutionMaitriseRetr.append(Personnel.objects.filter(pers_date_nais__year=y).filter(pers_catpers_9=5).count())
    context['dataCadreRetr']=dataCadreRetr
    context['dataMaitriseRetr']=dataMaitriseRetr
    context['dataExecutionRetr']=dataExecutionRetr
    context['dataExecutionMaitriseRetr']=dataExecutionMaitriseRetr

    return render(request, 'dashboards/fluxDashboard.html', context)

@login_required(login_url='login_user')
def additionalStatistics(request):
    context = {}
    labelsCategorie = ['Cadre' , 'Maitrise' , 'Execution' , 'Execution-maitrise' ]
    ListCat=[4,2,1,5]
    dataActif = []
    datainactif_Temporaire = []
    dataInactif = []
    pers_queryset_all=Personnel.objects.all()
    pers_queryset=Personnel.objects.filter(pers_cet_9=0)
    for i in ListCat:
        dataActif.append(pers_queryset_all.filter(pers_cet_9=0).filter(pers_catpers_9=i).count())
        datainactif_Temporaire.append(pers_queryset_all.filter(pers_cet_9=1).filter(pers_catpers_9=i).count())
        dataInactif.append(pers_queryset_all.filter(pers_cet_9=2).filter(pers_catpers_9=i).count())
    context['dataActif']=dataActif
    context['datainactif_Temporaire']=datainactif_Temporaire
    context['dataInactif']=dataInactif
    context['labelsCategorie']=labelsCategorie

    dataGestion = []
    dataTechnique = []
    for i in ListCat:
        dataGestion.append(pers_queryset.filter(pers_natpers_9=1).filter(pers_catpers_9=i).count())
        
        dataTechnique.append(pers_queryset.filter(pers_natpers_9=2).filter(pers_catpers_9=i).count())
    context['dataGestion']=dataGestion
    context['dataTechnique']=dataTechnique

    labelsNatureagent = []
    labelsNatureagentExplicit = []
    dataNatureagent= []
    dataNatureagentCadre= []
    dataNatureagentMaitrise= []
    dataNatureagentExecution= []
    dataNatureagentExecution_Maitrise =[]
    distinct_natureagent = Natureagent.objects.all()

    for i in distinct_natureagent:
        labelsNatureagent.append(str(i.natag_code_93))
        labelsNatureagentExplicit.append(i.natag_lib_x50.title())
        dataNatureagent.append(pers_queryset.filter(pers_naturagent_93 = i.natag_code_93).count())
        dataNatureagentCadre.append(pers_queryset.filter(pers_catpers_9=4).filter(pers_naturagent_93 = i.natag_code_93).count())
        dataNatureagentMaitrise.append(pers_queryset.filter(pers_catpers_9=2).filter(pers_naturagent_93 = i.natag_code_93).count())
        dataNatureagentExecution.append(pers_queryset.filter(pers_catpers_9=1).filter(pers_naturagent_93 = i.natag_code_93).count())
        dataNatureagentExecution_Maitrise.append(pers_queryset.filter(pers_catpers_9=5).filter(pers_naturagent_93 = i.natag_code_93).count())
    labelsNatureagent2=zip(labelsNatureagent,labelsNatureagentExplicit)
    context['labelsNatureagent']=labelsNatureagent
    context['labelsNatureagent2']=labelsNatureagent2
    context['dataNatureagentCadre']=dataNatureagentCadre
    context['dataNatureagentMaitrise']=dataNatureagentMaitrise
    context['dataNatureagentExecution']=dataNatureagentExecution
    context['dataNatureagentExecution_Maitrise']=dataNatureagentExecution_Maitrise
    context['dataNatureagent']=dataNatureagent


    natag_cat=[]
    
    for i in distinct_natureagent:

        listtt=[]
        for j in [4,2,1,5]:
            listtt.append(pers_queryset.filter(pers_catpers_9=j).filter(pers_naturagent_93 = i.natag_code_93).count())
        natag_cat.append(listtt)

    listttt=zip(labelsNatureagent,natag_cat)
    context['listttt']=listttt

    cadre=[0,0,0,0,0,0]
    exec=[0,0,0,0,0,0]
    maitr=[0,0,0,0,0,0]
    exec_maitr=[0,0,0,0,0,0]
    for i in pers_queryset.filter(pers_catpers_9=4):
        anc = Anc_Calculator(i)
        Anc_Group(anc, cadre)
    for i in pers_queryset.filter(pers_catpers_9=2):
        anc = Anc_Calculator(i)
        Anc_Group(anc, exec)
    for i in pers_queryset.filter(pers_catpers_9=1):
        anc = Anc_Calculator(i)
        Anc_Group(anc, maitr)
    for i in pers_queryset.filter(pers_catpers_9=5):
        anc = Anc_Calculator(i)
        Anc_Group(anc, exec_maitr)

    labelsAnc=['0-5 ans', '5-10 ans', '10-15 ans', '15-20 ans','20-25 ans', 'plus de 25 ans']

    context['cadre']=cadre
    context['maitr']=maitr
    context['exec']=exec
    context['exec_maitr']=exec_maitr
    context['labelsAnc']=labelsAnc

    return render(request, 'dashboards/additionalStatistics.html', context)




@login_required(login_url='login_user')
def congeDashboard(request):
    context={}
    labels=['Annuel' , 'Recuperation' , 'Exceptionnel']
    data=[]
    
    conge_queryset=Conge.objects.all()
    for i in range(1,4):
        data.append(conge_queryset.filter(cong_nat_9=i).count())

    context['labels'] = labels
    context['data'] = data

    dataM=[]
    dataF=[]
    for j in range(1,4):
            dataM.append(conge_queryset.filter(cong_nat_9=j).filter(cong_mat_95__pers_sexe_x='M').count())
            dataF.append(conge_queryset.filter(cong_nat_9=j).filter(cong_mat_95__pers_sexe_x='F').count()) 

    context['dataM'] = dataM
    context['dataF'] = dataF

    dataCadre= []
    dataMaitrise= []
    dataExecution= []
    dataExecution_Maitrise =[]

    for j in range(1,4):
            dataCadre.append(conge_queryset.filter(cong_nat_9=j).filter(cong_mat_95__pers_catpers_9=4).count()) 
            dataMaitrise.append(conge_queryset.filter(cong_nat_9=j).filter(cong_mat_95__pers_catpers_9=2).count()) 
            dataExecution.append(conge_queryset.filter(cong_nat_9=j).filter(cong_mat_95__pers_catpers_9=1).count())
            dataExecution_Maitrise.append(conge_queryset.filter(cong_nat_9=j).filter(cong_mat_95__pers_catpers_9=5).count())

    context['dataCadre'] = dataCadre
    context['dataMaitrise'] = dataMaitrise
    context['dataExecution'] = dataExecution
    context['dataExecution_Maitrise'] = dataExecution_Maitrise
    
    labelsDirection= []
    dataAnnuel = []
    dataRecuperation =[]
    dataExceptionnel =[]
    dir_queryset = Direction.objects.all()

    for i in dir_queryset:
        labelsDirection.append(i.code_direction)
        
        dataAnnuel.append(conge_queryset.filter(cong_nat_9=1).filter(cong_mat_95__pers_affect_92=i).count())
        dataRecuperation.append(conge_queryset.filter(cong_nat_9=2).filter(cong_mat_95__pers_affect_92=i).count())
        dataExceptionnel.append(conge_queryset.filter(cong_nat_9=3).filter(cong_mat_95__pers_affect_92=i).count())

    context['labelsDirection'] = labelsDirection
    context['dataAnnuel'] = dataAnnuel
    context['dataRecuperation'] = dataRecuperation
    context['dataExceptionnel'] = dataExceptionnel

    return render(request, 'dashboards/congeDashboard.html', context)

import pickle
import pymysql
import pandas as pd
import datetime

@login_required(login_url='login_user')
def prevision(request):
    conn=pymysql.connect(host='localhost',port=int(3306),user='root',passwd='',db='hr')
    personnel1=pd.read_sql_query("SELECT * FROM personnel ",conn)
    personnel1 = personnel1.loc[personnel1['PERS_CET_9']==0]
    personnel = personnel1.drop(columns=['PERS_DATE_REC','PERS_DATE_NAIS', 'PERS_AFFECT_92', 'PERS_NATURAGENT_93', 'PERS_QUALIF_X45', 'PERS_CATPERS_9', 'PERS_NATPERS_9', 'PERS_SEXE_X', 'PERS_CET_9'])
    absence = pd.read_sql_query("SELECT * FROM absence ",conn)
    pers_abs = personnel.merge(absence,left_on='PERS_MAT_95',right_on='ABS_MAT_95', how='left')
    pers_abs = pers_abs.drop(columns=['ABS_MAT_95', 'ABS_PERDEB_X', 'ABS_DATE_FIN', 'ABS_PERFIN_X', 'ABS_CUMULE_9', 'INDEX_PK'])
    retard = pd.read_sql_query("SELECT * FROM retard ",conn)
    pers_ret = personnel.merge(retard,left_on='PERS_MAT_95',right_on='PERS_MAT_95', how='left')
    pers_ret = pers_ret.drop(columns=['TRIM', 'RECAP', 'INDEX_PK'])

    def absence_condition(mat, year, data):
        pers = pers_abs[pers_abs.PERS_MAT_95==mat]
        
        not_justified = False
        y=pd.DatetimeIndex(pers['ABS_DATE_DEB']).year
        year1data = pers[y==year-2]
        year2data = pers[y==year-1]
        year1_abs = year1data['ABS_NBRJOUR_93'].sum() # set the value of the selected rows' new 'year1' 
                                                                            # column to the number of his abs in the first year
        year2_abs = year2data['ABS_NBRJOUR_93'].sum()
        if (9 in year1data['ABS_NAT_9'].unique()) or (9 in year2data['ABS_NAT_9'].unique()):
            not_justified = True
        
        data['year1_abs'].append(year1_abs)
        data['year2_abs'].append(year2_abs)
        data['not_justified'].append(not_justified)


    def retard_condition(mat, year, data):
        pers = pers_ret[pers_ret.PERS_MAT_95==mat]
        
        y=pers['ANNE']
        year1data = pers[y==year-2]
        year2data = pers[y==year-1]
        year1_ret = year1data['NB_RETARD'].sum()
        year2_ret = year2data['NB_RETARD'].sum()
        
        data['year1_ret'].append(year1_ret)
        data['year2_ret'].append(year2_ret)


    fonction = pd.read_sql_query("SELECT * FROM fonction ",conn)
    pers_fonction = personnel.merge(fonction,left_on='PERS_MAT_95',right_on='HFONC_MAT_95', how='left')

    def fonction_condition(mat, data):
        current_year = pd.to_datetime(datetime.date.today())
        if mat in pers_fonction.HFONC_MAT_95.unique():
            pers = pers_fonction[pers_fonction.PERS_MAT_95==mat]
            

            y=pd.to_datetime(pd.DatetimeIndex(pers['HFONC_DATE1']))

            ancienneté = current_year-y
            ancienneté = (ancienneté[0].days)/365
            data['ancienneté'].append(ancienneté)
        else : 
            pers = personnel1[personnel1.PERS_MAT_95==mat]
            anc = pd.to_datetime(pd.DatetimeIndex(pers['PERS_DATE_REC']))
            ancienneté = current_year-anc
            ancienneté = (ancienneté[0].days)/365
            data['ancienneté'].append(ancienneté)


    note = pd.read_sql_query("SELECT * FROM note ",conn)
    pers_note = personnel.merge(note,left_on='PERS_MAT_95',right_on='NOTE_MAT_95', how='left')


    def note_condition(mat, year, data):
        pers = pers_note[pers_note.PERS_MAT_95==mat]
        
        y=pers['NOTE_ANNEE_94']
        year1data = pers[y==year-2]
        year2data = pers[y==year-1]
        year1_note = year1data['NOTE_NOTETRIMES_92'].sum()/4
        year2_note = year2data['NOTE_NOTETRIMES_92'].sum()/4
        
        data['year1_note'].append(year1_note)
        data['year2_note'].append(year2_note)


    personnel = personnel.set_index('PERS_MAT_95')

    current_year = datetime.date.today().year
    data = dict()
    data = {'mat':[],'year':[], 'year1_abs':[], 'year2_abs':[], 'not_justified':[], 'year1_ret':[], 'year2_ret':[] , 'year1_note':[], 'year2_note':[], 'ancienneté':[]}
    for index, row in personnel.iterrows():
        data['mat'].append(index)
        data['year'].append(current_year)
        absence_condition(index, current_year, data) # after setting the index to PERS_MAT_95, each rows' index is the PERS_MAT_95 of the personnel
        retard_condition(index, current_year, data)
        note_condition(index, current_year, data)
        fonction_condition(index, data)
    
    df_for_ml = pd.DataFrame(data)
    prevision_df = df_for_ml.drop(columns=['mat', 'year'])
    random_forest = pickle.load(open("random_forest.sav","rb"))
    y_pred = random_forest.predict(prevision_df)

    mats = df_for_ml['mat'].tolist()
    preds = y_pred.tolist()

    context = {}
    output = zip(mats,preds)
    context['output'] = output

    return render(request, 'prevision.html', context)


@login_required(login_url='login_user')
def pers_prom_detail_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["plist"] = Personnel.objects.filter(pers_mat_95=id)

    return render(request, "Promotion_pers.html", context)



from django.db.models import Sum


def absenceDashboard(request):
    context = {}
    year = datetime.date.today().year
    labelGenre = [year-2 , year-1, year]    
    dataHomme =[]
    dataFemme = []
    absence_queryset=Absence.objects.all()
    for i in labelGenre:
        dataFemme.append(float(str(absence_queryset.filter(abs_date_deb__year=i).filter(abs_mat_95__pers_sexe_x='F').aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))
        dataHomme.append(float(str(absence_queryset.filter(abs_date_deb__year=i).filter(abs_mat_95__pers_sexe_x='M').aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))

    context['dataFemme'] = dataFemme
    context['dataHomme'] = dataHomme
    context['labelGenre'] = labelGenre

    labelNature=[]
    dataF =[]
    dataH =[]
    natabs_queryset =  NatAbs.objects.all()
    for i in natabs_queryset:
        labelNature.append(i.libelle_abs)
        if absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_sexe_x='F').filter(abs_nat_9=i.code_abs):
             dataF.append(float(str(absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_sexe_x='F').filter(abs_nat_9=i.code_abs).aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))
        else:
            dataF.append(0) 
        if absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_sexe_x='M').filter(abs_nat_9=i.code_abs):
             dataH.append(float(str(absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_sexe_x='M').filter(abs_nat_9=i.code_abs).aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))
        else:
            dataH.append(0)

    context['labelNature'] = labelNature
    context['dataF'] = dataF
    context['dataH'] = dataH

    natabs_cat=[]
    genre_label = ['Femme', 'Homme']
    natabs_code = []
    for i in natabs_queryset:
        natabs_code.append(i.code_abs)
        listt=[]
        for j in ['F', 'M']:
            if absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_sexe_x=j).filter(abs_nat_9=i.code_abs):
                listt.append(float(str(absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_sexe_x=j).filter(abs_nat_9=i.code_abs).aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))
            else:
                listt.append(0) 
        natabs_cat.append(listt)

    listt=zip(natabs_code,natabs_cat)
    context['listt']=listt
    context['genre_label']=genre_label
    context['natabs_code'] = natabs_code
    legend_natabs = zip(natabs_code,labelNature)
    context['legend_natabs'] = legend_natabs
    data =[]

    for i in natabs_queryset:
        if absence_queryset.filter(abs_date_deb__year=2021).filter(abs_nat_9=i.code_abs):
        
             data.append(float(str(absence_queryset.filter(abs_date_deb__year=2021).filter(abs_nat_9=i.code_abs).aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))
        else:
            data.append(0)

    context['data'] = data


    labelGenreCat=['Femme', 'Homme' ]
    ListGenre=['F', 'M']
    dataCadre =[]
    dataMaitrise =[]
    dataExec =[]
    dataExecMait =[]
    
    for i in ListGenre:
     
        dataCadre.append(float(str(absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_catpers_9=4).filter(abs_mat_95__pers_sexe_x=i).aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))
        
        dataMaitrise.append(float(str(absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_catpers_9=2).filter(abs_mat_95__pers_sexe_x=i).aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))

        dataExec.append(float(str(absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_catpers_9=1).filter(abs_mat_95__pers_sexe_x=i).aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))
        
        dataExecMait.append(float(str(absence_queryset.filter(abs_date_deb__year=2021).filter(abs_mat_95__pers_catpers_9=5).filter(abs_mat_95__pers_sexe_x=i).aggregate(Sum('abs_nbrjour_93'))['abs_nbrjour_93__sum'])))

    context['labelGenreCat'] = labelGenreCat
    context['dataCadre'] = dataCadre
    context['dataMaitrise'] = dataMaitrise
    context['dataExec'] = dataExec
    context['dataExecMait'] = dataExecMait


    return render(request, 'dashboards/absenceDashboard.html', context)
