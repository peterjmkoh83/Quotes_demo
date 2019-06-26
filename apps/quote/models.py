from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class UserManager(models.Manager):
   def basic_validator(self, postData):
      errors = {}
      if len(postData['first_name']) < 2:
         errors['first_name'] = "First name should be at least 2 characters"
      if len(postData['last_name']) < 2:
         errors['last_name'] = "Last name should be at least 2 characters"
      if not EMAIL_REGEX.match(postData['email']):
         errors['email'] = "Invalid email"
      if len(postData['password']) < 8:
         errors['password'] = "Password needs to be more than 8 characters"
      if postData['password'] != postData['confirm_password']:
         errors['password'] = "Passwords do not match!"
      return errors
     
   def login_validator(self, postData):
      errors = {}
      
      if not EMAIL_REGEX.match(postData['email']):
         errors['wrong_email_format'] = "Please enter correct email format"
      
      user = User.objects.filter(email=postData['email'])
      if not user:
         errors['email_not_found'] = "Please check your email again"
         return errors
      
      if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
         errors['password'] = "You have enetered wrong password"
      return errors 
   
   def quote_validator(self, postData):
      errors = {}
      if len(postData['quoted_by']) < 3:
         errors['quoted_by'] = "Quoted By needs to be at least 3 characters"
      if len(postData['message']) < 10:
         errors['message'] = "Message must be at least 10 characters"
      return errors

class User(models.Model):
   first_name = models.CharField(max_length=255)
   last_name = models.CharField(max_length=255)
   email = models.CharField(max_length=255)
   password = models.CharField(max_length=255)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   objects = UserManager()

class Quote(models.Model):
   quoted_by = models.CharField(max_length=255)
   message = models.CharField(max_length=255)
   uploaded_by = models.ForeignKey(User, related_name="uploaded_quote")
   liked_by = models.ManyToManyField(User, related_name="favorite_quote")
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
