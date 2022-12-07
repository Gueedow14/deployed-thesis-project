from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
import re

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

        email = req.POST.get("email-input")
        pwd = req.POST.get("pwd-input")
        confirm = req.POST.get("confirm-input")

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if pwd == confirm and re.fullmatch(regex, email):

            if typeAccount == 0:
                req.session["email-owner"] = email
                req.session["pwd-owner"] = pwd
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
                    
        elif pwd == confirm and not(re.fullmatch(regex, email)):
            return render(req, 'anon/registration.html', {'email_flag': True})
        elif pwd != confirm and re.fullmatch(regex, email):
            return render(req, 'anon/registration.html', {'pwd_flag': True})
        else:
            return render(req, 'anon/registration.html', {'both_flag': True})
    
    

    return render(req, 'anon/registration.html')





def selectCampaign(req):
    
    if req.method == "POST":
        campaign = req.POST.get('selected-campaign')
        if campaign != "":
            req.session["sel-camp"] = campaign
            return redirect('/anon/campaigndata')


    return render(req, 'anon/selectcampaign.html')









def homeDataProvider(req):
    return render(req, 'anon/homedataprovider.html')



def campaignData(req):
    
    if req.method == "POST":
        #CHECK THAT ALL DATA ARE FILLED

        attributes = req.POST.getlist("data")

        chkEmptyFields = False

        for attr in attributes:
            if attr == '':
                chkEmptyFields = True

        if not(chkEmptyFields):
            req.session["attrs"] = attributes
            return redirect('/anon/seclev')
        
    return render(req, 'anon/campaigndata.html')





def secLev(req):

    if req.method == "POST":

        if req.POST.get("button") == "confirm":
            req.session["kval"] = req.POST.get("kval")

            #REGISTRATION OF USER IN DB

            return redirect('/anon/homedataowner')

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