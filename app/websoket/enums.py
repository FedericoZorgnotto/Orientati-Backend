from enum import Enum


class UserRole(str, Enum):
    USER = "users"
    ADMIN = "admin"
    ADMIN_DASHBOARD = "adminDashboard"
