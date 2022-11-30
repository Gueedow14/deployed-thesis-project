from django.shortcuts import render

def logreg(req):
    return render(req, 'anon/logreg.html')

def registration(req):
    return render(req, 'anon/registration.html')

def selectCampaign(req):
    return render(req, 'anon/selectcampaign.html')

def homeDataProvider(req):
    return render(req, 'anon/homedataprovider.html')

def campaignData(req):
    return render(req, 'anon/campaigndata.html')

def secLev(req):
    return render(req, 'anon/seclev.html')

def homeDataOwner(req):
    return render(req, 'anon/homedataowner.html')

def profile(req):
    return render(req, 'anon/profile.html')

def createCampaign(req):
    return render(req, 'anon/createcampaign.html')

def campaignPage(req):
    return render(req, 'anon/campaignpage.html')

def compareHome(req):
    return render(req, 'anon/comparehome.html')

def compareResults(req):
    return render(req, 'anon/compareresults.html')

def anonymize(req):
    return render(req, 'anon/anonymize.html')

def resetPwd(req):
    return render(req, 'anon/resetpwd.html')