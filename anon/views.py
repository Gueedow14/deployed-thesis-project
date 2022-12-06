from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

def logreg(req):
    if req.method == "POST":
        data = req.POST
        action = data.get("button")
        if action == "login":
            form = AuthenticationForm(req, data=req.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email-input')
                pwd = form.cleaned_data.get('pwd-input')
                user= authenticate(username=email, password=pwd)
                if user is not None:
                    login(req, user)
                    if user.type == "provider":
                        req.session["utente"] = user
                        return redirect('/anon/homedataprovider')
                    elif user.type == "owner":
                        req.session["utente"] = user
                        return redirect('/anon/homedataowner')
        if action == "owner":
            req.session["accountType"] = 0
            return redirect('/anon/registration')
        if action == "provider":
            req.session["accountType"] = 1
            return redirect('/anon/registration')

    return render(req, 'anon/logreg.html')





def registration(req):
    typeAccount = req.session["accountType"]

    if req.method == "POST":
        data = req.POST
        action = data.get("button")
        if action == "registrate":

            if typeAccount == 0:
                req.session["email"] = req.POST.get("email-input")
                req.session["pwd"] = req.POST.get("pwd-input")
                return redirect('/anon/selectcampaign')

            if typeAccount == 1:
                email = req.POST.get("email-input")
                pwd = req.POST.get("pwd-input")


                #CREATION OF THE PROVIDER IN THE DATABASE


                user = authenticate(username=email, password=pwd)
                if user is not None:
                    login(req, user)
                    req.session["utente"] = user
                    return redirect('/anon/homedataprovider')
    
    

    return render(req, 'anon/registration.html')





def selectCampaign(req):
    
    if req.method == "POST":
        print(req.POST)
        campaign = req.POST.get('selected-campaign')
        if campaign != "":
            req.session["sel-camp"] = campaign
            return redirect('/anon/campaigndata')


    return render(req, 'anon/selectcampaign.html')









def homeDataProvider(req):
    return render(req, 'anon/homedataprovider.html')

def campaignData(req):
    email = req.session["email"]
    pwd = req.session["pwd"]
    campaign = req.session["sel-camp"]

    print("Email: " + email)
    print("Password: " + pwd)
    print("Selected Campaign: " + campaign)





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