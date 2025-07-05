from django.shortcuts import render


def index(request):
    """
    View function for home page of site.
    """
    template = 'material/material.html'
    return render(
        request,
        template,
        context={
            },
    )
