from django.db import models

import datetime



class Provider(models.Model):
    email = models.EmailField(primary_key=True)
    pwd = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.email

class Attribute(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self) -> str:
        return self.name

class Relationship(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self) -> str:
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    creator = models.ForeignKey(Provider, on_delete=models.CASCADE)
    attributes = models.ManyToManyField(Attribute, blank=True)
    relationships = models.ManyToManyField(Relationship, blank=True)

    def __str__(self) -> str:
        return self.name

class Owner(models.Model):
    email = models.EmailField(primary_key=True)
    pwd = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.email
    
class OwnerCampaign(models.Model):
    owner_campaign_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    k = models.IntegerField(null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.owner.email + " attends campaign " + self.campaign.name + " with k-val: " + str(self.k)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'campaign'], name='unique_campaign_owner_combination'
            )
        ]


class Value(models.Model):
    value = models.CharField(max_length=300, primary_key=True)

    def __str__(self) -> str:
        return self.value


class Attribute_Edge(models.Model):
    attr_edge_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(Value, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, default='error')

    def __str__(self) -> str:
        return self.owner.email + " ---[" + self.attribute.name + "]--> " + self.value.value + " for campaign: " + self.campaign.name

class Relationship_Edge(models.Model):
    rel_edge_id = models.AutoField(primary_key=True)
    owner1 = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='owner1')
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE)
    owner2 = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='owner2')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, default='error')

    def __str__(self) -> str:
        return self.owner1.email + " ---[" + self.relationship.name + "]--> " + self.owner2.email + " for campaign: " + self.campaign.name


class AnonyGraph(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, default='error')
    calgo = models.CharField(max_length=20, default='error')
    enforcer = models.CharField(max_length=20, default='error')
    ail = models.FloatField()
    rru = models.FloatField()
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.campaign.name + " {AIL: " + str(self.ail) + "} {RRU: " + str(self.rru) + "} [" + str(self.last_updated) + "]"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['campaign', 'calgo', 'enforcer'], name='unique_campaign_calgo_enforcer_combination'
            )
        ]