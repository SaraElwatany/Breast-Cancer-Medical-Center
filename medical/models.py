import uuid
from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    dob = models.DateField(default="2000-01-01")  # Default date, adjust as needed
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    email = models.EmailField(default="")
    phone_number = models.CharField(max_length=15, default="")  
    ssn = models.CharField(max_length=9, default="")  
    password = models.CharField(max_length=128, default="")  
    patient_id = models.AutoField(primary_key=True, default=1)


class Doctor(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    dob = models.DateField(default="2000-01-01")  
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    email = models.EmailField(default="")
    phone_number = models.CharField(max_length=15, default="")  
    ssn = models.CharField(max_length=9, default="")  
    password = models.CharField(max_length=128, default="")  
    doctor_id = models.AutoField(primary_key=True, default=1)
    specialty = models.CharField(max_length=100, default="")


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    appointment_id = models.AutoField(primary_key=True, default=1)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    date = models.DateField(default="2000-01-01")  # Default date, adjust as needed
    time = models.TimeField(default="00:00")  # Default time, adjust as needed


class MedicalRecord(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='medical_records', null=True, blank=True)
    diagnosis = models.TextField(default="")
    treatment = models.TextField(default="")

   

