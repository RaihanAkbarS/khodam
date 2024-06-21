from flask import Flask, render_template, request, jsonify
import csv
import random
import re
from markupsafe import escape

app = Flask(__name__)

def ambil_nama_acak(file_csv):
    with open(file_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        data = [row[0].strip() for row in reader if row and row[0].strip()]  # Ambil kolom pertama dari baris yang tidak kosong

    # Mengambil satu nama secara acak dari data yang tersedia
    while True:
        if data:
            nama_acak = random.choice(data)
            if nama_acak:
                break  # Keluar dari loop jika nama tidak kosong
        else:
            nama_acak = "Tidak ada nama yang tersedia untuk dipilih secara acak"
            break  # Keluar dari loop jika data kosong

    return nama_acak

def clean_input(input_string):
    # Hanya izinkan huruf, spasi, dan beberapa karakter khusus seperti ', -
    cleaned_string = re.sub(r'[^a-zA-Z\s\'\-]', '', input_string)
    return cleaned_string[:50]  # Batasi panjang maksimal input

def is_valid_input(s):
    # Fungsi untuk memeriksa apakah input valid
    cleaned_input = clean_input(s)
    return bool(cleaned_input)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ambil_nama_acak', methods=['POST'])
def ambil_nama_acak_api():
    nama_file_csv = 'nama_indonesia_bersih.csv'  # Sesuaikan nama file CSV
    nama_acak = ambil_nama_acak(nama_file_csv)
    nama_input = request.form.get('inputNama', '').strip()

    # Validasi input
    if not is_valid_input(nama_input):
        return jsonify({'reload': True})  # Kirimkan flag reload jika input tidak valid

    nama_input_clean = clean_input(nama_input)
    nama_input_escaped = escape(nama_input_clean)

    return jsonify({'nama_input': nama_input_escaped, 'nama_acak': nama_acak})

if __name__ == '__main__':
    app.run(debug=True)
