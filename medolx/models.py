from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField
from django.db.models import IntegerField
from datetime import datetime



departments=[
('Endocrine Disorders','Endocrine Disorders'),
('Dermatologists','Dermatologists'),
('Gyneology and Obstetrics','Gyneology and Obstetrics'),
('Pain Management','Pain Management'),
('Dietitian & Nutritionist','Dietitian & Nutritionist'),
('General Physician','General Physician'),
('Sexual Discorders','Sexual Discorders'),
('Lifestyle Disorders','Lifestyle Disorders'),
('Ear Nose Throat Specialist','Ear Nose Throat Specialist'),
('PANCHKARMA SPECIALIST','PANCHKARMA SPECIALIST'),
('SKIN & COSMETOLOGIST','SKIN & COSMETOLOGIST'),
('HAIR CARE & TRICHOLOGY','HAIR CARE & TRICHOLOGY'),
('PSYCOLOGIST','PSYCOLOGIST'),
('PAEDIATRIC','PAEDIATRIC'),
('DIABITIS SPACIAlist','DIABITIS SPACIAlist'),
('Covid Care','Covid Care'),
]


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=35)
    phone_no = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=40)
    qualification = CharField(max_length=25)
    hospital_name = models.CharField(max_length=50)
    gender = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=gender)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    experience = CharField(max_length=5)
    consultation_fee = CharField(max_length=5)
    profile_pic= models.ImageField(upload_to='static/profile_pic/DoctorProfilePic/',null=True,blank=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return "Dr. " + self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)




class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, default=None)
    email=models.CharField(max_length=30)
    phone_no = models.CharField(max_length=10, unique=True)
    gender = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=gender)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.username



# class Schedule(models.Model):
#     doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     open=models.TimeField()
#     close=models.TimeField()

class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patient_name = models.CharField(max_length=40, null=True)
    doctor_name = models.CharField(max_length=40, null=True)
    email = models.CharField(max_length=40, null=True)
    phone_no = models.CharField(max_length=10, null=False)
    whatsapp_no = models.CharField(max_length=10, null=True)
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=7, choices=gender)
    city = models.CharField(max_length=40, null=False)
    problems = models.CharField(max_length=200, null=False)
    consultation_mode = (
        ('Audio', 'Audio'),
        ('Video', 'Video'),
        ('Chat', 'Chat'),
    )
    consultation_mode = models.CharField(max_length=7, choices=consultation_mode, null=False)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    tracker = (
        ('Consult', 'Consult'),
        ('Follow_Up', 'Follow Up'),
        ('Complete', 'Complete')
    )
    tracker = models.CharField(max_length=12, choices=tracker, default='Consult')
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.patient_name



class Product(models.Model):
    name = models.CharField(max_length=40)
    profile_pic= models.ImageField(upload_to='static/profile_pic/ProductProfilePic/',null=True,blank=True)
    used_for = models.CharField(max_length=40)
    price = models.IntegerField()
    discount = models.IntegerField()

    def __str__(self):
        return self.name




class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 




class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total



class ShippingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address





class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    desc = models.CharField(max_length=300)
    featured_pic= models.ImageField(upload_to='static/blog_pic/BlogFeaturedPic/',null=True,blank=True)
    content = models.TextField()
    author = models.CharField(max_length=20)
    author_pic= models.ImageField(upload_to='static/blog_pic/BlogAuthorPic/',null=True,blank=True)
    
    def __str__(self):
        return self.title



class Contact(models.Model):
    fname = models.CharField(max_length=10, blank = False, null = False)
    lname = models.CharField(max_length=20, blank = False, null = False)
    email = models.CharField(max_length=35, blank = False, null = False)
    message = models.TextField(blank = False, null = False)

    def __str__(self):
        return self.email


# Chat App Start 


class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)