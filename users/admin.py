from django.contrib import admin

from .models import TailorDetail, TailorProduct,CustomUser


# Register your models here.
admin.site.register(TailorDetail)
admin.site.register(TailorProduct)
admin.site.register(CustomUser)
