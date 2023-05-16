from django.contrib import admin
from .models import CruxHistory, Annotations

admin.site.register(CruxHistory)
admin.site.register(Annotations)

