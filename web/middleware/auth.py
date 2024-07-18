from web import models
from django.utils.deprecation import MiddlewareMixin
class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        '''如果用户已登录，在request中赋值'''
        user_id = request.session.get('user_id',0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()

        request.tracer = user_object