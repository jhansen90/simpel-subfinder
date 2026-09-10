🔎 Simple Subfinder

Simple Subfinder adalah tools sederhana untuk melakukan subdomain enumeration atau pencarian subdomain dari suatu domain. Tools ini dirancang agar proses reconnaissance menjadi lebih mudah, ringan, dan praktis, terutama untuk kebutuhan cybersecurity learning, bug hunting, dan penetration testing yang berizin.

«⚠️ Gunakan hanya pada target yang Anda miliki atau telah memberikan izin untuk diuji.»

---

📌 Apa Itu Subdomain Enumeration?

Subdomain enumeration adalah proses mengidentifikasi subdomain yang berkaitan dengan sebuah domain utama.

Contohnya:

example.com
├── www.example.com
├── api.example.com
├── dev.example.com
├── mail.example.com
└── admin.example.com

Informasi subdomain dapat membantu security researcher memahami attack surface suatu aplikasi atau organisasi sebelum melakukan pengujian keamanan.

---

✨ Fitur

- 🔎 Subdomain enumeration
- 🎯 Mendukung single-domain scanning
- 📂 Mendukung scanning menggunakan daftar domain
- 💾 Menyimpan hasil ke file
- ⚡ Penggunaan sederhana
- 🪶 Ringan dan mudah dimodifikasi
- 🧑‍💻 Cocok untuk belajar reconnaissance
- 🛡️ Dapat digunakan sebagai bagian dari workflow penetration testing berizin

---

📦 Instalasi

Clone repository:

git clone https://github.com/jhansen90/simpel-subfinder

cd simple-subfinder

Jalankan tools:

python subfinder.py

---

🚀 Cara Penggunaan

Single Domain

Untuk melakukan enumeration pada satu domain:

python subfinder.py example.com

Multiple Domain

Siapkan file:

domains.txt

Contoh isi:

example.com
example.org
example.net

Kemudian jalankan:

python subfinder.py -l domains.txt

Menyimpan Hasil

Untuk menyimpan hasil ke file:

python subfinder.py example.com -o hasil.txt

Contoh hasil:

www.example.com
api.example.com
dev.example.com
mail.example.com

---

🔄 Workflow Reconnaissance

Simple Subfinder dapat digunakan sebagai salah satu tahap awal dalam proses security assessment:

Target Domain
     │
     ▼
Subdomain Enumeration
     │
     ▼
Identifikasi Subdomain
     │
     ▼
Validasi Host
     │
     ▼
Security Testing

Enumeration sendiri bukan berarti sebuah subdomain memiliki vulnerability. Hasil yang ditemukan tetap harus divalidasi dan diuji secara aman sesuai scope.

---

💡 Contoh Penggunaan

Misalnya target yang diizinkan adalah:

example.com

Jalankan:

python subfinder.py example.com

Kemudian tools dapat menghasilkan daftar seperti:

api.example.com
dev.example.com
staging.example.com
www.example.com

Daftar tersebut dapat digunakan untuk membantu pemetaan attack surface dalam pengujian keamanan yang sah.

---

📁 Struktur Project

Contoh struktur repository:

simple-subfinder/
│
├── subfinder.py
├── requirements.txt
├── domains.txt
├── hasil.txt
└── README.md

---

🛠️ Pengembangan

Tools ini dibuat sebagai project sederhana yang dapat dikembangkan lebih lanjut.

Beberapa fitur yang dapat ditambahkan:

- DNS resolution
- HTTP/HTTPS probing
- Concurrent scanning
- Filtering duplicate subdomain
- Output JSON/CSV
- Integrasi API passive DNS
- Status code detection
- Screenshot halaman web
- Integrasi dengan tools reconnaissance lainnya

---

🎯 Tujuan Project

Project ini dibuat untuk:

- Belajar konsep subdomain enumeration
- Memahami proses reconnaissance
- Membantu security researcher dalam pemetaan aset
- Eksperimen dan pengembangan tools cybersecurity
- Latihan membuat automation sederhana menggunakan Python

---

⚠️ Disclaimer

Tools ini dibuat untuk tujuan edukasi, security research, bug bounty, dan penetration testing yang memiliki izin.

Jangan gunakan tools ini untuk melakukan reconnaissance atau pengujian terhadap sistem tanpa izin dari pemiliknya.

Developer tidak bertanggung jawab atas penyalahgunaan tools ini.

🚫 Jangan diperjualbelikan

«Boleh dimodifikasi dan dikembangkan untuk pembelajaran. Jangan diperjualbelikan. Jangan digunakan sebagai alat untuk aktivitas ilegal atau tanpa izin.»

---

👨‍💻 Author

Simple Subfinder — Cybersecurity Reconnaissance Tool

Made for learning, research, and authorized security testing.

Learn • Build • Test • Secure
