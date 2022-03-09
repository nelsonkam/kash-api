from rest_framework.throttling import UserRateThrottle


class VerificationCodeThrottle(UserRateThrottle):
    scope = "verification-code"

    def allow_request(self, request, view):
        is_allowed = super(VerificationCodeThrottle, self).allow_request(request, view)
        if not is_allowed and hasattr(request, 'profile'):
            request.profile.push_notify(
                "Nombre d'essai dépassé",
                "Vous avez dépassé le nombre d'essai pour l'heure. Veuillez réessayer dans une heure.",
                obj=request.profile,
            )
        return is_allowed
