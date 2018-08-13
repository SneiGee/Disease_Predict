from django.contrib import admin
from .models import Profile, Doctor


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date', 'phone')

    def user_info(self, obj):
        return obj.location

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('user')
        return queryset


admin.site.register(Profile, UserProfileAdmin)
admin.site.register(Doctor)
