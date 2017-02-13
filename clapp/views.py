from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Gig, Profile, Purchase, Review
from .forms import *
from twilio.rest import TwilioRestClient
from sixerr.sms import send_sms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for registration
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

# for email
from django.core.mail import send_mail








import braintree
braintree.Configuration.configure(braintree.Environment.Sandbox,
									merchant_id="7f36yb4sb7v7x3vk",
									public_key="j9fxrnkcc7xtfb86",
									private_key="9f39d9bba752162ea348002871a3f16c"
)

# Create your views here.

class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail


def send_email(subject, user):
	
	message = "Dear %s, \nThanks for your registration ~ Now you can start to make your business! Enjoy !" % (user.username,)
	from_email = settings.DEFAULT_FROM_EMAIL
	to_email = [settings.EMAIL_HOST_USER, user.email]

	send_mail(subject, 
				message, 
				from_email, 
				to_email, 
				fail_silently=False)




@csrf_protect
def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
			username=form.cleaned_data['username'],
			password=form.cleaned_data['password1'],
			email=form.cleaned_data['email']
			)
			profile = Profile(user_id=user.id)
			profile.email = user.email
			profile.save()

			### email test
			subject = 'Welcome to Sixerr Super GIG!'
			# message = 'just test'
			# from_email = settings.EMAIL_HOST_USER
			# to_email = [settings.EMAIL_HOST_USER]

			send_email(subject, user)
			
			# send_mail(subject, 
			# 		message, 
			# 		from_email, 
			# 		to_email, 
			# 		fail_silently=False)
			### end of email test

			return HttpResponseRedirect('/register/success/')
		# else:
		# 	return redirect('/')
	else:
		form = RegistrationForm()

	variables = RequestContext(request, {'form': form})

	return render_to_response('registration/register.html', variables,)
	# return render_to_response('registration/register.html', {'form': form},)
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
# def logout_page(request):
#     logout(request)
#     return HttpResponseRedirect('/')



# Create user profile after receiving activation signal
from registration.signals import user_registered
 
def user_registered_profile(sender, user, request, **kwargs):
	profile = Profile(user_id=user.id)
	profile.email = user.email
	profile.save()
 
user_registered.connect(user_registered_profile)






def home(request):
	
	gigs = Gig.objects.filter(status=True).order_by('create_time')
	return render(request, 'home.html', {"gigs": gigs})

	# gig_list = Gig.objects.filter(status=True)
	# page = request.GET.get('page', 1)
	# paginator = Paginator(gig_list, 20)
	# try:
	# 	gigs = paginator.page(page)
	# except PageNotAnInteger:
	# 	gigs = paginator.page(1)
	# except EmptyPage:
	# 	gigs = paginator.page(paginator.num_pages)
	# return render(request, 'home.html', {"gigs": gigs})


# def home_all(request):
# 	gigs = Gig.objects.filter(status=True)
# 	return render(request, 'home.html', {"gigs": gigs})

def gig_detail(request, id):
	if request.method == 'POST' and \
		not request.user.is_anonymous() and \
		Purchase.objects.filter(gig_id=id, buyer=request.user).count() > 0 and \
		'content' in request.POST and \
		request.POST['content'].strip() != '':
		Review.objects.create(content=request.POST['content'], gig_id=id, user=request.user)

	try:
		gig = Gig.objects.get(id=id)
	except Gig.DoesNotExist:
		return redirect('/')

	if request.user.is_anonymous() or \
		Purchase.objects.filter(gig=gig, buyer=request.user).count() == 0 or \
		Review.objects.filter(gig=gig, user=request.user).count() > 0:
		show_post_review = False
	else:
		show_post_review = Purchase.objects.filter(gig=gig, buyer=request.user).count() > 0

	reviews = Review.objects.filter(gig=gig)
	client_token = braintree.ClientToken.generate()
	return render(request, 'gig_detail.html', {"show_post_review": show_post_review, "reviews": reviews, "gig": gig, "client_token": client_token})

@login_required(login_url="/")
def create_gig(request):
	error = ''
	if request.method == 'POST':
		gig_form = GigForm(request.POST, request.FILES)
		if gig_form.is_valid():
			gig = gig_form.save(commit=False)
			gig.user = request.user
			gig.save()
			return redirect('my_gigs')
		else:
			error = "Data is not valid"
	# gig_form = GigForm()
	return render(request, 'create_gig.html', {
		"error": error})

@login_required(login_url="/")
def edit_gig(request, id):
	try:
		gig = Gig.objects.get(id=id, user=request.user)
		error = ''
		if request.method == 'POST':
			gig_form = GigForm(request.POST, request.FILES, instance=gig)
			if gig_form.is_valid():
				gig.save()
				return redirect('my_gigs')
			else:
				error = "Data is not valid"
		return render(request, 'edit_gig.html', {"gig": gig, "error": error})
	except Gig.DoesNotExist:
		return redirect('/')


@login_required(login_url="/")
def my_gigs(request):
	gigs = Gig.objects.filter(user=request.user).order_by('create_time')
	return render(request, 'my_gigs.html', {"gigs": gigs})


def profile(request, username):
	if request.method == 'POST':
		profile = Profile.objects.get(user=request.user)
		profile.about = request.POST['about']
		profile.slogan = request.POST['slogan']
		profile.email = request.POST['email']
		profile.phone = request.POST['phone']
		profile.save()
	else:
		try:
			profile = Profile.objects.get(user__username=username)
		except Profile.DoesNotExist:
			return redirect('/')

	gigs = Gig.objects.filter(user=profile.user, status=True).order_by('create_time')
	return render(request, 'profile.html', {"profile": profile, "gigs": gigs})
	# gig_list = Gig.objects.filter(user=profile.user, status=True)
	# page = request.GET.get('page', 1)
	# paginator = Paginator(gig_list, 20)
	# try:
	# 	gigs = paginator.page(page)
	# except PageNotAnInteger:
	# 	gigs = paginator.page(1)
	# except EmptyPage:
	# 	gigs = paginator.page(paginator.num_pages)
	# return render(request, 'profile.html', {"profile": profile, "gigs": gigs})

@login_required(login_url="/")
def create_purchase(request):
	if request.method == 'POST':
		try:
			gig = Gig.objects.get(id = request.POST['gig_id'])
		except Gig.DoesNotExist:
			return redirect('/')

		nonce = request.POST["payment_method_nonce"]
		result = braintree.Transaction.sale({
				"amount": gig.price,
				"payment_method_nonce": nonce	
			})
		
		if gig.price == 0:

			Purchase.objects.create(gig=gig, buyer=request.user)
			#get seller phone # if exist
			seller_num = gig.phone
			if seller_num:
				message = 'Hi ' + gig.user.username + ': Your gig "' + gig.title + '" just sold to ' + request.user.username + ' at ' + str(timezone.localtime(timezone.now()))
				response = send_sms(seller_num, message)


			buyer_profile = Profile.objects.get(user=request.user)
			#get buyer phone # if exist
			buyer_num = buyer_profile.phone
			if buyer_num:
				message = 'Hello ' + request.user.username + ': You just bought the gig "' + gig.title + '" from ' + gig.user.username + ' Thank you !'
				response = send_sms(buyer_num, message)


		if result.is_success:

			Purchase.objects.create(gig=gig, buyer=request.user)
			#get seller phone # if exist
			seller_num = gig.phone
			if seller_num:
				message = 'Hi ' + gig.user.username + ': Your gig "' + gig.title + '" just sold to ' + request.user.username + ' at ' + str(timezone.localtime(timezone.now()))
				response = send_sms(seller_num, message)


			buyer_profile = Profile.objects.get(user=request.user)
			#get buyer phone # if exist
			buyer_num = buyer_profile.phone
			if buyer_num:
				message = 'Hello ' + request.user.username + ': You just bought the gig "' + gig.title + '" from ' + gig.user.username + ' Thank you !'
				response = send_sms(buyer_num, message)

	return redirect('/')


@login_required(login_url="/")
def my_sellings(request):
	purchases = Purchase.objects.filter(gig__user=request.user).order_by('time')
	return render(request, 'my_sellings.html', {"purchases": purchases})


@login_required(login_url="/")
def my_buyings(request):
	purchases = Purchase.objects.filter(buyer=request.user).order_by('time')
	return render(request, 'my_buyings.html', {"purchases": purchases})


def category(request, link):
	categories = {
		"graphics-design": "GD",
		"digital-marketing": "DM",
		"video-animation": "VA",
		"music-audio": "MA",
		"programming-tech": "PT"
	}

	if link == "all":
		try:
			gigs = Gig.objects.filter(status=True).order_by('create_time')
			return render(request, 'home.html', {"gigs": gigs, "show_all": "True"})

		except KeyError:
			return redirect('home')

	else:	
		try:
			gigs = Gig.objects.filter(category=categories[link]).order_by('create_time')
			return render(request, 'home.html', {"gigs": gigs})
			# gig_list = Gig.objects.filter(category=categories[link])
			# page = request.GET.get('page', 1)
			# paginator = Paginator(gig_list, 20)
			# try:
			# 	gigs = paginator.page(page)
			# except PageNotAnInteger:
			# 	gigs = paginator.page(1)
			# except EmptyPage:
			# 	gigs = paginator.page(paginator.num_pages)
			# return render(request, 'home.html', {"gigs": gigs})

		except KeyError:
			return redirect('home')

def search(request):
	gigs = Gig.objects.filter(title__icontains=request.GET['title']).order_by('create_time')
	return render(request, 'home.html', {"gigs": gigs})

