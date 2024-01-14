import datetime

from django.core.cache import cache

from core.settings import ROOT, WS_ROOT, GOOGLE_RECAPTCHA_SITE_KEY, GOOGLE_JS_MAP_API_KEY
from frontend.models import Frontend
from frontend.serializers import FrontendSerializer


def global_settings(request):
    my_context = {
        'GOOGLE_RECAPTCHA_SITE_KEY': GOOGLE_RECAPTCHA_SITE_KEY,
        'GOOGLE_JS_MAP_API_KEY': GOOGLE_JS_MAP_API_KEY,
        'ROOT': ROOT,
        'WS_ROOT': WS_ROOT,
        "today_min":  datetime.datetime.combine(datetime.date.today(), datetime.time.min),
        "today_max":  datetime.datetime.combine(datetime.date.today(), datetime.time.max),
        "model_years": cache.get("model_years", [y for y in range(datetime.date.today().year, 1974, -1)]),
        "AUTH_TOKEN": None,
        "frontend": FrontendSerializer(instance=Frontend.objects.filter(is_active=True
                                                                        ).order_by('-created_at').first()).data
    }

    if "status" in request.session:
        my_context["status"] = request.session["status"]
        my_context["message"] = request.session["message"]
        del request.session["status"]
        del request.session["message"]

    return my_context
