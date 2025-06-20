import logging
from datetime import datetime
from django.http import HttpResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        ''' One-time configuration and initialization. '''
        self.get_response = get_response
        self.logger = logging.getLogger('django')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.FileHandler('requests.log'))

    def __call__(self, request):
        ''' Code to be executed for each request before or after
            the view (and later middleware) are called. '''
        user = request.user if request.user.is_authenticated else 'Anonymous'
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        ''' One-time configuration and initialization. '''
        self.get_response = get_response

    def __call__(self, request):
        ''' Code to be executed for each request before or after
            the view (and later middleware) are called. '''
        now = datetime.now()
        if now.hour < 21 and now.hour > 18:
            return HttpResponse('Sorry, the service is only available from 9 to 17', status=403)
        response = self.get_response(request)

        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        ''' One-time configuration and initialization. '''
        self.get_response = get_response
        ips = {} # Store the number of requests per IP address

    def __call__(self, request):
        ''' Code to be executed for each request before or after
            the view (and later middleware) are called. '''
        path = request.path
        if request.method == "POST" and "messages" and "conversation" in path:
            # get the IP address of the client
            ip = request.META.get('REMOTE_ADDR')
            if ip in self.ips:
                self.ips[ip] = [datetime.now(), self.ips[ip][1] + 1]
            else:
                self.ips[ip] = [datetime.now(), 1]
            if self.ips[ip][1] > 5:
                return HttpResponse('You have reached the maximum number of requests', status=429)
            # reset the counter after 1 minute
            if (datetime.now() - self.ips[ip][0]).seconds > 60:
                self.ips[ip] = [datetime.now(), 0]
            
            # delete the IP address from the dictionary if it has not made any requests in the last 5 minutes
            if len(self.ips) > 10:
                for ip in self.ips:
                    if (datetime.now() - self.ips[ip][0]).seconds > 300:
                        print(f"Deleting {ip}")
                        del self.ips[ip]

        response = self.get_response(request)

        return response

class RolepermissionMiddleware:
    def __init__(self, get_response):
        ''' One-time configuration and initialization. '''
        self.get_response = get_response
    
    def __call__(self, request):
        ''' Code to be executed for each request before or after
            the view (and later middleware) are called. '''
        if not request.user.is_authenticated and not request.user.is_staff:
            return HttpResponse('You do not have permission to access this page', status=403)
        response = self.get_response(request)

        return response
