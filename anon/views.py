from datetime import datetime
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import numpy as np
import re, os, mimetypes, subprocess, csv, statistics
from .models import Provider, Campaign, Attribute, Relationship, Value, Owner, Attribute_Edge, Relationship_Edge, AnonyGraph

from github import Github

def logreg(req):

    #g = Github("Gueedow14", "!!*ci.ao123CI.AO*??")
    #access_token = "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"
    #g = Github(access_token)

    #for repo in g.get_user().get_repos():
        #print(repo)

    terminal = 'pwd && ls'
    subprocess.call(terminal, shell=True)


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

    if not "email-reset" in req.session or not "originalpage" in req.session:
        return redirect("/anon/error")

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
                user.pwd = pwd
                user.save()
                terminal = 'cd ../personalized-anony-kg && python reset_owner_pwd.py --owner=' + user.email + ' --pwd=' + user.pwd + ' --kval=' + str(user.k) + ' --campaign=\"' + user.campaign.name.lower() + '\"'
                subprocess.call(terminal, shell=True)

            if type == "provider":
                user.pwd = pwd
                user.save()
                terminal = 'cd ../personalized-anony-kg && python reset_provider_pwd.py --provider=' + user.email + ' --pwd=\"' + user.pwd + '\"'
                subprocess.call(terminal, shell=True)

            if origin == "logreg":
                del req.session["originalpage"]
                del req.session["email-reset"]
                return redirect('/anon/logreg')
            
            if origin == "profile":
                del req.session["originalpage"]
                req.session["owner"] = user.email
                del req.session["email-reset"]
                return redirect('/anon/profile')
        else:
            return render(req, 'anon/resetpwd.html', { 'pwd_error_flag': True })


    return render(req, 'anon/resetpwd.html')





def registration(req):

    if not "accountType" in req.session:
        return redirect("/anon/error")

    typeAccount = req.session["accountType"]    

    if req.method == "POST":

        email = req.POST.get("email-input")
        pwd = req.POST.get("pwd-input")
        confirm = req.POST.get("confirm-input")

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if pwd == confirm and re.fullmatch(regex, email):


            if typeAccount == 0:

                for o in Owner.objects.all():
                    if o.email.lower() == email.lower():
                        return render(req, 'anon/registration.html', {'owner_flag': True})

                req.session["email-owner"] = email
                req.session["pwd-owner"] = pwd
                return redirect('/anon/selectcampaign')

            if typeAccount == 1:

                for p in Provider.objects.all():
                    if p.email.lower() == email.lower():
                        return render(req, 'anon/registration.html', {'provider_flag': True})

                email = req.POST.get("email-input")
                pwd = req.POST.get("pwd-input")

                p = Provider(email=email.lower(), pwd=pwd)
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

    if not "email-owner" in req.session or not "pwd-owner" in req.session:
        return redirect("/anon/error")

    campaigns = Campaign.objects.all()

    campaignAttrs = []

    for campaign in campaigns:
        campaign_str = ""
        campaign_attrs = campaign.attributes.all()

        for attr in campaign_attrs:
            campaign_str += (attr.name + " , ")

        if campaign_attrs:
            campaign_str = campaign_str[:-3]
        else:
            campaign_str = None

        campaignAttrs.append(campaign_str)

    campaignRels = []

    for campaign in campaigns:
        campaign_str = ""

        for rel in campaign.relationships.all():
            campaign_str += (rel.name + " , ")

        if campaign.relationships.all():
            campaign_str = campaign_str[:-3]
        else:
            campaign_str = None

        campaignRels.append(campaign_str)

    campaign_data = zip(campaigns, campaignAttrs, campaignRels)
    
    if req.method == "POST":
        campaign = req.POST.get('selected-campaign')
        if campaign != "":
            req.session["sel-camp"] = campaign
            return redirect('/anon/campaigndata')

    campaigns = Campaign.objects.all()

    return render(req, 'anon/selectcampaign.html', {'campaigns': campaign_data})




def campaignData(req):

    if not "email-owner" in req.session or not "sel-camp" in req.session or not "pwd-owner" in req.session:
        return redirect("/anon/error")
    
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

    if not "email-owner" in req.session or not "sel-camp" in req.session or not "pwd-owner" in req.session or not "attrs" in req.session:
        return redirect("/anon/error")

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

                if ' ' in attributes[i]:
                    words = attributes[i].split(' ')
                    modifiedStr = ""
                    for w in words:
                        modifiedStr += w.capitalize() + " "
                    v = Value(value=modifiedStr[:-1])
                else:
                    v = Value(value=attributes[i].capitalize())

                if not(v in values):
                    v.save()
                    terminal = 'cd ../personalized-anony-kg && python -u generate_value.py --val=\"' + attributes[i].lower() + '\"'
                    subprocess.call(terminal, shell=True)

                a_edge = Attribute_Edge(owner=o, attribute=campaignAttrs[i], value=v)
                a_edge.save()
                terminal = 'cd ../personalized-anony-kg && python -u generate_attr_edge.py --owner=' + o.email.lower() + ' --attr=\"' + campaignAttrs[i].name.lower() + '\" --value=\"' + v.value.lower() + '\"'
                subprocess.call(terminal, shell=True)
                
            
            req.session["owner"] = o.email

            return redirect('/anon/homedataowner')

    return render(req, 'anon/seclev.html')





def homeDataOwner(req):

    if not "owner" in req.session:
        return redirect("/anon/error")
    
    owners = Owner.objects.all()

    for owner in owners:
        if owner.email == req.session["owner"]:
            o = owner
    
    if req.method == "POST":
        if "profile" in req.POST:
            req.session["owner"] = o.email
            return redirect('/anon/profile')
        if "logout" in req.POST:
            if "owner" in req.session:
                del req.session["owner"]
            if "attrs" in req.session:
                del req.session["attrs"]
            if "pwd-owner" in req.session:
                del req.session["pwd-owner"]
            if "email-owner" in req.session:
                del req.session["email-owner"]
            if "sel-camp" in req.session:
                del req.session["sel-camp"]
            return redirect('/anon/logreg')

    campaign_anony_graphs = []

    for anony_graph in AnonyGraph.objects.all():
        if anony_graph.campaign == o.campaign:
            campaign_anony_graphs.append(anony_graph)

    if campaign_anony_graphs:

        ails = []
        rrus = []

        for anony_graph in campaign_anony_graphs:
            ails.append(anony_graph.ail)
            rrus.append(anony_graph.rru)

        mean_ail = statistics.mean(ails)
        mean_rru = statistics.mean(rrus)
        k_val = o.k

        low = 0
        mid = 0
        high = 0

        if mean_ail < 0.4:
            high += 1
        elif mean_ail >= 0.8:
            low += 1
        else:
            mid += 1

        if mean_rru < 0.4:
            high += 1
        elif mean_rru >= 0.8:
            low += 1
        else:
            mid += 1

        if k_val < 3:
            low += 1
        elif k_val >= 6:
            high += 1
        else:
            mid += 1

        sec_value = [low, mid, high]

        sec_perc = 0
        
        if sec_value == [3,0,0]:
            sec_perc = 10
        elif sec_value == [2,1,0]: 
            sec_perc = 20
        elif sec_value == [2,0,1]: 
            sec_perc = 30
        elif sec_value == [1,2,0]:
            sec_perc = 40
        elif sec_value == [1,1,1]: 
            sec_perc = 50
        elif sec_value == [0,3,0]: 
            sec_perc = 60
        elif sec_value == [0,2,1]: 
            sec_perc = 70
        elif sec_value == [1,0,2]: 
            sec_perc = 80
        elif sec_value == [0,1,2]: 
            sec_perc = 90
        elif sec_value == [0,0,3]: 
            sec_perc = 100
    
    else:
        sec_perc = 0

        return render(req, 'anon/homedataowner.html', { 'owner': o, 'sec_perc': sec_perc, 'no_anony_graphs_flag': True })
            

    return render(req, 'anon/homedataowner.html', { 'owner': o, 'sec_perc': sec_perc, 'no_anony_graphs_flag': False })




def profile(req):

    if not "owner" in req.session:
        return redirect("/anon/error")

    owners = Owner.objects.all()

    for owner in owners:
        if owner.email == req.session["owner"]:
            o = owner

    attrEdges = []
    allAttributes = []
    
    for attr in Attribute.objects.all():
        allAttributes.append(attr.name)

    allAttributes.sort()

    for attr in allAttributes:
        for attrEdge in Attribute_Edge.objects.all():
            if attrEdge.owner.email == o.email and attrEdge.attribute.name == attr:
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
    
    if req.method == "POST":

        if "rels" in req.POST:
            req.session["currentRel"] = req.POST.get("rels")
            return redirect('/anon/userrelationships')

        if "done" in req.POST:

            modifiedAttrs = []

            for attr in req.POST.getlist("attribute"):
                modifiedAttrs.append(Attribute(name=attr))

            newAttrs = req.POST.getlist("data")

            previousAttrs = []

            for a in attrEdges:
                if a.attribute in modifiedAttrs:
                    previousAttrs.append(a.value.value)

            campAttrs = []

            for attr in allAttributes:
                a = Attribute(name=attr)
                if a in o.campaign.attributes.all() and a in modifiedAttrs:
                    campAttrs.append(a)

            modifications = zip(campAttrs, previousAttrs, newAttrs)

            for attr, prev, newVal in modifications:
                if prev != newVal and newVal != '':
                    for attributeEdge in attrEdges:
                        if attributeEdge.attribute == attr:
                            if ' ' in newVal:
                                words = newVal.split(' ')
                                modifiedStr = ""
                                for w in words:
                                    modifiedStr += w.capitalize() + " "
                                val = Value(value=modifiedStr[:-1])
                            else:
                                val = Value(value=newVal.capitalize())

                            if not(val in Value.objects.all()):
                                val.save()
                                terminal = 'cd ../personalized-anony-kg && python -u generate_value.py --val=\"' + val.value.lower() + '\"'
                                subprocess.call(terminal, shell=True)
                                attr = attributeEdge.attribute
                                attributeEdge.delete()
                                a = Attribute_Edge(owner=o, attribute=attr, value=val)
                                a.save()
                                terminal = 'cd ../personalized-anony-kg && python -u modify_attr_edge.py --owner=' + o.email.lower() + ' --attr=' + attr.name.lower() + ' --value=' + val.value.lower()
                                subprocess.call(terminal, shell=True)
                            else:
                                attr = attributeEdge.attribute
                                attributeEdge.delete()
                                a = Attribute_Edge(owner=o, attribute=attr, value=val)
                                a.save()
                                terminal = 'cd ../personalized-anony-kg && python -u modify_attr_edge.py --owner=' + o.email.lower() + ' --attr=' + attr.name.lower() + ' --value=' + val.value.lower()
                                subprocess.call(terminal, shell=True)

            return redirect('/anon/homedataowner')
        
        if "yes" in req.POST:
            req.session["email-reset"] = o.email
            req.session["originalpage"] = "profile"
            del req.session["owner"]
            return redirect('/anon/resetpwd')

    return render(req, 'anon/profile.html', { 'owner': o, 'attrs': attrEdges, 'owners': owners, 'userRelationships': userRels, 'inputRels': inputRels })




def userRelationships(req):

    if not "currentRel" in req.session:
        return redirect("/anon/error")

    currentRel = req.session["currentRel"]

    owners = Owner.objects.all()

    other_owners = []

    for owner in owners:
        if owner.email == req.session["owner"]:
            o = owner
        else:
            other_owners.append(owner)

    if other_owners:
        no_owners = False
    else:
        no_owners = True

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
                    terminal = 'cd ../personalized-anony-kg && python -u generate_rel_edge.py --o1=' + o.email.lower() + ' --rel=' + r.name.lower() + ' --o2=' + o2.email.lower()
                    subprocess.call(terminal, shell=True)

            for u in previousUsers:
                if not(u in selectedUsers):
                    for relEdge in Relationship_Edge.objects.all():
                        if relEdge.owner1.email == o.email and relEdge.relationship.name == currentRel and relEdge.owner2.email == u:
                            terminal = 'cd ../personalized-anony-kg && python -u delete_rel_edge.py --o1=' + relEdge.owner1.email.lower() + ' --rel=' + relEdge.relationship.name.lower() + ' --o2=' + relEdge.owner2.email.lower()
                            subprocess.call(terminal, shell=True)
                            relEdge.delete()

            return redirect('/anon/profile')


    return render(req, 'anon/userrelationships.html', { 'owner': o, 'userRels': userRels, 'owners': owners, 'currentRel': currentRel, 'inputRels': inputRels, 'no_owners': no_owners })



def homeDataProvider(req):

    if not "provider" in req.session:
        return redirect("/anon/error")

    providers = Provider.objects.all()

    for p in providers:
        if p.email == req.session["provider"]:
            provider = p

    campaigns = []

    for c in Campaign.objects.all():
        if c.name != "":
            campaigns.append(c)

    campaignAttrs = []

    for campaign in campaigns:
        campaign_str = ""
        campaign_attrs = campaign.attributes.all()

        for attr in campaign_attrs:
            campaign_str += (attr.name + " , ")

        if campaign_attrs:
            campaign_str = campaign_str[:-3]
        else:
            campaign_str = None

        campaignAttrs.append(campaign_str)

    campaignRels = []

    for campaign in campaigns:
        campaign_str = ""

        for rel in campaign.relationships.all():
            campaign_str += (rel.name + " , ")

        if campaign.relationships.all():
            campaign_str = campaign_str[:-3]
        else:
            campaign_str = None

        campaignRels.append(campaign_str)


    if req.method == "POST":

        if "campaign" in req.POST:
            req.session["sel-camp-prov"] = req.POST.get("campaign")

            terminal = 'cd ../personalized-anony-kg && python generate_raw_kg.py --data=anonykg_thesis --campaign=\"' + req.POST.get("campaign").lower() + '\"'
            subprocess.call(terminal, shell=True)

            terminal = 'cd ../personalized-anony-kg && python generate_k_values.py --data=anonykg_thesis --campaign=\"' + req.POST.get("campaign").lower() + '\"'
            subprocess.call(terminal, shell=True)

            terminal = 'cd ../personalized-anony-kg && python generate_dist_matrix.py --data=anonykg_thesis --campaign=\"' + req.POST.get("campaign").lower() + '\" --workers=1'
            subprocess.call(terminal, shell=True)

            return redirect('/anon/campaignpage')

        if "logout" in req.POST:
            del req.session["provider"]
            return redirect('/anon/logreg')
        
        if "create" in req.POST:
            return redirect('/anon/createcampaign')

    
    campaign_data = zip(campaigns, campaignAttrs, campaignRels)

    no_campaigns = False

    if not campaigns:
        no_campaigns = True

    return render(req, 'anon/homedataprovider.html', { "provider": provider, "campaigns": campaign_data, 'no_campaigns': no_campaigns })







def createCampaign(req):

    if not "provider" in req.session:
        return redirect("/anon/error")

    for p in Provider.objects.all():
        if p.email == req.session["provider"]:
            provider = p

    if req.method == "POST":

        name = req.POST.get("name")

        if name != "":
            attrsInput = req.POST.getlist("attr")
            relsInput = req.POST.getlist("rel")

            attributes = []
            relationships = []

            for c in Campaign.objects.all():
                if c.name.lower() == name.lower():
                    return render(req, 'anon/createcampaign.html', { 'name_existing_flag': True })
            
            for attr in attrsInput:
                if ' ' in attr:
                    words = attr.split(' ')
                    attr = ""
                    for w in words:
                        attr += w.capitalize() + " "
                    attr = attr[:-1]
                else:
                    attr = attr.capitalize()

                try:
                    a = Attribute.objects.get(pk=attr.capitalize())
                except Attribute.DoesNotExist:
                    a = None
                if a == None:
                    a = Attribute(name=attr)
                    a.save()
                    terminal = 'cd ../personalized-anony-kg && python generate_attribute.py --attr=\"' + a.name.lower() + '\"'
                    subprocess.call(terminal, shell=True)

                attributes.append(a)

            for rel in relsInput:
                if ' ' in rel:
                    words = rel.split(' ')
                    rel = ""
                    for w in words:
                        rel += w.capitalize() + " "
                    rel = rel[:-1]
                else:
                    rel = rel.capitalize()

                try:
                    r = Relationship.objects.get(pk=rel.capitalize())
                except Relationship.DoesNotExist:
                    r = None
                if r == None:
                    r = Relationship(name=rel)
                    r.save()
                    terminal = 'cd ../personalized-anony-kg && python generate_relationship.py --rel=\"' + r.name.lower() + '\"'
                    subprocess.call(terminal, shell=True)

                relationships.append(r)

            campaign_name = ""

            for word in name.split(" "):
                campaign_name += (word.lower().capitalize() + " ")

            c = Campaign(name=campaign_name[:-1], creator=provider)
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

    if not "sel-camp-prov" in req.session:
        return redirect("/anon/error")

    for c in Campaign.objects.all():
        if c.name == req.session["sel-camp-prov"]:
            campaign = c

    campaignOwners = []

    for owner in Owner.objects.all():
        if owner.campaign == campaign:
            campaignOwners.append(owner)

    ownerValues = []    # lenght is Num of Values

    for attrEdge in Attribute_Edge.objects.all():
        if attrEdge.owner in campaignOwners:
            ownerValues.append(attrEdge.value)

    ownerValues = list(set(ownerValues))

    otherEntitiesInvolved = []

    for relEdge in Relationship_Edge.objects.all():
        if relEdge.owner1 in campaignOwners and relEdge.owner2 not in campaignOwners:
            otherEntitiesInvolved.append(relEdge.owner2)

    otherEntitiesInvolved = list(set(otherEntitiesInvolved))

    numEntities = len(otherEntitiesInvolved) + len(campaignOwners)

    numNodes = len(ownerValues) + numEntities
    
    numRelationships = len(campaign.relationships.all())

    numAttributes = len(campaign.attributes.all())

    numRelations = numRelationships + numAttributes

    campaignRelEdges = []

    for relEdge in Relationship_Edge.objects.all():
        if relEdge.owner1 in campaignOwners:
            campaignRelEdges.append(relEdge)

    campaignAttrEdges = []

    for attrEdge in Attribute_Edge.objects.all():
        if attrEdge.owner in campaignOwners:
            campaignAttrEdges.append(attrEdge)

    totalEdges = len(campaignAttrEdges) + len(campaignRelEdges)


    if req.method == "POST":

        if "compare" in req.POST:
            print("compare")
            return redirect('/anon/comparehome')

        if "anonymize" in req.POST:
            
            return redirect('/anon/anonymize')


    return render(req, 'anon/campaignpage.html', { 'campaign': campaign, 'numEntities': numEntities, 'numValues': len(ownerValues), 'numNodes': numNodes, 'numRelations': numRelations, 'numRelationships': numRelationships, 'numAttributes': numAttributes, 'numEdges': totalEdges, 'numAttrEdges': len(campaignAttrEdges), 'numRelEdges': len(campaignRelEdges) })





def compareHome(req):

    if not "sel-camp-prov" in req.session:
        return redirect("/anon/error")

    for c in Campaign.objects.all():
        if c.name == req.session["sel-camp-prov"]:
            campaign = c

    campaign_graphs = []

    for graph in AnonyGraph.objects.all():
        if graph.campaign == campaign:
            campaign_graphs.append(graph)

    last_updates = []

    for graph in campaign_graphs:
        last_updates.append(graph.last_updated.strftime("%d/%m/%Y %H:%M"))

    calgos = []

    for graph in campaign_graphs:
        if graph.calgo == "vac":
            calgos.append(graph.calgo.upper())
        else:
            graph_calgo = graph.calgo.split("#")
            if graph_calgo[0] == "hdbscan":
                calgos.append((graph_calgo[0].upper() + "#" + graph_calgo[1].capitalize()))
            else:
                calgos.append(("k-Medoids#" + graph_calgo[1].capitalize()))

    campaign_graphs_data = zip(campaign_graphs, last_updates, calgos)

    rrus = []

    for graph in campaign_graphs:
        rrus.append(graph.rru)

    ails = []

    for graph in campaign_graphs:
        ails.append(graph.ail)

    maxail = None
    minail = None
    maxrru = None
    minrru = None
    
    if ails != []:
        maxail = np.max(ails)
        minail = np.min(ails)

    if rrus != []:
        maxrru = np.max(rrus)
        minrru = np.min(rrus)


    if req.method == "POST":

        if "campaign-page" in req.POST:
            return redirect('/anon/campaignpage')

        if req.POST.get("selected-graphs") != "":
            req.session["selected-graphs"] = req.POST.get("selected-graphs")
            return redirect('/anon/compareresults')


    return render(req, 'anon/comparehome.html', { 'graphs': campaign_graphs_data, 'campaign': campaign, 'maxail': maxail, "minail": minail, 'maxrru': maxrru, "minrru": minrru })


def compareResults(req):

    if not "selected-graphs" in req.session or not "sel-camp-prov" in req.session:
        return redirect("/anon/error")

    if req.method == "POST":
        del req.session["selected-graphs"]
        del req.session["sel-camp-prov"]
        return redirect("/anon/homedataprovider")

    selected_graphs = req.session["selected-graphs"].split("|")

    calgos = []
    enforcers = []
    rrus = []
    ails = []

    for graph in selected_graphs:
        values = graph.split(";")
        calgos.append(values[0])
        enforcers.append(values[1])
        rrus.append(values[2])
        ails.append(values[3])

    graph_data = zip(calgos, enforcers, rrus, ails)

    names = []

    for graph in selected_graphs:
        values = graph.split(";")
        names.append(values[0] + " - " + values[1])

    return render(req, 'anon/compareresults.html', { 'graphs': graph_data, 'rrus': rrus, 'ails': ails, 'names': names })


def downloadfile(req):

    if not "campaign" in req.session or not "calgo" in req.session or not "calgo_args" in req.session or not "enforcer" in req.session or not "enforcer_args" in req.session:
        return redirect("/anon/error")

    campaign = req.session["campaign"]
    calgo = req.session["calgo"]
    calgo_args = req.session["calgo_args"]
    enforcer = req.session["enforcer"]
    enforcer_args = req.session["enforcer_args"]

    current_dir = os.getcwd()
    base_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    filename = 'anony_' + campaign.replace(" ", "_") + '.txt'

    graph_str = campaign.replace(" ", "_") + "_adm#0.50,0.50_n_" + calgo

    if calgo_args is not None:
        graph_str += ("#" + calgo_args + "_")
    else:
        graph_str += "_"
    
    graph_str += enforcer

    if enforcer_args is not None:
        graph_str += ("#1.00")      #not really the best way

    filepath = os.path.join(base_dir, "personalized-anony-kg", "outputs", "anonykg_thesis_-1", campaign, "graphs", graph_str, filename)

    filename = os.path.basename(filepath)

    if req.method == "POST":

        if "download" in req.POST:
            path = open(filepath, 'r')
            mime_type, _ = mimetypes.guess_type(filepath)
            response = HttpResponse(path, mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename

            return response

        if "redirect" in req.POST:
            del req.session["sel-camp-prov"]

            return redirect('/anon/homedataprovider')

    return render(req, 'anon/download_page.html', {"path": filepath})


def anonymize(req):

    if not "sel-camp-prov" in req.session:
        return redirect("/anon/error")

    campaign = req.session["sel-camp-prov"]

    if req.method == "POST":

        if "home" in req.POST:
            del req.session["sel-camp-prov"]
            return redirect('/anon/homedataprovider')

        clust = req.POST.get("clust-alg")
        clust_arg = None

        if clust[0] != "v":
            clust_arg = clust.split("-")[1]
            clust = clust.split("-")[0]

        valid = req.POST.get("valid-alg")

        if valid == "sr":
            valid_arg = None
        else:
            valid_arg = "1.00"

        download = req.POST.get("save-choice")

        if clust == "vac":
            command_line = 'cd ../personalized-anony-kg && python generate_raw_clusters.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust
        else:
            command_line = 'cd ../personalized-anony-kg && python generate_raw_clusters.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust + ' --calgo_args=' + clust_arg

        terminal = command_line
        subprocess.call(terminal, shell=True)

        print("\n\n\n\n")




        current_dir = os.getcwd()
        base_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        filename = campaign.lower().replace(" ", "_") + "_adm#0.50,0.50_n_" + clust

        if clust_arg is not None:
            filename += ("#" + clust_arg)

        filename += ".txt"

        filepath = os.path.join(base_dir, "personalized-anony-kg", "outputs", "anonykg_thesis_-1", campaign.lower(), "clusters", "raw", filename)



        if not os.path.isfile(filepath):
            print("\n\n\n")
            print("Non esiste file: " + filepath)
            print("\n\n\n")
            return render(req, 'anon/anonymize.html', { "clusterError": True })



        if clust == "vac":
            command_line = 'cd ../personalized-anony-kg && python anonymize_clusters.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust
        else:
            command_line = 'cd ../personalized-anony-kg && python anonymize_clusters.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust + ' --calgo_args=' + clust_arg


        if valid == "sr":
            command_line += ' --enforcer=sr'
        else:
            command_line += ' --enforcer=ms --enforcer_args=1'

        terminal = command_line
        subprocess.call(terminal, shell=True)

        print("\n\n\n\n")

        command_line = 'cd ../personalized-anony-kg && python anonymize_kg.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\"'

        if clust == "vac":
            command_line += ' --calgo=' + clust
        else:
            command_line += ' --calgo=' + clust + ' --calgo_args=' + clust_arg

        if valid == "sr":
            command_line += ' --enforcer=sr'
        else:
            command_line += ' --enforcer=ms --enforcer_args=1'

        terminal = command_line
        subprocess.call(terminal, shell=True)

        print("\n\n\n\n")

        command_line = 'cd ../personalized-anony-kg && python visualize_outputs.py --data_list=anonykg_thesis --campaign=\"{}\" --refresh=y,y --src_type=graphs --exp_names={},{} --workers=1'.format(campaign.lower(), clust, valid)

        if clust == "vac":
            command_line += ' --calgo=' + clust
        else:
            command_line += ' --calgo=' + clust + ' --calgo_args=' + clust_arg

        if valid == "sr":
            command_line += ' --enforcer=sr'
        else:
            command_line += ' --enforcer=ms --enforcer_args=1'

        terminal = command_line
        subprocess.call(terminal, shell=True)

        print("\n\n\n\n")


        current_dir = os.getcwd()
        base_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        filename = campaign.lower().replace(" ", "_") + ".csv"

        filepath = os.path.join(base_dir, "personalized-anony-kg", "exp_data", "tuning_graphs", "anonykg_thesis_-1", filename)

        agg_filename = campaign.lower().replace(" ", "_") + "_agg.csv"

        agg_filepath = os.path.join(base_dir, "personalized-anony-kg", "exp_data", "tuning_graphs", "anonykg_thesis_-1", agg_filename)

        print("Path: " + agg_filepath)

        with open(agg_filepath, 'r') as f:
            csvreader = csv.reader(f)

            enforcer_index = -1
            calgo_index = -1
            ail_index = -1
            removed_entities_index = -1
            raw_entities_index = -1

            for i, row in enumerate(csvreader):
                if i == 0:
                    enforcer_index = row.index("enforcer_str")
                    calgo_index = row.index("calgo_str")
                    ail_index = row.index("radm")
                    removed_entities_index = row.index("removed_entities")
                    raw_entities_index = row.index("num_raw_entities")

                else:
                    enforcer = row[enforcer_index]
                    calgo = row[calgo_index]
                    ail = row[ail_index]
                    rem_ent = row[removed_entities_index]
                    raw_ent = row[raw_entities_index]

                    for c in Campaign.objects.all():
                        if c.name.lower() == campaign.lower():
                            selectedCampaign = c

                    ail_values = ail.split(".")
                    ail_values[1] = ail_values[1][:4]

                    ail = ail_values[0] + "." + ail_values[1]

                    rru = float(rem_ent)/float(raw_ent)

                    graph = AnonyGraph.objects.filter(campaign=selectedCampaign, calgo=calgo, enforcer=enforcer)

                    if not graph:
                        new_graph = AnonyGraph(campaign=selectedCampaign, calgo=calgo, enforcer=enforcer, ail=float(ail), rru=rru)
                        new_graph.save()
                    else:
                        graph[0].ail = float(ail)
                        graph[0].rru = rru
                        graph[0].last_updated = datetime.now()
                        graph[0].save()


        if download == "yes":

            command_line = 'cd ../personalized-anony-kg && python generate_anon_kg_file.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust

            if clust != "vac":
                command_line += ' --calgo_args=' + clust_arg
            
            command_line += ' --enforcer=' + valid

            if valid == "ms":
                command_line += ' --enforcer_args=1'

            terminal = command_line
            subprocess.call(terminal, shell=True)

            campaign = campaign.lower()

            req.session["campaign"] = campaign
            req.session["calgo"] = clust
            req.session["calgo_args"] = clust_arg
            req.session["enforcer"] = valid
            req.session["enforcer_args"] = valid_arg

            return redirect('/anon/download')



        del req.session["sel-camp-prov"]

        return redirect('/anon/homedataprovider')

    return render(req, 'anon/anonymize.html')


def errorpage(req):

    if req.method == "POST":

        for key in list(req.session.keys()):
            del req.session[key]

        return redirect('/anon/logreg')

    return render(req, 'anon/error_page.html')