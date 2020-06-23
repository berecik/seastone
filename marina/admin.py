from django.contrib import admin


from django.contrib import admin
from .models import Marina, Place, Contract, Leave, Pier, Ship, Stay, Hub, Flag, Connection, Connector


class MarinaAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name')
    # list_display_links = ('name')

admin.site.register(Marina, MarinaAdmin)




class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'pier', 'order')
    list_display_links = ('name',)


admin.site.register(Place, PlaceAdmin)


class ContractAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name')
    # list_display_links = ('name')

admin.site.register(Contract, ContractAdmin)


class LeaveAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name')
    # list_display_links = ('name')

admin.site.register(Leave, LeaveAdmin)




class PierAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_display_links = ('name',)


admin.site.register(Pier, PierAdmin)


class ShipAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name')
    # list_display_links = ('name')

admin.site.register(Ship, ShipAdmin)


class StayAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name')
    # list_display_links = ('name')

admin.site.register(Stay, StayAdmin)


class HubAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name')
    # list_display_links = ('name')

admin.site.register(Hub, HubAdmin)


class FlagAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name')
    # list_display_links = ('name')

admin.site.register(Flag, FlagAdmin)


class ConnectionAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name')
    # list_display_links = ('name')

admin.site.register(Connection, ConnectionAdmin)


class ConnectorAdmin(admin.ModelAdmin):
    pass
    # list_display = ('name')
    # list_display_links = ('name')

admin.site.register(Connector, ConnectorAdmin)
