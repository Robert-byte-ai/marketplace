class MobileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Mobile' in request.META['HTTP_USER_AGENT']:
            request.is_mobile = True
        response = self.get_response(request)
        return response
