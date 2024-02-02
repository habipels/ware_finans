<div class="container tablo" style="margin-top: 0px !important;">
        <input class="col-12 text-center" type="text" disabled value="Eğitim Sağlık Harcamaları">
      
        <div class="table-responsive " style=" 
        height: 400px;
        overflow: auto;">
          <table class="table table-bordered ">
            <thead style="position: sticky;top: 0">
              <tr>
                <th class="text-center" style="min-width: 150px ;">Harcama Türü</th>
                <th class="text-center" style="min-width: 150px ;">Hizmet Alınan Teşebbüsün Vergi / T.C. Kimilk No</th>
                <th class="text-center" style="min-width: 150px ;">Hizmet Alınan Teşebbüsün Unvan Unvanı</th>
                <th class="text-center" style="min-width: 150px ;">Beige Türü</th>
                <th class="text-center" style="min-width: 150px ;">Belge Tarihi</th>
                <th class="text-center" style="min-width: 150px ;">Belge Seri No</th>
                <th class="text-center" style="min-width: 150px ;">Tutar</th>
                <th class="text-center"><a href="javascript:void(0);" onclick="ekleYeniSatirehizmetleri()">SATIR EKLE</a></th>
              </tr>
            </thead>
            <tbody>
              <tr class="hizmetleri">
              <td><select name="alinanhizmetturu" id="">
                  <option value=""></option>
                  <option value="Eğitim">Eğitim</option>
                  <option value="Sağlık">Sağlık</option>    
                </select></td>
                <td>
                <td><input type="text" name="hizmettesebusvergiveyatc"></td>
                <td><input type="text" name="hizmettesebusadisoyadiunvan"></td>
                <td><select name="hizmetinbelgeturu" id="">
                  <option value=""></option>
                  <option value="Fatura">Fatura</option>
                  <option value="e-Fatura">e-Fatura</option>
                  <option value="e-Arşiv">e-Arşiv</option>
                  <option value="Diğer">Diğer</option>
                               
                </select></td>
                <td><input type="date" name="hizmetlerinbelgetarihi"></td>
                
                <td><input type="text" name="hizmetbelgeserino"></td>

                <td><input type="number" step="0.01" value="0" name="hizmettutarbilgisi"></td>
                
                <td></td>
              </tr>
              
            </tbody>
          </table>
        </div>
      </div>