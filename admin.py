from django.contrib import admin
from .models import User,Expenses,Income

# Register your models here.
admin.site.register(User)
admin.site.register(Expenses)
admin.site.register(Income)