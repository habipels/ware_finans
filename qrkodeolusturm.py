#QR Code Kütüphansesini uygulamamıza dahil ediyoruz
import qrcode

# Qr Kod oluşturma olayı
qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 4,
)

# karekod içinde saklamak istediğiniz verileriniz
data = {"unvan":"ware yazılım","vkntckn":"3333333302", "avkntckn":"70673705960 ", "senaryo":"EARSIVFATURA", "tip":"SATIS", "tarih":"2023-10-07", "no":"GIB2023000007471", "ettn":"4ae13a87-3741-41eb-9346-43f59bbc7685", "parabirimi":"TRY", "malhizmettoplam":"15", "kdvmatrah(20)":"12.75", "hesaplanankdv(20)":"2.55","vergidahil":"15.3", "odenecek":"15.3"}

# Veriyi ekleme
qr.add_data(data)
qr.make(fit=True)

# Görüntü dosyasının oluşturulması
img = qr.make_image()

# Oluşturulan görüntü dosyasının kayıt biçimleri. İstediğiniz formatı seçebilirsiniz.:
# img.save("image.png")
# img.save("image.bmp")
# img.save("image.jpeg")
img.save("image.jpg")