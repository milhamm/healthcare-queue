# Import XMLRPC
# Import Redis
from redis import Redis
# Import Queue
from rq import Queue

class KlinikService:
    """        
        - Buat queue kosong
        - Connect Redis
    """
    def __init__(self):
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
        self.q = Queue(Redis('178.128.25.31'))
       
    
    def register(self, name, date_of_birth, clinic_id):
        patient = {
            'patient_id': 0000, # Mbuh mau digenerate make apa
            'name': name,
            'dob': date_of_birth
        }   
        
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
        return patient

    def check_current_status(self, patient_id):
        """        
        Check the selected patient status
        Detail:
            - Find the patient based on patient_id 
            and calculate the estimated time
            - return queue, estimated_time
        """
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

# Main function
if __name__ == '__main__':
    # Create XMLRPC Server
    testttt
    # Register KlinikService instance

    # Serve forever 