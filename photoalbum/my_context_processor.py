from datetime import datetime, timezone, date
from django.contrib.auth.models import User


def my_cp(request):
    zalogowany = request.user
    cp_ctx = {
        "zalogowany":zalogowany,
        "now": date.today(),
    }
    return cp_ctx