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
    
]
