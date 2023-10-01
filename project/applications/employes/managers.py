from django.contrib.auth.models import BaseUserManager

class EmployeeManager(BaseUserManager):
    def get_employees_branch(self, branch):
        return self.filter(user__branch=branch, deleted_at=None)