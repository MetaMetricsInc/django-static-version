from django.conf import settings

def static_urls(request):
    return dict(request, static_version=settings.STATIC_VERSION)
