from datetime import datetime, timedelta

class ClinicService:
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
       
    def create_patient(self, name, date_of_birth, clinic_id):
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
        if len(self.clinic[clinic_id]["queue"]) == 0:
            etc = datetime.now() + timedelta(seconds=20)
        else:
            etc = self.clinic[clinic_id]["queue"][-1]["etc"] + timedelta(seconds=20)

        patient = {
            'patient_id': self.total_patients + 1,
            'name': name,
            'dob': date_of_birth,
            'etc': etc
        }

        self.total_patients += 1

        if self.clinic[clinic_id]["in_queue"] == self.clinic[clinic_id]["max_queue"]:
            print("Queue is full")
        else:
            self.clinic[clinic_id]["queue"].append(patient)
            self.clinic[clinic_id]["in_queue"] += 1
            
        return patient

    def check_current_status(self, patient_id):
        """        
            Check the selected patient status
            Detail:
                - Find the patient based on patient_id 
                and calculate the estimated time
                - return queue, estimated_time
        """

        print(self.clinic)
        for key in self.clinic:
            for patient in self.clinic[key]["queue"]:
                if patient["patient_id"] == patient_id:
                    return {
                        "queue": self.clinic[key]["queue"], 
                        "etc_in_seconds": (patient["etc"] - datetime.now()).seconds
                    }
        return {
            "queue": None,
            "etc_in_seconds": None
        }

    def show_clinics(self):
        available_clinics = []
        """        
        Find the available clinic (Queue not full)
        Detail:
            - Find the clinic that is not full
            - return 1 or more klinik
        """
        for key in self.clinic:
            if self.clinic[key]["in_queue"] != self.clinic[key]["max_queue"]:
                available_clinics.append(self.clinic[key])
        return available_clinics
    
    def remove_patient(self, clinic_id):
        """        
        Remove the patient when time is out
        Detail:
            - Find the clinic_id
            - Pop the first index
        """
        self.clinic[clinic_id]["queue"].pop(0)
        self.clinic[clinic_id]["in_queue"] -= 1
