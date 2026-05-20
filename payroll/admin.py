# payroll/admin.py — PRODUCTION READY
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.cache import cache
from .models import (
    User, Employee, Attendance, Deduction, 
    Payment, Company, SackedEmployee, Notification, 
    OTP, ExportToken, EmployeeRequest, EmployeeRequestAttachment,
    DownloadLog, AuditLog
)

# ─────────────────────────────────────────────
# USER ADMIN
# ─────────────────────────────────────────────
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Permissions', {
            'fields': (
                'role', 'employee_id',
                'is_company_admin', 'is_employee_admin',
                'is_payment_admin', 'is_deduction_admin',
                'is_hr_admin', 'is_request_admin',
                'is_notification_admin', 'is_password_admin',
            )
        }),
        ('Contact Info', {'fields': ('phone',)}),
    )


# ─────────────────────────────────────────────
# EMPLOYEE ADMIN
# ─────────────────────────────────────────────
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'type', 'status', 'location', 'salary']
    list_filter = ['type', 'status', 'location']
    search_fields = ['employee_id', 'name', 'email', 'phone']
    actions = ['clear_verification_cache']

    @admin.action(description='Clear Paystack verification cache for selected employees')
    def clear_verification_cache(self, request, queryset):
        count = 0
        for emp in queryset:
            bank_code = emp.bank_code or ""
            key = f"paystack:resolve:{bank_code}:{emp.account_number}"
            if cache.delete(key):
                count += 1
        self.message_user(request, f"Cleared verification cache for {count} employees.")


# ─────────────────────────────────────────────
# ATTENDANCE ADMIN
# ─────────────────────────────────────────────
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'clock_in', 'clock_out', 'clock_method']
    list_filter = ['status', 'clock_method', 'date']
    search_fields = ['employee__name', 'employee__employee_id']
    date_hierarchy = 'date'


# ─────────────────────────────────────────────
# DEDUCTION ADMIN
# ─────────────────────────────────────────────
@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'amount', 'date', 'status', 'hr_approved', 'hr_approved_by']
    list_filter = ['status', 'hr_approved', 'date']
    search_fields = ['employee__name', 'employee__employee_id', 'reason']
    date_hierarchy = 'date'


# ─────────────────────────────────────────────
# PAYMENT ADMIN
# ─────────────────────────────────────────────
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'net_amount', 'status', 'hr_approved',
        'payment_month', 'payment_method', 'payment_date'
    ]
    list_filter = ['status', 'hr_approved', 'payment_method', 'payment_date']
    search_fields = ['employee__name', 'employee__employee_id', 'transaction_reference']
    date_hierarchy = 'payment_date'


# ─────────────────────────────────────────────
# COMPANY ADMIN
# ─────────────────────────────────────────────
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'status', 'guards_count', 'profit']
    list_filter = ['status']
    search_fields = ['name', 'location']
    filter_horizontal = ['assigned_guards']


# ─────────────────────────────────────────────
# SACKED EMPLOYEE ADMIN
# ─────────────────────────────────────────────
@admin.register(SackedEmployee)
class SackedEmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date_sacked', 'terminated_by']
    list_filter = ['date_sacked']
    search_fields = ['employee__name', 'employee__employee_id']
    date_hierarchy = 'date_sacked'


# ─────────────────────────────────────────────
# NOTIFICATION ADMIN
# ─────────────────────────────────────────────
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'is_read', 'created_at']
    list_filter = ['type', 'is_read']
    search_fields = ['user__username', 'message']
    date_hierarchy = 'created_at'


# ─────────────────────────────────────────────
# OTP ADMIN
# ─────────────────────────────────────────────
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'reference', 'is_used', 'expires_at', 'created_at']
    list_filter = ['is_used']
    search_fields = ['email', 'reference']
    date_hierarchy = 'created_at'


# ─────────────────────────────────────────────
# EXPORT TOKEN ADMIN
# ─────────────────────────────────────────────
@admin.register(ExportToken)
class ExportTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'data_type', 'is_used', 'is_2fa_verified', 'expires_at']
    list_filter = ['is_used', 'is_2fa_verified', 'data_type']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'


# ═════════════════════════════════════════════
# MISSING MODELS — NOW REGISTERED
# ═════════════════════════════════════════════

# ─────────────────────────────────────────────
# EMPLOYEE REQUEST ADMIN
# ─────────────────────────────────────────────
@admin.register(EmployeeRequest)
class EmployeeRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'request_type', 'amount', 'status', 'created_at']
    list_filter = ['status', 'request_type']
    search_fields = ['employee__name', 'employee__employee_id', 'description']
    date_hierarchy = 'created_at'


# ─────────────────────────────────────────────
# EMPLOYEE REQUEST ATTACHMENT ADMIN
# ─────────────────────────────────────────────
@admin.register(EmployeeRequestAttachment)
class EmployeeRequestAttachmentAdmin(admin.ModelAdmin):
    list_display = ['request', 'file_type', 'file']
    list_filter = ['file_type']


# ─────────────────────────────────────────────
# DOWNLOAD LOG ADMIN
# ─────────────────────────────────────────────
@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee', 'doc_type', 'reference', 'ip_address', 'timestamp']
    list_filter = ['doc_type']
    search_fields = ['user__username', 'employee__name', 'reference']
    date_hierarchy = 'timestamp'


# ─────────────────────────────────────────────
# AUDIT LOG ADMIN
# ─────────────────────────────────────────────
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'timestamp']
    search_fields = ['user__username', 'action']
    date_hierarchy = 'timestamp'