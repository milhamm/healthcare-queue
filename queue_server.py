from xmlrpc.server import SimpleXMLRPCServer
from redis import Redis
from rq import Queue
import queue_service
from datetime import datetime


class QueueServer:
    def __init__(self, q):
        self.q = q
    
    def register(self, patient, clinic_id):
        converted = datetime.strptime(patient['etc'].value, "%Y%m%dT%H:%M:%S")
        if patient is not None:
            j = self.q.enqueue_at(converted, queue_service.remove_patient, clinic_id)
            print(f"Registered with job_id: {j.id}")
            return True
        return False

    def start(self):
        server = SimpleXMLRPCServer(("localhost", 6970), allow_none=True)
        server.register_introspection_functions()
        server.register_function(self.register)
        print("Starting Queue Server on Port 6970")
        server.serve_forever()


if __name__ == '__main__':
    queue = Queue(connection=Redis(host='178.128.25.31', port=6379))
    server = QueueServer(queue)
    server.start()
