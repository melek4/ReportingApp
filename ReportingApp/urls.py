from django.urls import path
from . import views



# this file contains paths of the apllication
# i.e: path('first/', views.Principal_Indicators, name='first') :  'first/' is the url to access the page, views.Principal_Indicators references
# the function Principal_Indicators in the views.py file which s the function to execute when visiting the associated path, name='first' gives it
# a name so it can be referenced in the html templates

urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('homepage/', views.homepage, name='homepage'),

    path('personnelDashboard/', views.personnelDashboard, name='personnelDashboard'),
    path('directionDashboard/', views.directionDashboard, name='directionDashboard'),
    path('fluxDashboard/', views.fluxDashboard, name='fluxDashboard'),
    path('additionalStatistics/', views.additionalStatistics, name='additionalStatistics'),
    path('congeDashboard/', views.congeDashboard, name='congeDashboard'),
    path('absenceDashboard/', views.absenceDashboard, name='absenceDashboard'),


    path('', views.homepage, name='homepage'),

    path('logout_user/', views.logout_user, name='logout_user'),
    path('bilan_social/', views.bilan_social, name='bilan_social'),

    path('I_1/', views.I_1, name='I_1'),
    path('I_2_1/', views.I_2_1, name='I_2_1'),
    path('I_2_2/', views.I_2_2, name='I_2_2'),
    path('I_2_3/', views.I_2_3, name='I_2_3'),
    path('I_2_4/', views.I_2_4, name='I_2_4'),
    path('I_2_5_1/', views.I_2_5_1, name='I_2_5_1'),
    path('I_2_5_2/', views.I_2_5_2, name='I_2_5_2'),
    path('I_2_6/', views.I_2_6, name='I_2_6'),
    path('I_2_7/', views.I_2_7, name='I_2_7'),
    path('I_2_7_1/', views.I_2_7_1, name='I_2_7_1'),
    path('I_2_7_2/', views.I_2_7_2, name='I_2_7_2'),
    path('I_2_8/', views.I_2_8, name='I_2_8'),
    path('I_2_8_1/', views.I_2_8_1, name='I_2_8_1'),
    path('I_3/', views.I_3, name='I_3'),
    path('I_4/', views.I_4, name='I_4'),
    path('I_5_1/', views.I_5_1, name='I_5_1'),
    path('I_5_2/', views.I_5_2, name='I_5_2'),
    path('Principaux_indicateurs/', views.Principaux_indicateurs,
         name='Principaux_indicateurs'),


    path('create_Personnel/', views.create_Personnel, name='create_Personnel'),
    path('list_Personnel/', views.list_Personnel, name='list_Personnel'),
    path('<id>/update_Personnel/', views.update_Personnel, name='update_Personnel'),
    path('<id>/delete_Personnel/', views.delete_Personnel, name='delete_Personnel'),
    path('create_Absence/', views.create_Absence, name='create_Absence'),
    path('list_Absence/', views.list_Absence, name='list_Absence'),
    path('<id>/update_Absence/', views.update_Absence, name='update_Absence'),
    path('<id>/delete_Absence/', views.delete_Absence, name='delete_Absence'),
    path('create_Conge/', views.create_Conge, name='create_Conge'),
    path('list_Conge/', views.list_Conge, name='list_Conge'),
    path('<id>/update_Conge/', views.update_Conge, name='update_Conge'),
    path('<id>/delete_Conge/', views.delete_Conge, name='delete_Conge'),
    path('<id>/<pk>/pers_abs_detail_view/',
         views.pers_abs_detail_view, name='pers_abs_detail_view'),
    path('<id>/<pk>/pers_cong_detail_view/',
         views.pers_cong_detail_view, name='pers_cong_detail_view'),
    path('<id>/view_pers_cong_abs/',
         views.view_pers_cong_abs, name='view_pers_cong_abs'),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(),
         name="pdf_download"),

     path('list_Paie/', views.list_Paie, name='list_Paie'),
     path('create_Paie/', views.create_Paie, name='create_Paie'),
     path('<id>/update_Paie/', views.update_Paie, name='update_Paie'),
     path('<id>/delete_Paie/', views.delete_Paie, name='delete_Paie'),
     path('<id>/<pk>/pers_paie_detail_view/',
         views.pers_paie_detail_view, name='pers_paie_detail_view'),
     path('<id>/view_pers_paie/',
         views.view_pers_paie, name='view_pers_paie'),
     path('<id>/<year>/<month>/fiche_de_paie/', views.fiche_de_paie, name='fiche_de_paie'),
     path('FDP_download/', views.FDP_download, name='FDP_download'),
     path('ViewFDPPDF/', views.ViewFDPPDF.as_view(), name="ViewFDPPDF"),
     path('DownloadFDPPDF/', views.DownloadFDPPDF.as_view(), name="DownloadFDPPDF"),


     path('prevision/', views.prevision, name="prevision"),
     path('<id>/pers_prom_detail_view/',
         views.pers_prom_detail_view, name='pers_prom_detail_view'),
]
