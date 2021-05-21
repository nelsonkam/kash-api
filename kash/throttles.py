from rest_framework.throttling import UserRateThrottle


class DepositRateThrottle(UserRateThrottle):
    scope = 'deposit'
