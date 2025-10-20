# 🤖 LifeNetworks Auto Daily Bot
<img width="1244" height="572" alt="image" src="https://github.com/user-attachments/assets/685db997-83f7-474b-b546-79d00411bd28" />

Bot otomatis untuk **Life Airdrop (LifeNetworks)** yang melakukan:
- Login menggunakan **Google ID Token**
- **Daily Check-in** otomatis
- **Daily Mission** otomatis
- Loop otomatis setiap **24 jam** tanpa perlu intervensi pengguna

---

## ⚙️ Fitur Utama

✅ Login otomatis menggunakan `idToken`  
✅ Daily Check-in otomatis  
✅ Daily Mission otomatis  
✅ Deteksi status jika sudah melakukan check-in/mission (kode 409)  
✅ Loop 24 jam — otomatis mengulang ke akun pertama setiap hari  

---

## 📦 Persyaratan

Pastikan kamu sudah menginstall **Python 3.8+**

Lalu install library yang dibutuhkan:
```
git clone https://github.com/AirdropFamilyIDN-V2-0/lifenetworks.git
```
```
cd lifenetworks
```
```
python bot.py
```

🧠 Catatan

Jika muncul pesan ⏳ Sudah check-in hari ini atau ⏳ Sudah kerjakan daily mission, berarti akun tersebut sudah menyelesaikan aktivitas hari ini dan bot akan otomatis menunggu 24 jam.

Pastikan token masih aktif. Jika kadaluarsa, update idToken baru di data.txt.
<img width="878" height="510" alt="image" src="https://github.com/user-attachments/assets/cdccc6c8-9889-47e2-ad4e-2172fd47b3ee" />



🏷️ Credits

Developer: AirdropFamilyIDN

Team: ADFMIDN TEAM
Network: Life Airdrop
