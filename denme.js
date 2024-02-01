let egitim = 0;
  function ekleYeniSatiregitim() {
    
    var elements = document.getElementsByClassName('egitim');

    if (elements[egitim]) {
        elements[egitim].classList.remove('egitim');
    } else {
        console.error("Ürün Sınırına Ulaştınız");
    }

   
  }