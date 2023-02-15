from django.urls import path
from . import views

urlpatterns = [
    path('logreg', views.logreg, name="logreg"),
    path('registration', views.registration, name="registration"),
    path('selectcampaign', views.selectCampaign, name="selectCampaign"),
    path('homedataprovider', views.homeDataProvider, name="homeDataProvider"),
    path('campaigndata', views.campaignData, name="campaignData"),
    path('seclev', views.secLev, name="seclev"),
    path('homedataowner', views.homeDataOwner, name="homedataowner"),
    path('profile', views.profile, name="profile"),
    path('createcampaign', views.createCampaign, name="createcampaign"),
    path('campaignpage', views.campaignPage, name="campaignpage"),
    path('comparehome', views.compareHome, name="comparehome"),
    path('compareresults', views.compareResults, name="compareresults"),
    path('anonymize', views.anonymize, name="anonymize"),
    path('resetpwd', views.resetPwd, name="resetPwd"),
    path('userrelationships', views.userRelationships, name="userRelationships"),
    path('campaignrelationships', views.campaignRelationships, name="campaignRelationships"),
    path('usercampaign', views.userCampaign, name="userCampaign"),
    path('clusteringpage', views.clusteringpage, name="clusteringPage"),
    path('clusteringresults', views.clusteringresults, name="clusteringResults"),

    
    path('download', views.downloadfile),
    path('error', views.errorpage)
    
]
