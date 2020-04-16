import json
import bcrypt
import jwt

from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import User 
from .utils import SECRET_KEY

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        new_user_id = data.get('user_id', None)
        new_user_password = data.get('password', None)

        if User.objects.filter(user_id=new_user_id):
            return JsonResponse({'message':'DUPLICATE_USER'}, status=401)
        if new_user_id == None or new_user_password == None:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)
        password_hashed = bcrypt.hashpw(new_user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User(
                user_id  = new_user_id,
                password = password_hashed
        ).save()
        return HttpResponse(status=200)

class UserView(View):
    def get(self, request):
        user_list = User.objects.values()
        return JsonResponse({'user_info':list(user_list)}, status=200)

class SigninView(View):
    def post(self, request):
        data = json.loads(request.body)
        login_id = data.get('user_id', None)
        login_password = data.get('password', None)

        if User.objects.filter(user_id=login_id).exists():
            valid_user=User.objects.get(user_id=login_id)
            if bcrypt.checkpw(login_password.encode('utf-8'), valid_user.password.encode('utf-8')):
                payload_data = {'request_id':str(valid_user.id)}
                token = jwt.encode(payload_data, SECRET_KEY, algorithm='HS256')
                decode_token = token.decode('utf-8')
                return JsonResponse({'TOKEN':decode_token}, status=200)
            return JsonResponse({'message':'INVALID_PASSWORD'}, status = 401)
        return JsonResponse({'message': 'INVALID_USER'}, status = 401)

