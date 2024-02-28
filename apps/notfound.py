from django.shortcuts import render


def notFound404(request, template_name='exception/notfound.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response