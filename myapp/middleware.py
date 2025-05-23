from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        
    def __call__(self,request):
        if request.user.is_authenticated:
            paths_to_redirect=[reverse('blog:login'),reverse('blog:register')]
            
            if request.path in paths_to_redirect:
                return redirect('blog:index')
        response = self.get_response(request)
        return response
        
        
class RedirectUnauthenticatedUserMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        
    def __call__(self, request):
        restricted_paths=[reverse('blog:dashboard')]
        if not request.user.is_authenticated and request.path in restricted_paths:
            return redirect(reverse('blog:login'))
    
        response=self.get_response(request)
        return response
        
        