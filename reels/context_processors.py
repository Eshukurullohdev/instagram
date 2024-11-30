from .models import Reel

def first_reel(request):
    reel = Reel.objects.first()
    return {"reel": reel}