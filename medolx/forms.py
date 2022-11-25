from django import forms
from django.contrib.auth.models import User
from . import models




class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password', 'email']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['phone_no','address','qualification','hospital_name', 'gender', 'department', 'experience', 'consultation_fee', 'profile_pic', 'status']






class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    class Meta:
        model=models.Patient
        fields=['email','phone_no','gender']



class ProductForm(forms.ModelForm):
    class Meta:
        model=models.Product
        fields=['name','profile_pic', 'used_for','price', 'discount']



class AppointmentForm(forms.ModelForm):
    class Meta:
        model=models.Appointment
        fields=['phone_no', 'whatsapp_no', 'gender', 'city', 'problems', 'consultation_mode']


class BlogForm(forms.ModelForm):
    class Meta:
        model=models.Blog
        fields=['title', 'desc', 'featured_pic', 'content', 'author', 'author_pic']



class ContactForm(forms.ModelForm):
    class Meta:
        model=models.Contact
        fields=['fname','lname', 'email','message']