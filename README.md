<h1>Bank API</h1>

<p>This is the README file for the Bank API project. This project is built using Django and Django REST Framework. It provides endpoints for managing banks and their branches.</p>

<h2>Table of Contents</h2>

<ul>
  <li><a href="#installation">Installation</a></li>
  <li><a href="#endpoints">Endpoints</a></li>
  <ul>
    <li><a href="#load-database">Load Database</a></li>
    <li><a href="#get-all-banks">Get All Banks</a></li>
    <li><a href="#get-bank-detail">Get Bank Detail</a></li>
    <li><a href="#get-all-branches">Get All Branches</a></li>
    <li><a href="#get-branches-of-a-bank">Get Branches of a Bank</a></li>
    <li><a href="#get-branch-detail">Get Branch Detail</a></li>
  </ul>
  <li><a href="#data-load-procedure">Data Load Procedure</a></li>
  <li><a href="#response-codes">Response Codes</a></li>
</ul>

<h2 id="installation">Installation</h2>

<p>1. Clone the repository:<br>
<code>git clone &lt;repository_url&gt;</code></p>

<p>2. Install the dependencies:<br>
<code>pip install -r requirements.txt</code></p>

<p>3. Run the migrations:<br>
<code>python manage.py migrate</code></p>

<p>4. Start the development server:<br>
<code>python manage.py runserver</code></p>

<h2 id="endpoints">Endpoints</h2>

<h3 id="load-database">Load Database</h3>

<p><b>URL:</b> /load-db/</p>
<p><b>Method:</b> GET</p>
<p><b>Description:</b> Loads the database with data from a CSV file.</p>
<p><b>Response:</b></p>

<pre><code>{
  "message": "Data loaded successfully.",
  "failed_rows": [
    {
      "row": ["row_data"],
      "error": "Error description"
    }
  ]
}
</code></pre>

<h3 id="get-all-banks">Get All Banks</h3>

<p><b>URL:</b> /banks/</p>
<p><b>Method:</b> GET</p>
<p><b>Description:</b> Retrieves a list of all banks.</p>
<p><b>Response:</b></p>

<pre><code>[
  {
    "uuid": "bank_uuid",
    "name": "Bank Name",
    "bank_id": "Bank ID"
  },
  ...
]
</code></pre>

<h3 id="get-bank-detail">Get Bank Detail</h3>

<p><b>URL:</b> /banks/&lt;uuid:uuid&gt;/</p>
<p><b>Method:</b> GET</p>
<p><b>Description:</b> Retrieves details of a specific bank by UUID.</p>
<p><b>Response:</b></p>

<pre><code>{
  "uuid": "bank_uuid",
  "name": "Bank Name",
  "bank_id": "Bank ID"
}
</code></pre>

<h3 id="get-all-branches">Get All Branches</h3>

<p><b>URL:</b> /all/branches/</p>
<p><b>Method:</b> GET</p>
<p><b>Description:</b> Retrieves a list of all branches with pagination.</p>
<p><b>Query Parameters:</b> page (optional, for pagination)</p>
<p><b>Response:</b></p>

<pre><code>[
  {
    "uuid": "branch_uuid",
    "ifsc_code": "IFSC Code",
    "bank": "Bank UUID",
    "branch": "Branch Name",
    "address": "Address",
    "city": "City",
    "district": "District",
    "state": "State"
  },
  ...
]
</code></pre>

<h3 id="get-branches-of-a-bank">Get Branches of a Bank</h3>

<p><b>URL:</b> /branches/&lt;uuid:uuid&gt;/bank/</p>
<p><b>Method:</b> GET</p>
<p><b>Description:</b> Retrieves a list of all branches for a specific bank by bank UUID.</p>
<p><b>Response:</b></p>

<pre><code>[
  {
    "uuid": "branch_uuid",
    "ifsc_code": "IFSC Code",
    "bank": "Bank UUID",
    "branch": "Branch Name",
    "address": "Address",
    "city": "City",
    "district": "District",
    "state": "State"
  },
  ...
]
</code></pre>

<h3 id="get-branch-detail">Get Branch Detail</h3>

<p><b>URL:</b> /branches/&lt;uuid:uuid&gt;/</p>
<p><b>Method:</b> GET</p>
<p><b>Description:</b> Retrieves details of a specific branch by UUID.</p>
<p><b>Response:</b></p>

<pre><code>{
  "uuid": "branch_uuid",
  "ifsc_code": "IFSC Code",
  "bank": "Bank UUID",
  "branch": "Branch Name",
  "address": "Address",
  "city": "City",
  "district": "District",
  "state": "State"
}
</code></pre>

<h2 id="data-load-procedure">Data Load Procedure</h2>

<p>The data load procedure is handled by the <code>load_db</code> function. This function reads a CSV file located in the <code>STATIC_ROOT</code> directory and loads the data into the database.</p>

<p>1. The function reads the CSV file and iterates over each row.<br>
2. For each row, it first checks if the bank exists in the database. If not, it creates a new bank entry.<br>
3. It then creates a new branch entry associated with the bank.<br>
4. If any errors occur during the process, the row and the error message are stored in the <code>failed_rows</code> list.<br>
5. The function returns a list of failed rows, if any.</p>

<p>Here is the implementation of the <code>load_db</code> function:</p>

<pre><code>import csv
import os
from django.conf import settings
from bank.serializers import BankSerializer, BranchSerializer
from bank.models import Bank, Branch
from django.db import IntegrityError

def load_db():
    file_path = os.path.join(settings.STATIC_ROOT, "bank_csv.csv")
    
    with open(file_path, mode="r") as file:
        csv_reader = csv.reader(file)
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
</code></pre>

<h2 id="response-codes">Response Codes</h2>

<p>The project uses custom response functions to standardize the API responses.</p>

<p><b>HTTP_200:</b> OK<br>
<b>HTTP_201:</b> Created<br>
<b>HTTP_400:</b> Bad Request<br>
<b>HTTP_404:</b> Not Found</p>

<p>Here are the implementations of the response functions:</p>

<pre><code>from rest_framework import status
from rest_framework.response import Response

def HTTP_200(data):
    if not isinstance(data, dict):
        data = {"message": data}
    return Response(data=data, status=status.HTTP_200_OK)

def HTTP_201(data):
    if not isinstance(data, dict):
        data = {"message": data}
    return Response(data=data, status=status.HTTP_201_CREATED)

def HTTP_400(data):
    if not isinstance(data, dict):
        data = {"message": data}
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

def HTTP_404(data):
    if not isinstance(data, dict):
        data = {"message": data}
    return Response(data=data, status=status.HTTP_404_NOT_FOUND)

</code></pre>

<p>These functions ensure that the API responses are consistent and follow RESTful conventions.</p>
