import os
import django
import socket
import sqlite3
from django.conf import settings




# Specify the absolute path to your Django project directory
project_directory = 'D:\\HCIS\\current_repo\\Medical-Center-Server'
# Construct the path to the settings module
settings_path = os.path.join(project_directory, 'hospitalmanagement', 'settings.py') 
print("Path to settings.py:", settings_path)
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hospitalmanagement.settings")
# Call django.setup() to initialize Django
django.setup()


# Now you can import Django models
from hospital.models import Appointment  # Import the Appointment Model





# Function to extract information from the HL7 Message
def read_hl7_message(hl7_appointment):

    """
    Example of a SIU HL7 Message:
    
    MSH|^~\&|SendingApplication|SendingFacility|ReceivingApplication|ReceivingFacility|DateTime||SIU^S12|MessageControlID|P|2.3||||||
    SCH|ScheduleID^ScheduleID|||AppointmentID^AppointmentID|10345|AppointmentType^EventReason|AppointmentReason|AppointmentLocation|AppointmentDuration|m|^^ScheduledStartDateTime^ScheduledEndDateTime|||||OrderedBy^||||PerformedBy^|||||Scheduled
    PID|1||PatientID||PatientName||PatientDOB|PatientSex|||PatientAddress||PatientPhone|||PatientMaritalStatus||PatientSSN|||||||||||||||||||||
    PV1|1|O|||||AttendingDoctor|ReferringDoctor||||||||||||||||||||||||||||||||||||||||||VisitNumber||  => (Optional Segment)
    RGS|1|ResourceGroupType
    AIG|1|ResourceType|ResourceID|ResourceGroup^ResourceGroupName
    AIL|1|LocationType|Location^^^LocationDescription|LocationStartDateTime|||LocationDuration|m^Minutes||Scheduled
    AIP|1|PersonnelType|PersonnelID|PersonnelName||PersonnelStartDateTime|||PersonnelDuration|m^Minutes||Scheduled

    """

    # Cut the message into segments
    segments = hl7_appointment.split('\n')

    # Extract information from specific segments
    for segment in segments:
        if segment.startswith('MSH'):
            # Extract sending and receiving application and facility
            SendingApplication, SendingFacility, ReceivingApplication, ReceivingFacility, date_time, _ = segment.split('|')[2:8]
            print('SendingApplication:' , SendingApplication)
            print('SendingFacility:' , SendingFacility)
            print('ReceivingApplication:' , ReceivingApplication)
            print('ReceivingFacility:' , ReceivingFacility)
            print('date_time:' , date_time)

        elif segment.startswith('SCH'):
            # Extract patient information
            ScheduleID, _ , _ , AppointmentID, _ , AppointmentType_EventReason, AppointmentReason, AppointmentLocation, AppointmentDuration,\
            _ , ScheduledStartDateTime_ScheduledEndDateTime, _ , _ , _ , _ , OrderedBy, _ , _ , _ , PerformedBy = segment.split('|')[1:21]
            ScheduledStartDateTime, ScheduledEndDateTime = ScheduledStartDateTime_ScheduledEndDateTime.split('^')[2] , ScheduledStartDateTime_ScheduledEndDateTime.split('^')[3]
            print('ScheduleID:' , ScheduleID)
            print('EventReason:' , AppointmentType_EventReason.split('^')[1])
            print('OrderedBy:' , OrderedBy)
            print('PerformedBy:' , PerformedBy)
            print('AppointmentID:' , AppointmentID)
            print('AppointmentType:' , AppointmentType_EventReason.split('^')[0])
            print('AppointmentReason:' , AppointmentReason)
            print('AppointmentLocation:' , AppointmentLocation)
            print('AppointmentDuration:' , AppointmentDuration)
            print('ScheduledStartDateTime_ScheduledEndDateTime:' , ScheduledStartDateTime_ScheduledEndDateTime)
            print('ScheduledStartDateTime:' , ScheduledStartDateTime)
            print('ScheduledEndDateTime:' , ScheduledEndDateTime)
            

        elif segment.startswith('PID'):
            # Extract doctor information
            PatientID, _ , PatientName, _ , PatientDOB , PatientSex, _ , _ , PatientAddress, _ , PatientPhone, \
            _ , _ , PatientMaritalStatus, _ , PatientSSN = segment.split('|')[3:19]
            print('PatientID:' , PatientID)
            patient_first_name, patient_last_name = PatientName.split('^')
            print('PatientName_split:' , PatientName.split('^'))
            print('PatientDOB:' , PatientDOB)
            print('PatientSSN:' , PatientSSN)
            print('PatientSex:' , PatientSex)
            print('PatientPhone:' , PatientPhone)
            print('PatientAddress:' , PatientAddress)
            print('PatientMaritalStatus:' , PatientMaritalStatus)


        elif segment.startswith('RGS'):
            # Extract RGS information
            ResourceGroupType = segment.split('|')[2]
            print('ResourceGroupType:' , ResourceGroupType)


        elif segment.startswith('AIG'):
            # Extract AIG information
            ResourceType, ResourceID, ResourceGroup_ResourceGroupName = segment.split('|')[2:]
            print('ResourceID:' , ResourceID)
            print('ResourceType:' , ResourceType)
            print('ResourceGroup:' , ResourceGroup_ResourceGroupName.split('^')[0])
            print('ResourceGroupName:' , ResourceGroup_ResourceGroupName.split('^')[1])
            print('ResourceGroup_ResourceGroupName:' , ResourceGroup_ResourceGroupName)

        
        elif segment.startswith('AIL'):
            # Extract AILinformation
            LocationType, Location_LocationDescription, LocationStartDateTime, _ , _ , LocationDuration = segment.split('|')[2:8]
            print('LocationType:' , LocationType)
            doctor_first_name, doctor_last_name = Location_LocationDescription.split('^^^')
            print('LocationStartDateTime:' , LocationStartDateTime)
            print('LocationDuration:' , LocationDuration)
            print('Location_LocationDescription:' , Location_LocationDescription)


        elif segment.startswith('AIP'):
            # Extract AIP information
            PersonnelType, PersonnelID, PersonnelName, _ , PersonnelStartDateTime, _ , _ , PersonnelDuration = segment.split('|')[2:10]
            doctor_first_name, doctor_last_name = PersonnelName.split('^')
            print('PersonnelType:' , PersonnelType)
            print('PersonnelType:' , PersonnelID)
            print('PersonnelFirstName:' , doctor_first_name)
            print('PersonnelLastName:' , doctor_last_name)
            print('PersonnelType:' , PersonnelStartDateTime)
            print('PersonnelType:' , PersonnelDuration)
            




    # Return extracted information
    return {
        'date_time': ScheduledStartDateTime,
        'patient_id': PatientID,
        'patient_first_name': patient_first_name,
        'patient_last_name': patient_last_name,
        'doctor_id': PersonnelID,
        'doctor_first_name': doctor_first_name,
        'doctor_last_name': doctor_last_name,
        'reason': AppointmentReason,
        'appointment_id': AppointmentID,
    }




HOST = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOST)
print("Hostname:", HOST)
print("IP Address:", IP_ADDRESS)


# Server IP address and port
#HOST = '127.0.0.1'   # Listen on all available interfaces => '0.0.0.0'  , 
PORT = 8000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server IP and port
# server_socket.bind((HOST, PORT))
server_socket.bind((IP_ADDRESS, PORT))

# Listen for incoming connections
server_socket.listen()
print("Server is listening for incoming connections...")


while True:

    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from '{client_address}' has been established.")

    # Receive HL7 message
    hl7_message = client_socket.recv(1024).decode()
    print('Received HL7 Message: ', hl7_message)

    # Parse the HL7 message
    appointment_data = read_hl7_message(hl7_message)
    print('The Parsed Appointment Data: ', appointment_data)


    appointment_date = appointment_data['date_time'].split(' ')[0]
    appointment_time = appointment_data['date_time'].split(' ')[1]
    patient_full_name = appointment_data['patient_first_name'] + appointment_data['patient_last_name']
    doctor_full_name = appointment_data['doctor_first_name'] + appointment_data['doctor_last_name']


    # Create an Appointment object
    appointment = Appointment(id=int(appointment_data['appointment_id'].split('^')[0]), patientId=int(appointment_data['patient_id']), \
                              doctorId=int(appointment_data['doctor_id']), patientName=patient_full_name, doctorName=doctor_full_name, \
                              appointmentDate=appointment_date, appointmentTime=appointment_time, description=appointment_data['reason'], status=False\
                            )

    # Save the object to the database
    appointment.save()
    print("Appointment Details saved to the database.")



    # Close the connection
    client_socket.close()










# Save appointment data to SQLite database
# Establish a connection with the SQLite database
#conn = sqlite3.connect('db.sqlite3')
#cursor = conn.cursor()
# Insert appointment data into the database
#cursor.execute("INSERT INTO hospital_appointment (id, patientId, doctorId, patientName, doctorName, appointmentDate, appointmentTime, description, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                #(int(appointment_data['appointment_id'].split('^')[0]), int(appointment_data['patient_id']), int(appointment_data['doctor_id']), patient_full_name, doctor_full_name, appointment_date, appointment_time, appointment_data['reason'], False))
# Commit changes and close connection to database
#conn.commit()
#cursor.close()
#conn.close()
# Save to the database
# appointment = Appointment(patient_name=patient_name, appointment_date=appointment_date)
# appointment.save()
#print("Appointment Details saved to the database.")