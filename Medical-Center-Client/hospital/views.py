# Create your views here


# Import the necessary Modules

import cv2
import io
import uuid
import socket
import base64
import pydicom
import numpy as np
from PIL import Image
from . import forms,models
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime,timedelta,date
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import login_required,user_passes_test




user_type , view = 'GUEST' , ''
received_message = []
pixel_array , image = np.array([]) , np.array([])


# Navigate to the homepage 
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


# for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    #if request.user.is_authenticated and is_admin(request.user):
        #return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


# for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    #if request.user.is_authenticated and is_doctor(request.user):
        #return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


# for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    #if request.user.is_authenticated and is_patient(request.user):
        #return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')



# Get Info From Admin Signup Form
def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})



# Get Info From Doctor Signup Form
def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)



# Get Info From Patient Signup Form
def patient_signup_view(request):
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
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/patientsignup.html',context=mydict)






# Functions For checking If user is: doctor , patient or admin (by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()




# AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------


# Function For Retrieving Info For Admin Dashboard
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)



# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
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
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
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

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
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
            patient.dob = request.POST.get('dob')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
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
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing


import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START-------------------------------------------------------


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter()
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):

    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            #appointment_date_str = request.POST.get('appointmentDate')
            #appointment_date = datetime.fromisoformat(appointment_date_str)
            #appointment.appointmentDate = appointment_date
            # Parse date string to datetime object
            appointment.appointmentDate = datetime.strptime(request.POST.get('appointmentDate'), '%Y-%m-%d').date()
            # Parse time string to datetime object
            appointment.appointmentTime = datetime.strptime(request.POST.get('appointmentTime'), '%H:%M').time()
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name + ' ' + models.User.objects.get(id=request.POST.get('doctorId')).last_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name + ' ' + models.User.objects.get(id=request.POST.get('patientId')).last_name
            appointment.status=False        # Wait For Doctor Approval
            appointment.save()

            # Generate a Dictionary of appointment Data to be converted to HL7 Message
            appointment_data = {'patient_id': request.POST.get('patientId'),
                                'patient_first_name': models.User.objects.get(id=request.POST.get('patientId')).first_name,
                                'patient_last_name':  models.User.objects.get(id=request.POST.get('patientId')).last_name,
                                'patient_date_of_birth': models.Patient.objects.get(user_id=request.POST.get('patientId')).dob,
                                'doctor_id': request.POST.get('doctorId'),
                                'doctor_first_name':  models.User.objects.get(id=request.POST.get('doctorId')).first_name,
                                'doctor_last_name': models.User.objects.get(id=request.POST.get('doctorId')).last_name,
                                'date': request.POST.get('appointmentDate') ,
                                'time': request.POST.get('appointmentTime') ,
                                'message': request.POST.get('description'),                                
                                'appointment_id': models.Appointment.objects.latest('id').id,
                                'patient_address': models.Patient.objects.get(user_id=request.POST.get('patientId')).address,
                                'patient_phone': models.Patient.objects.get(user_id=request.POST.get('patientId')).mobile,
            }



            # Get the HL7 Message
            hl7_message = generate_hl7_message(appointment_data)
            print(hl7_message)

            # Try to establish a connection with the server & send the HL7 message
            # Server IP address and port
            HOST = '192.168.1.10'
            PORT = 8000

            try:
                print('Starting Connection From the Client Side')
                # Create a socket object
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect to the server
                client_socket.connect((HOST, PORT))
                # Send HL7 message
                client_socket.sendall(hl7_message.encode())
                # Close the connection
                client_socket.close()
            except Exception as e:
                return HttpResponse(f"Error: {e}")

            return HttpResponseRedirect('admin-view-appointment')

        #return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')



#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START -----------------------------
#---------------------------------------------------------------------------------



def wait_approval_view(request):
    return render(request,'hospital/index.html')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})





@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) # for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=False, doctorId=request.user.id) # 
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True, user_id__in=patientid) # 
    print("Length of appointments:", len(appointments))
    print("Length of patients:", len(patients))
    # appointments_with_patients = zip(appointments, patients)
    appointments_with_patients = appointments
    #print("Zipped appointments:", appointments_with_patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments_with_patients':appointments_with_patients,'doctor':doctor})







@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_approve_appointment_view(request,pk):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    #patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    #appointments=zip(appointments,patients)
    #return render(request,'hospital/doctor_delete_appointment.html', context={'appointments': appointments, 'doctor': doctor})
    return redirect('doctor-view-appointment')







@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_reject_appointment_view(request,pk):
    doctor=models.Doctor.objects.get(user_id=request.user.id) # for profile picture of doctor in sidebar
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    #patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    #appointments=zip(appointments,patients)
    #return render(request,'hospital/doctor_delete_appointment.html', context={'appointments': appointments, 'doctor': doctor})
    return redirect('doctor-view-appointment')






@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) # for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid=[]
    pictures = []
    for a in appointments:
        patientid.append(a.patientId)
        #patient=models.Patient.objects.get(status=True,user_id=a.patientId)
        #pictures.append(patient.profile_pic)
    #patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    #appointments_with_patients = zip(appointments, patients)
    print("Length of appointments:", len(appointments))
    print("Length of pictures:", len(pictures))
    #print("Length of patients:", len(patients))
    #appointments_with_pic = zip(appointments, pictures)
    appointments_with_pic = appointments
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments_with_pic':appointments_with_pic,'doctor':doctor})
    






@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    #patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    #appointments=zip(appointments,patients)
    #return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})
    return redirect('doctor-delete-appointment')



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END -------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ----------------------------
#---------------------------------------------------------------------------------



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})






# WebSocket client code to send HL7 message to the server
# Replace 'your-server-address' with the actual WebSocket server address
import asyncio
import websockets

async def send_hl7_message(message):
    uri = "ws://127.0.0.1:8000/ws/"  # "ws://localhost:8000/ws/patient_book_appointment/"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)



def send_appointment_hl7_message(appointment_data):
    asyncio.run(send_hl7_message(appointment_data))



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))

            if doctor.department == 'Emergency Medicine Specialists':
                if 'fever' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Anesthesiologists':
                if 'surgery' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})


            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id # user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name + ' ' + models.User.objects.get(id=request.POST.get('doctorId')).last_name
            appointment.patientName=request.user.first_name + ' ' + request.user.last_name
            # Parse date string to datetime object
            appointment.appointmentDate = datetime.strptime(request.POST.get('appointmentDate'), '%Y-%m-%d').date()
            # Parse time string to datetime object
            appointment.appointmentTime = datetime.strptime(request.POST.get('appointmentTime'), '%H:%M').time()
            appointment.status=False
            appointment.description = desc
            appointment.save()

            # Generate a Dictionary of appointment Data to be converted to HL7 Message
            appointment_data = {'patient_id': request.user.id,
                                'patient_first_name': models.User.objects.get(id=request.user.id).first_name,
                                'patient_last_name':  models.User.objects.get(id=request.user.id).last_name,
                                'patient_date_of_birth': models.Patient.objects.get(user_id=request.user.id).dob,
                                'doctor_id': request.POST.get('doctorId'),
                                'doctor_first_name':  models.User.objects.get(id=request.POST.get('doctorId')).first_name,
                                'doctor_last_name': models.User.objects.get(id=request.POST.get('doctorId')).last_name,
                                'date': request.POST.get('appointmentDate') ,
                                'time': request.POST.get('appointmentTime') ,
                                'message': request.POST.get('description'),
                                'appointment_id': models.Appointment.objects.latest('id').id,
                                'patient_address': models.Patient.objects.get(user_id=request.user.id).address,
                                'patient_phone': models.Patient.objects.get(user_id=request.user.id).mobile,
            }


            # Encrypt the Appointment Data using HL7 Protocol
            hl7_message = generate_hl7_message(appointment_data)
            print('HL7 Message:', hl7_message)


            # Try to establish a connection with the server & send the HL7 message
            # Server IP address and port
            HOST = '192.168.1.10'     #  '156.204.43.154'  
            PORT = 8000

            try:
                print('Starting Connection From the Client Side')
                # Create a socket object
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # client_socket.settimeout(1200)  # Set timeout to 120 seconds
                # Connect to the server
                client_socket.connect((HOST, PORT))
                # Send HL7 message
                client_socket.sendall(hl7_message.encode())
                # Close the connection
                client_socket.close()
            except Exception as e:
                return HttpResponse(f"Error: {e}")

            # Send HL7 message via WebSocket
            #send_appointment_hl7_message(hl7_message)
            return HttpResponseRedirect('patient-view-appointment')

    return render(request, 'hospital/patient_book_appointment.html', context=mydict)






@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})





@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START --------------------
#---------------------------------------------------------------------------------



def aboutus_view(request):
    return render(request,'hospital/aboutus.html')



def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------





#---------------------------------------------------------------------------------
#------------------------ FOOTER RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------


# for directing to the privacy policy page
def privacy_policy_view(request):
    return render(request,'hospital/privacy_policy.html')


# for directing to the terms page
def terms_view(request):
    return render(request,'hospital/terms.html')

#---------------------------------------------------------------------------------
#------------------------ FOOTER RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ Electronic Records RELATED VIEWS START -----------------
#---------------------------------------------------------------------------------


# for directing to the admin's medical records options
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_medical_records_view(request):
    return render(request,'hospital/admin-medical-records.html') 



# for directing to the admin's medical records related Database
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_records_view(request):
    medical_records=models.MedicalRecord.objects.all()
    return render(request,'hospital/admin-view-records.html', {'medical_records': medical_records,})





# for adding a medical record to the related Database
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_records_view(request):
    print('Entered Route')
    medicalRecordForm=forms.MedicalRecordForm()
    mydict={'medicalRecordForm': medicalRecordForm,}
    if request.method=='POST':
        print('Entered POST')
        medicalRecordForm=forms.MedicalRecordForm(request.POST, request.FILES)
        if medicalRecordForm.is_valid():
            record=medicalRecordForm.save(commit=False)
            # Get the corresponding IDs
            doctor_id = request.POST.get('doctor_id')
            patient_id = request.POST.get('patient_id')
            record.doctor_id = doctor_id
            record.patient_id = patient_id

            # Fetch doctor and patient names from the database , models.User.objects.get(id=request.POST.get('patientId')).first_name
            doctor = models.User.objects.get(id=doctor_id)
            patient = models.User.objects.get(id=patient_id)
            print("Doctor ID:", doctor_id)
            print("Patient ID:", patient_id)
            print("Doctor Name:", doctor.first_name)
            print("Patient Name:", patient.first_name)

            record.doctorName = doctor.first_name
            record.patientName = patient.first_name

            # Print the image URL
            print("Image URL:", record.image.url)

            # Save the medical record in the database
            record.save()
 
            return HttpResponseRedirect('admin-view-records')
    
        else:
            print("Form is not valid:", medicalRecordForm.errors)
    
    return render(request,'hospital/admin-add-records.html', context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_medical_record_view(request,pk):
    record=models.MedicalRecord.objects.get(id=pk)
    record.delete()
    return redirect('admin-view-records')





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_medical_record_view(request,pk):
    record=models.MedicalRecord.objects.get(id=pk)
    medicalRecordForm=forms.MedicalRecordForm(request.FILES,instance=record)
    if request.method=='POST':
        print('Entered POST')
        medicalRecordForm=forms.MedicalRecordForm(request.POST, request.FILES, instance=record)
        if medicalRecordForm.is_valid():
            record=medicalRecordForm.save(commit=False)
            # Get the corresponding IDs
            doctor_id = request.POST.get('doctor_id')
            patient_id = request.POST.get('patient_id')
            record.doctor_id = doctor_id
            record.patient_id = patient_id

            # Fetch doctor and patient names from the database , models.User.objects.get(id=request.POST.get('patientId')).first_name
            doctor = models.User.objects.get(id=doctor_id)
            patient = models.User.objects.get(id=patient_id)
            print("Doctor ID:", doctor_id)
            print("Patient ID:", patient_id)
            print("Doctor Name:", doctor.first_name)
            print("Patient Name:", patient.first_name)

            record.doctorName = doctor.first_name
            record.patientName = patient.first_name

            # Print the image URL
            print("Image URL:", record.image.url)

            # Save the medical record in the database
            record.save()
 
            return redirect('admin-view-records')
    
        else:
            print("Form is not valid:", medicalRecordForm.errors)

    mydict={'medicalRecordForm': medicalRecordForm,}
    return render(request,'hospital/admin-add-records.html', context=mydict)



#for directing to the doctor's medical records options
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_medical_records_view(request):
    doctor = models.Doctor.objects.get(user=request.user)  # Adjust this query according to your model structure
    context = {
        'doctor': doctor,
    }
    return render(request,'hospital/doctor-medical-records.html', context)



#for directing to the doctor's medical records related Database
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_records_view(request):
    doctor = models.Doctor.objects.get(user=request.user)  # Get the current user
    medical_records=models.MedicalRecord.objects.filter(doctor_id=request.user.id)
    return render(request,'hospital/doctor-view-records.html', {'medical_records': medical_records, 'doctor': doctor,})



#for directing to the doctor's medical records options
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_records_view(request):
    #print('Entered Route')
    medicalRecordForm=forms.MedicalRecordForm()
    doctor = models.Doctor.objects.get(user=request.user)  # Get the current user
    mydict={'medicalRecordForm': medicalRecordForm, 'doctor': doctor,}
    if request.method=='POST':
        print('Entered POST')
        medicalRecordForm=forms.MedicalRecordForm(request.POST, request.FILES)
        if medicalRecordForm.is_valid():
            record=medicalRecordForm.save(commit=False)
            # Get the corresponding IDs
            doctor_id = request.POST.get('doctor_id')
            patient_id = request.POST.get('patient_id')
            record.doctor_id = doctor_id
            record.patient_id = patient_id

            # Fetch doctor and patient names from the database , models.User.objects.get(id=request.POST.get('patientId')).first_name
            doctor = models.User.objects.get(id=doctor_id)
            patient = models.User.objects.get(id=patient_id)
            print("Doctor ID:", doctor_id)
            print("Patient ID:", patient_id)
            print("Doctor Name:", doctor.first_name)
            print("Patient Name:", patient.first_name)

            record.doctorName = doctor.first_name
            record.patientName = patient.first_name

            # Print the image URL
            print("Image URL:", record.image.url)

            # Save the medical record in the database
            record.save()
 
            return HttpResponseRedirect('doctor-view-records')
    
        else:
            print("Form is not valid:", medicalRecordForm.errors)
    
    return render(request,'hospital/doctor-add-records.html', context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_medical_record_view(request, pk):
    doctor = models.Doctor.objects.get(user=request.user)  # Get the current user
    record=models.MedicalRecord.objects.get(id=pk)
    record.delete()
    return redirect('doctor-view-records')




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_update_medical_record_view(request,pk):
    record=models.MedicalRecord.objects.get(id=pk)
    medicalRecordForm=forms.MedicalRecordForm(request.FILES,instance=record)
    doctor = models.Doctor.objects.get(user=request.user)  # Get the current user
    if request.method=='POST':
        print('Entered POST')
        medicalRecordForm=forms.MedicalRecordForm(request.POST, request.FILES, instance=record)
        if medicalRecordForm.is_valid():
            record=medicalRecordForm.save(commit=False)
            # Get the corresponding IDs
            doctor_id = request.POST.get('doctor_id')
            patient_id = request.POST.get('patient_id')
            record.doctor_id = doctor_id
            record.patient_id = patient_id

            # Fetch doctor and patient names from the database , models.User.objects.get(id=request.POST.get('patientId')).first_name
            doctor = models.User.objects.get(id=doctor_id)
            patient = models.User.objects.get(id=patient_id)
            print("Doctor ID:", doctor_id)
            print("Patient ID:", patient_id)
            print("Doctor Name:", doctor.first_name)
            print("Patient Name:", patient.first_name)

            record.doctorName = doctor.first_name
            record.patientName = patient.first_name

            # Print the image URL
            print("Image URL:", record.image.url)

            # Save the medical record in the database
            record.save()
 
            return redirect('doctor-view-records')
    
        else:
            print("Form is not valid:", medicalRecordForm.errors)

    mydict={'medicalRecordForm': medicalRecordForm,
            'doctor': doctor,}

    return render(request,'hospital/doctor-add-records.html', context=mydict)




#for directing to the patient's medical 
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_records_view(request):
    medical_records=models.MedicalRecord.objects.filter(patient_id=request.user.id)
    patient = models.Patient.objects.get(user=request.user)  # Get the current user
    return render(request,'hospital/patient-view-records.html', {'medical_records': medical_records, 'patient': patient,})


#---------------------------------------------------------------------------------
#------------------------ Electronic Records RELATED VIEWS END -------------------
#---------------------------------------------------------------------------------















#---------------------------------------------------------------------------------
#------------------------ HL7 Format Message RELATED VIEWS START------------------
#---------------------------------------------------------------------------------


# Import necessary modules
import re
import socket
import hl7apy
import threading




# Function to extract symptoms from the patient's Message/Details Section
def extract_symptoms(text):
    # Define a list of common symptoms or keywords
    symptoms_list = ['fever', 'cough', 'headache', 'nausea', 'fatigue', 'pain', 'shortness of breath', 'vomiting', 'diarrhea']
    # Compile a regular expression pattern to match symptoms
    pattern = re.compile(r'\b(?:' + '|'.join(symptoms_list) + r')\b', re.IGNORECASE)
    # Find all matches in the text
    symptoms = re.findall(pattern, text)
    return symptoms






# Function to generate the HL7 Message from a Dictionary of Information
def generate_hl7_message(appointment_data):

    """
    Example of an HL7 Message Of An SIU Type:
        
    MSH|^~\&|SendingApplication|SendingFacility|ReceivingApplication|ReceivingFacility|DateTime||SIU^S12|MessageControlID|P|2.3||||||
    SCH|ScheduleID^ScheduleID|EventReason|||AppointmentID|AppointmentType|AppointmentReason|AppointmentLocation|AppointmentDuration|m|^^ScheduledStartDateTime^ScheduledEndDateTime|||||OrderedBy||||PerformedBy|||||Scheduled
    PID|1||PatientID||PatientName||PatientDOB|PatientSex|||PatientAddress||PatientPhone|||PatientMaritalStatus||PatientSSN|||||||||||||||||||||
    PV1|1|O|||||AttendingDoctor|ReferringDoctor||||||||||||||||||||||||||||||||||||||||||VisitNumber|| => (optional)
    RGS|1|ResourceGroupType
    AIG|1|ResourceType|ResourceID|ResourceGroup^ResourceGroupName
    AIL|1|LocationType|Location^^^LocationDescription|LocationStartDateTime|||LocationDuration|m^Minutes||Scheduled
    AIP|1|PersonnelType|PersonnelID|PersonnelName||PersonnelStartDateTime|||PersonnelDuration|m^Minutes||Scheduled


    """

    from datetime import timedelta


    def generate_control_id():
        return str(uuid.uuid4())


    # Message Header Related Variables
    SendingApplication = "Patient Management System"  # Sending application
    ReceivingApplication = "Doctor Scheduling System"   # Receiving application
    SendingFacility = 'Patient Account'
    ReceivingFacility = 'MammoCare Solutions'
    MessageControlID = generate_control_id()        # Generate A Unique Control ID For the HL7 Message
    print("Message Control ID:", MessageControlID)
    CurrentDateTime = datetime.now().strftime("%Y%m%d%H%M%S")   # Get the Date & Time, of the message generation
    print("Message Date & Time:", CurrentDateTime)


    # Schedule Activity Information Header Related Variables
    ScheduleID = '10345'
    AppointmentID = appointment_data['appointment_id']
    EventReason = 'Diagnosis'
    AppointmentType = 'Mammography'
    AppointmentReason = appointment_data['message']
    AppointmentLocation = 'EXAMINATION ROOM'
    AppointmentDuration = '60'
    appointment_date = appointment_data['date'].replace('-', '')
    appointment_time = appointment_data['time'].replace(':', '')
    # Convert appointment_date and appointment_time to datetime objects
    ScheduledStartDateTime = datetime.strptime(appointment_date + appointment_time, '%Y%m%d%H%M')
    ScheduledEndDateTime = ScheduledStartDateTime + timedelta(hours=1)      # Add one hour to the start date & time
    OrderedBy = 'DOCTOR1'
    PerformedBy = 'DOCTOR2'


    # Patient Identification Related Variables
    PatientID = appointment_data['patient_id']
    PatientSSN = 'UNKNOWN'
    PatientDOB = str(appointment_data['patient_date_of_birth']).replace('-','')
    PatientSex = 'F'
    PatientAddress = appointment_data['patient_address']
    PatientPhone = appointment_data['patient_phone']
    PatientMaritalStatus = 'UNKNOWN'
    PatientName = appointment_data['patient_first_name'] + '^' + appointment_data['patient_last_name']



    # Appointment Information - General Resource Related Variables
    ResourceType = 'Equipment'  # Specify the type of resource (e.g., equipment)
    ResourceID = 'MAM1234'  # Unique identifier for the resource (e.g., equipment ID)
    ResourceGroup = 'MammographyEquipment'  # Group identifier for the resource (e.g., equipment category)
    ResourceGroupName = 'MammographyMachine'  # Name or description of the resource group (e.g., equipment type)




    # Appointment Information - Location Related Variables
    LocationType = 'C'  # 'C' for clinic or examination room
    Location = 'Radiologic Department'  # Specify the specific location within the facility
    LocationDescription = 'Room 203'  # Additional description of the location if needed
    LocationStartDateTime = ScheduledStartDateTime  # Use the same start datetime as the appointment
    LocationDuration = '30'  # Duration of the appointment in minutes (30 mins for a mammography scan)





    # Appointment Information - Personnel Resource Related Variables
    PersonnelType = 'D' # 'D' for Doctor (e.g., Doctor, Technician, Nurse, Others)
    PersonnelID = appointment_data['doctor_id'] 
    PersonnelName = appointment_data['doctor_first_name'] + '^' + appointment_data['doctor_last_name']
    PersonnelStartDateTime = ScheduledStartDateTime
    PersonnelDuration = '60'  # Appointment would last for 60 minutes (1 hr.)




    hl7_message = (
        f"MSH|^~\&|{SendingApplication}|{SendingFacility}|{ReceivingApplication}|{ReceivingFacility}|{CurrentDateTime}||SIU^S12|{MessageControlID}|P|2.3||||||\n"
        f"SCH|{ScheduleID}^{ScheduleID}|||{AppointmentID}^{AppointmentID}|10345|{AppointmentType}^{EventReason}|{AppointmentReason}|{AppointmentLocation}|{AppointmentDuration}|m|^^{ScheduledStartDateTime}^{ScheduledEndDateTime}|||||{OrderedBy}^||||{PerformedBy}^|||||Scheduled\n"
        f"PID|1||{PatientID}||{PatientName}||{PatientDOB}|{PatientSex}|||{PatientAddress}||{PatientPhone}|||{PatientMaritalStatus}||{PatientSSN}|||||||||||||||||||||\n"
        f"RGS|1|A\n"
        f"AIG|1|{ResourceType}|{ResourceID}|{ResourceGroup}^{ResourceGroupName}\n"
        f"AIL|1|{LocationType}|{Location}^^^{LocationDescription}|{LocationStartDateTime}|||{LocationDuration}|m^Minutes||Scheduled\n"
        f"AIP|1|{PersonnelType}|{PersonnelID}|{PersonnelName}||{PersonnelStartDateTime}|||{PersonnelDuration}|m^Minutes||Scheduled\n"
    )


    return hl7_message







# Function that establishes a connection between the client & server, to send the hl7 message (from the client's side/Patient)
def send_hl7_message(hl7_message):
    # Define Client parameters
    HOST = '127.0.0.1'
    PORT = 8000
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Try to connect to the server
    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print('Connected to server on port', PORT)
        # Send the HL7 message
        client_socket.sendall(hl7_message.encode('utf-8'))
        print('HL7 message sent successfully')
        # Receive response from server (if any)
        response = client_socket.recv(1024)
        print('Received response from server:', response.decode('utf-8'))
    finally:
        # Close the socket
        client_socket.close()








# Start the HL7 message handling thread when Django initializes
# hl7_thread = threading.Thread(target=hl7_message_handler)
# hl7_thread.daemon = True  # Thread will terminate when main program exits
# hl7_thread.start()





#---------------------------------------------------------------------------------
#------------------------ HL7 Format Message RELATED VIEWS END--------------------
#---------------------------------------------------------------------------------









#---------------------------------------------------------------------------------
#------------------------ CDSS VIEW RELATED VIEWS START--------------------------
#---------------------------------------------------------------------------------

import os
import torch
import torch.nn as nn
from io import BytesIO
import matplotlib.pyplot as plt
from torchvision import transforms
from torch.autograd import Variable
from django.http import JsonResponse
from torchvision.models import mobilenet_v2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage





# for directing to the CDSS Page
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def assistant_view(request):
    doctor = models.Doctor.objects.get(user=request.user)  # Get the current user
    # Get all group names
    #group_names = Group.objects.values_list('name', flat=True)
    #print("Available group names:", group_names)
    # Fetch patient names from the User model
    patients = models.User.objects.filter(groups__name='PATIENT')
    print(patients)
    for patient in patients:
        print(patient.first_name)
    # patients = models.Patient.objects.all()  # Assuming you have a Patient model with a 'name' field
    context = {
        'doctor': doctor,
        'patients':patients,
    }
    return render(request,'hospital/assistant.html', context)
    




def process_image(request):

    global pixel_array, image

    if request.method == 'POST' and request.FILES.get('image'):
        dicom_file = request.FILES['image']

        # Read DICOM file and extract metadata
        ds = pydicom.dcmread(dicom_file)
        pixel_array = ds.pixel_array.astype(np.float32)

        # Take the 1st slice from the 3D volume
        pixel_array = np.array(pixel_array[0, :, :]) 

        #plt.imshow(image, cmap='gray')
        #plt.imshow(image)
        #plt.axis('off')  # Turn off axis ticks and labels
        #plt.savefig('display_image.png', bbox_inches='tight', pad_inches=0) # Save the grayscale image for displaying purposes only
        # plt.show()
        # Convert the numpy array to PIL image
        image = Image.fromarray(pixel_array.astype('uint8'), 'L')
        # Save the grayscale image
        image.save('display_image.png')

        print('Image Shown Successfully')
        
        # Read the saved grayscale image
        with open('display_image.png', 'rb') as file:
            image_data = file.read()

        # Encode image data as base64 string
        encoded_image_data = base64.b64encode(image_data).decode('utf-8')

        return HttpResponse(encoded_image_data, content_type="image/png")
    else:
        return JsonResponse({'error': 'No image file provided.'}, status=400)









def diagnose_view(request):

    global view

    class MobileNetV2(nn.Module):
        def __init__(self, num_classes):
            super(MobileNetV2, self).__init__()
            # Load a pre-trained MobileNetV2 model
            self.mobilenet = mobilenet_v2(pretrained=True)
            # Modify the last layer
            num_inputs = self.mobilenet.classifier[1].in_features
            self.mobilenet.features[0][0] = nn.Conv2d(1, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
            self.mobilenet.classifier[1] = nn.Linear(num_inputs, num_classes)

        def forward(self, image):
            # Ensure that the input tensor has the correct dimensions
            if len(image.shape) == 3:
                # Add an additional dimension for the batch size
                image = image.unsqueeze(0)
            x = self.mobilenet(image)
            return x

    class_dict = {0: 'Normal',
                  1: 'Actionable',
                  2: 'Benign',
                  3: 'Cancer'}
    
    view_opts = {'option1': 'rmlo',
                 'option2': 'lmlo',
                 'option3': 'rcc',
                 'option4': 'lcc',
                }
    
    # Apply Preprocessing to the images, and divide to batches
    transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Normalize((0.5), (0.5)),
                                  ])

    if (request.method == 'POST'):

        print('Entered Route')
        # Retrieve the selected view type from the POST data
        view_type = request.POST.get('view_type')
        view = view_opts[view_type]
        print('Selected View: ', view)
        # Load the saved Model
        model_path = 'D:/HCIS/current_repo/Medical-Center-Client/model.pkl'
        model = MobileNetV2(num_classes=4)
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu')))
        model.eval()  # Set the model to evaluation mode
        # Transform the image
        image = np.resize(pixel_array.astype(np.float32), (500, 500))
        img = transform(np.array(image))
        img = img.unsqueeze(0)  # Add batch dimension
        img = Variable(img)     # Convert the input to a Variable
        # Make a prediction
        with torch.no_grad():
            output = model(img)
            # Get the Predicted Class
            probabilities, predicted_class = torch.max(output.data, 1)
            predicted_class = predicted_class.item()
            print(f'Prediction: {predicted_class}')

        # Return the diagnosis text as JSON response
        return JsonResponse({'diagnosis_text': '65 % Chance ' + class_dict[predicted_class]})

    # If the request is not AJAX or not POST, return a 400 Bad Request response
    return JsonResponse({'error': 'Invalid request'}, status=400)





def submit_record(request):

    class_dict = {'diagnose1': 'Normal',
                  'diagnose2': 'Actionable',
                  'diagnose3': 'Benign',
                  'diagnose4': 'Cancer'}

    if request.method == 'POST':

        # Retrieve the diagnosis, notes, and patient from the POST data
        diagnosis = class_dict[request.POST.get('diagnosis')]
        notes = request.POST.get('notes')
        doctor = models.Doctor.objects.get(user=request.user)  # Get the current user (doctor)
        doctor_user = models.User.objects.get(id=request.user.id)
        patient_id = request.POST.get('patient')
        patient_user = models.User.objects.get(id=patient_id)
        patient_obj = models.Patient.objects.get(user=patient_user)
        
        print("Doctor's Diagnosis: ", diagnosis)
        print("Doctor's Notes: ", notes)
        print('Doctor: ', doctor)
        print("Associated Patient ID: ", patient_id, type(patient_id))
        print('Associated Patient: ', patient_user)
        print('Associated Patient Object: ', patient_obj)
        
        # Save the data to the MedicalRecord model
        dicom_file = request.FILES.get('image')
        #dicom_data = pydicom.dcmread(dicom_file)

        #pixel_array = dicom_data.pixel_array.astype(np.float32)
        # Take the 1st slice from the 3D volume
        #pixel_array = np.array(pixel_array[0, :, :]) 
        normalized_array = (pixel_array / np.max(pixel_array)) * 255
        image = Image.fromarray(normalized_array.astype('uint8'), 'L')


        # Define the directory within static to save the image
        static_dir = os.path.join(settings.STATICFILES_DIRS[0], 'medical_record_images')

        # Create the directory if it doesn't exist
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)

        # Save the image file to the static directory
        file_name = f"{patient_id}_{diagnosis}.png"
        file_path = os.path.join(static_dir, file_name)
        image.save(file_path)


        medical_record = models.MedicalRecord.objects.create(patient_id= int(patient_id),
                                                             doctor_id= request.user.id,
                                                             patientName= patient_user.first_name + patient_user.last_name,
                                                             doctorName= doctor_user.first_name + doctor_user.last_name,
                                                             details= notes,
                                                             diagnosis= diagnosis,
                                                             image=os.path.join('medical_record_images', file_name),
                                                             view = view,
                                                            )
        
        print('Medical Record Saved Successfully To Database')
        
        # Return a JSON response to indicate success
        return JsonResponse({'message': 'Diagnosis submitted successfully'})
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=400)



#---------------------------------------------------------------------------------
#------------------------ CDSS VIEW RELATED VIEWS END----------------------------
#---------------------------------------------------------------------------------