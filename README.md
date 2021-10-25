# wot
Wheel of Tractatus
1. Asenna Python, jos sitä ei ole. Windows-koneissa ei tavallisesti ole oletuksena.
Komento paljastaa onko: python --version
Pelkän Pythonin asennuspaketti löytyy osoitteesta: https://www.python.org/downloads/
Valitse Python 3.9.7!
Nähtävästi 3.10 törmää ongelmiin pandasin kanssa. WoT käyttää Pandasia excel-tiedostojen lukemiseen.
Ja jotta asennusvaiheen jälkeen asiat menisivät jatkossa simppelimmin, sieltä voi valita "Lisää Python järjestelmämuuttujiin".

Toinen vaihtoehto on ladata Anaconda, mutta sen mukana tulee melkoinen liuta kehittäjän työkaluja, joita et ehkä tarvitse. Mutta jos tarvitset, osannet sen etsiä.

Pythonin perusasennus on kovin suppea, joten siitä puuttuu paketteja, joita varsin yleisesti käytetään. Pandas, pyfiglet, colorama ja openpyxl tarvitaan.

Komentokehotteessa:
pandas ilmaantuu komennolla: pip install pandas

pyfiglet tarvitaan äärest hienon ASCII-art tekstin esittämiseen: pip install pyfiglet

Ja colorama tarvitaan värillisten tekstien näyttämiseen: pip install colorama

JA koska peruasennus on kovin suppea, seuraavaksi se itkee, että openpyxl puuttuu, joten: pip install openpyxl

Ja sitten se pahalainen vasta alkaa skulata. Ja hienosti skulaakin.

2. Tallenna ja pura peli johonkin. Esim omaan Documents kansioon.
3. Navigeeraa komentokehotteessa kansioon.
4. python WheelOfTractatus.py

Sitten pelaamaan.

0 lopettaa pelin.
9 näyttää pelin tilanteen.

save-kansioon menevät tallennetut pelit
data-kansiossa ovat Tractatuksen lauseet ja pelin kielitiedosto.
