from django.contrib import admin
from .models import Emprunt, Livre, DVD, CD, Membre, JeuDePlateau

admin.site.register(Membre)
admin.site.register(Livre)
admin.site.register(DVD)
admin.site.register(CD)
admin.site.register(JeuDePlateau)
admin.site.register(Emprunt)

# Register your models here.
