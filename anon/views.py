from datetime import datetime
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import numpy as np
import re, os, mimetypes, subprocess, csv, statistics
from .models import Provider, Campaign, Attribute, Relationship, Value, Owner, Attribute_Edge, Relationship_Edge, AnonyGraph, OwnerCampaign

# cd anony-kg-modified/


def logreg(req):

    if req.method == "POST":
        data = req.POST
        action = data.get("button")

        if action == "login":
            email = req.POST.get("email").lower()
            pwd = req.POST.get("pwd")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if email != "" and pwd != "" and re.fullmatch(regex, email):

                #check in owners
                for o in Owner.objects.all():
                    if o.email == email and o.pwd == pwd:
                        req.session["owner"] = email.lower();
                        return redirect('/anon/homedataowner')

                #check in providers
                for p in Provider.objects.all():
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
                for o in Owner.objects.all():
                    if o.email == email and o.pwd != pwd:
                        user.pwd = pwd
                        user.save()
                terminal = 'cd anony-kg-modified/ && python reset_owner_pwd.py --owner=' + user.email + ' --pwd=\"' + user.pwd + '\"'
                subprocess.call(terminal, shell=True)

            if type == "provider":
                for p in Provider.objects.all():
                    if p.email == email and p.pwd != pwd:                        
                        user.pwd = pwd
                        user.save()
                terminal = 'cd anony-kg-modified/ && python reset_provider_pwd.py --provider=' + user.email + ' --pwd=\"' + user.pwd + '\"'
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
                        return render(req, 'anon/registration.html', {'owner_flag': True, 'type': typeAccount})
                    
                o = Owner(email=email.lower(), pwd=pwd)
                o.save()

                terminal = 'cd anony-kg-modified/ && python -u generate_owner.py --owner=' + email.lower() + ' --pwd=\"' + pwd + '\"'
                subprocess.call(terminal, shell=True)

                req.session["owner"] = email.lower()
                req.session["origin"] = "registration"
                return redirect('/anon/selectcampaign')

            if typeAccount == 1:

                for p in Provider.objects.all():
                    if p.email.lower() == email.lower():
                        return render(req, 'anon/registration.html', {'provider_flag': True, 'type': typeAccount})

                p = Provider(email=email.lower(), pwd=pwd)
                p.save()

                terminal = 'cd anony-kg-modified/ && python generate_provider.py --provider=' + email.lower() + ' --pwd=\"' + pwd + '\"'
                subprocess.call(terminal, shell=True)


                req.session["provider"] = p.email

                return redirect('/anon/homedataprovider')
                    

        elif pwd == confirm and not(re.fullmatch(regex, email)):
            return render(req, 'anon/registration.html', {'email_flag': True, 'type': typeAccount})
        elif pwd != confirm and re.fullmatch(regex, email):
            return render(req, 'anon/registration.html', {'pwd_flag': True, 'type': typeAccount})
        else:
            return render(req, 'anon/registration.html', {'both_flag': True, 'type': typeAccount})
    
    

    return render(req, 'anon/registration.html', {'type': typeAccount})





def selectCampaign(req):

    if not "origin" in req.session or not "owner" in req.session:
        return redirect("/anon/error")

    if req.session["origin"] == "registration" or req.session["origin"] == "homepage":

        for o in Owner.objects.all():
            if o.email == req.session["owner"]:
                owner = o

        campaigns = [] 
        owner_campaigns = []

        for oc in OwnerCampaign.objects.all():
            chkOC = False
            if oc.owner == owner:
                chkOC = True
            if chkOC == True:
                owner_campaigns.append(oc.campaign)


        for c in Campaign.objects.all():
            if not c in owner_campaigns:
                campaigns.append(c)

        campaigns = set(campaigns)
          
        chkAllCampaignsAttended = False
        if not campaigns:
            chkAllCampaignsAttended = True

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
            if "no-campaigns-button" in req.POST:
                req.session["owner"] = owner.email
                return redirect('/anon/homedataowner')
            else:
                campaign = req.POST.get('selected-campaign')
                if campaign != "":

                    for c in Campaign.objects.all():
                        if c.name == campaign:
                            selectedCampaign = c

                    oc = OwnerCampaign(owner=owner, k= None, campaign= selectedCampaign)
                    oc.save()

                    req.session["sel-camp"] = campaign
                    return redirect('/anon/campaigndata')

        return render(req, 'anon/selectcampaign.html', {'campaigns': campaign_data, 'chkCampaignsAttended': chkAllCampaignsAttended})

    else:
        return redirect("/anon/error")




def campaignData(req):

    if not "origin" in req.session or not "owner" in req.session or not "sel-camp" in req.session:
        return redirect("/anon/error")

    if req.session["origin"] == "registration" or req.session["origin"] == "homepage":

        for c in Campaign.objects.all():
            if c.name == req.session["sel-camp"]:
                selectedCampaign = c
        
        if req.method == "POST":

            for owner in Owner.objects.all():
                if owner.email == req.session["owner"]:
                    o = owner

            attributes = req.POST.getlist("data")

            chkEmptyFields = False

            for attr in attributes:
                if attr == '':
                    chkEmptyFields = True

            if not(chkEmptyFields):

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
                        terminal = 'cd anony-kg-modified/ && python -u generate_value.py --val=\"' + attributes[i].lower() + '\"'
                        subprocess.call(terminal, shell=True)

                    a_edge = Attribute_Edge(owner=o, attribute=campaignAttrs[i], value=v, campaign=selectedCampaign)
                    a_edge.save()
                    terminal = 'cd anony-kg-modified/ && python -u generate_attr_edge.py --owner=' + o.email.lower() + ' --attr=\"' + campaignAttrs[i].name.lower() + '\" --value=\"' + v.value.lower() + '\"' + ' --campaign=\"' + selectedCampaign.name.lower() + '\"'
                    subprocess.call(terminal, shell=True)
                    
                if not selectedCampaign.relationships.exists():
                    return redirect('/anon/seclev')
                else:
                    return redirect('/anon/campaignrelationships')
            
        return render(req, 'anon/campaigndata.html', { 'attributes': selectedCampaign.attributes.all() })



def campaignRelationships(req):

    for c in Campaign.objects.all():
        if c.name == req.session["sel-camp"]:
            selectedCampaign = c

    no_owners = True

    for o in Owner.objects.all():
        if o.email == req.session["owner"]:
            owner = o
        else:
            no_owners = False

    owners_rels = []
    previous_rels = ""

    for rel in selectedCampaign.relationships.all():
        tmp = []
        for owner_rel in Relationship_Edge.objects.all():
            if owner_rel.owner1 == owner and owner_rel.relationship == rel:
                tmp.append(owner_rel.owner2.email)
                previous_rels += owner_rel.owner2.email + ","
        if previous_rels[:-1] == ',':
            previous_rels = previous_rels[:-1]
        previous_rels += "|"
        owners_rels.append(tmp)
    previous_rels = previous_rels[:-1]

    previous_owner_relationships = zip(selectedCampaign.relationships.all(), owners_rels)

    if req.method == "POST":

        if "owners-present-button" in req.POST:
            if previous_rels == req.POST.get("selectedUsers"):
                return redirect('/anon/seclev')
            else:
                campaignRels = req.POST.get("campaignRels").split('|')

                old_relationships = previous_rels.split('|')
                new_relationships = req.POST.get("selectedUsers").split('|')

                relationships = zip(old_relationships, new_relationships, campaignRels)


                for old_relationship, new_relationship, relationship in relationships:
                    old_users = old_relationship.split(",")
                    new_users = new_relationship.split(",")

                    for new_user in new_users:
                        if not new_user in old_users:
                            for rel in Relationship.objects.all():
                                if rel.name == relationship:
                                    r = rel
                            for owner2 in Owner.objects.all():
                                if owner2.email == new_user:
                                    o2 = owner2

                            e = Relationship_Edge(owner1=o, relationship=r, owner2=o2, campaign=selectedCampaign)
                            e.save()

                            terminal = 'cd anony-kg-modified/ && python -u generate_rel_edge.py --o1=' + o.email.lower() + ' --rel=\"' + r.name.lower() + '\" --o2=' + o2.email.lower() + ' --campaign=\"' + selectedCampaign.name.lower() + '\"'
                            subprocess.call(terminal, shell=True)

                    for old_user in old_users:
                        if not old_user in new_users:
                            for relEdge in Relationship_Edge.objects.all():
                                if relEdge.owner1.email == o.email and relEdge.relationship.name == relationship and relEdge.owner2.email == old_user and relEdge.campaign == selectedCampaign:
                                    
                                    terminal = 'cd anony-kg-modified/ && python -u delete_rel_edge.py --o1=' + relEdge.owner1.email.lower() + ' --rel=' + relEdge.relationship.name.lower() + ' --o2=' + relEdge.owner2.email.lower()
                                    subprocess.call(terminal, shell=True)

                                    relEdge.delete()

        return redirect('/anon/seclev')

    return render(req, 'anon/campaignrelationships.html', {'prev_rels': previous_owner_relationships, 'no_owners': no_owners, 'owners': Owner.objects.all(), 'owner': owner, 'previous_rels_str': previous_rels})






def secLev(req):

    if not "owner" in req.session or not "sel-camp" in req.session:
        return redirect("/anon/error")

    if req.method == "POST":

        if req.POST.get("button") == "confirm":

            kval = req.POST.get("kval")

            for o in Owner.objects.all():
                if o.email == req.session["owner"]:
                    owner = o             

            for c in Campaign.objects.all():
                if c.name == req.session["sel-camp"]:
                    selectedCampaign = c

            for ownerCamp in OwnerCampaign.objects.all():
                if ownerCamp.owner == owner and ownerCamp.campaign == selectedCampaign:
                    oc = ownerCamp

            oc.k = kval
            oc.save()

            terminal = 'cd anony-kg-modified/ && python -u generate_campaign_owner.py --owner=' + owner.email.lower() + ' --kval=\"' + kval + '\" --campaign=\"' + selectedCampaign.name.lower() + '\"'
            subprocess.call(terminal, shell=True)

            req.session["owner"] = owner.email

            if "origin" in req.session:
                return redirect('/anon/usercampaign')
            else:
                del req.session["sel-camp"]
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
        if "campaigns" in req.POST:
            req.session["origin"] = "homepage"
            req.session["owner"] = o.email
            return redirect('/anon/selectcampaign')
        if "logout" in req.POST:
            if "owner" in req.session:
                del req.session["owner"]
            if "attrs" in req.session:
                del req.session["attrs"]
            if "pwd-owner" in req.session:
                del req.session["pwd-owner"]
            if "sel-camp" in req.session:
                del req.session["sel-camp"]
            return redirect('/anon/logreg')
        
    owner_campaigns = []
    campaign_anony_graphs = []

    for oc in OwnerCampaign.objects.all():
        if oc.owner == o:
            owner_campaigns.append(oc.campaign)

    for anony_graph in AnonyGraph.objects.all():
        if anony_graph.campaign in owner_campaigns:
            campaign_anony_graphs.append(anony_graph)

    if campaign_anony_graphs:

        sec_percentages = []

        for campaign in owner_campaigns:

            oc = OwnerCampaign.objects.get(campaign=campaign, owner=o)

            if oc.k:

                ails = []
                rrus = []

                for anony_graph in campaign_anony_graphs:
                    if anony_graph.campaign == campaign:
                        ails.append(anony_graph.ail)
                        rrus.append(anony_graph.rru)

                if ails:

                    mean_ail = statistics.mean(ails)
                    mean_rru = statistics.mean(rrus)
                    k_val = oc.k

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

                    sec_percentages.append(sec_perc)

        if sec_percentages:
            sec_perc = statistics.mean(sec_percentages)
        else:
            sec_perc = 0
    
    else:
        sec_perc = 0

        return render(req, 'anon/homedataowner.html', { 'owner': o, 'sec_perc': sec_perc, 'no_anony_graphs_flag': True, 'missing_kval': False, 'missing_campaign': False })

    chk_no_oc = True
    
    for oc in OwnerCampaign.objects.all():
        if oc.owner == o:
            chk_no_oc = False
            if oc.k == None:
                return render(req, 'anon/homedataowner.html', { 'owner': o, 'sec_perc': sec_perc, 'no_anony_graphs_flag': False, 'missing_kval': True, 'missing_campaign': False })

    if chk_no_oc:
        return render(req, 'anon/homedataowner.html', { 'owner': o, 'sec_perc': sec_perc, 'no_anony_graphs_flag': False, 'missing_kval': False, 'missing_campaign': True })


    return render(req, 'anon/homedataowner.html', { 'owner': o, 'sec_perc': sec_perc, 'no_anony_graphs_flag': False, 'missing_kval': False, 'missing_campaign': False })




def profile(req):

    if not "owner" in req.session:
        return redirect("/anon/error")

    for owner in Owner.objects.all():
        if owner.email == req.session["owner"]:
            o = owner

    owner_campaigns = []
    owner_kvals = []

    for oc in OwnerCampaign.objects.all():
        if oc.owner == o:
            owner_campaigns.append(oc.campaign)
            owner_kvals.append(oc.k)

    owner_data = zip(owner_campaigns, owner_kvals)
    
    if req.method == "POST":

        if "done" in req.POST:
            return redirect('/anon/homedataowner')

        if "campaign" in req.POST:
            req.session["sel-camp"] = req.POST.get("campaign")
            return redirect('/anon/usercampaign')
        
        if "yes" in req.POST:
            req.session["email-reset"] = o.email
            req.session["originalpage"] = "profile"
            del req.session["owner"]
            return redirect('/anon/resetpwd')

    return render(req, 'anon/profile.html', { 'owner': o, 'owner_campaigns': owner_data })




def userCampaign(req):

    if not "owner" in req.session or not "sel-camp" in req.session:
        return redirect("/anon/error")

    for owner in Owner.objects.all():
        if owner.email == req.session["owner"]:
            o = owner

    for campaign in Campaign.objects.all():
        if campaign.name == req.session["sel-camp"]:
            c = campaign

    for oc in OwnerCampaign.objects.all():
        if oc.owner == o and oc.campaign == c:
            selectedOC = oc

    attrNames = []
    attrValues = []

    allAttributes = []

    attrEdges = []

    for attr in Attribute.objects.all():
        allAttributes.append(attr.name)

    allAttributes.sort()

    for attr in allAttributes:
        for attrEdge in Attribute_Edge.objects.all():
            if attrEdge.owner.email == o.email and attrEdge.attribute.name == attr and attrEdge.campaign == c:
                attrEdges.append(attrEdge)

    for attr in c.attributes.all().order_by("name"):
        attrNames.append(attr.name)
        try:
            value = Attribute_Edge.objects.get(owner=o, attribute=attr, campaign=c)
        except Attribute_Edge.DoesNotExist:
            value = None
        attrValues.append(value)


    attrData = zip(attrNames, attrValues)

    rels = selectedOC.campaign.relationships.all()

    if req.method == "POST":

        if "kval" in req.POST:
            return redirect('/anon/seclev')

        if "rels" in req.POST:
            req.session["currentRel"] = req.POST.get("rels")
            return redirect('/anon/userrelationships')

        if "done" in req.POST:

            modifiedAttrs = []

            for attr in req.POST.getlist("attribute"):
                modifiedAttrs.append(Attribute(name=attr))

            newAttrs = req.POST.getlist("data")

            previousAttrs = []

            if attrEdges:
                for a in attrEdges:
                    if a.attribute in modifiedAttrs:
                        previousAttrs.append(a.value.value)
            else:
                for a in c.attributes.all().order_by("name"):
                    previousAttrs.append(None)

            campAttrs = []

            for attr in allAttributes:
                a = Attribute(name=attr)
                if a in selectedOC.campaign.attributes.all() and a in modifiedAttrs:
                    campAttrs.append(a)

            modifications = zip(campAttrs, previousAttrs, newAttrs)

            for attr, prev, newVal in modifications:
                if prev != newVal and newVal != '':

                    if attrEdges:

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

                                    chkExists = False
                                    for value in Value.objects.all():
                                        if value.value == val.value:
                                            chkExists = True
                                    if chkExists == False:
                                        val.save()

                                    terminal = 'cd anony-kg-modified/ && python -u generate_value.py --val=\"' + val.value.lower() + '\"'
                                    subprocess.call(terminal, shell=True)
                                    attr = attributeEdge.attribute
                                    attributeEdge.delete()
                                    a = Attribute_Edge(owner=o, attribute=attr, value=val, campaign= selectedOC.campaign)

                                    chkExists = False
                                    for attr_edge in Attribute_Edge.objects.all():
                                        if attr_edge.owner == a.owner and attr_edge.attribute == a.attribute and attr_edge.value == a.value:
                                            chkExists = True
                                    if chkExists == False:
                                        a.save()

                                    terminal = 'cd anony-kg-modified/ && python -u modify_attr_edge.py --owner=' + o.email.lower() + ' --attr=\"' + attr.name.lower() + '\" --value=\"' + val.value.lower() + '\" --campaign=\"' + selectedOC.campaign.name.lower() + '\"'
                                    subprocess.call(terminal, shell=True)
                                else:
                                    attr = attributeEdge.attribute
                                    attributeEdge.delete()
                                    a = Attribute_Edge(owner=o, attribute=attr, value=val, campaign= selectedOC.campaign)

                                    chkExists = False
                                    for attr_edge in Attribute_Edge.objects.all():
                                        if attr_edge.owner == a.owner and attr_edge.attribute == a.attribute and attr_edge.value == a.value:
                                            chkExists = True
                                    if chkExists == False:
                                        a.save()
                                        
                                    terminal = 'cd anony-kg-modified/ && python -u modify_attr_edge.py --owner=' + o.email.lower() + ' --attr=\"' + attr.name.lower() + '\" --value=\"' + val.value.lower() + '\" --campaign=\"' + selectedOC.campaign.name.lower() + '\"'
                                    subprocess.call(terminal, shell=True)
                    
                    else:
                            
                        if ' ' in newVal:
                            words = newVal.split(' ')
                            modifiedStr = ""
                            for w in words:
                                modifiedStr += w.capitalize() + " "
                            val = Value(value=modifiedStr[:-1])
                        else:
                            val = Value(value=newVal.capitalize())

                        if not(val in Value.objects.all()):

                            chkExists = False
                            for value in Value.objects.all():
                                if value.value == val.value:
                                    chkExists = True
                            if chkExists == False:
                                val.save()

                            terminal = 'cd anony-kg-modified/ && python -u generate_value.py --val=\"' + val.value.lower() + '\"'
                            subprocess.call(terminal, shell=True)
                            
                            a = Attribute_Edge(owner=o, attribute=attr, value=val, campaign= selectedOC.campaign)

                            chkExists = False
                            for attr_edge in Attribute_Edge.objects.all():
                                if attr_edge.owner == a.owner and attr_edge.attribute == a.attribute and attr_edge.value == a.value:
                                    chkExists = True
                            if chkExists == False:
                                a.save()

                            terminal = 'cd anony-kg-modified/ && python -u generate_attr_edge.py --owner=' + o.email.lower() + ' --attr=\"' + attr.name.lower() + '\" --value=\"' + val.value.lower() + '\" --campaign=\"' + selectedOC.campaign.name.lower() + '\"'
                            subprocess.call(terminal, shell=True)
                        else:
                            a = Attribute_Edge(owner=o, attribute=attr, value=val, campaign= selectedOC.campaign)

                            chkExists = False
                            for attr_edge in Attribute_Edge.objects.all():
                                if attr_edge.owner == a.owner and attr_edge.attribute == a.attribute and attr_edge.value == a.value:
                                    chkExists = True
                            if chkExists == False:
                                a.save()
                                
                            terminal = 'cd anony-kg-modified/ && python -u generate_attr_edge.py --owner=' + o.email.lower() + ' --attr=\"' + attr.name.lower() + '\" --value=\"' + val.value.lower() + '\" --campaign=\"' + selectedOC.campaign.name.lower() + '\"'
                            subprocess.call(terminal, shell=True)


            del req.session["sel-camp"]
            return redirect('/anon/profile')


    return render(req, 'anon/usercampaign.html', { 'oc': selectedOC, 'campaign': c, 'attrs_campaign': c.attributes.all().order_by("name"),'attrs_data': attrData, 'rels': rels })




def userRelationships(req):

    if not "currentRel" in req.session:
        return redirect("/anon/error")
    
    for campaign in Campaign.objects.all():
        if campaign.name == req.session["sel-camp"]:
            c = campaign

    currentRel = req.session["currentRel"]

    other_owners = []

    for owner in Owner.objects.all():
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
            return redirect('/anon/usercampaign')
        else:
            previousUsers = inputRels.split('|')
            selectedUsers = req.POST.get("selectedUsers").split('|')
            for u in selectedUsers:
                if not(u in previousUsers):
                    for rel in Relationship.objects.all():
                        if rel.name == currentRel:
                            r = rel
                    for owner2 in Owner.objects.all():
                        if owner2.email == u:
                            o2 = owner2
                    e = Relationship_Edge(owner1=o, relationship=r, owner2=o2, campaign= c)
                    e.save()
                    terminal = 'cd anony-kg-modified/ && python -u generate_rel_edge.py --o1=' + o.email.lower() + ' --rel=' + r.name.lower() + ' --o2=' + o2.email.lower() + ' --campaign=\"' + c.name.lower() + '\"'
                    subprocess.call(terminal, shell=True)

            for u in previousUsers:
                if not(u in selectedUsers):
                    for relEdge in Relationship_Edge.objects.all():
                        if relEdge.owner1.email == o.email and relEdge.relationship.name == currentRel and relEdge.owner2.email == u:
                            terminal = 'cd anony-kg-modified/ && python -u delete_rel_edge.py --o1=' + relEdge.owner1.email.lower() + ' --rel=' + relEdge.relationship.name.lower() + ' --o2=' + relEdge.owner2.email.lower() + ' --campaign=\"' + c.name.lower() + '\"'
                            subprocess.call(terminal, shell=True)
                            relEdge.delete()

            return redirect('/anon/usercampaign')


    return render(req, 'anon/userrelationships.html', { 'owner': o, 'userRels': userRels, 'owners': other_owners, 'currentRel': currentRel, 'inputRels': inputRels, 'no_owners': no_owners })



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

            terminal = 'cd anony-kg-modified/ && python generate_raw_kg.py --data=anonykg_thesis --campaign=\"' + req.POST.get("campaign").lower() + '\"'
            subprocess.call(terminal, shell=True)

            terminal = 'cd anony-kg-modified/ && python generate_k_values.py --data=anonykg_thesis --campaign=\"' + req.POST.get("campaign").lower() + '\"'
            subprocess.call(terminal, shell=True)

            terminal = 'cd anony-kg-modified/ && python generate_dist_matrix.py --data=anonykg_thesis --campaign=\"' + req.POST.get("campaign").lower() + '\" --workers=1'
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
            
            if len(attrsInput) > 5:
                return render(req, 'anon/createcampaign.html', { 'name_existing_flag': False })
            
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
                    chkExists = False
                    for attribute in Attribute.objects.all():
                        if attribute.name == a.name:
                            chkExists = True
                    if chkExists == False:
                        a.save()
                    terminal = 'cd anony-kg-modified/ && python generate_attribute.py --attr=\"' + a.name.lower() + '\"'
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
                    chkExists = False
                    for relationship in Relationship.objects.all():
                        if relationship.name == a.name:
                            chkExists = True
                    if chkExists == False:
                        r.save()
                    terminal = 'cd anony-kg-modified/ && python generate_relationship.py --rel=\"' + r.name.lower() + '\"'
                    subprocess.call(terminal, shell=True)

                relationships.append(r)

            campaign_name = ""

            for word in name.split(" "):
                campaign_name += (word.lower().capitalize() + " ")

            c = Campaign(name=campaign_name[:-1], creator=provider)

            chkExists = False

            for campaign in Campaign.objects.all():
                if campaign == c:
                    chkExists = True
            if chkExists == False:
                c.save()

            scriptAttrs = ""
            scriptRels = ""

            for a in attributes:
                a.save()
                c.attributes.add(a)
                scriptAttrs += (a.name.lower() + "|")

            for r in relationships:
                r.save()
                c.relationships.add(r)
                scriptRels += (r.name.lower() + "|")

            scriptAttrs = scriptAttrs[:-1]
            scriptRels = scriptRels[:-1]


            terminal = 'cd anony-kg-modified/ && python generate_campaign.py --name=\"' + c.name.lower() + '\" --creator=\"' + c.creator.email + '\" --attrs=\"' + scriptAttrs + '\" --rels=\"' + scriptRels + '\"'
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

    for oc in OwnerCampaign.objects.all():
        if oc.campaign == campaign:
            campaignOwners.append(oc.owner)

    ownerValues = []    # lenght is Num of Values

    for attrEdge in Attribute_Edge.objects.all():
        if attrEdge.owner in campaignOwners and attrEdge.campaign == campaign:
            ownerValues.append(attrEdge.value)

    ownerValues = list(set(ownerValues))

    otherEntitiesInvolved = []

    for relEdge in Relationship_Edge.objects.all():
        if relEdge.owner1 in campaignOwners and relEdge.owner2 not in campaignOwners and relEdge.campaign == campaign:
            otherEntitiesInvolved.append(relEdge.owner2)

    otherEntitiesInvolved = list(set(otherEntitiesInvolved))

    numEntities = len(otherEntitiesInvolved) + len(campaignOwners)

    numNodes = len(ownerValues) + numEntities
    
    numRelationships = len(campaign.relationships.all())

    numAttributes = len(campaign.attributes.all())

    numRelations = numRelationships + numAttributes

    campaignRelEdges = []

    for relEdge in Relationship_Edge.objects.all():
        if relEdge.campaign == campaign:
            campaignRelEdges.append(relEdge)

    campaignAttrEdges = []

    for attrEdge in Attribute_Edge.objects.all():
        if attrEdge.campaign == campaign:
            campaignAttrEdges.append(attrEdge)

    totalEdges = len(campaignAttrEdges) + len(campaignRelEdges)


    if req.method == "POST":

        if "home" in req.POST:
            del req.session["sel-camp-prov"]
            return redirect('/anon/homedataprovider')

        if "compare" in req.POST:
            return redirect('/anon/comparehome')

        if "anonymize" in req.POST:
            return redirect('/anon/clusteringpage')


    return render(req, 'anon/campaignpage.html', { 'campaign': campaign, 'numEntities': numEntities, 'numValues': len(ownerValues), 'numNodes': numNodes, 'numRelations': numRelations, 'numRelationships': numRelationships, 'numAttributes': numAttributes, 'numEdges': totalEdges, 'numAttrEdges': len(campaignAttrEdges), 'numRelEdges': len(campaignRelEdges), 'allOwners': campaignOwners + otherEntitiesInvolved, 'allValues': ownerValues, 'attrEdges': campaignAttrEdges, 'relEdges': campaignRelEdges })





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

    #base_dir = "/app"
    base_dir = "/home/guido/Documenti/Thesis Project - Test/kg-anonymization"
    filename = 'anony_' + campaign.replace(" ", "_") + '.ttl'

    graph_str = campaign.replace(" ", "_") + "_adm#0.50,0.50_n_" + calgo

    if calgo_args is not None:
        graph_str += ("#" + calgo_args + "_")
    else:
        graph_str += "_"
    
    graph_str += enforcer

    if enforcer_args is not None:
        graph_str += ("#1.00")      #not really the best way

    filepath = os.path.join(base_dir, "anony-kg-modified", "outputs", "anonykg_thesis_-1", campaign, "graphs", graph_str, filename)

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


def clusteringpage(req):

    if not "sel-camp-prov" in req.session:
        return redirect("/anon/error")

    campaign = req.session["sel-camp-prov"]

    if req.method == "POST":

        clust = req.POST.get("clust-alg")
        clust_arg = None

        print(clust)

        if clust[0] != "v":
            clust_arg = clust.split("-")[1]
            clust = clust.split("-")[0]

        if clust == "vac":
            command_line = 'cd anony-kg-modified/ && python generate_raw_clusters.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust
        else:
            command_line = 'cd anony-kg-modified/ && python generate_raw_clusters.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust + ' --calgo_args=' + clust_arg

        terminal = command_line
        subprocess.call(terminal, shell=True)

        req.session["clust"] = clust
        req.session["clust-arg"] = clust_arg

        return redirect('/anon/clusteringresults')

    return render(req, 'anon/clusteringpage.html')



def clusteringresults(req):


    if not "sel-camp-prov" in req.session and not "clust" in req.session and not "clust-arg" in req.session:
        return redirect("/anon/error")

    campaign = req.session["sel-camp-prov"]
    clust = req.session["clust"]
    clust_arg = req.session["clust-arg"]

    if clust == "km":
        clust_str = "k-Medoids"
    else:
        clust_str = clust.upper()

    if clust_arg != None:
        clust_str += ("#" + clust_arg.capitalize())


    #base_dir = "/app"
    base_dir = "/home/guido/Documenti/Thesis Project - Test/kg-anonymization"

    filename = campaign.lower().replace(" ", "_") + "_adm#0.50,0.50_n_" + clust

    if clust_arg is not None:
        filename += ("#" + clust_arg)

    filename += ".txt"

    clusters_filepath = os.path.join(base_dir, "anony-kg-modified", "outputs", "anonykg_thesis_-1", campaign.lower(), "clusters", "raw", filename)

    if not os.path.exists(clusters_filepath):
        print("File " + str(clusters_filepath) + " non esiste")
        return render(req, 'anon/clusteringresults.html', {'clusters': None})
    
    filename = "entities.idx"
    
    owners_filepath = os.path.join(base_dir, "anony-kg-modified", "outputs", "anonykg_thesis_-1", campaign.lower(), "raw", filename)

    if not os.path.exists(owners_filepath):
        print("File " + str(owners_filepath) + " non esiste")
        return render(req, 'anon/clusteringresults.html', {'clusters': None})

    filename = campaign.replace(" ", "_").lower() + ".txt"

    kvals_filepath = os.path.join(base_dir, "anony-kg-modified", "outputs", "anonykg_thesis_-1", campaign.lower(), "k_values", filename)

    if not os.path.exists(kvals_filepath):
        print("File " + str(kvals_filepath) + " non esiste")
        return render(req, 'anon/clusteringresults.html', {'clusters': None})


    kvals = {}

    with open(kvals_filepath, "r") as f:
        for row in f.readlines():
            row_values = row[:-1].split(",")
            kvals[row_values[0]] = row_values[1]

    owners = []

    with open(owners_filepath, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            owners.append(row_values[0] + "|" + row_values[1][:-1])

    clusters = []

    with open(clusters_filepath, "r") as f:
        for row in f.readlines():
            cluster = []
            cluster_kval = []
            for cluster_owner in row[:-1].split(","):
                for owner in owners:
                    owner_values = owner.split("|")
                    if owner_values[1] == cluster_owner:
                        cluster.append(owner_values[0])
                        cluster_kval.append(kvals[owner_values[1]])
            print(cluster)
            print(cluster_kval)
            cluster_values = zip(cluster, cluster_kval)
            clusters.append(cluster_values)


    if req.method == "POST":

        if "proceed" in req.POST:
            return redirect('/anon/anonymize')
        
        if "regen" in req.POST:
            del req.session["clust"]
            del req.session["clust-arg"]
            return redirect('/anon/clusteringpage')

    return render(req, 'anon/clusteringresults.html', {'clusters': clusters, 'clust_str': clust_str})





def anonymize(req):

    if not "sel-camp-prov" in req.session and not "clust" in req.session and not "clust-arg" in req.session:
        return redirect("/anon/error")
    
    clust = req.session["clust"]
    clust_arg = req.session["clust-arg"]

    campaign = req.session["sel-camp-prov"]

    if req.method == "POST":

        valid = req.POST.get("valid-alg")

        if valid == "sr":
            valid_arg = None
        else:
            valid_arg = "1.00"

        download = req.POST.get("save-choice")


        if clust == "vac":
            command_line = 'cd anony-kg-modified/ && python anonymize_clusters.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust
        else:
            command_line = 'cd anony-kg-modified/ && python anonymize_clusters.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust + ' --calgo_args=' + clust_arg


        if valid == "sr":
            command_line += ' --enforcer=sr'
        else:
            command_line += ' --enforcer=ms --enforcer_args=1'

        terminal = command_line
        subprocess.call(terminal, shell=True)

        command_line = 'cd anony-kg-modified/ && python anonymize_kg.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\"'

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

        command_line = 'cd anony-kg-modified/ && python visualize_outputs.py --data_list=anonykg_thesis --campaign=\"{}\" --refresh=y,y --src_type=graphs --exp_names={},{} --workers=1'.format(campaign.lower(), clust, valid)

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

        #base_dir = "/app"
        base_dir = "/home/guido/Documenti/Thesis Project - Test/kg-anonymization"



        filename = campaign.lower().replace(" ", "_") + ".csv"

        filepath = os.path.join(base_dir, "anony-kg-modified", "exp_data", "tuning_graphs", "anonykg_thesis_-1", filename)

        agg_filename = campaign.lower().replace(" ", "_") + "_agg.csv"

        agg_filepath = os.path.join(base_dir, "anony-kg-modified", "exp_data", "tuning_graphs", "anonykg_thesis_-1", agg_filename)

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

                    rru = str(float(rem_ent)/float(raw_ent))

                    rru_values = rru.split(".")
                    rru_values[1] = rru_values[1][:4]

                    rru = rru_values[0] + "." + rru_values[1]

                    graph = AnonyGraph.objects.filter(campaign=selectedCampaign, calgo=calgo, enforcer=enforcer)

                    if not graph:
                        new_graph = AnonyGraph(campaign=selectedCampaign, calgo=calgo, enforcer=enforcer, ail=float(ail), rru=float(rru))
                        new_graph.save()
                        print("Anony Graph added.")
                    else:
                        if graph[0].ail != float(ail) or graph[0].rru != float(rru):
                            graph[0].ail = float(ail)
                            graph[0].rru = float(rru)
                            graph[0].last_updated = datetime.now()
                            graph[0].save()
                            print("Anony Graph updated.")


        if download == "yes":

            command_line = 'cd anony-kg-modified/ && python generate_anon_kg_file.py --data=anonykg_thesis --campaign=\"' + campaign.lower() + '\" --calgo=' + clust

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