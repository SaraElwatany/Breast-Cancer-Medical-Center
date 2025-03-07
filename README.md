# Mammocare - A Breast Cancer Medical Center Web Application 🩺
This repository contains the implementation of a Breast Cancer Medical Center Web Application, designed to serve both client (patient) and server (doctors/admin) sides.


## Abstract

This project replicates a hospital management system with an innovative Clinical Decision Support System (CDSS) to facilitate the decision-making process. Patients can store their medical records in the database, which are also transmitted to the server side for interpretation and diagnosis by doctors. Medical records are transmitted using the HL7 protocol for secure medical data encoding. Doctors can diagnose breast DICOM images, with the CDSS acting as a second reader to assist in the decision-making process.

### Server Side:

- Manage appointments, doctors, and patients with full database operations (add, update, delete).
- Upload DICOM medical images and receive support from the Decision Support System (DSS) that classifies images as normal, benign, malignant, etc.


### Client Side:

- Book and track appointments easily.
- Access personal medical data and history.


## Demo
https://github.com/user-attachments/assets/3fe6b33a-c835-49b1-86b0-87f925af7477


## Snapshots

### - Example on HL7 Message
![HL7 - Mess](https://github.com/user-attachments/assets/348cfd14-8f35-49c1-b970-6d9c607f3882)

### - Home Page
![Homepage](https://github.com/user-attachments/assets/b6e21343-c3a4-4a16-a961-517a6e7613e6)

### - Login Page
![Login](https://github.com/user-attachments/assets/319d662f-ece3-46f8-adf8-b9c3a5b9b81b)

### - Admin Portal
![Admin Portal](https://github.com/user-attachments/assets/ee4da449-30c8-48e6-bc7d-21c1e75b471a)

### - Patient Portal
![Patient Portal](https://github.com/user-attachments/assets/85db3024-c7c8-42d4-b5b0-eff4171bdfd7)

### - Doctor Portal
![Doctor Portal](https://github.com/user-attachments/assets/417f1cc0-fe31-46dd-b65e-7db65ac814f6)

### - CDSS 
![CDSS](https://github.com/user-attachments/assets/64d8427c-1ea1-47f8-baa0-419f278401a0)


This project aims to provide an efficient and accurate platform for medical diagnosis and patient management.


## Repository Contents

1- Medical-Center-Client: A folder which includes the client side for the project.

2- Medical-Center-Server: A folder which includes the server side for the project.

3- Breast_Cancer_Detection.ipynb: Python Notebook for the steps included in the model development stages.

4- HCIS_Breas Cancer Detection Using Tomosenthesis.docx: A document file which includes details about the dataset used in the project for the classification task.

### Disclaimer:
I used this repository as a base for my initial system design, including Django views, HTML templates, databases, and other foundational components: [Hospital Management System by sumitkumar1503](https://github.com/sumitkumar1503/hospitalmanagement)
