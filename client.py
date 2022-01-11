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
    return (etc - datetime.now()).seconds

def print_queue(queue):
    if len(queue) == 0:
        print("Empty Queue")
    else:
        print("| {:<8} | {:<15} | {:<12} | {:12} |"
              .format("PID",
                      "Patient Name",
                      "Birthdate",
                      "Completed In"))
        print(f"{'-' * 60}")
        for patient in queue:
            converted = datetime.strptime(patient['etc'].value, "%Y%m%dT%H:%M:%S")
            etc_time = calculate_estimated(converted)
            etc_minutes = etc_time // 60
            etc_seconds = etc_time % 60

            print("| {:<8} | {:<15} | {:<12} | {:12} |"
                  .format(patient['patient_id'],
                          patient['name'],
                          patient['dob'],
                          f"{etc_minutes}m {etc_seconds}s left"))
        print(f"{'-'*60}\n")

def print_clinic(clinics):
    ids = 1
    for clinic in clinics:
        print(f"ID\t\t\t: {ids}")
        print(f"Name\t\t: {clinic['name']}")
        print(f"Capacity\t: {clinic['in_queue']}/{clinic['max_queue']}")
        print("{} {:<18} {}".format('-'*19, f"{clinic['name']}'s Queue", '-'*19))
        print_queue(clinic['queue'])
        ids += 1


class Client:
    def __init__(self, host):
        self.clinic_service = ServerProxy(f"{host}:6969")
        self.queue_service = ServerProxy(f"{host}:6970")

    def show_clinic(self):
        return self.clinic_service.show_clinics()

    def register_patient(self):
        name = input("Patient name: ")
        dob = input("Date of birth: ")
        clinic_id = input_number(
            message="Clinic ID: ",
            ranges=range(1, 3),
            error_message="Invalid Clinic ID")

        patient = self.queue_service.register(name, dob, clinic_id)
        print(patient)

    def check_status(self):
        return

    def menu(self, options):
        if options == 1:
            clinics = self.show_clinic()
            print("-- Clinics Available --")
            print_clinic(clinics)
        elif options == 2:
            print("-- Register Patient --")
            self.register_patient()

    def start(self):
        print("Parallel & Distributed System Final Project")
        print("Group 1 - Healthcare Queue")

        while True:
            print("Menu\n"
                  "1. Show Available Clinics\n"
                  "2. Register Patient\n"
                  "3. Check Patient Status\n"
                  "4. Exit")

            option = input_number(
                message="Selection: ",
                ranges=range(1, 5),
                error_message="Please enter a valid input")

            if option == 4:
                break

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
    client = Client('http://localhost')
    client.start()
