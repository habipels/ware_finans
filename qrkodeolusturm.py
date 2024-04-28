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
data = "https://cohucoffeehuman.site/menu/"

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