from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import CustomUser, Equipment, Reservation, Terrain, Order, OrderItem, Club

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'telephone', 'email')
    list_filter = ('ville',)
    search_fields = ('nom', 'ville', 'email')
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'image')
        }),
        ('Contact', {
            'fields': ('adresse', 'ville', 'telephone', 'email')
        }),
    )

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_club_agent', 'club')
    ordering = ('email',)
    search_fields = ('email', 'username')
    list_filter = ('is_club_agent', 'club', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'telephone', 'niveau', 'societe')}),
        ('Club', {'fields': ('club', 'is_club_agent')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'localisation', 'prix_par_heure', 'disponible', 'discipline', 'club')
    fields = ('id', 'nom', 'localisation', 'prix_par_heure', 'caracteristiques', 'image', 'disponible', 'discipline', 'club')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_method', 'payment_status', 'total_price', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_status')
    search_fields = ('id', 'user__email', 'shipping_email')
    readonly_fields = ('created_at', 'total_price')

admin.site.register(Equipment)
admin.site.register(Reservation)
admin.site.register(OrderItem)
