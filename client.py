from xmlrpc.client import ServerProxy
from datetime import datetime


def input_number(message, ranges, error_message):
    while True:
        payload = input(message)
        if payload.isdigit():
            if int(payload) in ranges:
                return int(payload)
            else:
                print(error_message)
        else:
            print("Number only")


def calculate_estimated(etc):
    estimated = (etc - datetime.now()).seconds
    if estimated >= 300:
        return None
    return estimated


def convert_to_minutes_and_seconds(etc_time):
    return etc_time // 60, etc_time % 60


def get_estimated_string(patient):
    converted = datetime.strptime(patient['etc'].value, "%Y%m%dT%H:%M:%S")
    etc_time = calculate_estimated(converted)
    if etc_time is None:
        etc_string = "Soon"
    else:
        etc_minutes, etc_seconds = convert_to_minutes_and_seconds(etc_time)
        etc_string = f"{etc_minutes}m {etc_seconds}s left"
    return etc_string


def print_queue(queue):
    if len(queue) == 0:
        print("Empty Queue")
    else:
        print("| {:<8} | {:<15} | {:<12} | {:14} |"
              .format("PID",
                      "Patient Name",
                      "Birthdate",
                      "Completed In"))
        print(f"{'-' * 60}")
        for patient in queue:
            etc_string = get_estimated_string(patient)
            print("| {:>8} | {:<15} | {:<12} | {:14} |"
                  .format(patient['patient_id'],
                          patient['name'],
                          patient['dob'],
                          etc_string))
        print(f"{'-'*62}\n")


def print_clinic(clinics):
    ids = 1
    for clinic in clinics:
        print(f"ID\t\t\t: {ids}")
        print(f"Name\t\t: {clinic['name']}")
        print(f"Capacity\t: {clinic['in_queue']}/{clinic['max_queue']}")
        print("{} {:<18} {}".format('-'*19, f"{clinic['name']}'s Queue", '-'*19))
        print_queue(clinic['queue'])
        ids += 1


def print_patient(patient):
    etc_string = get_estimated_string(patient)
    print(f"{'-' * 62}")
    print("| {:<8} | {:<15} | {:<12} | {:14} |"
          .format("PID",
                  "Patient Name",
                  "Birthdate",
                  "Completed In"))
    print(f"{'-' * 60}")
    print("| {:>8} | {:<15} | {:<12} | {:14} |"
          .format(patient['patient_id'],
                  patient['name'],
                  patient['dob'],
                  etc_string))
    print(f"{'-' * 62}\n")


class Client:
    def __init__(self, host):
        self.clinic_service = ServerProxy(f"{host}", allow_none=True)

    def show_clinic(self):
        return self.clinic_service.show_clinics()

    def show_all_clinic(self):
        return self.clinic_service.show_all_clinics()

    def register_patient(self):
        name = input("Patient name: ")
        dob = input("Date of birth: ")
        clinic_id = input_number(
            message="Clinic ID: ",
            ranges=range(1, 3),
            error_message="Invalid Clinic ID")

        patient = self.clinic_service.register(name, dob, clinic_id)
        if patient is None:
            print("Queue is full")

        print("Register Success")
        print_patient(patient)

    def check_status(self):
        patient_id = input_number(
            "Patient ID: ", range(0, 999), "Not a valid Patient ID")
        patient = self.clinic_service.check_current_status(patient_id)
        if patient is None:
            print("Not Found\n")
            return
        print_patient(patient['patient'])

    def menu(self, options):
        if options == 1:
            clinics = self.show_clinic()
            print("-- Clinics Available --")
            print_clinic(clinics)
        elif options == 2:
            clinics = self.show_all_clinic()
            print("-- All Clinics --")
            print_clinic(clinics)
        elif options == 3:
            print("-- Register Patient --")
            self.register_patient()
        elif options == 4:
            print("-- Patient Status --")
            self.check_status()
        else:
            exit(0)

    def start(self):
        print("Parallel & Distributed System Final Project")
        print("Group 1 - Healthcare Queue")

        while True:
            print("Menu\n"
                  "1. Show Available Clinics\n"
                  "2. Show All Clinics\n"
                  "3. Register Patient\n"
                  "4. Check Patient Status\n"
                  "5. Exit")

            option = input_number(
                message="Selection: ",
                ranges=range(1, 6),
                error_message="Please enter a valid input")

            self.menu(option)


if __name__ == '__main__':
    """Main Client Function
    Detail:
    - Connect RPC 
    - Main menu
        1. Show Klinik (show_clinics)
        2. Register Patient (register)
        3. Check Status of a Patient (check_current_status)
        4. Exit
    """
    client = Client('http://localhost:6969')
    client.start()
