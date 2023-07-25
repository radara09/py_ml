import json
import firebase_admin
from firebase_admin import credentials, db
from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging

cred = credentials.Certificate("medical-record-7557a-firebase-adminsdk-bnaep-ee0229ec92.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://medical-record-7557a-default-rtdb.asia-southeast1.firebasedatabase.app"})

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

app = NDNApp()

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
# Check if data is not None (data exists)
    if data:
    # Input nama yang ingin Anda cari dari terminal
        # nama_to_search = input("Masukkan nama yang ingin Anda cari: ")
    # List untuk menyimpan data yang sesuai dengan nama yang dicari
        matching_records = []
        for record_id, record_data in data.items():
        # Access and check the "nama" parameter
            #print(record_data)
            nama = record_data.get("nama")
            if nama and nama == nama_to_search:
             matching_records.append({
                #   "ID": record_id,
                  "Nama": record_data.get("nama"),
                  "Umur": record_data.get("umur"),
                  "Sex": record_data.get("sex"),
                  "Diagnosis": record_data.get("Diagnosis"),
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
    
    content = record_str.encode()
    app.put_data(name, content=content, freshness_period=10000)
    print(f'<< D: {Name.to_str(name)}')
    print(MetaInfo(freshness_period=10000))
    print(f'Content: (size: {len(content)})')
    print('')


@app.route('/data/adduser')
def on_data(name: FormalName, param: InterestParam, ap: Optional[BinaryStr]):
    data_to_save = str(bytes(ap)).split('b\'')[1].split('\'')[0]
    print(f'>> I: {Name.to_str(name)}, {param}')
    print(data_to_save)
    # Mendapatkan data dari body permintaan
    # data = request.get_json()

    data_dict = json.loads(data_to_save)
    #data = json.dumps(data_dict)

    # Simpan data ke Firebase Realtime Database
    records_ref = db.reference('records')  # Ganti 'records' sesuai dengan nama folder Anda di database
    new_record_ref = records_ref.push(data_dict)
    response_data = {"record_id": new_record_ref.key}
    print(response_data)
    content = str(response_data).encode()
    app.put_data(name, content=content, freshness_period=5000)
    print(f'<< D: {Name.to_str(name)}')
    print(MetaInfo(freshness_period=10000))
    print(f'Content: (size: {len(content)})')
    response_data = {"record_id": new_record_ref.key}
    print('')

    # # Lakukan pemrosesan data di sini (misalnya menyimpan data ke database atau melakukan tindakan lainnya)
    # print(data)
    # return jsonify({"message": "Data berhasil diterima di server backend Python."})


@app.route('/data/alluser')
def on_interest(name: FormalName, param: InterestParam, ap: Optional[BinaryStr]):
    all_data = str(bytes(ap)).split('b\'')[1].split('\'')[0]
    print(f'>> I: {Name.to_str(name)}, {param}')
    
    # Get a reference to the root of the database
    root_ref = db.reference()
    # Get a reference to the "records" folder in the database
    records_ref = root_ref.child("records")
    # Read data from the "records" folder
    data = records_ref.get()
# Check if data is not None (data exists)
    if data:
    # Input nama yang ingin Anda cari dari terminal
        # nama_to_search = input("Masukkan nama yang ingin Anda cari: ")
    # List untuk menyimpan data yang sesuai dengan nama yang dicari
        matching_records = []
        for record_id, record_data in data.items():
        # Access and check the "nama" parameter
            #print(record_data)
            nama = record_data.get("nama")
            if nama and nama == all_data:
             matching_records.append({
                #   "ID": record_id,
                  "Nama": record_data.get("nama"),
                  "Umur": record_data.get("umur"),
                  "noPasien": record_data.get("sex"),
                })

    # Print or process the matching records
        if matching_records:
         print(f"Data yang terkait dengan nama '{all_data}':")
         for record in matching_records:
            # Menggunakan json.dumps untuk mengubah data menjadi string format JSON
                record_str = json.dumps(record)
                print(record_str)
        else:
            print(f"Tidak ditemukan data '{all_data}'.")
    else:
        print("No data available in the 'records' folder.")
    
    content = record_str.encode()
    app.put_data(name, content=content, freshness_period=10000)
    print(f'<< D: {Name.to_str(name)}')
    print(MetaInfo(freshness_period=10000))
    print(f'Content: (size: {len(content)})')
    print('')

if __name__ == '__main__':
    app.run_forever()

# id		name
# nopasien	noPasien
# nama		nama
# umur		umur
# bmi		bmi
# heartrate	heartrate
# height		height
# weight		weight

#{"noPasien":"75", "nama":"Radara", "umur": "35", "bmi": "25", "heartrate": "60", "height": "158", "weight": "60"}