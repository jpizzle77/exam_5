from django.shortcuts import render, HttpResponse, redirect
from models import Wish, Wish_maker
from django.contrib import messages
from .. login_app.models import User
import datetime




def index(request):
	print "------##############  inside TRIP APP INDEX route ##################----------"
	print request.session['user']['id'],"<------------------here's the user_id"
	
	# this will give me anyone who created a wish_list
	wish_makers = Wish_maker.objects.filter(wish_maker=True)
	
	'''for wm in wish_makers:
		#wm= wm.values('name','alias')
		#print wm.id
		print wm.wishes.id,
		print wm.wishes.item, 
		
		print wm.user.name, "person who created the item for the wish-list"'''
		
	
	current_user= User.objects.get(id=request.session['user']['id'])  #give me the current user
	
	user_items= current_user.wishes.all()
	
	user_items=user_items.values('id','item', 'added_by', 'created_at')
	

	'''print user_items
	print type(user_items)
	for item in user_items:
		print item['item']
		print item['id']
		print item['added_by']'''
	

	z = user_items.values('id') 						# create a list of dictionaries of just the ID's for the objects
	# e.g  z=[{'id'}: 49, {'id'}: 52,{'id'}: 55,{'id'}: 60]

	non_user_items= Wish.objects.exclude(id__in=z) 		#grabbing all wish instances except for the signed in users wishes
	non_user_items= non_user_items.values('id','item', 'added_by', 'created_at')
	
	


	context= {

		"current_user":current_user, 		# -current user that is signed in

		"user_items":user_items, 			# -all the items the current user created
		"non_user_items":non_user_items, 	# -all the items the current user did not create
		
		
		"wish_makers":wish_makers,          # -all the users that have created a wish_list
		

	}

	

	return render(request, 'wish_list_app/index.html', context)




def create_wish(request):
	print "VIEWS...........................................   create a wish"
	#creates HTML page that lets you create an ITEM/wish for your wishlist
	return render(request, 'wish_list_app/create_wish.html')


def add_wish(request, methods='POST'):

	print "VIEWS.....................................where the wish is posted"
	print request.session['user']['id'],"<------------------here's the user_id"
	print request.POST['start_date'] , "here is the date the person adds onto someone else's wishlist"


	response = Wish_maker.objects.add_wish(request,request.POST)

	if response[0]== False:
		for message in response[1]: #saying  for message in errors:
			print "errors on the add wish form"
			messages.error(request, message[1])
		return redirect('wish_list_app:create_wish')

	else:
		print response[0]
		print response[1]
		return redirect('wish_list_app:index')


def join_wish(request, number, methods='POST'):

	print "VIEWS...........................................add to wishlist"

	# number is the wish.id   Setting it in request.session allows me to use it elseware
	request.session['number']= number

	join_wish = Wish.objects.join_wish(request,request.POST)

	return redirect('wish_list_app:index')


def show_wish(request,number):
	print "VIEWS...........................................   show the wish list item"

	#grabs the wish instance using number for its id
	item=Wish.objects.get(id=number)

	#grabs all users that has created or joined on a wish_list
	users_who_wished= item.users.all()
	print users_who_wished

	context= {

		'item':item,
		"users_who_wished":users_who_wished
	}


	return render(request, 'wish_list_app/show_wish.html', context)


def remove(request,number):
	#render delete webpage, and grabs the id that will be deleted via the context dictionary
	print number, "<----here is the item ID/number to be deleted---------------"
	print request

	

	request.session['number']= number

	context= {

		'item': Wish.objects.get(id=number)
	
	}

	
	
	return render(request, 'wish_list_app/remove.html', context)

	

def confirm_remove(request,number, methods='POST'):
	# uses the delete_info() method to delete user
	print "< ------------------this is where we confirm the delete----------------"

	response = Wish.objects.remove(request,request.POST)

	return redirect('wish_list_app:index')



def delete(request,number):
	#render delete webpage, and grabs the id that will be deleted via the context dictionary
	print number, "<----here is the item ID/number to be deleted---------------"
	print request

	

	request.session['number']= number

	context= {

		'item': Wish.objects.get(id=number)
	
	}

	
	
	return render(request, 'wish_list_app/delete.html', context)

	

def confirm_delete(request,number, methods='POST'):
	# uses the delete_info() method to delete user
	print "< ------------------this is where we confirm the delete----------------"

	response = Wish.objects.delete(request,request.POST)

	return redirect('wish_list_app:index')


def clear(request):
	print '----------------            CLEARING THE SESSION         ---------------------'

	request.session.clear()

	return redirect('login_app:index')
