# import pyrebase
import json
import firebase_admin
from firebase_admin import credentials, db
from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging


logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

app = NDNApp()

cred = credentials.Certificate("medical-record-7557a-firebase-adminsdk-bnaep-ee0229ec92.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://medical-record-7557a-default-rtdb.asia-southeast1.firebasedatabase.app"})


@app.route('/data/getuser')
def on_interest(name: FormalName, param: InterestParam, ap: Optional[BinaryStr]):
    nama_to_search = str(bytes(ap)).split('b\'')[1].split('\'')[0]
    print(f'>> I: {Name.to_str(name)}, {param}')
    
    # Get a reference to the root of the database
    root_ref = db.reference()

    # Get a reference to the "records" folder in the database
    records_ref = root_ref.child("records")

    # Read data from the "records" folder
    data = records_ref.get()

# Print the data or perform further processing.
# print(data)

# Check if data is not None (data exists)
    if data:
    # Input nama yang ingin Anda cari dari terminal
        # nama_to_search = input("Masukkan nama yang ingin Anda cari: ")

    # List untuk menyimpan data yang sesuai dengan nama yang dicari
        matching_records = []

        for record_id, record_data in data.items():
        # Access and check the "nama" parameter
            nama = record_data.get("nama")
            if nama and nama == nama_to_search:
             matching_records.append({
                #   "ID": record_id,
                  "Nama": record_data.get("nama"),
                  "Umur": record_data.get("umur"),
                  "Sex": record_data.get("sex"),
                  "Diagnosis": record_data.get("diagnosis"),
                  "DBP": record_data.get("DBP"),
                  "SBP": record_data.get("SBP"),
                })

    # Print or process the matching records
        if matching_records:
         print(f"Data yang terkait dengan nama '{nama_to_search}':")
         for record in matching_records:
            # Menggunakan json.dumps untuk mengubah data menjadi string format JSON
                record_str = json.dumps(record)
                print(record_str)
        else:
            print(f"Tidak ditemukan data dengan nama '{nama_to_search}'.")
    else:
        print("No data available in the 'records' folder.")

    content = f.encode()
    app.put_data(name, content=content, freshness_period=10000)
    print(f'<< D: {Name.to_str(name)}')
    print(MetaInfo(freshness_period=10000))
    print(f'Content: (size: {len(content)})')
    print('')

if __name__ == '__main__':
    app.run_forever()

# config = {
#     'apiKey': "AIzaSyBfwJoBt2kT0iOMjlDBw_heFaqjwjlp5ZU",
#     'authDomain': "medical-record-7557a.firebaseapp.com",
#     'databaseURL': "https://medical-record-7557a-default-rtdb.asia-southeast1.firebasedatabase.app",
#     'projectId': "medical-record-7557a",
#     'storageBucket': "medical-record-7557a.appspot.com",
#     'messagingSenderId': "973084416066",
#     'appId': "1:973084416066:web:50c8c2831db284a7e835db",
#     'measurementId': "G-MZ9NN8VEQZ"
# }

# cred = credentials.Certificate("medical-record-7557a-firebase-adminsdk-bnaep-ee0229ec92.json")
# firebase_admin.initialize_app(cred)


# firebase = pyrebase.initialize_app(config)
# db = firebase.database()
