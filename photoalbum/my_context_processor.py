from datetime import datetime, timezone, date
from django.contrib.auth.models import User


def my_cp(request):
    logged_in = request.user
    cp_ctx = {
        "logged_in":logged_in,
        "now": date.today(),
    }
    return cp_ctx