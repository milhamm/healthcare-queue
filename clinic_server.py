from xmlrpc.server import SimpleXMLRPCServer
from clinic_service import ClinicService
from xmlrpc.client import ServerProxy


class ClinicServer:
    def __init__(self, clinic_service):
        self.clinic_service = clinic_service

    def start(self):
        server = SimpleXMLRPCServer(("localhost", 6969), allow_none=True)
        server.register_introspection_functions()
        server.register_instance(self.clinic_service)
        print("Starting Clinic Server on Port 6969")
        server.serve_forever()


if __name__ == '__main__':
    queue_service = ServerProxy('http://localhost:6970', allow_none=True)
    service = ClinicService(queue_service)
    server = ClinicServer(service)
    server.start()
