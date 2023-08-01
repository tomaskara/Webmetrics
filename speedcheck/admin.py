from django.contrib import admin

from .models import Annotations, CruxHistory

admin.site.register(CruxHistory)
admin.site.register(Annotations)

