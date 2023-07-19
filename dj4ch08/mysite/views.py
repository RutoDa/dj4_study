from django.shortcuts import render, redirect
from mysite import models


def index(request):
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['mood']
    except:
        user_id = None
        message = '如要張貼訊息，請確認每一個欄位皆有填寫．．．'

    if user_id != None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message = f'成功儲存！請記得你的編輯密碼[{user_id}]，訊息經審查後才會顯示。'
    moods = models.Mood.objects.all()
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    return render(request, 'index.html', locals())

def delpost(request, pid=None, del_pass=None):
    if del_pass and pid:
        try:
            post = models.Post.objects.get(id=pid)
            if post.del_pass == del_pass:
                post.delete()
        except:
            pass
    return redirect('/')
