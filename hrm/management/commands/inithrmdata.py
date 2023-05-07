'''
Initial data loading into HRM models
    1. Load Employee, BankDatabase **no dependents
    2. Load EmployeeBankAccount, EmployeeBenefitAccount
'''

import os
import csv
import django
from django.core.management.base import BaseCommand
import datetime as dt
# import your Django models here
from hrm.models import Employee, EmployeeBenefitAccount, EmployeeBankAccount
from core.models import BankDatabase
# set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "businessmanagement.settings")
django.setup()


class Command(BaseCommand):
    help = 'Loads initial data for the HRM app.'

    def handle(self, *args, **options): 
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        # open your CSV files here
        employee_file = open(data_path+'/employee.csv', 'r')
        employee_benefit_file = open(data_path+'/employeebenefitaccount.csv', 'r')
        employee_bank_file = open(data_path+'/employeebankaccount.csv', 'r')
        bank_file = open(data_path+'/bankdatabase.csv', 'r')

        # load your CSV files into Django models here
        employee_reader = csv.DictReader(employee_file)
        for row in employee_reader:
            if not Employee.objects.filter(emp_name=row['emp_name']).exists():
                employee = Employee(
                    emp_name = row['emp_name'],
                    emp_dob = dt.datetime.strptime(row['emp_dob'], "%d/%m/%Y").date(),
                    emp_address = row['emp_address'],
                    emp_nric = row['emp_nric'],
                    emp_phone_num = row['emp_phone_num'],
                    emp_salary = row['emp_salary']
                )
                employee.save()

        bank_reader = csv.DictReader(bank_file)
        for row in bank_reader:
            if not BankDatabase.objects.filter(bank_name=row['bank_name']).exists():
                bank = BankDatabase(
                    bank_name = row['bank_name'],
                    bank_swift_code = row['bank_swift_code'],
                    bank_city = row['bank_city']
                )
                bank.save()

        employee_benefit_reader = csv.DictReader(employee_benefit_file)
        for row in employee_benefit_reader:
            if not EmployeeBenefitAccount.objects.filter(benefit_acc_num=row['benefit_acc_num']).exists():
                emp = Employee.objects.get(emp_name=row.pop('name'))
                employee_benefit = EmployeeBenefitAccount(
                    benefit_acc_name = row['benefit_acc_name'],
                    benefit_acc_type = row['benefit_acc_type'],
                    benefit_acc_num = row['benefit_acc_num'],
                    emp = emp
                )
                employee_benefit.save()

        employee_bank_reader = csv.DictReader(employee_bank_file)
        for row in employee_bank_reader:
            emp = Employee.objects.get(emp_name=row.pop('name'))
            bank = BankDatabase.objects.get(bank_swift_code=row.pop('bank_routing_num'))
            employee_bank = EmployeeBankAccount(
                bank = bank,
                bank_acc_num = row['bank_acc_num'],
                bank_acc_type = row['bank_acc_type'],
                emp = emp
            )
            employee_bank.save()

        # close your CSV files here
        employee_file.close()
        employee_benefit_file.close()
        employee_bank_file.close()
        bank_file.close()

        # print a message to indicate that the data has been loaded
        print("Data has been loaded.")
