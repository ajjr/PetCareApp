# PetCareApp, ehdotus
PetCareAppin avulla on tarkoitus pitää kirjaa oman lemmikkieläimen hoitotoimenpiteistä ja hyvinvointiin liittyvistä tapahtumista. Se koostuu päivä-, viikko- ja kuukausinäkymistä, jotka näyttävät päivittäin, viikoittain tai kuukausittain toistuvat toimenpiteet. Tällaisia toimenpiteitä eräiden koirarotujen kohdalla voivat olla esim. trimmaus, pesu ja kynsien leikkuu. Jos eläimelle määrätään lääkekuuri, päivittäisiä toimenpiteitä ovat lääkkeen annostelu ja syöttäminen. Lisäksi sovellukseen pitäisi voida kirjata eläimen päivittäinen ruokavalio. Tämä voidaan yhdistää terveyteen liittyviin tapahtumiin kuten esim. yllättävään ripuliin, jolloin omistaja voi tehdä päätelmiä ruokavalion ja/tai lääkkeiden sopivuudesta lemmikilleen.

## Käsitteitä
<table>
<tbody>
<tr><td>eläin, lemmikki</td><td>Käsitteellisesti eläimellä ja lemmikillä ei ole tämän sovelluksen kannalta eroa. Käytännössä oliot ja taulut nimetään etuliitteellä Pet.</td></tr>
<tr><td>käyttäjä</td><td>Eläimen omistaja, toimenpiteen suorittaja tai tapahtuman kirjaaja. Sidottu käyttäjätunnukseen, jonka avulla käyttäjä tunnistetaan ja käyttöoikeus varmistetaan.</td></tr>
<tr><td>tapahtuma</td><td>Yksittäinen eläimelle sattunut tapahtuma, joka voi olla etukäteen suunniteltu, mutta yleensä jälkikäteen kirjattava yllättävä tapahtuma.</td></tr>
<tr><td>toimenpide</td><td>Aikataulutettu tapahtuma, jossa eläin on omistajan valtuuttaman toimenpiteen kohteen. Esim. trimmaus tai eläinlääkärissä toteutettu verinäyte.</td></tr>
</tbody>
</table>

## Näkymät ja reititykset
Aion toteuttaa ainakin kolme vakionäkymää, jotka saavat oman URL-reitityksen (esim. /month/):
- Päivänäkymä
- Viikkonäkymä
- Kuukausinäkymä

Kukin edellämainituista näyttää näkymän mukaiset toimenpiteet käynnissä olevalle ajanjaksolle. Tarkoitukseni on toteuttaa nämä näkymät parametriohjattuina siten, että (esim. muotoa /month/<year-month>) näyttää annetun aikajakson, mutta ilman parametriä meneillään olevan jakson.

Lisäksi aion toteuttaa lemmikinhallintanäkymän (/pet/<pet_name>), jonka avulla käyttäjä voi lisätä lemmikin ja hallita tämän tietoja. Samassa näkymässä on myös luettelo eläimen viimeisimmistä tapahtumista ja toimenpiteistä.

Kolmanneksi voisin vielä toteuttaa käyttäjänhallintanäkymän, jonka avulla voidaan ainakin lisätä käyttäjä. 

## Tavoite 18.10.
Tavoitteena 18.10. minulla on MVP, jolla on mahdollista:
- kirjautua sovellukseen
- lisätä tietokantaan eläin
- poistaa sellainen eläin, johon ei liity tapahtumia
- lisätä eläimelle tapahtumia ja toimenpiteitä
- näyttää eläimen tapahtumat ja aikataulutetut toimenpiteet päivä, viikko ja kuukausitasolla
