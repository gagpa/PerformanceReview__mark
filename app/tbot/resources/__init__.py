from app.services.review.review_period import ReviewPeriodService
from app.tbot.extensions.request_serializer import RequestSerializer
from app.tbot.services.forms import ReviewIsNotUpped


def only_on_review(func):
    def decorator(request: RequestSerializer):
        if ReviewPeriodService().is_now:
            return func(request)
        return ReviewIsNotUpped()

    return decorator
