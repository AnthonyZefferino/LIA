from django.utils import translation

class SetLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_language = 'it'  # Codice della lingua italiana
        translation.activate(user_language)
        response = self.get_response(request)
        translation.deactivate()
        return response
