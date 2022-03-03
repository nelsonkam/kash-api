from rest_framework.throttling import UserRateThrottle


class VerificationCodeThrottle(UserRateThrottle):
    scope = 'verification-code'