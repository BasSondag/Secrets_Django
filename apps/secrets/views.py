from django.shortcuts import render, redirect, HttpResponse
from .models import User, Post
from django.contrib import messages
from django.db.models import Count
# Create your views here.

def index(request):
	return render(request, 'secrets/index.html')

def show(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'secrets': Post.objects.annotate(numlike= Count('like')).order_by('-created_at')[:5]
    }
    return render(request, 'secrets/show.html',context)

def populair(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'secrets':  Post.objects.annotate(numlike=Count('like')).order_by('-numlike')[:4]
    }
    return render(request,'secrets/secrets.html', context)

def create_signup(request):
    if request.method == "POST":
        print ('you post a form')
        user_details = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'pw_comfirm': request.POST['pw_comfirm']
        }
        user= User.objects.register(user_details)
        # print type(user), 'the user came back from models'
        if 'errors' in user:
            print ('there are errors', user['errors'])
            for message in user['errors']:
                messages.add_message(request, messages.INFO, message)   
            return redirect('index')
        if 'theuser' in user:
            print user['theuser'].id
            request.session['user_id'] = user['theuser'].id
            return redirect('show')
    else:
        return redirect("index")

def login(request):
    if request.method == 'POST':
        user = User.objects.authenticate(request.POST)
        if 'errors' in user:
            messages.add_message(request, messages.INFO, user['errors'])   
            return redirect('index')
        if 'theuser' in user:
            print user['theuser'].id
            request.session['user_id'] = user['theuser'].id
            return redirect('show')
    else:
        return redirect("index")	

def destroy(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('index')

def create_secrets(request):
    if request.method == 'POST':
        print(request.POST, 'controller')
        secret_details = {
            'content': request.POST['content'],
            'user_id': request.session['user_id']
        }
        secret = Post.objects.create_post(secret_details)
        if 'errors' in secret:
            for message in secret['errors']:
                messages.add_message(request,  messages.INFO, message)
            return redirect("show")
        if 'thesecret' in secret:
            print ('hehehehehehe secret is created ')
            return redirect("show")
    else:
        print('this was not a post')
        return redirect("show")

def delete_secrets(request):
    if request.method == 'POST':
        try:
            target = Post.objects.get(id = request.POST['id'])
        except Post.DoesNotExist:
            messages.info(request, 'Post was not found')
            return redirect('show')
        target.delete()
        return redirect('show')
    else:
        return redirect('show')

def like_recent(request):
    if request.method == 'POST':
        like_details = {
            'liker': request.session["user_id"],
            'liked_post': request.POST['secret_id']
        }
        print(like_details, 'in controller')
        add_like = Post.objects.create_like(like_details)
        if 'errors' in add_like:
            print(add_like['errors'], 'this is your error')
            messages.add_message(request,  messages.INFO, add_like['errors'])
            return redirect('show')
        else:
            return redirect('show')
    else:
        return redirect('show')

def un_like_recent(request):
    if request.method == "POST":
        unlike_details = {
            'liker': request.session["user_id"],
            'liked_post': request.POST['secret_id']
        }
        un_like = Post.objects.delete_like(unlike_details)
        if 'errors' in un_like:
            print(un_like['errors'], 'this is your error')
            messages.add_message(request,  messages.INFO, un_like['errors'])
            return redirect('show')
        else:
            return redirect('show')
    else:
        return redirect('show')

def delete_secrets_pop(request):
    if request.method == 'POST':
        print('your in populair')
        try:
            target = Post.objects.get(id = request.POST['id'])
        except Post.DoesNotExist:
            messages.info(request, 'Post was not found')
            return redirect('poppulair')
        target.delete()
        return redirect('populair')
    else:
        return redirect('populair')

def like_pop(request):
    if request.method == 'POST':
        print('your in populair')
        like_details = {
            'liker': request.session["user_id"],
            'liked_post': request.POST['secret_id']
        }
        print(like_details, 'in controller')
        add_like = Post.objects.create_like(like_details)
        if 'errors' in add_like:
            print(add_like['errors'], 'this is your error')
            messages.add_message(request,  messages.INFO, add_like['errors'])
            return redirect('populair')
        else:
            return redirect('populair')
    else:
        return redirect('populair')

def un_like_pop(request):
    if request.method == "POST":
        print('your in populair')
        unlike_details = {
            'liker': request.session["user_id"],
            'liked_post': request.POST['secret_id']
        }
        un_like = Post.objects.delete_like(unlike_details)
        if 'errors' in un_like:
            print(un_like['errors'], 'this is your error')
            messages.add_message(request,  messages.INFO, un_like['errors'])
            return redirect('/secrets/populair')
        else:
            return redirect('populair')
    else:
        return redirect('populair')



