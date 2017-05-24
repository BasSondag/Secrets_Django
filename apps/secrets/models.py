# Create your models here.
# Inside your app's models.py file
from __future__ import unicode_literals
from django.db import models
import re, bcrypt


#Our new manager!
#No methods in our new manager should ever catch the whole request object with a parameter!!! (just parts, like request.POST)
class UserManager(models.Manager):
    def authenticate(self, postData):
        print ("Running a login function!")
        print (postData, "data made it to the model")
        if 'email' in postData and 'password' in postData:
            try:
                user = User.objects.get(email=postData['email'])

            except User.DoesNotExist:
                return {'errors': 'Invalid email, or password does not match email'}
            user_pw = user.pw_hash.encode()
            pw_match = bcrypt.hashpw(postData['password'].encode(),user_pw)
            if pw_match == user_pw:
                return {'theuser': user}
            else:
                return {'errors': 'Email and password combination do not match'}
        else:
            return {'errors': 'Please enter Login information'}
        print ("If successful login occurs, maybe return {'theuser':user} where user is a user object?")

        print ("If unsuccessful, maybe return { 'errors':['Login unsuccessful'] }")
    def register(self, user):
        print ("Register a user here")
        print (user, "data made it to the model")
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not user['first_name']:
            errors.append('First name cannot be blank')
        elif len(user['first_name']) < 2:
            errors.append('First name must at least 2 characters long')
        if not user['last_name']:
            errors.append('Last name cannot be blank')
        elif len(user['last_name']) < 2:
            errors.append('Last name must at least 2 characters long')
        if not user['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user['email']):
            errors.append('Email format must be valid!')
        elif len(User.objects.filter(email=user['email']))>0:
            errors.append('This email is already registered')    
        if not user['password']:
            errors.append('Password cannot be blank')
        elif len(user['password'])< 8:
            errors.append('Password must be at least 8 characters long')
        elif user['password'] != user['pw_comfirm']:
            errors.append('Password and confirmation must match')
        if errors:
            print(errors, "?are there errors")
            return {"errors": errors}
        else:    
            user = User.objects.create(first_name=user['first_name'], last_name= user['last_name'], email= user['email'], pw_hash=bcrypt.hashpw(user['password'].encode(),bcrypt.gensalt()))
            return {"theuser": user}
 
        print ("If successful, maybe return {'theuser':user} where user is a user object?")
        print ("If unsuccessful do something like this? return {'errors':['User first name to short', 'Last name too short'] ")

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    pw_hash= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # *************************
    # Connect an instance of UserManager to our User model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UserManager()
    # *************************


class SecretManager(models.Manager):
    def create_post(self, secret_details):
        print('create a secret here')
        print(secret_details['content'], 'postdata made it to the model manager')
        errors= []
        if len(secret_details['content']) < 10:
            errors.append('Secret need to have atleast 10 caracters')
        if not secret_details['content']:
            errors.append('secret cannot be blanc')
        if errors:
            print(errors, "?are there errors")
            return {"errors": errors}
        if len(errors) == 0:
            secret = Post.objects.create(content=secret_details['content'], creator= User.objects.get(id= secret_details['user_id']))
            return {"thesecret": secret}

    def create_like(self, like_details):
        if 'liked_post' in like_details:
            try:   
                post = Post.objects.get(id=like_details['liked_post'])
            except Post.DoesNotExist:
                return {'errors': "the post you try tol like does not exist"}
                print("error with post id" )
            else:
                print('found post looking for liker auto_now')
                if 'liker' in like_details:  
                    try:
                        liker = User.objects.get(id=like_details['liker'])
                    except User.DoesNotExist:
                        return {'errors': "the post you try tol like does not exist"}
                        print("error with post id" )
                    else:
                        user_likes = User.objects.filter(likes= post, id= like_details['liker'])
                        if len(user_likes) != 0:
                            return {"errors": "You can only like this secret ones"}
                        else:
                            print( post, liker , "alright just add them")
                            post.like.add(liker)
                            return {"success": " You succesful liked this"}

    def delete_like(selt, unlike_details):
        if 'liked_post' in unlike_details:
            try:   
                post = Post.objects.get(id=unlike_details['liked_post'])
            except Post.DoesNotExist:
                return {'errors': "the post you try to unlike does not exist"}
                print("error with post id" )
            else:
                print('found post looking for liker auto_now')
                if 'liker' in unlike_details:  
                    try:
                        liker = User.objects.get(id=unlike_details['liker'])
                    except User.DoesNotExist:
                        return {'errors': "you are not the user to unlike"}
                        print("error with unliker id" )
                    else:
                        user_likes = User.objects.filter(likes= post, id= unlike_details['liker'])
                        if len(user_likes) <= 0:
                            return {"errors": "You can not unlike this secret anymore"}
                        else:
                            print( post, liker , "alright just delete them")
                            post.like.remove(liker)
                            return {"success": " You succesful unliked this"}

class Post(models.Model):
    content = models.TextField(max_length=1000)
    creator = models.ForeignKey(User)
    like = models.ManyToManyField(User, related_name='likes')
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at= models.DateTimeField(auto_now =True)
    
    objects = SecretManager()




