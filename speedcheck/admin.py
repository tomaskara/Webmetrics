from django.contrib import admin

from .models import Annotations, CruxHistory, CruxWeeklyHistory

admin.site.register(CruxHistory)
admin.site.register(Annotations)
admin.site.register(CruxWeeklyHistory)

