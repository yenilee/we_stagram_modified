import json

from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Comment
from user.models import User 

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)

        if User.objects.filter(user_id=data['user_id']).exists():
            valid_user = User.objects.get(user_id=data['user_id'])
            Comment(
                    user_id = valid_user.id,
                    comment = data['comment']
            ).save()
            return HttpResponse(status=200)
        return JsonResponse({'message': 'INVALID_USER'}, status=401)

    def get(self, request):
        comment = Comment.objects.values()
        return JsonResponse({'comments':list(comment)}, status=200)


class CommentfilterView(View):
    def post(self, request):
        data = json.loads(request.body)
        comment_user = data.get('user_id', None)

        if User.objects.filter(user_id=comment_user).exists():
            user_fk_key = User.objects.get(user_id=comment_user).id
            user_comment_list = Comment.objects.filter(user_id=user_fk_key).values('comment')
            return JsonResponse({'user_comment_list':list(user_comment_list)}, status=200)
        return JsonResponse({'message':"INVALID_KEY"}, status=400)

