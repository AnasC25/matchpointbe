from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import CustomUser, Equipment, Reservation, Terrain, Reservation, Order, OrderItem

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')  # ✅ Colonnes affichées
    ordering = ('email',)  # ✅ Trier par email
    search_fields = ('email', 'username')  # ✅ Ajout de recherche
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'telephone', 'niveau', 'societe')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(Equipment)
admin.site.register(Reservation)
admin.site.register(Terrain)
admin.site.register(Order)
admin.site.register(OrderItem)

