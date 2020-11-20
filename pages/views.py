from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from userprofiles.models import UserProfiles
from django.core.mail import send_mail
from products.models import Product
from .forms import ProductForm
from django.core.paginator import Paginator
import datetime

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
			request.session['userid'] = get_user_details.userid
			request.session['isadmin'] = get_user_details.isadmin
			return HttpResponseRedirect(reverse('home-view', kwargs={"userid": get_user_details.userid}))
		else:
			context={
				"error_message":"Invalid Email/Password"
			}
	return render(request,"login.html",context)


def home_view(request,*args,**kwargs):
	#print(kwargs["userid"])
	
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


def upload_product_view(request,*args,**kwargs):
	print('offer item ',kwargs)
	form = ProductForm()
	if request.method == 'POST':
		form = ProductForm(request.POST or None,request.FILES)
		if form.is_valid():
			print('session userid ',request.session['userid'])
			form = form.save(commit=False)
			form.userid = request.session['userid']
			form.save()
			form = ProductForm()
			return HttpResponseRedirect(reverse('home-view'))

	context = {
		'form':form
	}
	return render(request,"uploadproduct.html",context)


def products_list_view(request, *args, **kwargs):
	all_products = Product.objects.all()
	print('pg no ',request.GET.get('page'))
	if request.GET.get('page') == None:
		page_number = 1
	else:
		page_number = request.GET.get('page')

	if request.GET.get('productid') != None:
		product_id = request.GET.get('productid')
		print('productid',product_id)
		return HttpResponseRedirect(reverse('product-view',kwargs={"productid": product_id}))

	paginator = Paginator(all_products, 8) # 8 items per page
	products = paginator.page(page_number)
	return render(request, 'viewlistings.html', {'products': products})

def product_view(request, *args, **kwargs):
	context = {}
	if len(kwargs) != 0 :
		print(kwargs)
		product=Product.objects.get(productid=kwargs["productid"])
		print(request.session['isadmin'] )
		if product.endtime :
			bidtime = product.endtime
			bidtime  = str(bidtime)[:-6]
		else:
			bidtime = datetime.datetime.now()

		print('bidtime',bidtime)
		context={
			"productid" : kwargs["productid"],
			"product" : product,
			"isadmin" : request.session['isadmin'], 
			#"bidtime" : "Nov 17, 2020 15:45:25"
			#"bidtime" : "2020-11-17 15:47:17.012056"
			"bidtime" : bidtime
		}
	print(request.POST.get('Option'))

	if request.POST.get('Option') != None :
		product=Product.objects.get(productid=request.POST.get("productid"))
		context ={
		"productid" : request.POST.get("productid"),
		"product" : product,
		"isadmin" : request.session['isadmin'],
		}

		if request.POST.get('Option') == 'start_bidding' :	
			product.endtime = datetime.datetime.now()+datetime.timedelta(minutes = 5)
			product.save()
			context["bidtime"] = product.endtime

		if request.POST.get('Option') == 'bid' :
			bid_price = request.POST.get("bid_price")
			product.highestbid = bid_price
			product.highestbid_userid = request.session['userid']
			product.save()
			context["bidtime"] = str(product.endtime)[:-6]

        

	return render(request, 'viewproduct.html',context)
