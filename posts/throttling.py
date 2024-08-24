from rest_framework.throttling import UserRateThrottle

class PostRateThrottle(UserRateThrottle):
    scope = "Post"
