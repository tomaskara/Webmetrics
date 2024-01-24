from django.shortcuts import render, redirect
from .forms import UtmBuilder


def utm_builder(request):
    form = UtmBuilder()
    return render(request, template_name="utm_generator/utm_builder.html", context={"form": form})

def utm_builder_redirect(request):
    return redirect(utm_builder)
