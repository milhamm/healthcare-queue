from xmlrpc.server import SimpleXMLRPCServer
# Import Redis
from redis import Redis
# Import Queue
from rq import Queue

import datetime

class ClinicService:
    """        
        - Buat queue kosong
        - Connect Redis
    """
    def __init__(self, q):
        self.total_patients = 0
        self.clinic = {
            1: {
                "name": "Klinik Umum",
                "queue": [],
                "in_queue": 0,
                "max_queue": 4
            },
            2: {
                "name": "Klinik Anak",
                "queue": [],
                "in_queue": 0,
                "max_queue": 5
            }
        }
        self.q = q
       
    
    def register(self, name, date_of_birth, clinic_id):
        """        
            Register the patient by name and date of birth
            Detail:
                - Create a patient_id based on the current queue
                - Check whether the queue is full
                - Insert the data to the queue (FIFO)
                - Update the klinik data (in_queue + 1)
                - Enqueue the remove_patient to the Task Queue (Redis)
                - return patient data
        """
        
        patient = {
            'patient_id': self.total_patients + 1,
            'name': name,
            'dob': date_of_birth
        } 
        self.total_patients += 1

        if self.clinic[clinic_id].in_queue == self.clinic[clinic_id].max_queue:
            print("Queue is full")
        else:
            self.clinic[clinic_id].queue.append(patient)
            self.clinic[clinic_id].in_queue += 1
            self.q.enqueue_in(datetime.timedelta(minutes=1), self.remove_patient, clinic_id)

        return patient

    def check_current_status(self, patient_id):
        """        
            Check the selected patient status
            Detail:
                - Find the patient based on patient_id 
                and calculate the estimated time
                - return queue, estimated_time
        """

        for key in self.clinic:
            for patient in self.clinic[key].queue:
                if patient.patient_id == patient_id:
                    queue = self.clinic[key].queue
                    estimated_time =0 #calculate estimated time

        return queue, estimated_time

    def show_clinics(self):
        available_clinics = []
        """        
        Find the available clinic (Queue not full)
        Detail:
            - Find the clinic that is not full
            - return 1 or more klinik
        """
        for key in self.clinic:
            if self.clinic[key].in_queue != self.clinic[key].max_queue:
                available_clinics.append(self.clinic[key])
        return available_clinics
    
    def remove_patient(self, clinic_id):
        """        
        Remove the patient when time is out
        Detail:
            - Find the clinic_id
            - Pop the first index
        """
        del self.clinic[clinic_id].queue[0]
        
        self.clinic[clinic_id].in_queue -= 1

# Main function
if __name__ == '__main__':
    q = Queue(connection=Redis(host='178.128.25.31', port=6379))

    server = SimpleXMLRPCServer(("localhost", 6969))
    server.register_introspection_functions()
    server.register_instance(ClinicService(q))
    server.serve_forever()