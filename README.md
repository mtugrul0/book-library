# **Kütüphane Yönetim Sistemi**

Bu proje, kişisel bir kitap kütüphanesini yönetmek için geliştirilmiş bir uygulamadır. Proje, hem bir terminal uygulaması (Aşama 1-2) hem de bir REST API sunucusu (Aşama 3\) içermektedir. Sistem, kitap bilgilerini ISBN numarası aracılığıyla [Open Library API](https://openlibrary.org/developers/api)'sından otomatik olarak çeker ve yerel bir JSON dosyasında saklar.

## **Kurulum**

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### **1\. Repoyu Klonlayın**

Öncelikle projeyi klonlayın:

``git clone https://github.com/kullanici-adiniz/proje-adiniz.git
cd proje-adiniz``

### **2\. Bağımlılıkları Kurun**

Projenin çalışması için gerekli olan Python paketlerini requirements.txt dosyası aracılığıyla kurun:

``pip install \-r requirements.txt``

Not: Eğer bir requirements.txt dosyanız yoksa, fastapi, uvicorn ve httpx paketlerini kurmanız gerekmektedir:  
pip install fastapi uvicorn httpx

## **Kullanım**

Projenin iki farklı kullanım şekli bulunmaktadır:

### **1\. Terminal Uygulaması (Aşama 1 ve 2\)**

Kütüphanenizi yönetmek için interaktif komut satırı arayüzünü başlatın:

``python main.py``

Uygulama sizden bir kütüphane adı girmenizi veya mevcut bir kütüphaneyi yüklemenizi isteyecektir. Ardından menü üzerinden kitap ekleme, silme, listeleme ve arama gibi işlemleri yapabilirsiniz.

### **2\. API Sunucusu (Aşama 3\)**

FastAPI tabanlı REST API sunucusunu başlatmak için aşağıdaki komutu çalıştırın:

`uvicorn api:app \--reload`

Sunucu varsayılan olarak http://127.0.0.1:8000 adresinde çalışmaya başlayacaktır. \--reload parametresi, kodda yaptığınız değişikliklerin sunucuya otomatik olarak yansımasını sağlar.

## **API Dokümantasyonu (Aşama 3\)**

API sunucusu çalışırken, interaktif dokümantasyona (Swagger UI) http://127.0.0.1:8000/docs adresi üzerinden erişebilirsiniz.

### **Endpoint'ler**

#### **GET /books**

* **Açıklama:** Kütüphanede kayıtlı olan tüm kitapların bir listesini döndürür.  
* **Örnek Yanıt:**  
``  
[  
    {  
      "title": "Fantastic Mr. Fox",  
      "author": "Roald Dahl",  
      "isbn": "9780140328721"  
    },  
    {  
      "title": "The Hobbit",  
      "author": "J.R.R. Tolkien",  
      "isbn": "9780547928227"  
    }  
  ]
  ``

#### **POST /books**

* **Açıklama:** Verilen ISBN numarasını kullanarak Open Library'den kitap bilgilerini alır ve kütüphaneye yeni bir kitap ekler.  
* **Body Yapısı:**  
  ``{  
    "isbn": "string"  
  }``

* **Örnek Body:**  
  ``{  
    "isbn": "9780140328721"  
  }``

* **Başarılı Yanıt (201 Created):** Eklenen kitabın bilgilerini döndürür.

#### **DELETE /books/{isbn}**

* **Açıklama:** Belirtilen ISBN numarasına sahip kitabı kütüphaneden siler.  
* **Path Parametresi:** isbn (string) \- Silinecek kitabın ISBN numarası.  
* **Örnek İstek:** DELETE http://127.0.0.1:8000/books/9780140328721  
* **Başarılı Yanıt (204 No Content):** İşlem başarılı olduğunda herhangi bir içerik döndürmez.