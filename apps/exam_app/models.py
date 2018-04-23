from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import re
import bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, first_name, last_name, username, email, password, confirm):
        errors = []
        if len(first_name) < 3:
            errors.append("First name must be 3 characters or more")
        if len(last_name) < 3:
            errors.append("Last name must be 3 characters or more")
        if len(username) < 3:
            errors.append("Username must be 3 characters or more")
        else:
            userMatchingUsername = User.objects.filter(username=username)
            if len(userMatchingUsername) > 0:
                errors.append("Username already in use")
        if len(email) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            userMatchingEmail = User.objects.filter(email=email)
            if len(userMatchingEmail) > 0:
                errors.append("Email already in use")
        if len(password) < 1:
                errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")
        if len(confirm) < 1:
            errors.append("Confirm Password is required")
        elif password != confirm:
            errors.append("Confirm Password must match Password")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
        else:
            response["user"] = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email.lower(),
                password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            )
        return response

    def login(self, username, password):
        errors = []
        if len(username) < 1:
            errors.append("Username is required")
        else:
            userMatchingUsername = User.objects.filter(username=username)
            if len(userMatchingUsername) == 0:
                errors.append("Unknown Username")

        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) == 0:
            if bcrypt.checkpw(password.encode('utf-8'), userMatchingUsername[0].password.encode()):
                response["user"] = userMatchingUsername[0]
            else:
                errors.append("Incorrect password")

        if len(errors) > 0:
            response["errors"] = errors
            response["valid"] = False

        return response
        

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    def __repr__(self):
        return "User Object({}) {} {}>".format(self.id, self.first_name, self.last_name)
# Create your models here.

class TripManager(models.Manager):
    def add_trip(self, destination, start, end, plan, user_id):
        errors = []
        if len(destination)<1:
            errors.append("Destination must be provided.")
        if len(plan)<1:
            errors.append("Description must be provided.")
        if len(start)<1:
            errors.append("Travel from date required")
        else:
            st = datetime.strptime(start, "%Y-%m-%d")
            print (st)
            if st < datetime.now():
                errors.append("Travel from date must be in the future")
        if len(end)<1:
            errors.append("Travel to date required")
        else:
            st = datetime.strptime(start, "%Y-%m-%d")
            et = datetime.strptime(end, "%Y-%m-%d")
            print (et)
            if et < st:
                errors.append("Travel to date cannot be before Travel from date.")
        
        response = {
            "errors": errors,
            "valid": True,
            "user": None
        }
        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
       
        else:
            response["user"] = Trip.objects.create(
                destination=destination,
                start=start,
                end=end,
                plan=plan,
                planner_id=user_id,
            ).joined_by.add(User.objects.get(id=user_id))
            return {"valid":True, "errors":errors}
        return response
    def join_trip(self, user_id, id):
        response = {
            "valid": True,
        }
        Trip.objects.get(id=id).joined_by.add(User.objects.get(id=user_id))
        return response

class Trip(models.Model):
    destination=models.CharField(max_length=255)
    start=models.DateField()
    end=models.DateField()
    plan=models.TextField()
    planner=models.ForeignKey(User, on_delete=models.CASCADE, related_name="planned")
    joined_by=models.ManyToManyField(User, related_name="joined_trip")
    objects=TripManager()
    def __repr__(self):
        return "Trip Object({}) {} {}>".format(self.id, self.destination, self.plan)