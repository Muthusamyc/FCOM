import logging
from functools import wraps

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse



def api_error_logger(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:            
            if isinstance(e, ValueError):
                logging.error(str(e))
                return JsonResponse({'message': e.args[0], 'type': 'ValueError'})
            elif isinstance(e, AttributeError):
                logging.error(str(e))
                return JsonResponse({'message': e.args[0], 'type': 'AttributeError'})
            elif isinstance(e, KeyError):
                logging.error(str(e))
                return JsonResponse({'message': e.args[0], 'type': 'KeyError'})
            elif isinstance(e, TypeError):
                logging.error(str(e))
                return JsonResponse({'message': e.args[0], 'type': 'TypeError'})
            else:
                logging.error(str(e))
                return JsonResponse({'message': str(e), 'type': 'InternalServerError'})
    return wrapped


logger = logging.getLogger(__name__)

def request_error_logger(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as e:  
            print(e)                     
            logger.error(str(e))
            messages.error(request, str(e))
            return HttpResponseRedirect(request.path)
    return wrapped
