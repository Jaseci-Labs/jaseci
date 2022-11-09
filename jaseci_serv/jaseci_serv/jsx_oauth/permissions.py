# from django.conf import settings
# import requests
# from rest_framework import permissions
# from rest_framework.exceptions import PermissionDenied
# from datetime import datetime
# from jaseci_enterprise.auto_jobs.jobs import schedule_api_call

# from jaseci_enterprise.jsx_oauth.models import LicenseCheckStatus


# class IsValidateLicense(permissions.BasePermission):
#     message = settings.LICENSE_VALIDATION_ERROR_MSG

#     def has_permission(self, request, view):
#         super().has_permission(request, view)
#         try:
#             license_data = LicenseCheckStatus.objects.all().first()
#             if license_data:
#                 if (
#                     license_data.license_status == True
#                     and license_data.is_user_active == True
#                 ):
#                     return True
#                 raise PermissionDenied(self.message)
#             else:
#                 if schedule_api_call():
#                     return True
#                 raise PermissionDenied(self.message)
#         except requests.exceptions.RequestException as e:
#             raise PermissionDenied(self.message)
