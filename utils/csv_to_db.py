import csv
import os
from django.conf import settings
from bank.serializers import BankSerializer, BranchSerializer
from bank.models import Bank, Branch
from django.db import IntegrityError

def load_db():
    file_path = os.path.join(settings.STATIC_ROOT, "bank_csv.csv")
    
    with open(file_path, mode="r") as file:
        csv_reader = csv.reader(file)
        print(len(csv_reader),"this is length")
        return 
        failed_rows = []

        for row in csv_reader:
            bank_data = {
                "bank_id": row[1],
                "name": row[-1]
            }

            # Check if bank already exists
            bank = Bank.objects.filter(bank_id=row[1]).first()
            if not bank:
                bank_serializer = BankSerializer(data=bank_data)
                try:
                    bank_serializer.is_valid(raise_exception=True)
                    bank = bank_serializer.save()
                except Exception as e:
                    failed_rows.append((row, str(e)))
                    continue

            branch_data = {
                "ifsc_code": row[0],
                "bank": bank.uuid,
                "branch": row[2],
                "address": row[3],
                "city": row[4],
                "district": row[5],
                "state": row[6]
            }

            # Check if branch already exists
            branch_serializer = BranchSerializer(data=branch_data)
            try:
                branch_serializer.is_valid(raise_exception=True)
                branch_serializer.save()
            except IntegrityError as e:
                failed_rows.append((row, str(e)))
                continue
            except Exception as e:
                failed_rows.append((row, str(e)))
                continue

        if failed_rows:
            print(f"Failed to process {len(failed_rows)} rows.")
            for row, error in failed_rows:
                print(f"Row: {row} Error: {error}")
        return failed_rows

