from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from userprofiles.models import UserProfiles
from django.core.mail import send_mail

# Create your views here.
def login_view(request,*args,**kwargs):
	context={
		"error_message":""
	}
	if request.method=="POST":
		user_email=request.POST.get('emailid')
		user_password=request.POST.get('password')
		get_user_details=UserProfiles.objects.filter(emailid=user_email, password=user_password)
		if len(get_user_details)!=0:
			get_user_details=UserProfiles.objects.get(emailid=user_email, password=user_password)
			
			return HttpResponseRedirect(reverse('home-view', kwargs={"userid": get_user_details.userid}))
		else:
			context={
				"error_message":"Invalid Email/Password"
			}
	return render(request,"login.html",context)


def home_view(request,userid):
	print(userid)
	return render(request,"home.html",{})

def register_view(request,*args,**kwargs):
	context={
		"error_message":""
	}
	if request.method=="POST":
		user_firstname=request.POST.get('firstname')
		user_lastname=request.POST.get('lastname')
		user_email=request.POST.get('emailid')
		user_password=request.POST.get('password')
		get_user_details=UserProfiles.objects.filter(emailid=user_email)
		if len(get_user_details)==0:
			UserProfiles.objects.create(firstname=user_firstname,lastname=user_lastname,emailid=user_email, password=user_password)
			send_mail(
			    subject = "Registered successfully",
			    message = "You have successfully registered for Online Auction System",
			    from_email = "noreply@onlineauctionsystem.com",
			    recipient_list = [user_email,],
			)
			context={
				"error_message":"Registered successfully"
			}
		else:
			context={
				"error_message":"Email id already exists"
			}
	
	return render(request,"registeruser.html",context)