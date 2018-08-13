from django.contrib import admin
from .models import Symptom, Disease, DiseaseReport


class DiseaseListAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'views')

    def user_info(self, obj):
        return obj.location

    def get_queryset(self, request):
        queryset = super(DiseaseListAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-disease_name')
        return queryset


admin.site.register(Symptom)
admin.site.register(Disease, DiseaseListAdmin)
admin.site.register(DiseaseReport)
