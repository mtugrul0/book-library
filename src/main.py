from models import Library
import os

print("Kütüphane sistemine hoş geldiniz.\n" 
    "Başlamadan önce kütüphanenize bir isim verin veya mevcut kütüphanelerden birini yükleyin.\n"
    "Mevcut kütüphaneler:")

for f in os.listdir():
    if f.endswith("-library.json"):
        print(f.replace('-library.json', '').replace('-', ' '))
        
library_name = input("Yüklemek istediğiniz veya oluşturmak istedğiniz kütüphane adı: ")

library = Library(library_name)

while True:
    print("\n~~~~ Kütüphane Sistemi ~~~~")
    print("1. Kitap Ekle")
    print("2. Kitap Sil")
    print("3. Kitapları listele")
    print("4. Kitapları ara")
    print("5. Çıkış")
    secim = input("Seçiminiz: ")
    print("")
    
    if secim == "1":
        new_book = input("Kitabın ISBN numarası: ")
        library.add_book(new_book)

    elif secim == "2":
        isbn = input("Silmek istediğiniz kitabın ISBN numarasını yazınız: ")
        library.remove_book(isbn)

    elif secim =="3":
        library.list_books()

    elif secim =="4":
        isbn = input("Aramak İstedğiniz kitabın ISBN numarasını giriniz: ")
        b = library.find_book(isbn)
        if b:
            print(b)
        else:
            print("Kitap bulunamadı.")

    elif secim == "5":
        print("Hoşçakalın\n")
        break
    else:
        print("Seçiminiz hatalı, tekrar deneyin.")