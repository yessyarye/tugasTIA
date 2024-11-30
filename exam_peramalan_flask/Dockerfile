# Menggunakan image dasar dari Python
FROM python:3.9-slim

# Menentukan direktori kerja di dalam container
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt .

# Menginstal dependencies yang ada di requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin semua file aplikasi ke dalam container
COPY . .

# Menentukan port yang akan digunakan
EXPOSE 5000

# Menjalankan aplikasi Flask
CMD ["python", "app.py"]
