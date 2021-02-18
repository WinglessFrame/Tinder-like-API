from rest_framework.throttling import UserRateThrottle

from GinderApp.api.api_utils import get_user_daily_limit


class SubscriptionRateThrottle(UserRateThrottle):
    # Define a custom scope name to be referenced by DRF in settings.py
    scope = "subscription"

    def __init__(self):
        super().__init__()

    def allow_request(self, request, view):
        """
        Override rest_framework.throttling.SimpleRateThrottle.allow_request

        Check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if request.user.is_staff:
            return True

        if request.user.is_authenticated:
            user_daily_limit = get_user_daily_limit(request.user)
            if user_daily_limit:
                # Override the default from settings.py
                self.duration = 86400
                self.num_requests = user_daily_limit
            else:
                # No limit == unlimited plan
                return True

        # Original logic from the parent method...

        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()
