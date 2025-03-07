from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),

    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),


    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[

    path('index', views.wait_approval_view, name='index'),
    path('doctor-dashboard', views.doctor_dashboard_view, name='doctor-dashboard'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),


    path('doctor-delete-appointment/<int:pk>', views.delete_appointment_view, name='doctor-delete-appointment'),
    path('doctor_approve_appointment/<int:pk>', views.doctor_approve_appointment_view,name='doctor_approve_appointment'),
    path('doctor_reject_appointment/<int:pk>', views.doctor_reject_appointment_view,name='doctor_reject_appointment'),

    
]




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]



#---------FOR FOOTER RELATED URLS-------------------------------------

urlpatterns +=[
    # Add a URL pattern for the privacy policy page
    path('privacy_policy', views.privacy_policy_view, name='privacy_policy'),
    path('terms', views.terms_view, name='terms'),
]



#---------MEDICAL RECORDS RELATED URLS-------------------------------------

urlpatterns +=[
    # Add a URL pattern for the Admin's Medical Records Different Routes
    path('admin-medical-records', views.admin_medical_records_view, name='admin-medical-records'),
    path('admin-view-records', views.admin_view_records_view, name='admin-view-records'),
    path('admin-add-records', views.admin_add_records_view, name='admin-add-records'),

    path('delete-record/<int:pk>', views.delete_medical_record_view, name='delete-record'),
    path('update-record/<int:pk>', views.update_medical_record_view, name='update-record'),


    # Add a URL pattern for the Doctor's Medical Records Different Routes
    path('doctor-medical-records', views.doctor_medical_records_view, name='doctor-medical-records'),
    path('doctor-view-records', views.doctor_view_records_view, name='doctor-view-records'),
    path('doctor-add-records', views.doctor_add_records_view, name='doctor-add-records'),

    path('doctor-delete-record/<int:pk>', views.doctor_delete_medical_record_view, name='doctor-delete-record'),
    path('doctor-update-record/<int:pk>', views.doctor_update_medical_record_view, name='doctor-update-record'),


    path('patient-view-records', views.patient_view_records_view, name='patient-view-records'),


    path('assistant', views.assistant_view, name='assistant'),

    path('process_image/', views.process_image, name='process_image'),
    path('diagnose/', views.diagnose_view, name='diagnose'),
    path('submit-record/', views.submit_record, name='submit-record'),

]






#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders
