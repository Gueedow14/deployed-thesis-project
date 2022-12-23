from django.shortcuts import render, redirect
import re
import subprocess
from .models import Provider, Campaign, Attribute, Relationship, Value, Owner, Attribute_Edge, Relationship_Edge

def logreg(req):
    if req.method == "POST":
        data = req.POST
        action = data.get("button")

        if action == "login":
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

                return render(req, 'anon/logreg.html', {'not_found_flag': True, 'not_valid_email_reset': False})
                
        if action == "owner":
            req.session["accountType"] = 0
            return redirect('/anon/registration')

        if action == "provider":
            req.session["accountType"] = 1
            return redirect('/anon/registration')
        
        if "resetpwd" in req.POST:
            email = req.POST.get("email-reset")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            chkDB = False

            for o in Owner.objects.all():
                if o.email == email:
                    chkDB = True
            
            for p in Provider.objects.all():
                if p.email == email:
                    chkDB = True

            if email != "" and re.fullmatch(regex, email) and chkDB:
                print(req.POST)
                req.session["email-reset"] = email
                req.session["originalpage"] = "logreg"
                return redirect('/anon/resetpwd')
            elif email == "" or not(re.fullmatch(regex, email)) or not(chkDB):
                return render(req, 'anon/logreg.html', {'not_found_flag': False, 'not_valid_email_reset': True, 'emailreset': email })

    return render(req, 'anon/logreg.html', {'not_found_flag': False, 'not_valid_email_reset': False})




def resetPwd(req):

    email = req.session["email-reset"]
    origin = req.session["originalpage"]

    if req.method == "POST":
        pwd = req.POST.get("pwd")
        confirm = req.POST.get("confirm")
        if pwd == confirm:

            user = None
            type = None

            for o in Owner.objects.all():
                if o.email == email:
                    user = o
                    type = "owner"
            
            for p in Provider.objects.all():
                if p.email == email:
                    user = p
                    type = "provider"

            if type == "owner":
                o = Owner(email=user.email, pwd=pwd, k=user.k, campaign=user.campaign)
                user.delete()
                o.save()
                terminal = 'cd ../personalized-anony-kg && python reset_owner_pwd.py --owner=' + o.email + ' --pwd=' + o.pwd + ' --kval=' + str(o.k) + ' --campaign=\"' + o.campaign.name.lower() + '\"'
                subprocess.call(terminal, shell=True)

            if type == "provider":
                p = Provider(email=user.email, pwd=pwd)
                user.delete()
                p.save()
                terminal = 'cd ../personalized-anony-kg && python reset_provider_pwd.py --provider=' + p.email + ' --pwd=\"' + p.pwd + '\"'
                subprocess.call(terminal, shell=True)

            if origin == "logreg":
                del req.session["originalpage"]
                del req.session["email-reset"]
                return redirect('/anon/logreg')
            
            if origin == "profile":
                del req.session["originalpage"]
                req.session["owner"] = o.email
                del req.session["email-reset"]
                return redirect('/anon/profile')


    return render(req, 'anon/resetpwd.html')





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

                terminal = 'cd ../personalized-anony-kg && python generate_provider.py --provider=' + email + ' --pwd=' + pwd
                subprocess.call(terminal, shell=True)


                req.session["provider"] = p.email

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

            terminal = 'cd ../personalized-anony-kg && python -u generate_owner.py --owner=' + email + ' --pwd=\"' + pwd + '\" --kval=' + kval + ' --campaign=\"' + selectedCampaign.name.lower() + "\""
            subprocess.call(terminal, shell=True)


            attributes = req.session["attrs"]

            values = Value.objects.all()

            campaignAttrs = selectedCampaign.attributes.all()

            for i in range(len(attributes)):
                v = Value(value=attributes[i])

                if not(attributes[i] in values):
                    v.save()
                    terminal = 'cd ../personalized-anony-kg && python -u generate_value.py --val=\"' + attributes[i].lower() + '\"'
                    pValue = subprocess.call(terminal, shell=True)
                    print("Subprocess di valore " + attributes[i].lower() + ":   " + str(pValue))

                a_edge = Attribute_Edge(owner=o, attribute=campaignAttrs[i], value=v)
                a_edge.save()
                terminal = 'cd ../personalized-anony-kg && python -u generate_attr_edge.py --owner=' + o.email.lower() + ' --attr=' + campaignAttrs[i].name.lower() + ' --value=' + v.value.lower()
                pEdge = subprocess.call(terminal, shell=True)
                print("Subprocess di edge attr " + o.email.lower() + "---[" + campaignAttrs[i].name.lower() + "]-->" + v.value.lower() + ":   " + str(pEdge))

            
            req.session["owner"] = o.email

            return redirect('/anon/homedataowner')

    return render(req, 'anon/seclev.html')





def homeDataOwner(req):

    owners = Owner.objects.all()

    for owner in owners:
        if owner.email == req.session["owner"]:
            o = owner

    if req.method == "POST":
        if "profile" in req.POST:
            req.session["owner"] = o.email
            return redirect('/anon/profile')
        if "logout" in req.POST:
            del req.session["owner"]
            del req.session["attrs"]
            del req.session["pwd-owner"]
            del req.session["email-owner"]
            del req.session["sel-camp"]
            return redirect('/anon/logreg')
            

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
        
        if "yes" in req.POST:
            req.session["email-reset"] = o.email
            req.session["originalpage"] = "profile"
            del req.session["owner"]
            return redirect('/anon/resetpwd')


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

    providers = Provider.objects.all()

    for p in providers:
        if p.email == req.session["provider"]:
            provider = p

    campaigns = Campaign.objects.all()


    if req.method == "POST":

        if "campaign" in req.POST:
            req.session["sel-camp-prov"] = req.POST.get("campaign")
            return redirect('/anon/campaignpage')

        if "logout" in req.POST:
            del req.session["provider"]
            return redirect('/anon/logreg')
        
        if "create" in req.POST:
            return redirect('/anon/createcampaign')



    return render(req, 'anon/homedataprovider.html', { "provider": provider, "campaigns": campaigns })







def createCampaign(req):

    for p in Provider.objects.all():
        if p.email == req.session["provider"]:
            provider = p

    if req.method == "POST":

        name = req.POST.get("name")
        attrsInput = req.POST.getlist("attr")
        relsInput = req.POST.getlist("rel")

        attributes = []
        relationships = []

        for c in Campaign.objects.all():
            if c.name.lower() == name.lower():
                return render(req, 'anon/createcampaign.html', { 'name_existing_flag': True })
        
        for attr in attrsInput:
            try:
                a = Attribute.objects.get(pk=attr.capitalize())
            except Attribute.DoesNotExist:
                a = None
            if a == None:
                a = Attribute(name=attr.capitalize())
                a.save()
                terminal = 'cd ../personalized-anony-kg && python generate_attribute.py --attr=\"' + a.name.lower() + '\"'
                subprocess.call(terminal, shell=True)

            attributes.append(a)

        for rel in relsInput:
            try:
                r = Relationship.objects.get(pk=rel.capitalize())
            except Relationship.DoesNotExist:
                r = None
            if r == None:
                r = Relationship(name=rel.capitalize())
                r.save()
                terminal = 'cd ../personalized-anony-kg && python generate_relationship.py --rel=\"' + r.name.lower() + '\"'
                subprocess.call(terminal, shell=True)

            relationships.append(r)

        c = Campaign(name=name, creator=provider)
        c.save()

        scriptAttrs = ""
        scriptRels = ""

        for a in attributes:
            c.attributes.add(a)
            scriptAttrs += (a.name.lower() + "|")

        for r in relationships:
            c.relationships.add(r)
            scriptRels += (r.name.lower() + "|")

        scriptAttrs = scriptAttrs[:-1]
        scriptRels = scriptRels[:-1]


        terminal = 'cd ../personalized-anony-kg && python generate_campaign.py --name=\"' + c.name.lower() + '\" --creator=\"' + c.creator.email + '\" --attrs=\"' + scriptAttrs + '\" --rels=\"' + scriptRels + '\"'
        subprocess.call(terminal, shell=True)


        return redirect('/anon/homedataprovider')
        

    return render(req, 'anon/createcampaign.html', { 'name_existing_flag': False })





def campaignPage(req):

    for c in Campaign.objects.all():
        if c.name == req.session["sel-camp-prov"]:
            campaign = c

    if req.method == "POST":

        if "compare" in req.POST:
            print("compare")
            return redirect('/anon/comparehome')

        if "anonymize" in req.POST:
            print("anonymize")
            return redirect('/anon/anonymize')


    return render(req, 'anon/campaignpage.html', { 'campaign': campaign })





def compareHome(req):
    return render(req, 'anon/comparehome.html')

def compareResults(req):
    return render(req, 'anon/compareresults.html')

def anonymize(req):
    return render(req, 'anon/anonymize.html')