# ✅ Web Tabanlı Günlük Görev Takip Sistemi (Flask + Google Sheets)

Bu sistem, bireylerin veya küçük takımların günlük görevlerini takip edip tamamlayabileceği, puan toplayabileceği ve tüm verilerini Google Sheets üzerinde saklayabileceği bir uygulamadır. Modern yazılım prensiplerine uygun, tamamen modüler ve genişletilebilir yapısıyla geliştirilmiştir.

---

## 🔍 Özellikler ve Detaylı Açıklamaları

### 📅 Günlük Görev Sekmesi Oluşturma

Her kullanıcı için, her gün otomatik olarak Google Sheets üzerinde şu formatta bir sekme (sheet) oluşturulur:

📄 Örnek Sekme Adı: `mehmet_2025-03-27`

Bu sekmede şu sütunlar bulunur:

| gorev       | durum        |
|-------------|--------------|
| Kitap oku   | bekliyor     |
| Spora git   | tamamlandı   |

Bu işlem `task_service.py` > `create_daily_sheet()` fonksiyonu ile yapılır. Görev tamamlandığında `"durum"` sütunu `"tamamlandı"` olarak güncellenir.

---

### 🎯 Puanlama Sistemi

Her gün sonunda sistem, kullanıcının görev performansına göre puan hesaplar. Puanlama şu şekilde yapılır:

| Eksik Görev Sayısı | Puan |
|--------------------|------|
| 0                  | +5   |
| 1                  | +3   |
| 2                  |  0   |
| 3                  | -2   |
| 4+                 | -5   |

Bu puan hem `score.json` dosyasına hem de Google Sheets içindeki `"Puan"` sekmesine kaydedilir.

📁 Örnek `score.json` içeriği:

```json
[
  {
    "kullanici": "mehmet",
    "tarih": "2025-03-27",
    "puan": 3
  }
]
```

---

### 🔐 Kullanıcı Rolleri

- `admin`: tüm kullanıcıların görev ve puan verilerini görüp sistem modüllerini kontrol edebilir.
- `kullanıcı`: sadece kendi görevlerini görüp yönetebilir.

---

### ⚙️ Modül Genişletme

Yeni bir sistem modülü eklemek istersen örneğin “Alışkanlık Takibi”, aşağıdaki 5 dosyayı oluşturman yeterlidir:

| Dosya                             | Açıklama                        |
|----------------------------------|---------------------------------|
| `models/habit_model.py`          | Veri modeli                     |
| `repositories/habit_repository.py` | Google Sheets işlemleri       |
| `services/habit_service.py`      | İş mantığı                      |
| `controllers/habit_controller.py`| İstek yöneticisi                |
| `routes/habit_routes.py`         | Flask Blueprint yönlendirme     |

Ayrıca `app.py` içinde `habit_bp` blueprint’ini tanımlamalısın:

```python
from routes.habit_routes import habit_bp
app.register_blueprint(habit_bp, url_prefix="/habit")
```

---

## ⚙️ Kurulum

### 1. Gerekli Paketleri Kur

```bash
pip install -r requirements.txt
```

### 2. `.env` Dosyasını Oluştur

```env
FLASK_SECRET_KEY=gizli_flask_anahtar
SPREADSHEET_ID=1AbCdEfGhIjKlMnOpQrStUvWxYzEXAMPLE
SERVICE_ACCOUNT_FILE=credentials.json
```

#### Açıklamalar:

| Değişken             | Açıklama                                  |
|----------------------|--------------------------------------------|
| FLASK_SECRET_KEY     | Flask oturumlarını şifrelemek için         |
| SPREADSHEET_ID       | Google Sheets belgenizin ID'si             |
| SERVICE_ACCOUNT_FILE | Google API kimlik dosyanızın adı           |

🔑 `SPREADSHEET_ID`, Google Sheets linkindeki şu kısımdır:  
`https://docs.google.com/spreadsheets/d/🟡BU_KISIM🟡/edit#gid=0`

---

## 🔐 Google API Ayarları

1. Google Cloud Console’a gir: [https://console.cloud.google.com](https://console.cloud.google.com)
2. Yeni bir proje oluştur.
3. Sheets API ve Drive API’yi etkinleştir.
4. Servis Hesabı oluştur, `credentials.json` dosyasını indir.
5. Google Sheets belgenizi açın ve servis hesabı e-postasını "Edit" yetkisiyle paylaşın.

📧 Örnek servis hesabı e-postası: `my-bot@tracker-project.iam.gserviceaccount.com`

---

## ▶️ Uygulamayı Çalıştır

```bash
python app.py
```

Tarayıcıdan şu adrese git: [http://localhost:5000](http://localhost:5000)

---

## 👤 Varsayılan Kullanıcılar (Test için)

| Kullanıcı Adı | Şifre     | Rol     |
|---------------|-----------|----------|
| admin         | admin123  | Admin    |
| mehmet        | 1234      | Kullanıcı |
| ayse          | abcd      | Kullanıcı |

---

## 🛡️ Güvenlik Önlemleri

- `.env` ve `credentials.json` dosyaları `.gitignore` içine alınmalıdır.
- Kullanıcı oturumları Flask session ile şifrelenir.
- Admin yetkisi olmayan kullanıcılar admin paneline erişemez.
- Veriler yalnızca kullanıcıya özeldir.

📁 `.gitignore` örneği:

```gitignore
.env
credentials.json
score.json
__pycache__/
*.pyc
.vscode/
.idea/
```

---

## 📜 Lisans

MIT Lisansı © 2025

---

## 🤝 Katkıda Bulunmak

Pull request, issue ve yeni modül önerileri her zaman memnuniyetle karşılanır!