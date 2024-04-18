from django.db import models

# Create your models here.

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()  
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)  # Adjust max_length as needed
    ssn = models.CharField(max_length=9)  # Assuming Social Security Number is 9 digits
    password = models.CharField(max_length=128)  # Storing password hashes
    patient_id = models.AutoField(primary_key=True)


# Can only be accessed by the admin
class Doctor(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()  
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)  # Adjust max_length as needed
    ssn = models.CharField(max_length=9)  # Assuming Social Security Number is 9 digits
    password = models.CharField(max_length=128)  # Storing password hashes
    doctor_id = models.AutoField(primary_key=True)
    specialty = models.CharField(max_length=100)



class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    


class MedicalRecord(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='medical_records', null=True, blank=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
   

