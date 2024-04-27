# import socket

# def send_hl7_message(host, port, hl7_message):
#     # Create a TCP/IP socket
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#         # Connect to the server
#         client_socket.connect((host, port))

#         # Send the HL7 message
#         client_socket.sendall(hl7_message.encode('utf-8'))

# # Example usage
# hl7_message = "MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|201301011226||ADT^A01|HL7MSG00001|P|2.3"
# send_hl7_message('127.0.0.1', 8000, hl7_message)



# ---------------------------- Another HL7 Message ----------------------------
import socket

def send_hl7_message(host, port, hl7_message):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))

        # Send the HL7 message
        client_socket.sendall(hl7_message.encode('utf-8'))

# Example usage
hl7_message_adt_a04 = """\
MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|202404271200||ADT^A04|HL7MSG00004|P|2.5
PID|1|123456|789012|Doe^John^^Mr.|Doe^Jane^^Mrs.|19800101|M|||123 Main St.^Springfield^IL^12345^USA||(555)555-5555|(555)555-1234|johndoe@example.com
PV1|1|I|200^201^01|||123^Smith^John^Dr.^MD|||IN|||1|123456^Smith^John^Dr.^MD||ADM|A0|"""

send_hl7_message('127.0.0.1', 8000, hl7_message_adt_a04)


