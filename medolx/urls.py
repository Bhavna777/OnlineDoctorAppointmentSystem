from django.contrib.auth import logout
from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('doctors', views.doctors, name="doctors"),
    path('appointment', views.appointment, name="appointment"),
    path('doctor/<int:pk>', views.doctor, name="doctor"),


    # Admin Dashboard 


    path('dashboard', views.dashboard, name="dashboard"),
    path('admin_dashboard', views.admin_dashboard, name="admin_dashboard"),
    path('admin_doctor', views.admin_doctor, name="admin_doctor"),
    path('admin_view_doctor', views.admin_view_doctor, name="admin_view_doctor"),
    path('admin_add_doctor', views.admin_add_doctor, name="admin_add_doctor"),
    path('admin_update_doctor/<int:pk>', views.admin_update_doctor, name="admin_update_doctor"),
    path('admin_delete_doctor/<int:pk>', views.admin_delete_doctor, name="admin_delete_doctor"),
    path('admin_patient', views.admin_patient, name="admin_patient"),
    path('admin_view_patient', views.admin_view_patient, name="admin_view_patient"),
    path('admin_add_patient', views.admin_add_patient, name="admin_add_patient"),
    path('admin_update_patient/<int:pk>', views.admin_update_patient, name="admin_update_patient"),
    path('admin_delete_patient/<int:pk>', views.admin_delete_patient, name="admin_delete_patient"),
    path('admin_view_appointments', views.admin_view_appointments, name="admin_view_appointments"),
    path('admin_view_appointment/<int:pk>', views.admin_view_appointment, name="admin_view_appointment"),
    path('admin_update_appointment/<int:pk>', views.admin_update_appointment, name="admin_update_appointment"),
    path('admin_delete_appointment/<int:pk>', views.admin_delete_appointment, name="admin_delete_appointment"),
    path('admin_view_room', views.admin_view_room, name="admin_view_room"),
    path('admin_delete_room/<int:pk>', views.admin_delete_room, name="admin_delete_room"),
    path('admin_add_product', views.admin_add_product, name="admin_add_product"),
    path('admin_view_product', views.admin_view_product, name="admin_view_product"),
    path('admin_update_product/<int:pk>', views.admin_update_product, name="admin_update_product"),
    path('admin_delete_product/<int:pk>', views.admin_delete_product, name="admin_delete_product"),
    path('admin_view_blog', views.admin_view_blog, name="admin_view_blog"),
    path('admin_add_blog', views.admin_add_blog, name="admin_add_blog"),
    path('admin_update_blog/<int:pk>', views.admin_update_blog, name="admin_update_blog"),
    path('admin_delete_blog/<int:pk>', views.admin_delete_blog, name="admin_delete_blog"),
    path('admin_view_message', views.admin_view_message, name="admin_view_message"),


    # Doctor Dashboard
    path('doctor_dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    path('doctor_view_appointments', views.doctor_view_appointments, name="doctor_view_appointments"),
    path('doctor_view_appointment/<int:pk>', views.doctor_view_appointment, name="doctor_view_appointment"),


    # Product Start 

    path('store', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

    # Product End 

    
    # Blog Start 
    path('blogs', views.blogs, name="blogs"),
    path('blog/<int:pk>', views.blog, name="blog"),
    # Blog End 



    # path('signup', views.signup, name="signup"),
    # path('contact', views.contact, name="contact"),
    # path('dashboard', views.dashboard, name="dashboard"),
    # path('doctor_dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    # path('admin_dashboard', views.admin_dashboard, name="admin_dashboard"),
    # path('admin_doctor', views.admin_doctor, name="admin_doctor"),
    # path('admin_view_doctor', views.admin_view_doctor, name="admin_view_doctor"),
    # path('admin_add_doctor', views.admin_add_doctor, name="admin_add_doctor"),
    # path('admin_update_doctor/<int:pk>', views.admin_update_doctor, name="admin_update_doctor"),
    # path('admin_delete_doctor/<int:pk>', views.admin_delete_doctor, name="admin_delete_doctor"),
    # path('admin_patient', views.admin_patient, name="admin_patient"),
    # path('admin_view_patient', views.admin_view_patient, name="admin_view_patient"),
    # path('admin_add_patient', views.admin_add_patient, name="admin_add_patient"),
    # path('admin_update_patient/<int:pk>', views.admin_update_patient, name="admin_update_patient"),
    # path('admin_delete_patient/<int:pk>', views.admin_delete_patient, name="admin_delete_patient"),
    # path('admin_add_product', views.admin_add_product, name="admin_add_product"),
    # path('admin_view_product', views.admin_view_product, name="admin_view_product"),
    # path('admin_update_product/<int:pk>', views.admin_update_product, name="admin_update_product"),
    # path('admin_delete_product/<int:pk>', views.admin_delete_product, name="admin_delete_product"),
    # path('admin_view_blog', views.admin_view_blog, name="admin_view_blog"),
    # path('admin_add_blog', views.admin_add_blog, name="admin_add_blog"),
    # path('admin_update_blog/<int:pk>', views.admin_update_blog, name="admin_update_blog"),
    # path('admin_delete_blog/<int:pk>', views.admin_delete_blog, name="admin_delete_blog"),
    # path('admin_view_message', views.admin_view_message, name="admin_view_message"),
    




    # for chat app

    path('<str:room>/<str:userid>', views.room, name='room'),
    # path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),




    # Winsome Natural Product

    path('winsome_naturals/', views.winsome_naturals, name='winsome_naturals'),



    # Logout


    path('logout/', views.logout_view, name='logout'),
]

