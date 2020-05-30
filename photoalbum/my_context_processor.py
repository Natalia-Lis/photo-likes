from datetime import datetime
from django.contrib.auth.models import User


def my_cp(request):
    zalogowany = request.user
    cp_ctx = {
        "zalogowany":zalogowany,
        "now": datetime.now(),
    }
    return cp_ctx