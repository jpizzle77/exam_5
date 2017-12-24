from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from ..login_app.models import User
import datetime
from time import time, gmtime, strftime, strptime
import pytz
import time



class WishManager(models.Manager):
	

	def join_wish(self,request,data):
		print "MODELS..............................join_wish()"
		print data, "Data ............"

		#grabbing the signed in user that will be adding to their wishlist (or create in the add_wish())
		user= User.objects.get(id=request.session['user']['id'])
		print user.id, "The user that will be adding to his/her wishlist"

		#this finds the wish that is being selected. Request.session['number'] idenities the wish ID
		item=Wish.objects.get(id=request.session['number'])

		#this is where we add the user_id and wishes_id to the intermediate table. Since the user is joining and not creating, we set
		# wish_maker = False
		x= Wish_maker(user=user, wishes= item, wish_maker=False)
		x.save()
		
		return [True, x]



	def delete(self,request,data):
		print "MODELS...................................delete wish-list item"
		
		#this finds the wish that is being selected. Request.session['number'] idenities the wish ID
		item= Wish.objects.get(id=request.session['number'])
		item.delete()

		return request


	def remove(self,request,data):
		print "MODELS...................................remove wish-list item"
		print request.session['number']
		print data

		#grabbing the signed in user that will be removing an item from their wishlist)
		user= User.objects.get(id=request.session['user']['id'])
	
		#this finds the wish that is being selected. Request.session['number'] idenities the wish ID
		wish = Wish.objects.get(id= request.session['number'] )

		#grabbing just the instance to be removed. Not the whole object in DB
		wish_maker= Wish_maker.objects.get(user=user, wishes=wish)
		wish_maker.delete()

		return request

class Wish_plannerManager(models.Manager):
	def add_wish(self,request,data):
		print "MODELS..........................add wish"

		errors=[]
		# checking to make sure something is inputted. min 3 characters
		if len(data['wish']) < 3:
			errors.append([request,"Entry must be at least 3 characters long."])
			return [False, errors]

		else:
			#grabbing the signed in user that will be creating an item for their wishlist)
			user= User.objects.get(id=request.session['user']['id'])

			#creating an wish instance. Storng values for data['wish']  and request.session['user']['name'] 
			item = Wish(item= data['wish'], added_by= request.session['user']['name'])
			
			item.save()
		 
		 	#storing instance info (user_id,wishes_id, wish_maker) onto intermediate table
		 	x= Wish_maker(user=user, wishes= item, wish_maker=data['wish_maker'])
			x.save()
			return [True, errors]
		return request



class Wish(models.Model):
	item = models.CharField(max_length=255)
	added_by = models.CharField(max_length=255)
	users = models.ManyToManyField(User,  related_name="wishes", through="Wish_maker") #use through to add another field into intermediate table
	start_date = models.DateField(['%b-%d-%Y'], null=True)
	created_at = models.DateField(['%b-%d-%Y'],auto_now_add = True, null=True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = WishManager()

	

	def __repr__(self):
		return "<ID: {}-Item: {}- Aded by:{}- Users{}-  >".format(self.id, self.item, self.added_by, self.users)


#this is the intermediate model. I added an extra field called "wish_make" using through above. This will allow me to separate the users who create
#items/wishes vs the users that join an item/wishlist
class Wish_maker(models.Model):
    user = models.ForeignKey(User)
    wishes = models.ForeignKey(Wish)
    wish_maker = models.BooleanField(default=False)
   
    objects = Wish_plannerManager()

    def __repr__(self):
		return "<User Id: {}- Wish Id:{}- Wish Maker:{}- >".format(self.user, self.wishes, self.wish_maker)
