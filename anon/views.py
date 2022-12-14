from django.shortcuts import render, redirect
import re
from .models import Provider, Campaign, Attribute, Relationship, Value, Owner, Attribute_Edge, Relationship_Edge

def logreg(req):
    if req.method == "POST":
        data = req.POST
        action = data.get("button")

        if action == "login":
            print(req.POST)
            email = req.POST.get("email")
            pwd = req.POST.get("pwd")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if email != "" and pwd != "" and re.fullmatch(regex, email):
                owners = Owner.objects.all()
                providers = Provider.objects.all()

                #check in owners
                for o in owners:
                    if o.email == email and o.pwd == pwd:
                        req.session["owner"] = email;
                        return redirect('/anon/homedataowner')

                #check in providers
                for p in providers:
                    if p.email == email and p.pwd == pwd:
                        req.session["provider"] = email;
                        return redirect('/anon/homedataprovider')

                return render(req, 'anon/logreg.html', {'not_found_flag': True})
                
        if action == "owner":
            req.session["accountType"] = 0
            return redirect('/anon/registration')
        if action == "provider":
            req.session["accountType"] = 1
            return redirect('/anon/registration')

    return render(req, 'anon/logreg.html', {'not_found_flag': False})





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

                p = Provider(email=email, pwd=pwd)
                p.save()

                req.session["provider"] = p

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

    campaigns = Campaign.objects.all()

    return render(req, 'anon/selectcampaign.html', {'campaigns': campaigns})




def campaignData(req):
    
    if req.method == "POST":

        attributes = req.POST.getlist("data")

        chkEmptyFields = False

        for attr in attributes:
            if attr == '':
                chkEmptyFields = True

        if not(chkEmptyFields):
            req.session["attrs"] = attributes
            return redirect('/anon/seclev')

    campaigns = Campaign.objects.all()

    for c in campaigns:
        if c.name == req.session["sel-camp"]:
            selectedCampaign = c
        
    return render(req, 'anon/campaigndata.html', { 'attributes': selectedCampaign.attributes.all() })





def secLev(req):

    if req.method == "POST":

        if req.POST.get("button") == "confirm":

            email = req.session["email-owner"]
            pwd = req.session["pwd-owner"]
            kval = req.POST.get("kval")

            for c in Campaign.objects.all():
                if c.name == req.session["sel-camp"]:
                    selectedCampaign = c

            o = Owner(email=email, pwd=pwd, k=kval, campaign=selectedCampaign)
            o.save()

            attributes = req.session["attrs"]

            values = Value.objects.all()

            campaignAttrs = selectedCampaign.attributes.all()

            for i in range(len(attributes)):
                v = Value(value=attributes[i])

                if not(attributes[i] in values):
                    v.save()
                    print(v)

                a_edge = Attribute_Edge(owner=o, attribute=campaignAttrs[i], value=v)
                a_edge.save()
            
            req.session["owner"] = o.email

            return redirect('/anon/homedataowner')

    return render(req, 'anon/seclev.html')





def homeDataOwner(req):

    owners = Owner.objects.all()

    for owner in owners:
        if owner.email == req.session["owner"]:
            o = owner

    if req.method == "POST":
        req.session["owner"] = o.email
        return redirect('/anon/profile')

    return render(req, 'anon/homedataowner.html', { 'owner': o })




def profile(req):

    owners = Owner.objects.all()

    for owner in owners:
        if owner.email == req.session["owner"]:
            o = owner

    attrEdges = []

    for attrEdge in Attribute_Edge.objects.all():
        if str(attrEdge.owner) == o.email:
            attrEdges.append(attrEdge)

    rels = o.campaign.relationships.all()

    userRelsTmp = []
    inputRelsTmp = []

    for rel in rels:
        rel = []
        inputRel = ""
        for relEdge in Relationship_Edge.objects.all():
            if str(relEdge.owner1) == o.email:
                rel.append(str(relEdge.owner2))
                inputRel += relEdge.owner2.email + "|"
        userRelsTmp.append(rel)
        inputRelsTmp.append(inputRel)

    userRels = zip(rels, userRelsTmp)
    inputRels = zip(rels, inputRelsTmp)

    ##########################################

    
    if req.method == "POST":
        print(req.POST)

        if "rels" in req.POST:
            req.session["currentRel"] = req.POST.get("rels")
            return redirect('/anon/userrelationships')

        if "done" in req.POST:
            attributes = req.POST.getlist("data")

            previousAttrs = []

            for a in attrEdges:
                previousAttrs.append(a.value.value)

            modifications = zip(o.campaign.attributes.all(), previousAttrs, attributes)

            for attr, prev, newVal in modifications:
                if prev != newVal and newVal != '':
                    for attributeEdge in attrEdges:
                        if attributeEdge.attribute == attr:
                            if not(newVal in Value.objects.all()):
                                val = Value(value=newVal)
                                val.save()
                                attr = attributeEdge.attribute
                                attributeEdge.delete()
                                a = Attribute_Edge(owner=o, attribute=attr, value=val)
                                a.save()
                            else:
                                val = Value(value=newVal)
                                attr = attributeEdge.attribute
                                attributeEdge.delete()
                                a = Attribute_Edge(owner=o, attribute=attr, value=val)
                                a.save()
            return redirect('/anon/homedataowner')


    return render(req, 'anon/profile.html', { 'owner': o, 'attrs': attrEdges, 'owners': owners, 'userRelationships': userRels, 'inputRels': inputRels })




def userRelationships(req):

    currentRel = req.session["currentRel"]

    owners = Owner.objects.all()

    for owner in owners:
        if owner.email == req.session["owner"]:
            o = owner

    userRels = []

    inputRels = ""

    for relEdge in Relationship_Edge.objects.all():
        if relEdge.owner1.email == o.email and relEdge.relationship.name == currentRel:
            userRels.append(relEdge.owner2.email)
            inputRels += relEdge.owner2.email + "|"

    if req.method == "POST":
        if inputRels == req.POST.get("selectedUsers"):
            del req.session['currentRel']
            return redirect('/anon/profile')
        else:
            previousUsers = inputRels.split('|')
            selectedUsers = req.POST.get("selectedUsers").split('|')
            for u in selectedUsers:
                if not(u in previousUsers):
                    for rel in Relationship.objects.all():
                        if rel.name == currentRel:
                            r = rel
                    for owner2 in owners:
                        if owner2.email == u:
                            o2 = owner2
                    e = Relationship_Edge(owner1=o, relationship=r, owner2=o2)
                    e.save()
            for u in previousUsers:
                if not(u in selectedUsers):
                    for relEdge in Relationship_Edge.objects.all():
                        if relEdge.owner1.email == o.email and relEdge.relationship.name == currentRel and relEdge.owner2.email == u:
                            relEdge.delete()
            return redirect('/anon/profile')


    return render(req, 'anon/userrelationships.html', { 'owner': o, 'userRels': userRels, 'owners': owners, 'currentRel': currentRel, 'inputRels': inputRels })





def homeDataProvider(req):
    return render(req, 'anon/homedataprovider.html')

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