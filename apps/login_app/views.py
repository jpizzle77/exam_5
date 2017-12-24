from django.shortcuts import render, HttpResponse, redirect
from models import User
from django.contrib import messages
from .. wish_list_app.models import Wish


def index(request):
	print "--------inside INDEX route----------"
	
	return render(request, 'login_app/index.html')


def register(request, methods='POST'):
	print '------------------------      IN REGISTER ROUTE  (POST)                                ---------------'
	print '*'*50
	print request.POST['birthday']," <---heres the birthday input"
	print type(request.POST['birthday'])
	if request.method == 'GET':
		return redirect('login_app:index')
		
	else:
		response = User.objects.check_create(request,request.POST)
		# response will return a list [] that will contain either a False and the errors, or a True statement with the new user that is created
		# response = [False, errors] or [True, new_user]

		print response, '<----------here is the response'
		if response[0]== False:
			for message in response[1]: #saying  for message in errors:
				print "joe mamma"
				messages.error(request, message[1])
			return redirect('login_app:index')
		else:
			request.session['message'] = "Successfully Registered!"
			request.session['user']= {
			"id": response[1].id,
			'name': response[1].name,
			'alias': response[1].alias,
			}
			print request.session['user']
			print request.method
			return redirect('wish_list_app:index')

	




def login(request, methods='POST'):
	print '------------------------      IN LOGIN ROUTE    (POST)                              ---------------'
	print '*'*50

	if request.method == 'POST':
		print request.POST, "<-------------------------- here is what is being posted"
		response = User.objects.check_password(request,request.POST)

		print response, '<----------here is the response'
		
		if response[0]== False:
			for message in response[1]:
				print "joe mamma"
				messages.error(request, message[1])
				return redirect('login_app:index')
		else:
			print response[0]
			print response[1]
			
			request.session['message'] = "Successfully Logged In!"
			print request.session['message'] 

			
			request.session['user']= {
	
				'name': response[1].name,
				'alias': response[1].alias,
				'id': response[1].id,
				'email': response[1].email
				}
			
			print request.session['user'], "<<<<------------request.session['user']----------->>>"
			return redirect('wish_list_app:index')
	else:

		return redirect('login_app:index')


'''def show_user(request, number):

	print "--------inside SHOW TRIP route----------"

	
	user=User.objects.get(id=number)

	print user.id, "heres the asshole userr"

	context= {

		'user':user
	}

	
	return render(request, 'login_app/show_user.html', context)

def delete(request,number):
	#render delete webpage, and grabs the id that will be deleted via the context dictionary
	print number, "<----here is the user ID/number to be deleted---------------"
	print request

	print "time to delete  this dipshit!!!!!!!!!!!!!!!!!!!"

	request.session['number']= number

	context= {

		'friend': User.objects.get(id=number)
	
	}

	print context, "heres the friend"
	
	return render(request, 'login_app/delete.html', context)

	

def confirm_delete(request,number, methods='POST'):
	# uses the delete_info() method to delete user
	print "< ------------------this is where we confirm the delete----------------"
	print request.POST["friend_id"], "<--------------the appointment id"

	#Appointment.objects.delete_appointment(request,request.POST)

	response = Friend.objects.delete_friend(request,request.POST)

	return redirect('friends_app:index')'''




