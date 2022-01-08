# Import XMLRPC
# Import Redis
# Import Queue

class KlinikService:
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
            'patient_id': 0000, # Mbuh mau digenerate make apa
            'name': name,
            'dob': date_of_birth
        }  

        if self.clinic[clinic_id].in_queue == self.clinic[clinic_id].max_queue:
            print("Queue is full")
        else:
            self.clinic[clinic_id].queue.append(patient)
            self.clinic[clinic_id].in_queue += 1
            self.q.enqueue()

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
                    estimated_time = #calculate estimated time

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

# Main function
if __name__ == '__main__':
    # Create XMLRPC Server
    testttt
    # Register KlinikService instance

    # Serve forever 