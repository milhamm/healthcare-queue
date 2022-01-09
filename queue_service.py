from xmlrpc.client import ServerProxy
server = ServerProxy('http://localhost:6969', allow_none=True)

def remove_patient(clinic_id):
    print("Masuk Remove")
    server.remove_patient(clinic_id)
