# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
from time import strptime
from datetime import date, datetime

class userManager(models.Manager):
    def validate (self, postData):
        errors = []

        if len(postData['name']) <= 3:
            errors.append("Name needs to be more than 3 letter")

        if postData['name'].replace(' ','').isalpha() == False:
            errors.append("First name cannot contain numbers")

        if len(User.objects.filter(username = postData['username'])) > 0:
            errors.append("Username already exists")

        if postData['password'] != postData['confirm_password']:
            errors.append("Your passwords don't match")

        if len(postData['password']) < 8:
            errors.append("Password needs to be more than 8 letters")

        if len(errors) == 0:
            new_user = User.objects.create(name= postData['name'], username= postData['username'], password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, new_user)
        else:
            return (False, errors)

    def login(self, postData):
        errors = []
        if 'username' in postData and 'password' in postData:
            try:
                user = User.objects.get(username = postData['username'])
            except User.DoesNotExist:
                errors.append("Oh snap! Please try logging in again")
                return (False, errors)
        pw_match = bcrypt.hashpw(postData['password'].encode(), user.password.encode())
        if pw_match == user.password:
            return (True, user)
        else:
            errors1.append("Oh snap! Please try again")
            return (False, errors)

class travelManager(models.Manager):
    def travelvalidate(self, postData, id):
        errors=[]

        if len(postData['destination']) < 1 :
            errors.append("Destination field can not be empty")

        if len(postData['description']) < 1 :
            errors.append("Description field can not be empty")

        if str(date.today()) > str(postData['start']):
            errors.append("Start time can not be in the past.")

        if str(date.today()) > postData['end']:
            errors.append("End date must be in the future")

        if postData['start'] > postData['end']:
            errors.append("Travel Date From can not be in the future of Travel Date To")

        if len(errors) == 0:
            plan = Travel.objects.create(destination=postData['destination'], description=postData['description'], start=postData['start'], end=postData['end'], creator= User.objects.get(id=id))
            return (True, plan)
        else:
            return (False, errors)

    def join(self, id, travel_id):
        if len(Travel.objects.filter(id=travel_id).filter(join__id=id))>0:
            return {'errors':'You already Joined this'}
        else:
            joiner = User.objects.get(id=id)
            plan = self.get(id=travel_id)
            plan.join.add(joiner)
            return {}

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    objects = userManager()

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    start = models.DateField()
    end = models.DateField()
    creator = models.ForeignKey(User, related_name="planner")
    join = models.ManyToManyField(User, related_name="joiner")

    objects = travelManager()