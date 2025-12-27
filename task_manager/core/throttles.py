from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class SignupRateThrottle(AnonRateThrottle):
    scope = "signup"


class LoginRateThrottle(AnonRateThrottle):
    scope = "login"


class TaskCreateRateThrottle(UserRateThrottle):
    scope = "task_create"


class TaskListRateThrottle(UserRateThrottle):
    scope = "task_list"
