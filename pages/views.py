from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from userprofiles.models import UserProfiles
from django.core.mail import send_mail

# Create your views here.
def login_view(request,*args,**kwargs):
	context={
		"error_message":"none"
	}
	if request.method=="POST":
		user_email=request.POST.get('emailid')
		user_password=request.POST.get('password')
		get_user_details=UserProfiles.objects.filter(emailid=user_email, password=user_password)
		if len(get_user_details)!=0:
			get_user_details=UserProfiles.objects.get(emailid=user_email, password=user_password)
			# send_mail(
			#     subject = "Login Successfull",
			#     message = "You have logged in successfully",
			#     from_email = "noreply@auctionsystem.com",
			#     recipient_list = ["saikrishnametpalli@gmail.com",],
			# )
			return HttpResponseRedirect(reverse('home-view', kwargs={"userid": get_user_details.userid}))
		else:
			context={
				"error_message":"block"
			}
	return render(request,"login.html",context)


def home_view(request,userid):
	print(userid)
	return render(request,"home.html",{})

def register_view(request,*args,**kwargs):

	return render(request,"registeruser.html",{})