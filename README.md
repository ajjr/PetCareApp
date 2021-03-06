# PetCareApp
PetCareAppin avulla on tarkoitus pitää kirjaa oman lemmikkieläimen hoitotoimenpiteistä ja hyvinvointiin liittyvistä tapahtumista. Se koostuu päivä-, viikko- ja kuukausinäkymistä, jotka näyttävät päivittäin, viikoittain tai kuukausittain toistuvat toimenpiteet. Tällaisia toimenpiteitä eräiden koirarotujen kohdalla voivat olla esim. trimmaus, pesu ja kynsien leikkuu. Jos eläimelle määrätään lääkekuuri, päivittäisiä toimenpiteitä ovat lääkkeen annostelu ja syöttäminen. Lisäksi sovellukseen pitäisi voida kirjata eläimen päivittäinen ruokavalio. Tämä voidaan yhdistää terveyteen liittyviin tapahtumiin kuten esim. yllättävään ripuliin, jolloin omistaja voi tehdä päätelmiä ruokavalion ja/tai lääkkeiden sopivuudesta lemmikilleen.

Sovellus on asennettu Herokuun osoitteessa: https://thawing-harbor-87016.herokuapp.com. Tämä asennus päivittyy automaattisesti vastaamaan tämän Git-repositorion tilaa. Jotta sovellusta voi testat, testaajan on enisn luotava itselleen käyttäjä. Rekisteröintilomake kysyy käyttäjänimeä, nimeä ja sähköpostiosoitetta, mutta näiden ei tarvitse olla aitoja tai edes näyttää aidoilta. Tämän jälkeen kannattaa luoda itselleen lemmikki profiili-sivun kautta, minkä jälkeen lemmikille voi lisätä tapahtumia. Jokaisella lemmikillä on omasivu https://thawing-harbor-87016.herokuapp.com/pet/[lemmikin nimi], joka näyttää lemmikin tiedot ja jonka kautta niitä voi  muokata. Käyttäjän profiilisivun kautta käyttäjä näkee omat lemmikkinsä ja voi lisätä uusia.

## Asennus

### Kehitysympäristöön
1. Asenna jokin tietokanta.
2. Kloonaa tämä repositorio ja luo juurihakemistoon virtual environment:
    ```
    $ git clone https://github.com/ajjr/PetCareApp
    $ cd PetCareApp
    $ python -m venv venv
    ```
3. Asenna riippuvuudet requirements.txt -tiedoston avulla:
    ```
    $ pip install -r requirements.txt
    ```
4. Aseta muuttujaan PETCARE_DB_URI tietokannan yhteysosoite.
5. Aja Flask. Sovellus luo käynnistyessään tietokantaan tarvitsemansa taulut automaattisesti:
    ```
    $ cd petcare
    $ flask run
    ```
6. Palaa PetCareApp -hakemistoon ja lataa tietokannan alustustieto tietokantaan:
    ```
    $ cd util
    $ python load_data.py
    ```
7. Sovelluksen pitäisi nyt olla käyttövalmis. Voit kuitenkin vielä käynnistää sen uudestaan.

### Herokuun
1. Luo itsellesi Heroku-tunnukset ja asenna Herokun komentorivityökalu
2. Kloonaa tämä repositorio:
    ```
    $ git clone https://github.com/ajjr/PetCareApp
    $ cd PetCareApp
    ```
3. Luo Heroku-sovellus:
    ```
    $ heroku create
    ```
   Oletuksena Heroku sijoittaa sovelluksen Pohjois-Amerikkaan. Jos haluat sijoittaa sen Eurooppaan, anna komennolle parametri *--region=eu*:
    ```
    $ heroku create --region=eu
    ```
4. Jos sinulla ei ole vielä Heroku-palvelun ilmaiseen tasoon kuuluvaa Postgres-tietokantaa, ota se käyttöön nyt ja anna juuri luomallesi sovellukselle resurssiksi. Heroku luo Postgresiin oletuskäyttäjän ja settaa sovellukselle config-muuttujan *DATABASE_URL* joka sisältää tietokannan yhteyspolun. PetCareApp käyttää muuttujaa *PETCARE_DB_URI*, johon on asetettava sama arvo, uin *DATABASE_URL* -muuttujalla.

   Tee tämä muutos Web-käyttöliittymässä tai komennolla:
   ```
   $ heroku config:set PETCARE_DB_URI [tietokannan polku]
   ```
5. Vie git-repositorio Herokuun:
    ```
    $ git push heroku master
    ```
    tai
    ```
    $ git push heroku main
    ```
6. Tässä vaiheessa sovelluksen pitäisi käynnistyä. Se luo automaattisesti itselleen tietomallin, mutta ei osaa ladata tarvitsemaansa alustusdataa tietokantaan. Jotta sovellusta voisi käyttää, nämä tiedot on ladattava käsin. Tämä tapahtuu käynnistämällä sovelluksensisäinen bash ja ajamalla latausskripti:
    ```
    $ heroku run bash
    Running bash on ⬢ random-appname... up, run.1234 (Free) 
    ~ $ cd util/
    ~/util $ python load_data.py
   [tässä tulosteessa ei pitäisi näkyä virheilmoituksia]
    ~/util $ exit
   Ctrl^C
   ```
7. Käynnistä sovellus uudestaan. Voit tehdä sen joko Herokun web-käyttöliittymästä tai komennolla:
    ```
    $ heroku restart web
    ```

## Nykytila
Herokuun asennetun sovelluksen nykytila:
- Päivä-, viikko- ja kuukausinäkymät toimivat ja hakevat tietokannasta kullekin päivällä kuuluvat tapahtumat.
- Lemmikkejä on mahdollista lisätä tietokantaan ja muuttaa niiden tietoja.
- Lemmikin tiedot voi hakea lomakkeelle surffaamalla osoitteeseen */pet/[PET_NAME]*. Esim. */pet/Haukku* näyttää kirjautuneen käyttäjän Haukku-nimisen lemmikin tiedot.
- Käyttäjän rekisteröityminen ja kirjautuminen toteuttettu.
- Tapahtuman ja tehtävän lisääminen on toteutettu.


## Käsitteitä
| käsite    | synonyymi | tietomallinimi    | kommentti |
|-----------|-----------|-------------------|-----------|
| lemmikki  | eläin     | Pet               |
| laji      | eläinlaji | Species           |
| rotu      | alalaji   | Breed             | Käytännössä kissa- tai koirarotu, mutta voi tarkoittaa myös esim. kilpikonnalajia. |
| tapahtuma |           | Event             | Konkreettinen tapahtuma, jolle voidaan osoittaa ajankohta. Voi sijoittua tulevaisuuteen tai menneisyyteen. |
| tehtävätyyppi   | operaatio, toimenpidetyyppi | Operation | Tehtävät |
| tehtävä | toimenpide  | OperationInstance | Suunniteltu tai toteutettu tehtävä, jolle on määrätty ajankohta. Tämä tekee tehtävästä tapahtuman, joka määrää sen ajankohdan. |
| käyttäjä | omistaja   | User              | Käyttäjä luodaan rekisteröitymällä. Jokaisen lemmikin omistaja on käyttäjä ja jokaiseen tapahtumaan liittyy käyttäjä. | 

