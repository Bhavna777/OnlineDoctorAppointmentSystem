from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import JsonResponse
from .utils import cookieCart, cartData, guestOrder
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
import basehash


hash_fn = basehash.base36()

# Create your views here.


def index(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    blogs=models.Blog.objects.all().filter()
    doc_info = []
    for i in range(4):
        doc_info.append(doctors[i])

    blog_info = []
    for i in range(3):
        blog_info.append(blogs[i])
    return render(request, 'index.html',{'doctors':doctors, 'doc_info' : doc_info, 'blog_info' : blog_info})




def signup(request):       
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        
            messages.success(request, 'Your account has been created please login now')
            return HttpResponseRedirect('signin')

        else:
            messages.warning(request, 'Invalid Details, May be user already exist')
    return render(request,'signup.html',context=mydict)



def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


@user_passes_test(is_patient)
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'dashboard.html')



@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    # return render(request, 'admin_dashboard.html')
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    # appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    # pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    # 'appointmentcount':appointmentcount,
    # 'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'admin_dashboard.html',context=mydict)


@user_passes_test(lambda u: u.is_superuser)
def admin_doctor(request):
    return render(request, 'admin_doctor.html')


@user_passes_test(lambda u: u.is_superuser)
def admin_view_doctor(request):
    # return render(request, 'admin_view_doctor.html')
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor.html',{'doctors':doctors})


@user_passes_test(lambda u: u.is_superuser)
def admin_add_doctor(request):
    # return render(request, 'admin_add_doctor.html')
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin_view_doctor')
    return render(request,'admin_add_doctor.html',context=mydict)


@user_passes_test(lambda u: u.is_superuser)
def admin_update_doctor(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'doctor': doctor, 'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin_view_doctor')
    return render(request,'admin_update_doctor.html', context=mydict)

@user_passes_test(lambda u: u.is_superuser)
def admin_delete_doctor(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin_view_doctor')

@user_passes_test(lambda u: u.is_superuser)
def admin_patient(request):
    return render(request, 'admin_patient.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_view_patient(request):
    # return render(request, 'admin_view_patient.html')
    patients=models.Patient.objects.all().filter()
    return render(request,'admin_view_patient.html',{'patients':patients})
    print(patients)

@user_passes_test(lambda u: u.is_superuser)
def admin_add_patient(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            messages.success(request, 'Patient Added Successfully')
            return HttpResponseRedirect('admin_view_patient')
        else:
            messages.warning(request, 'Invalid Details, May be user already exist')

        
    return render(request,'admin_add_patient.html',context=mydict)


@user_passes_test(lambda u: u.is_superuser)
def admin_update_patient(request,pk):
    # return render(request, 'admin_update_patient.html')
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'patient': patient, 'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin_view_patient')
            return HttpResponseRedirect('admin_view_patient')
        else:
            messages.warning(request, 'Please Enter Valid Details')
    return render(request,'admin_update_patient.html',context=mydict)


@user_passes_test(lambda u: u.is_superuser)
def admin_delete_patient(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin_view_patient')



@user_passes_test(lambda u: u.is_superuser)
def admin_view_appointments(request):
    appointments=models.Appointment.objects.all().filter()
    return render(request, 'admin_view_appointments.html', {'appointments':appointments})

@user_passes_test(lambda u: u.is_superuser)
def admin_delete_appointment(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin_view_appointments')


@user_passes_test(lambda u: u.is_superuser)
def admin_view_appointment(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    return render(request,'admin_view_appointment.html', {'appointment':appointment})

@user_passes_test(lambda u: u.is_superuser)
def admin_update_appointment(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    return render(request,'admin_update_appointment.html', {'appointment':appointment})


@user_passes_test(lambda u: u.is_superuser)
def admin_view_product(request):
    # return render(request, 'admin_view_product.html')
    products=models.Product.objects.all().filter()
    return render(request,'admin_view_product.html',{'products':products})


@user_passes_test(lambda u: u.is_superuser)
def admin_add_product(request):
    productForm=forms.ProductForm()
    mydict={'productForm':productForm}
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            product=productForm.save()
            product.save()

            # my_product_group = Group.objects.get_or_create(name='PRODUCT')
            # my_product_group[0].user_set.add(name)

        return HttpResponseRedirect('admin_view_product')
    return render(request,'admin_add_product.html',context=mydict)

@user_passes_test(lambda u: u.is_superuser)
def admin_update_product(request,pk):
    product=models.Product.objects.get(id=pk)

    productForm=forms.ProductForm(request.FILES,instance=product)
    mydict={'product':product, 'productForm':productForm}
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            product=productForm.save()
            product.save()
            return redirect('admin_view_product')
    return render(request,'admin_update_product.html',context=mydict)


@user_passes_test(lambda u: u.is_superuser)
def admin_delete_product(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin_view_product')



@user_passes_test(lambda u: u.is_superuser)
def admin_view_blog(request):
    # return render(request, 'admin_view_product.html')
    blogs=models.Blog.objects.all().filter()
    return render(request,'admin_view_blog.html',{'blogs':blogs})

@user_passes_test(lambda u: u.is_superuser)
def admin_add_blog(request):
    blogForm=forms.BlogForm()
    mydict={'blogForm':blogForm}
    if request.method=='POST':
        blogForm=forms.BlogForm(request.POST, request.FILES)
        if blogForm.is_valid():
            blog=blogForm.save()
            blog.save()


        return HttpResponseRedirect('admin_view_blog')
    return render(request,'admin_add_blog.html',context=mydict)



@user_passes_test(lambda u: u.is_superuser)
def admin_update_blog(request,pk):
    blog=models.Blog.objects.get(id=pk)

    blogForm=forms.BlogForm(request.FILES,instance=blog)
    mydict={'blog':blog, 'blogForm':blogForm}
    if request.method=='POST':
        blogForm=forms.BlogForm(request.POST,request.FILES,instance=blog)
        if blogForm.is_valid():
            blog=blogForm.save()
            blog.save()
            return redirect('admin_view_blog')
    return render(request,'admin_update_blog.html',context=mydict)


@user_passes_test(lambda u: u.is_superuser)
def admin_delete_blog(request,pk):
    blog=models.Blog.objects.get(id=pk)
    blog.delete()
    return redirect('admin_view_blog')


@user_passes_test(lambda u: u.is_superuser)
def admin_view_message(request):
    # return render(request, 'admin_view_product.html')
    contacts=models.Contact.objects.all().filter()
    return render(request,'admin_view_message.html',{'contacts':contacts})


@user_passes_test(lambda u: u.is_superuser)
def admin_view_room(request):
    # return render(request, 'admin_view_product.html')
    rooms=models.Room.objects.all()
    username=hash_fn.hash(request.user.id)
    return render(request,'admin_view_room.html',{'rooms':rooms, 'username':username})


@user_passes_test(lambda u: u.is_superuser)
def admin_delete_room(request,pk):
    room=models.Room.objects.get(id=pk)
    room.delete()
    return redirect('admin_view_room')


# Doctor dashboard

@user_passes_test(is_doctor)
def doctor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'doctor_dashboard.html')

def doctor_view_appointments(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    doctor_id = doctor.id
    appointments=models.Appointment.objects.all().filter(doctorId=doctor_id)
    print(appointments)
    return render(request,'doctor_view_appointments.html',{'appointments':appointments,'doctor':doctor})


@user_passes_test(is_doctor)
def doctor_view_appointment(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    return render(request,'doctor_view_appointment.html', {'appointment':appointment})



def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if is_patient(request.user):
                return redirect('doctors')
            elif is_doctor(request.user):
                return redirect('doctor_dashboard')
            return HttpResponseRedirect('admin_dashboard')
        else:
            return HttpResponseRedirect('signin')
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        if is_doctor(request.user):
            return redirect('doctor_dashboard')
        elif is_patient(request.user):
            return redirect('dashboard')
        return HttpResponseRedirect('admin_dashboard')
    return render(request, 'signin.html')






def doctors(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'doctors.html',{'doctors':doctors})


def doctor(request,pk):
    appointmentForm=forms.AppointmentForm()
    doctor=models.Doctor.objects.get(id=pk)
    
    if request.method=='POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'First you have to login')
            return redirect('signin')

        appointmentForm=forms.AppointmentForm(request.POST, request.FILES)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=doctor.id
            appointment.patientId=request.user.id
            appointment.doctor_name=models.Doctor.objects.get(id=doctor.id).get_name
            appointment.patient_name=models.User.objects.get(id=request.user.id).first_name
            appointment.email=models.User.objects.get(id=request.user.id).email
            room=str(hash_fn.hash(str(appointment.doctorId)+str(appointment.patientId)))
            userid=str(hash_fn.hash(str(request.user.id)))

            validation=str(hash_fn.hash(str(appointment.doctorId)+str(appointment.patientId)))

            if models.Room.objects.filter(name=room).exists() and room==validation:
                return redirect('/'+room+'/'+userid)
            elif(room==validation):
                new_room = models.Room.objects.create(name=room)
                new_room.save()
                return redirect('/'+room+'/'+userid)
            else:
                return HttpResponseRedirect("Invalid, You can not access")

            return render(request, 'appointments.html', {'doctor':doctor, 'room':room})
    return render(request,'doctor.html', {'doctor':doctor, 'appointmentForm':appointmentForm})





def room(request, room, userid):
    print(request.user.id)
    print(room)

    username = request.GET.get('username')
    room_details = models.Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'userid':userid,
        'room': room,
        'room_details': room_details
    })



# def checkview(request):
#     room = request.POST['room_name']
#     username = request.POST['username']
#     userid = request.POST['userid']

    # if models.Room.objects.filter(name=room).exists():
    #     return redirect('/'+room+'/'+userid)
    # else:
    #     new_room = models.Room.objects.create(name=room)
    #     new_room.save()
    #     return redirect('/'+room+'/'+userid)


def send(request):
    message = request.POST['message']
    username = request.user
    room_id = request.POST['room_id']

    new_message = models.Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = models.Room.objects.get(name=room)

    messages = models.Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})





def appointment(request):
    return render(request, 'appointments.html')



# Products Start 


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = models.Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	print(items)

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	user = request.user
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(user=user, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		user = request.user
		order, created = Order.objects.get_or_create(user=user, complete=False)
	else:
		user, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		user=user,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)






def blogs(request):
    blogs=models.Blog.objects.all().filter()
    return render(request,'blogs.html',{'blogs':blogs})


def blog(request,pk):
    blog=models.Blog.objects.get(id=pk)
    return render(request,'blog.html',{'blog':blog})





# Product Views Start 








# Winsome Natural Product Start 


def winsome_naturals(request):
    return render(request, 'winsome_naturals.html')











# Logout View 

def logout_view(request):
    logout(request)
    return redirect('/')