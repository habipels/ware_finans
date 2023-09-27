from django.shortcuts import render ,redirect,get_object_or_404,HttpResponse
from .forms import *
from users.models import *
# Create your views here.
def firma_ekleme(request):
    form = firma_ekle(request.POST)
    v = vergi_dairesi.objects.all()
    faliyet_kace_kodu_modal = faliyet_bilgisi.objects.all()
    cvsgik = calisma_sosyal_guvenlik_is_kollari.objects.all()
    kayitli_firmalarim = firma.objects.filter(silinme_bilgisi = False,firma_muhasabecisi = request.user)
    sgkpersonelkanun = sgk_kanunlari.objects.all()
    content = {"form":form,"vergidaireleri":v,
               "faliyet_nace":faliyet_kace_kodu_modal,
               "cvsgik":cvsgik,"firmalrim":kayitli_firmalarim,"sgkpersonelkanun":sgkpersonelkanun}
    if request.method == "POST":
        tanitici_isim = request.POST.get("firmataniticiadi")
        firma_adi = request.POST.get("firmaunvanadi")
        firma_soyadi = request.POST.get("firmaunvansoyadi")
        sube_adi = request.POST.get("subeadi")
        sube_soyadi = request.POST.get("subeunvani")
        adres_aciklama = request.POST.get("adresaciklama")
        mahallekoy = request.POST.get("mahallekoy")
        bulvar = request.POST.get("bulvar")
        cadde = request.POST.get("cadde")
        sokak = request.POST.get("sokak")
        adaparselno = request.POST.get("adaparselno")
        diskapino = request.POST.get("diskapino")
        ickapino = request.POST.get("ickapino")
        postakodu = request.POST.get("postakodu")
        semt = request.POST.get("semt")
        ilce = request.POST.get("ilce")
        il = request.POST.get("il")
        firmaverginumarasi = request.POST.get("firmaverginumarasi")
        firmavergidairesi = request.POST.get("firmavergidairesi")
        firmavergidairesikodu = request.POST.get("firmavergidairesikodu")
        sahisisetc = request.POST.get("sahisisetc")
        firmaeposta = request.POST.get("firmaeposta")
        firmawebadresi = request.POST.get("firmawebadresi")
        firmatelefon = request.POST.get("firmatelefon")
        defterturu = request.POST.get("defterturu")
        kdv1 =request.POST.get("kdv1")
        turizim = request.POST.get("turizim")
        muhsgk = request.POST.get("muhsgk")
        poset = request.POST.get("poset")
        firmadefterturu = request.POST.get("firmadefterturu")
        kdv2 = request.POST.get("kdv2")
        kdvorani = request.POST.get("kdvorani")
        firmamt = request.POST.get("firmamt")
        firmastokenvanter = request.POST.get("firmastokenvanter")
        faliyet_kurulus_tarihi = request.POST.get("faliyet_kurulus_tarihi")
        faliyet_terk_tarihi =request.POST.get("faliyet_terk_tarihi")
        faliyetnacekodu = request.POST.get("faliyetnacekodu")
        faliyetniteligi = request.POST.get("faliyetniteligi")
        faliyetsektoru = request.POST.get("faliyetsektoru")
        yapilanisinniteligi = request.POST.get("yapilanisinniteligi")
        faliyetcalismasgi = request.POST.get("faliyetcalismasgi")
        sahisisetu = request.POST.get("sahisisetu")
        ticarisicilgazatesitarihi = request.POST.get("ticarisicilgazatesitarihi")
        tsgsayfano = request.POST.get("tsgsayfano")
        tsgazateno = request.POST.get("tsgazateno")
        meslektesekkuladi =request.POST.get("meslektesekkuladi")
        meslektesekkulno = request.POST.get("meslektesekkulno")
        adresno = request.POST.get("adresno")
        tahutedilensermaye = request.POST.get("tahutedilensermaye")
        odenensermaye = request.POST.get("odenensermaye")
        epostaadresi2 = request.POST.get("epostaadresi2")
        kotsmi = request.POST.get("kotsmi")
        ticaretsicilno =request.POST.get("ticaretsicilno")
        mersisno = request.POST.get("mersisno")
        isyerituru  =request.POST.get("isyerituru")
        faliyetisyerikodu = request.POST.get("faliyetisyerikodu")
        faliyetisyerimulkiyet = request.POST.get("faliyetisyerimulkiyet")
        faliyetisyerimulkiyet = request.POST.get("faliyetisyerimulkiyet")
        faliyetvergidairesikodu = request.POST.get("faliyetvergidairesikodu")
        yetkiliadisoyadi = request.POST.get("yetkiliadisoyadi")
        vergikimlikno = request.POST.get("vergikimlikno")
        faliyettckimlik = request.POST.get("faliyettckimlik")
        faliyetboosn = request.POST.get("faliyetboosn")
        faliyetcyvn = request.POST.get("faliyetcyvn")
        faliyetbirvn= request.POST.get("faliyetbirvn")
        ihaleyi_yapan_makam = request.POST.get("ihaleyi_yapan_makam")
        isyeribildirgesi_imzalayan = request.POST.get("isyeribildirgesi_imzalayan")
        ihaleyiyapanmakamadresi = request.POST.get("ihaleyiyapanmakamadresi")
        ihaleisverentipi = request.POST.get("ihaleisverentipi")
        taseronunvanbilgisi = request.POST.get("taseronunvanbilgisi")
        adres_aciklamat = request.POST.get("adresaciklamat")
        mahallekoyt = request.POST.get("mahallekoyt")
        bulvart = request.POST.get("bulvart")
        caddet = request.POST.get("caddet")
        sokakt = request.POST.get("sokakt")
        adaparselnot = request.POST.get("adaparselnot")
        diskapinot = request.POST.get("diskapinot")
        ickapinot = request.POST.get("ickapinot")
        postakodut = request.POST.get("postakodut")
        semtt = request.POST.get("semtt")
        ilcet = request.POST.get("ilcet")
        ilt = request.POST.get("ilt")
        taseronvergikimlikno = request.POST.get("taseronvergikimlikno")
        taserontcno = request.POST.get("taserontcno")
        taserontelefon = request.POST.get("taserontelefon")
        taseroneposta = request.POST.get("taseroneposta")
        kurumlarvergiveyatckimlikno = request.POST.get("kurumlarvergiveyatckimlikno")
        kurumlarvergikimlikno = request.POST.get("kurumlarvergikimlikno")
        kurumlarsoyadiunvan = request.POST.get("kurumlarsoyadiunvan")
        kurumlaradiunvan = request.POST.get("kurumlaradiunvan")
        kurumlarticaretsicilno  =request.POST.get("kurumlarticaretsicilno")
        Kurumlarepostaadresi = request.POST.get("Kurumlarepostaadresi")
        kurumlarirtibatnumarasi = request.POST.get("kurumlarirtibatnumarasi")
        kurumlarsube = request.POST.get("kurumlarsube")
        cikisyeri = request.POST.get("cikisyeri")
        kurumlarajanlik = request.POST.get("kurumlarajanlik")
        kurmlarimalatyeri= request.POST.get("kurmlarimalatyeri")
        kurumlarsatisyeri = request.POST.get("kurumlarsatisyeri")
        kurumlarsair = request.POST.get("kurumlarsair")
        kurumlartoplam =request.POST.get("kurumlartoplam")
        beyannamehangisifatlaverildi = request.POST.get("beyannamehangisifatlaverildi")
        beyannamesoyadiunvan = request.POST.get("beyannamesoyadiunvan")
        beyannameadiunvandevami =request.POST.get("beyannameadiunvandevami")
        beyannameyeaitticaretsicilno = request.POST.get("beyannameyeaitticaretsicilno")
        beyannameemailadresi = request.POST.get("beyannameemailadresi")
        beyannametelefonumarasi = request.POST.get("beyannametelefonumarasi")
        beyannamekanunitemsicitc  = request.POST.get("beyannamekanunitemsicitc")
        beyannamekanunitemsicivergino = request.POST.get("beyannamekanunitemsicivergino")
        beyannamekanunitemsicisoyadi = request.POST.get("beyannamekanunitemsicisoyadi")
        beyannamekanunitemsiciadiunvandevami = request.POST.get("beyannamekanunitemsiciadiunvandevami")
        beyannamekanunitemsiciticaretsicilno = request.POST.get("beyannamekanunitemsiciticaretsicilno")
        beyannamekanunitemsicieposta = request.POST.get("beyannamekanunitemsicieposta")
        beyannamekanunitemsicitelefon = request.POST.get("beyannamekanunitemsicitelefon")
        beyannameduzenleyeneaittc = request.POST.get("beyannameduzenleyeneaittc")
        beyannameduzenleyeneaitvergino = request.POST.get("beyannameduzenleyeneaitvergino")
        beyannameduzenleyeneaitsoyadiunvan = request.POST.get("beyannameduzenleyeneaitsoyadiunvan")
        beyannameduzenleyeneaitadiunvandevami = request.POST.get("beyannameduzenleyeneaitadiunvandevami")
        beyannameduzenleyeneaitticaretsicilno = request.POST.get("beyannameduzenleyeneaitticaretsicilno")
        beyannameduzenleyeneaiteposta = request.POST.get("beyannameduzenleyeneaiteposta")
        beyannameduzenleyeneaittelefon = request.POST.get("beyannameduzenleyeneaittelefon")
        ymmaitbilgilertc = request.POST.get("ymmaitbilgilertc")
        ymmaitbilgilervergino = request.POST.get("ymmaitbilgilervergino")
        ymmaitbilgilersoyadiunvan = request.POST.get("ymmaitbilgilersoyadiunvan")
        ymmaitbilgileradiunvanbilgisi = request.POST.get("ymmaitbilgileradiunvanbilgisi")
        ymmaitbilgileraditicaretsicilno = request.POST.get("ymmaitbilgileraditicaretsicilno")
        ymmaitbilgilereposta = request.POST.get("ymmaitbilgilereposta")
        ymmaitbilgilertelefonbilgisi = request.POST.get("ymmaitbilgilertelefonbilgisi")
        beyannamegonderentc = request.POST.get("beyannamegonderentc")
        beyannamegonderenvergino = request.POST.get("beyannamegonderenvergino")
        beyannamegonderensoyadiunvan = request.POST.get("beyannamegonderensoyadiunvan")
        beyannamegonderenadiunvandevami = request.POST.get("beyannamegonderenadiunvandevami")
        beyannamegonderentivaretsicilno = request.POST.get("beyannamegonderentivaretsicilno")
        beyannamegondereneposta = request.POST.get("beyannamegondereneposta")
        beyannamegonderentelefon = request.POST.get("beyannamegonderentelefon")
        sgkdosyaacilistarihi = request.POST.get("sgkdosyaacilistarihi")
        sgkdosyakapanistarihi = request.POST.get("sgkdosyakapanistarihi")
        sgkdosyam = request.POST.get("sgkdosyam")
        sgkdosyaiskolukod = request.POST.get("sgkdosyaiskolukod")
        sgkdosyayeni = request.POST.get("sgkdosyayeni")
        sgkdosyaeski = request.POST.get("sgkdosyaeski")
        sgkdosyaisyerisirano = request.POST.get("sgkdosyaisyerisirano")
        sgkdosyailkodu = request.POST.get("sgkdosyailkodu")
        sgkdosyailcekodu = request.POST.get("sgkdosyailcekodu")
        sgkdosyakontrolno = request.POST.get("sgkdosyakontrolno")
        sgkdosyaarackodu = request.POST.get("sgkdosyaarackodu")
        sgkdosyaiskodu = request.POST.get("sgkdosyaiskodu")
        sgkdosyasfkbolgemud = request.POST.get("sgkdosyasfkbolgemud")
        sgkdosyail = request.POST.get("sgkdosyail")
        sgkdosyailce = request.POST.get("sgkdosyailce")
        sgkdosyatehlikederecesi = request.POST.get("sgkdosyatehlikederecesi")
        sgkdosyatehlikesinifi = request.POST.get("sgkdosyatehlikesinifi")
        sgkdosyaprimorani = request.POST.get("sgkdosyaprimorani")
        sgkfazlamesaiyuzdesialt = request.POST.get("sgkfazlamesaiyuzdesialt")
        sgkfazlamesaiyuzdesiust = request.POST.get("sgkfazlamesaiyuzdesiust")
        sgkdosyalaribesuygulamasi = request.POST.get("sgkdosyalaribesuygulamasi")
        sgkdosyatesfik6111kanun = request.POST.get("sgkdosyatesfik6111kanun")
        sgkdosyatesfik6111faydalanmaayi = request.POST.get("sgkdosyatesfik6111faydalanmaayi")
        personel_girisinde_otomatik_kanun= request.POST.get("personel_girisinde_otomatik_kanun")
        personel_6116645yararlanmiyorsayenikanun =request.POST.get("personel_6116645yararlanmiyorsayenikanun")
        sgkbolges = request.POST.get("sgkbolges")
        sgkbolgemeslek = request.POST.get("sgkbolgemeslek")
        sgkbolgedosyano = request.POST.get("sgkbolgedosyano")
        sgkbolgeilkodu = request.POST.get("sgkbolgeilkodu") 
        sgkbolgeyazismaadresi = request.POST.get("sgkbolgeyazismaadresi")
        sgkbolgetaseronadisoyadi = request.POST.get("sgkbolgetaseronadisoyadi")
        iskurisyerinumarasi =request.POST.get("iskurisyerinumarasi")
        iskurisverentc = request.POST.get("iskurisverentc")
        iskurilmudkayittarihi = request.POST.get("iskurilmudkayittarihi")
        iskursifresi=request.POST.get("iskursifresi")
        if isyeribildirgesi_imzalayan == "01":
            isyeribildirgesi_imzalayan = "İş Veren"
        elif isyeribildirgesi_imzalayan == "02":
            isyeribildirgesi_imzalayan = "İşveren Yetkili"
        else:
            isyeribildirgesi_imzalayan = ""
        if ihaleisverentipi == "01":
            ihaleisverentipi = "Asıl İşveren"
        elif ihaleisverentipi == "02":
            ihaleisverentipi = "Alt Yüklenici"
        else:
            ihaleisverentipi = ""
        if defterturu == "genelmuhasabe":
            defterturu = "Genel Muhasebe"
        elif defterturu == "isletmedefteri":
            defterturu = "İşletme Defteri"
        if kdv1 == "kdv1aylik":
            kdv1 = "Aylık"
        elif kdv1 == "kdv1ucaylik":
            kdv1 = "Üç Aylık"
        if turizim == "turizimaylik":
            turizim = "Aylık"
        elif turizim == "turizimucaylik":
            turizim = "Üç Aylık"
        if muhsgk == "sgkaylik":
            muhsgk = "Aylık"
        elif muhsgk == "sgkucaylik":
            muhsgk = "Üç Aylık"
        if poset == "posetaylik":
            poset = "Aylık"
        elif poset == "posetucaylik":
            poset = "Üç Aylık"
        elif poset == "posetaltiaylik":
            poset = "Altı Aylık"
        if firmadefterturu == "isletme":
            firmadefterturu = "İşletme"
        elif firmadefterturu == "serbestmeslekdefteri":
            firmadefterturu = "Serbest Meslek Defteri"
        if kdv2 == "kdv2aylik":
            kdv2 = "Aylık"
        elif kdv2 == "kdv2ucaylik":
            kdv2 = "Üç Aylık"
        firma_olustur = firma.objects.create(firma_muhasabecisi = request.user,
                             tanitici_isim = tanitici_isim ,
                             firma_unvani = firma_adi,
                             Firma_unvani2 = firma_soyadi,
                             silinme_bilgisi = False)
        yeni_adres  = adresler.objects.create(
            adres = adres_aciklama,mahhalle_koy=mahallekoy,
            bulvar = bulvar,cadde = cadde, sokak = sokak,
            adaparselno = adaparselno,diskapino = diskapino,
            ickapino = ickapino,posta_kodu = postakodu,semt=semt,
            ilce = ilce,il = il,silinme_bilgisi = False
        )
        yeni_sube = sube.objects.create(
            bagli_oldugu_firma = get_object_or_404(firma,id = firma_olustur.id ),
            sube_adi = sube_adi,sube_unvani = sube_soyadi,adres_bilgisi = get_object_or_404(adresler,id = yeni_adres.id),
            vergi_dairesi_adi =get_object_or_404(vergi_dairesi,vergi_dairesi_adi = firmavergidairesi) ,vergi_dairesi_kodu = firmavergidairesikodu,
            vergi_numarasi = firmaverginumarasi,sahis_ise_tc = sahisisetc,
            email_adresi = firmaeposta,web_adresi = firmawebadresi,
            telefon_numarasi = firmatelefon,
            sube_defter_turu =defterturu,
            kdv1 = kdv1,kdv2 = kdv2,turizm = turizim,
            muhsgk = muhsgk,poset = poset,firma_defter_turu =firmadefterturu,
            mukellefiyet_turu= firmamt,stok_bilgisi =firmastokenvanter,
            gecici_vergi_orani = kdvorani
        )
        sube_faliyet_bilgileri.objects.create(sube_bilgisi = get_object_or_404(sube,id = yeni_sube.id),
        kurulus_tarihi = faliyet_kurulus_tarihi ,terk_tarihi = faliyet_terk_tarihi 
        ,faliyet_nace_kodu = get_object_or_404(faliyet_bilgisi,faliyet_kodu = faliyetnacekodu ),
        tabi_oldugu_sektor = faliyetsektoru ,faliyet_niteligi = faliyetniteligi ,yapilan_is_niteligi = yapilanisinniteligi ,
        calisma_ve_sosyal_is_kolu = get_object_or_404(calisma_sosyal_guvenlik_is_kollari,id = faliyetcalismasgi ),
        sahis_ise_ticaret_unvani = sahisisetu ,ticaret_sicil_gazete = ticarisicilgazatesitarihi,
        ticaret_sicil_gazete_sayfa_no = tsgsayfano ,ticaret_sicil_gazete_no = tsgazateno ,meslek_tesekkul_adi = meslektesekkuladi ,
        meslek_tesekkul_no = meslektesekkulno ,adres_no = adresno ,taahut_edilen_sermaye = tahutedilensermaye ,
        odenen_sermaye = odenensermaye ,e_posta_adresi2 = epostaadresi2 ,
        kayitli_oldugu_il  = kotsmi ,ticaret_sicil_no = ticaretsicilno ,
        mersis_no = mersisno , isyeri_turu = isyerituru,isyeri_kodu = faliyetisyerikodu ,
        isyeri_mulkiyet = faliyetisyerimulkiyet ,vergi_dairesi_adi = get_object_or_404(vergi_dairesi,vergi_dairesi_adi =faliyetvergidairesikodu  ),
        yetkili_adi_soyadi = yetkiliadisoyadi ,yetkili_tckimlikno =  faliyettckimlik,
        vergi_kimlikno =  vergikimlikno,oda_sicil_no = faliyetboosn ,cevre_temizlik_vergi_no = faliyetcyvn ,
        beldye_ilan_reklam_vergi_no  = faliyetbirvn
        )
        ihale_bilgileri.objects.create(sube_bilgisi = get_object_or_404(sube,id = yeni_sube.id),
        ihalekonusundaihaleyapanmakam = ihaleyi_yapan_makam ,isyeri_bildirgersi_imzalayan =isyeribildirgesi_imzalayan ,
          ihalekonusundaihaleyapanmakamadresi =ihaleyiyapanmakamadresi ,isveren_tipi =   ihaleisverentipi  )
        yeni_adres_taseron  = adresler.objects.create(
            adres = adres_aciklamat,mahhalle_koy=mahallekoyt,
            bulvar = bulvart,cadde = caddet, sokak = sokakt,
            adaparselno = adaparselnot,diskapino = diskapinot,
            ickapino = ickapinot,posta_kodu = postakodut,semt=semtt,
            ilce = ilcet,il = ilt,silinme_bilgisi = False
        )
        taseronbilgileri.objects.create(sube_bilgisi = get_object_or_404(sube,id = yeni_sube.id),
        taseronunvanbilgisi =  taseronunvanbilgisi ,adres_bilgisi =   get_object_or_404(adresler,id = yeni_adres_taseron.id),
          vergi_numarasi = taseronvergikimlikno ,sahis_tc = taserontcno ,
          email_adresi = taseroneposta , telefon_numarasi =  taserontelefon                 
        )
        kurumlar_dar_mukkelef_kimlik_ve_adres_bilgisi.objects.create(
          sube_bilgisi = get_object_or_404(sube,id = yeni_sube.id),
          kurumlarvergiveyatckimlikno =   kurumlarvergiveyatckimlikno,
          kurumlarvergikimlikno =kurumlarvergikimlikno,kurumlarsoyadiunvan =kurumlarsoyadiunvan
          ,kurumlaradiunvan = kurumlaradiunvan,kurumlarticaretsicilno = kurumlarticaretsicilno,
          Kurumlarepostaadresi = Kurumlarepostaadresi,kurumlarirtibatnumarasi = kurumlarirtibatnumarasi,
          kurumlarsube =kurumlarsube,cikisyeri = cikisyeri,kurumlarajanlik = kurumlarajanlik,
          kurmlarimalatyeri =kurmlarimalatyeri,kurumlarsatisyeri =kurumlarsatisyeri,
          kurumlarsair =kurumlarsair,kurumlartoplam = kurumlartoplam

        )
        beyanname_verilme = beyanname_bilgileri.objects.create(sube_bilgisi = get_object_or_404(sube,id = yeni_sube.id),
        beyannamehangisifatlaverildi  = beyannamehangisifatlaverildi ,beyannamesoyadiunvan =beyannamesoyadiunvan ,
        beyannameadiunvandevami = beyannameadiunvandevami ,beyannameyeaitticaretsicilno =beyannameyeaitticaretsicilno ,
        beyannameemailadresi= beyannameemailadresi,beyannametelefonumarasi= beyannametelefonumarasi
        
        )
        beyanname_kanuni_temsilcisi.objects.create(
            beyanname_bilgisi = get_object_or_404(beyanname_bilgileri,id = beyanname_verilme.id),
            beyannamekanunitemsicitc = beyannamekanunitemsicitc,beyannamekanunitemsicivergino = beyannamekanunitemsicivergino,
            beyannamekanunitemsicisoyadi = beyannamekanunitemsicisoyadi,
            beyannamekanunitemsiciadiunvandevami =beyannamekanunitemsiciadiunvandevami,
            beyannamekanunitemsiciticaretsicilno = beyannamekanunitemsiciticaretsicilno,
            beyannamekanunitemsicieposta = beyannamekanunitemsicieposta,
            beyannamekanunitemsicitelefon = beyannamekanunitemsicitelefon 
        )
        beyanname_duzenleyene_ait_bilgiler.objects.create(
            beyanname_bilgisi = get_object_or_404(beyanname_bilgileri,id = beyanname_verilme.id),
            beyannameduzenleyeneaittc = beyannameduzenleyeneaittc,
            beyannameduzenleyeneaitvergino = beyannameduzenleyeneaitvergino,
            beyannameduzenleyeneaitsoyadiunvan = beyannameduzenleyeneaitsoyadiunvan,
            beyannameduzenleyeneaitadiunvandevami = beyannameduzenleyeneaitadiunvandevami,
            beyannameduzenleyeneaitticaretsicilno = beyannameduzenleyeneaitticaretsicilno,
            beyannameduzenleyeneaiteposta = beyannameduzenleyeneaiteposta,
            beyannameduzenleyeneaittelefon = beyannameduzenleyeneaittelefon
        )
        ymmbilgileri.objects.create(
            beyanname_bilgisi = get_object_or_404(beyanname_bilgileri,id = beyanname_verilme.id),
            ymmaitbilgilertc = ymmaitbilgilertc,ymmaitbilgilervergino = ymmaitbilgilervergino,
            ymmaitbilgilersoyadiunvan = ymmaitbilgilersoyadiunvan,ymmaitbilgileradiunvanbilgisi = 
            ymmaitbilgileradiunvanbilgisi,ymmaitbilgileraditicaretsicilno = ymmaitbilgileraditicaretsicilno,
            ymmaitbilgilereposta = ymmaitbilgilereposta,ymmaitbilgilertelefonbilgisi = ymmaitbilgilertelefonbilgisi
        )
        Beyannameyi_gonderen_bilgileri.objects.create(
            beyanname_bilgisi = get_object_or_404(beyanname_bilgileri,id = beyanname_verilme.id),
            beyannamegonderentc = beyannamegonderentc,beyannamegonderenvergino = beyannamegonderenvergino,
            beyannamegonderensoyadiunvan = beyannamegonderensoyadiunvan,beyannamegonderenadiunvandevami= beyannamegonderenadiunvandevami
            ,beyannamegonderentivaretsicilno = beyannamegonderentivaretsicilno,beyannamegondereneposta = beyannamegondereneposta,
            beyannamegonderentelefon = beyannamegonderentelefon
        )
        sgk_bilgileri.objects.create(
            sube_bilgisi = get_object_or_404(sube,id = yeni_sube.id),
            sgkdosyaacilistarihi= sgkdosyaacilistarihi,sgkdosyakapanistarihi = sgkdosyakapanistarihi,
            sgkdosyam = sgkdosyam,sgkdosyaiskolukod=sgkdosyaiskolukod,sgkdosyayeni=sgkdosyayeni,
            sgkdosyaeski = sgkdosyaeski,sgkdosyaisyerisirano=sgkdosyaisyerisirano,sgkdosyailkodu = sgkdosyailkodu
            ,sgkdosyailcekodu = sgkdosyailcekodu,sgkdosyakontrolno=sgkdosyakontrolno,sgkdosyaarackodu=sgkdosyaarackodu,
            sgkdosyaiskodu = sgkdosyaiskodu,sgkdosyasfkbolgemud = sgkdosyasfkbolgemud,sgkdosyail=sgkdosyail,
            sgkdosyailce = sgkdosyailce,sgkdosyatehlikederecesi = sgkdosyatehlikederecesi,sgkdosyatehlikesinifi=sgkdosyatehlikesinifi,
            sgkdosyaprimorani = sgkdosyaprimorani,sgkfazlamesaiyuzdesialt = sgkfazlamesaiyuzdesialt,sgkfazlamesaiyuzdesiust=sgkfazlamesaiyuzdesiust,
            sgkdosyalaribesuygulamasi = sgkdosyalaribesuygulamasi,sgkdosyatesfik6111kanun=sgkdosyatesfik6111kanun,
            sgkdosyatesfik6111faydalanmaayi=sgkdosyatesfik6111faydalanmaayi,
            personel_girisinde_otomatik_kanun = get_object_or_404(sgk_kanunlari,id = personel_girisinde_otomatik_kanun),
            personel_6116645yararlanmiyorsayenikanun = get_object_or_404(sgk_kanunlari,id = personel_6116645yararlanmiyorsayenikanun)
        )
        sgk_bolgecalisma_mudurlukleri.objects.create(
            sube_bilgisi = get_object_or_404(sube,id = yeni_sube.id),
            sgkbolges=sgkbolges,sgkbolgemeslek=sgkbolgemeslek,sgkbolgedosyano=sgkbolgedosyano,
            sgkbolgeilkodu=sgkbolgeilkodu,sgkbolgeyazismaadresi=sgkbolgeyazismaadresi,
            sgkbolgetaseronadisoyadi=sgkbolgetaseronadisoyadi
        )
        iskurbilgileri.objects.create(
            sube_bilgisi = get_object_or_404(sube,id = yeni_sube.id),
            iskurisyerinumarasi=iskurisyerinumarasi,iskurisverentc=
            iskurisverentc,iskurilmudkayittarihi=iskurilmudkayittarihi,
            iskursifresi=iskursifresi

        )
        return redirect ("/")
    else:  
        return render (request,"firma_durumlari/firma_index.html",content)
    

def firma_gosterme(request,slug):
    kayitli_firmam = get_object_or_404(firma,silinme_bilgisi = False,firma_ozel_anahtar = slug)
    sube_bilgisi = get_object_or_404(sube,bagli_oldugu_firma =  kayitli_firmam)
    content = {}
    content["kayitlifirmam"]= kayitli_firmam
    content["sube_bilgisi"] = sube_bilgisi
    return render (request,"firma_durumlari/firma_duzeletme.html",content)