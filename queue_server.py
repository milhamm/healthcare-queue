from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from redis import Redis
from rq import Queue
import queue_service

class QueueServer:
    def __init__(self, q, clinic_service):
        self.clinic_service = clinic_service
        self.queue_service = queue_service
        self.q = q
    
    def register(self, name, date_of_birth, clinic_id):
        patient = self.clinic_service.create_patient(name, date_of_birth, clinic_id)
        print(f"A new patient has been registered: {patient}")
        j = self.q.enqueue_at(patient["etc"], queue_service.remove_patient, clinic_id)
        print(f"Registered with job_id: {j.id}")

    def start(self):
        server = SimpleXMLRPCServer(("localhost", 6970), allow_none=True)
        server.register_introspection_functions()
        server.register_function(self.register)
        print("Starting Queue Server on Port 6970")
        server.serve_forever()

if __name__ == '__main__':
    clinic_service = ServerProxy('http://localhost:6969', allow_none=True, use_datetime=True)
    queue = Queue(connection=Redis(host='178.128.25.31', port=6379))
    server = QueueServer(queue, clinic_service)
    server.start()