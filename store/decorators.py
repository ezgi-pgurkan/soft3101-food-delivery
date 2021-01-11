from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_customer==True:
				return redirect('home')
			if request.user.is_admin==True:
				return redirect('adminpage')
			if request.user.is_restaurant==True:
				return redirect('restOwner')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

#who can view this page - filtered by roles
def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		return wrapper_func
	return decorator

#only customer should be able to order so if not customer, redirect to another page
def canorder(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return redirect('cannotorder')
		return wrapper_func
	return decorator