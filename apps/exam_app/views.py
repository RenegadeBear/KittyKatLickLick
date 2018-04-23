from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages

# Create your views here.
def index(req):
    return render(req, "exam_app/index.html")

def register(req):
    check = User.objects.register(
        req.POST["first_name"],
        req.POST["last_name"],
        req.POST["username"],
        req.POST["email"],
        req.POST["password"],
        req.POST["confirm"]
    )
    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(req, messages.ERROR, error)
        return redirect("/")
    else:
        req.session['user_id'] = check["user"].id
        messages.add_message(req, messages.SUCCESS, "Welcome to Exam App, {}".format(req.POST["username"]))
        return redirect("/travels")

def login(req):
    print (req.POST["username"])
    check = User.objects.login(
        req.POST["username"],
        req.POST["password"]
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(req, messages.ERROR, error)
        return redirect("/")
    else:
        req.session["user_id"] = check["user"].id
        req.session['status'] = "logged_in"
        # messages.add_message(req, messages.SUCCESS, "Welcome back, {}".format(check["user"].username))
        return redirect("/travels")

def travels(req):
    user = User.objects.get(id=req.session["user_id"])
    yourtrips = User.objects.get(id=req.session["user_id"]).joined_trip.all()
    othertrips = Trip.objects.all().exclude(joined_by=req.session["user_id"])
    data = {
        "user": user,
        "yourtrips": yourtrips,
        "othertrips": othertrips
    }
    return render(req, "exam_app/travels.html", data)

def join(req, id):
    print (req.POST)
    check=Trip.objects.join_trip(
        req.session["user_id"],
        id,   
    )
    return redirect('/travels')

def trip(req, id):
    trip=Trip.objects.get(id=id)
    planned_by=User.objects.get(planned=id).id
    joined_by=User.objects.filter(joined_trip=id).exclude(planned=planned_by)
    data = {
        "trip":trip,
        "joined_by":joined_by,
    }
    return render(req, "exam_app/trip.html", data)

def add(req):
    return render(req, "exam_app/add.html")

def add_trip(req):
    print (req.POST)
    check=Trip.objects.add_trip(
        req.POST["destination"],
        req.POST["start"],
        req.POST["end"],
        req.POST["plan"],
        req.session["user_id"],
        )
    print (check)
    if not check["valid"]:
        for error in check ["errors"]:
            messages.add_message(req, messages.ERROR, error)
            return redirect('/add')
    else:
        return redirect('/travels')

def logout(req):
    req.session.clear()
    return redirect('/')