from django.http import HttpResponsePermanentRedirect
from django.utils.http import escape_leading_slashes

class SlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifier si l'URL se termine par un slash
        if request.path_info.endswith('/'):
            # Si oui, enlever le slash et rediriger
            new_path = request.path_info.rstrip('/')
            if new_path:
                return HttpResponsePermanentRedirect(
                    escape_leading_slashes(request.get_full_path().replace(request.path_info, new_path))
                )
        else:
            # Si non, ajouter le slash et rediriger
            new_path = request.path_info + '/'
            return HttpResponsePermanentRedirect(
                escape_leading_slashes(request.get_full_path().replace(request.path_info, new_path))
            )
        
        return self.get_response(request) 