
from datetime import date
from distutils.log import ERROR
from django.contrib import admin, messages
from django.db.models import Value
from django.db.models.functions import Concat
from .models import Passenger, Staff
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext


class BalanceListFilter(admin.SimpleListFilter):
    title = 'Balance'
    parameter_name = 'balance'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        if qs.filter(balance__lt=20).exists():
            yield ('<20', _('Low Balance'))
        if qs.filter(balance__gte=20, balance__lt=100).exists():
            yield ('20-100', _('Between 20 and 100'))
        if qs.filter(balance__gte=100, balance__lt=200).exists():
            yield ('100-200', _('Between 100 and 200'))
        if qs.filter(balance__gte=200, balance__lt=300).exists():
            yield ('200-300', _('Between 200 and 300'))
        if qs.filter(balance__gte=300, balance__lt=400).exists():
            yield ('300-400', _('Between 300 and 400'))
        if qs.filter(balance__gte=400, balance__lt=500).exists():
            yield ('400-500', _('Between 400 and 500'))
        if qs.filter(balance__gte=500).exists():
            yield ('>500', _('High Balance'))
        if qs.filter(balance__lt=0).exists():
            yield ('<0', _('In Debt'))

    def queryset(self, request, queryset):
        if self.value() == '<20':
            return queryset.filter(balance__lt=20)
        if self.value() == '20-100':
            return queryset.filter(balance__gte=20, balance__lt=100)
        if self.value() == '100-200':
            return queryset.filter(balance__gte=100, balance__lt=200)
        if self.value() == '200-300':
            return queryset.filter(balance__gte=200, balance__lt=300)
        if self.value() == '300-400':
            return queryset.filter(balance__gte=300, balance__lt=400)
        if self.value() == '400-500':
            return queryset.filter(balance__gte=400, balance__lte=500)
        if self.value() == '>500':
            return queryset.filter(balance__gte=500)
        if self.value() == '<0':
            return queryset.filter(balance__lt=0)


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    date_hierarchy = 'registration_date'
    readonly_fields = ('last_update', 'registration_date')
    empty_value_display = 'None'
    # actions = ['clear_balance']

    fieldsets = (
        (None, {
            'fields': ('first_name', 'middle_name', 'last_name')
        }),
        ('Tag ID and Balance', {
            'fields': (('tag_id', 'balance'),)
        }),
        ('Contact Information', {
            'fields': (('phone_number', 'email_address'),)
        }),
        ('Date Information', {
            'classes': ('collapse',),
            'fields': (('last_update', 'registration_date'),)
        }),
    )
    list_filter = (BalanceListFilter, 'registration_date',
                   'last_update')
    list_display = ('full_name', 'balance', 'tag_id',
                    'phone_number', 'email_address')
    sortable_by = ('full_name', 'balance')
    list_per_page = 10
    # search_help_text = 'Use name of client for searching'
    search_fields = ['first_name', 'middle_name', 'last_name']
    show_full_result_count = False
    ordering = ['first_name', 'middle_name', 'last_name']
    # list_editable = ['balance']

    @admin.display(description='Full Name', ordering=Concat('first_name', Value(' '), 'middle_name', Value(' '), 'last_name'))
    def full_name(self, obj):
        return ("%s %s %s" % (obj.first_name, obj.middle_name, obj.last_name))

    @admin.action(description='Clear Balance')
    def clear_balance(self, request, queryset):
        updated = queryset.update(balance=0)
        self.message_user(
            request,
            ngettext(
                '%d user was successfully updated.',
                '%d users were successfully updated.',
                updated,
            ) % updated,
            messages.SUCCESS
        )


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    # date_hierarchy = 'registration_date'
    # actions = None
    readonly_fields = ('date_joined', 'last_login')
    empty_value_display = 'None'
    # actions = ['clear_balance']

    fieldsets = (
        (None, {
            'fields': ('first_name', 'middle_name', 'last_name')
        }),
        ('Contact Information', {
            'fields': (('phone_number', 'email'),)
        }),
        ('Date Information', {
            'classes': ('collapse',),
            'fields': (('last_login', 'date_joined'),)
        }),
    )
    list_filter = ('is_superadmin', 'last_login', 'date_joined')
    list_display = ('full_name', 'email', 'phone_number', 'last_login')
    sortable_by = ('full_name',)
    list_per_page = 10
    # search_help_text = 'Use name of client for searching'
    search_fields = ['first_name', 'middle_name', 'last_name']
    show_full_result_count = False
    ordering = ['first_name', 'middle_name', 'last_name']
    # list_editable = ['balance']

    @admin.display(description='Full Name', ordering=Concat('first_name', Value(' '), 'middle_name', Value(' '), 'last_name'))
    def full_name(self, obj):
        return ("%s %s %s" % (obj.first_name, obj.middle_name, obj.last_name))
