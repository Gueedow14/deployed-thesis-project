from django.contrib import admin
from .models import Provider, Campaign, Attribute, Relationship, Value, Owner, Attribute_Edge, Relationship_Edge

admin.site.register(Provider)
admin.site.register(Campaign)
admin.site.register(Attribute)
admin.site.register(Relationship)
admin.site.register(Value)
admin.site.register(Owner)
admin.site.register(Attribute_Edge)
admin.site.register(Relationship_Edge)


