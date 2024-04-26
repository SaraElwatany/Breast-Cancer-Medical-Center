import socket

def send_hl7_message(host, port, hl7_message):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))

        # Send the HL7 message
        client_socket.sendall(hl7_message.encode('utf-8'))

# Example usage
hl7_message = "MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|201301011226||ADT^A01|HL7MSG00001|P|2.3"
send_hl7_message('127.0.0.1', 8000, hl7_message)
