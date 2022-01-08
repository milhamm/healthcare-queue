from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
# Import Redis
# Import Queue

class ClinicService:
    """        
        - Buat queue kosong
        - Connect Redis
    """
    def __init__(self):
        """ 
            klinik = {
                1: {
                    name: "Klinik Umum",
                    queue: [0, 1, 2, 3]
                    in_queue: 3,
                    max_queue: 4
                },
                2: {
                    name: "Klinik Anak",
                    queue: []
                    in_queue: 4,
                    max_queue: 4
                }
            }
        """
    
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
        available_klinik = []
        """        
        Find the available clinic (Queue not full)
        Detail:
            - Find the clinic that is not full
            - return 1 or more klinik
        """
        return available_klinik
    
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
    server = SimpleXMLRPCServer(("localhost", 6969))
    server.register_introspection_functions()
    server.register_instance(ClinicService())
    server.serve_forever()