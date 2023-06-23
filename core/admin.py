from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import IntakeForm, Request, Template


from .views import sign_up_api, sign_in_api

class UserAdmin(BaseUserAdmin):
    def sign_up_link(self, obj):
        url = reverse('admin:sign_up')
        return format_html('<a href="{}">Sign Up API</a>', url)

    def sign_in_link(self, obj):
        url = reverse('admin:sign_in')
        return format_html('<a href="{}">Sign In API</a>', url)

    sign_up_link.short_description = 'Sign Up API'
    sign_in_link.short_description = 'Sign In API'
    readonly_fields = ['sign_up_link', 'sign_in_link']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register_view('sign-up/', view=sign_up_api, name='sign_up')
admin.site.register_view('sign-in/', view=sign_in_api, name='sign_in')

admin.site.register(IntakeForm)
admin.site.register(Request)
admin.site.register(Template)
