#!/usr/bin/env Rscript
# One-off: build saksa_epasaannolliset_verbit_lauseet_praesens.csv

for (loc in c("en_US.UTF-8", "C.UTF-8", "en_US.utf8")) {
  if (!is.na(Sys.setlocale("LC_CTYPE", loc))) break
}

library(readr)

ranked <- read_csv(
  "saksa_epasaannolliset_verbit_ranked.csv",
  show_col_types = FALSE,
  locale = locale(encoding = "UTF-8")
)

fi <- c(
  "Minusta tulee väsynyt.", "Minulla on aikaa.", "Osaan uida.",
  "Annan sinulle vettä.", "Minun pitää opiskella.", "Minun täytyy työskennellä.",
  "Tulen huomenna.", "Menen kotiin.", "Haluan nukkua.", "Seison täällä.",
  "Näen auton.", "Jään kotiin.", "Jätän ikkunan auki.", "Löydän avaimen.",
  "Kirja on täällä.", "Tuon leipää.", "Otan bussin.", "Puhun saksaa.",
  "Tapaan ystäväni.", "Pidän ovea.", "Nimeni on Anna.",
  "Lippu on voimassa tänään.", "Teen paljon.", "Tiedän sen.", "Saan mennä.",
  "Tarjoamme kahvia.", "Kirjoitan sähköpostin.", "Vedän pöytää.",
  "Muutan Berliiniin.", "Juoksen puistossa.", "Matkustan Turkuun.",
  "Ajan autoa.", "Lasi putoaa alas.", "Aloitan nyt.", "Kadotan puhelimeni.",
  "Voitan pelin.", "Nousen pois kyydistä.", "Autan äitiäni.", "Selviän siitä.",
  "Suljen oven.", "Kannan laukkua.", "Kutsun häntä Maxiksi.", "Aurinko paistaa.",
  "Ajattelen sinua.", "Astun sisään.", "Astelen hitaasti.",
  "Se onnistuu minulle.", "Lyön palloa.", "Tunnen hänet.", "Heitän pallon.",
  "Pyydän apua.", "Kasvi kuolee.", "Istun täällä.", "Syön leipää.",
  "Lataan puhelimen.", "Tartutan lasiin.", "Luen kirjaa.",
  "Soitan ystävälleni.", "Lapsi kasvaa nopeasti.", "Osoitan tien.",
  "Neuvon sinua.", "Kutsun sinut.", "Juoksen nopeasti.", "Sidon kengät.",
  "Laiva uppoaa.", "Taulu roikkuu siellä.", "Pidän kahvista.",
  "Se kuulostaa hyvältä.", "Lennän Saksaan.", "Suosittelen kirjaa.",
  "Nautin lomasta.", "Katkaisen leivän.", "Oksa katkeaa.",
  "Mitä täällä tapahtuu?", "Työnnän ovea.", "Törmään pöytään.",
  "Kärsin päänsärystä.", "Harrastan urheilua.", "Leikkaan leivän.",
  "Näytät isältäsi.", "Kamppailen ongelman kanssa.", "Koira katoaa.",
  "Hän varastaa rahaa.", "Otan valokuvan.", "Maalaan seinän.",
  "Mittaan pöydän.", "Nostan laatikon.", "Unohdan nimen.",
  "Sää pakottaa minut jäämään kotiin.", "Laulan laulun.",
  "Vesi virtaa nopeasti.", "Otan pallon kiinni.", "Hyppään korkealle.",
  "Juon vettä.", "Tuli palaa.", "Revin paperin.", "Käännän lihan.",
  "Väistyn taaksepäin.", "Työnnän kärryä.", "Nukun pitkään.",
  "He ylistävät tuotetta.", "Kissa pakenee.", "Uin mielelläni.",
  "Olen nyt hiljaa.", "Lähetän viestin.", "Mehiläinen pistää minua.",
  "Riitelen veljeni kanssa.", "Kastelen kukat.", "Vältän stressiä.",
  "Vesi tunkeutuu taloon.", "Leivon kakkua.", "En valehtele.",
  "Koira puree.", "Kaivan kuopan.", "Vauva huutaa.", "Pesen käteni.",
  "Koira syö lihaa.", "Kukat tuoksuvat hyvältä.", "Kello heiluu.",
  "Taivutan metallia.", "Tie kääntyy vasemmalle.", "Hän pettää ystävänsä.",
  "Vihellän laulua.", "Ratsastan hevosella.", "Sulatan voita.",
  "Jää sulaa.", "Lainaan rahaa.", "Tuuli puhaltaa voimakkaasti.",
  "Heitän pallon.", "Säikähdän helposti.", "Kissa hiipii hiljaa.",
  "Paistan kalaa.", "Vene liukuu veden yli.", "Vannon sen.",
  "Minulla on kylmä tänään.", "Annan sinulle anteeksi.",
  "Sade pilaa ruoan.", "Ruoka pilaantuu nopeasti.", "En käske mitään.",
  "Vauva ryömii."
)

de <- c(
  "Ich werde müde.", "Ich habe Zeit.", "Ich kann schwimmen.",
  "Ich gebe dir Wasser.", "Ich soll lernen.", "Ich muss arbeiten.",
  "Ich komme morgen.", "Ich gehe nach Hause.", "Ich will schlafen.",
  "Ich stehe hier.", "Ich sehe ein Auto.", "Ich bleibe zu Hause.",
  "Ich lasse das Fenster offen.", "Ich finde den Schlüssel.",
  "Das Buch liegt hier.", "Ich bringe Brot.", "Ich nehme den Bus.",
  "Ich spreche Deutsch.", "Ich treffe meinen Freund.", "Ich halte die Tür.",
  "Ich heiße Anna.", "Das Ticket gilt heute.", "Ich tue viel.", "Ich weiß das.",
  "Ich darf gehen.", "Wir bieten Kaffee an.", "Ich schreibe eine E-Mail.",
  "Ich ziehe den Tisch.", "Ich ziehe nach Berlin.", "Ich laufe im Park.",
  "Ich fahre nach Turku.", "Ich fahre das Auto.", "Das Glas fällt runter.",
  "Ich beginne jetzt.", "Ich verliere mein Handy.", "Ich gewinne das Spiel.",
  "Ich steige aus.", "Ich helfe meiner Mutter.", "Ich schaffe das.",
  "Ich schließe die Tür.", "Ich trage eine Tasche.", "Ich nenne ihn Max.",
  "Die Sonne scheint.", "Ich denke an dich.", "Ich trete ein.",
  "Ich schreite langsam.", "Das gelingt mir.", "Ich schlage den Ball.",
  "Ich kenne ihn.", "Ich werfe den Ball.", "Ich bitte um Hilfe.",
  "Die Pflanze stirbt.", "Ich sitze hier.", "Ich esse Brot.",
  "Ich lade das Handy.", "Ich greife nach dem Glas.", "Ich lese ein Buch.",
  "Ich rufe meinen Freund.", "Das Kind wächst schnell.", "Ich weise den Weg.",
  "Ich rate dir.", "Ich lade dich ein.", "Ich renne schnell.",
  "Ich binde die Schuhe.", "Das Schiff sinkt.", "Das Bild hängt dort.",
  "Ich mag Kaffee.", "Das klingt gut.", "Ich fliege nach Deutschland.",
  "Ich empfehle das Buch.", "Ich genieße den Urlaub.", "Ich breche das Brot.",
  "Der Ast bricht.", "Was geschieht hier?", "Ich stoße die Tür.",
  "Ich stoße gegen den Tisch.", "Ich leide an Kopfschmerzen.",
  "Ich treibe Sport.", "Ich schneide das Brot.", "Du gleichst deinem Vater.",
  "Ich ringe mit dem Problem.", "Der Hund verschwindet.", "Er stiehlt Geld.",
  "Ich schieße ein Foto.", "Ich streiche die Wand.", "Ich messe den Tisch.",
  "Ich hebe die Kiste.", "Ich vergesse den Namen.",
  "Das Wetter zwingt mich zu Hause zu bleiben.", "Ich singe ein Lied.",
  "Das Wasser fließt schnell.", "Ich fange den Ball.", "Ich springe hoch.",
  "Ich trinke Wasser.", "Das Feuer brennt.", "Ich reiße das Papier.",
  "Ich wende das Fleisch.", "Ich weiche zurück.", "Ich schiebe den Wagen.",
  "Ich schlafe lange.", "Sie preisen das Produkt.", "Die Katze flieht.",
  "Ich schwimme gern.", "Ich schweige jetzt.", "Ich sende eine Nachricht.",
  "Die Biene sticht mich.", "Ich streite mit meinem Bruder.",
  "Ich gieße die Blumen.", "Ich meide Stress.", "Wasser dringt ins Haus.",
  "Ich backe Kuchen.", "Ich lüge nicht.", "Der Hund beißt.",
  "Ich grabe ein Loch.", "Das Baby schreit.", "Ich wasche meine Hände.",
  "Der Hund frisst Fleisch.", "Die Blumen riechen gut.", "Die Glocke schwingt.",
  "Ich biege das Metall.", "Die Straße biegt nach links.",
  "Er betrügt seine Freunde.", "Ich pfeife ein Lied.", "Ich reite ein Pferd.",
  "Ich schmelze Butter.", "Das Eis schmilzt.", "Ich leihe Geld.",
  "Der Wind bläst stark.", "Ich schmeiße den Ball.", "Ich erschrecke leicht.",
  "Die Katze schleicht leise.", "Ich brate Fisch.",
  "Das Boot gleitet über das Wasser.", "Ich schwöre es.", "Ich friere heute.",
  "Ich verzeihe dir.", "Der Regen verdirbt das Essen.",
  "Das Essen verdirbt schnell.", "Ich befehle nichts.", "Das Baby kriecht."
)

fi_du <- c(
  "Sinusta tulee väsynyt.", "Sinulla on aikaa.", "Osaat uida.",
  "Annat minulle vettä.", "Sinun pitää opiskella.", "Sinun täytyy työskennellä.",
  "Tulet huomenna.", "Menet kotiin.", "Haluat nukkua.", "Seisot täällä.",
  "Näet auton.", "Jäät kotiin.", "Jätät ikkunan auki.", "Löydät avaimen.",
  "Kirja on täällä.", "Tuot leipää.", "Otat bussin.", "Puhut saksaa.",
  "Tapaat ystäväsi.", "Pidät ovea.", "Nimesi on Anna.",
  "Lippu on voimassa tänään.", "Teet paljon.", "Tiedät sen.", "Saat mennä.",
  "Tarjoatte kahvia.", "Kirjoitat sähköpostin.", "Vedät pöytää.",
  "Muutat Berliiniin.", "Juokset puistossa.", "Matkustat Turkuun.",
  "Ajaat autoa.", "Lasi putoaa alas.", "Aloitat nyt.", "Kadotat puhelimesi.",
  "Voitat pelin.", "Nouset pois kyydistä.", "Autat äitiäsi.", "Selviät siitä.",
  "Suljet oven.", "Kannat laukkua.", "Kutsut häntä Maxiksi.", "Aurinko paistaa.",
  "Ajattelet minua.", "Astut sisään.", "Astelet hitaasti.",
  "Se onnistuu sinulle.", "Lyöt palloa.", "Tunnet hänet.", "Heität pallon.",
  "Pyydät apua.", "Kasvi kuolee.", "Istut täällä.", "Syöt leipää.",
  "Lataat puhelimen.", "Tartut lasiin.", "Luet kirjaa.",
  "Soitat ystävällesi.", "Lapsi kasvaa nopeasti.", "Osoitat tien.",
  "Neuvot minua.", "Kutsut minut.", "Juokset nopeasti.", "Sidot kengät.",
  "Laiva uppoaa.", "Taulu roikkuu siellä.", "Pidät kahvista.",
  "Se kuulostaa hyvältä.", "Lennät Saksaan.", "Suosittelet kirjaa.",
  "Nautit lomasta.", "Katkaiset leivän.", "Oksa katkeaa.",
  "Mitä täällä tapahtuu?", "Työnnät ovea.", "Törmäät pöytään.",
  "Kärsit päänsärystä.", "Harrastat urheilua.", "Leikkaat leivän.",
  "Näytät isältäsi.", "Kamppailet ongelman kanssa.", "Koira katoaa.",
  "Varastat rahaa.", "Otat valokuvan.", "Maalaat seinän.",
  "Mittaat pöydän.", "Nostat laatikon.", "Unohdat nimen.",
  "Sää pakottaa sinut jäämään kotiin.", "Laulat laulun.",
  "Vesi virtaa nopeasti.", "Otat pallon kiinni.", "Hyppäät korkealle.",
  "Juot vettä.", "Tuli palaa.", "Revit paperin.", "Käännät lihan.",
  "Väistyt taaksepäin.", "Työnnät kärryä.", "Nukut pitkään.",
  "Ylistätte tuotetta.", "Kissa pakenee.", "Uit mielelläsi.",
  "Olet nyt hiljaa.", "Lähetät viestin.", "Mehiläinen pistää sinua.",
  "Riitelet veljesi kanssa.", "Kastelet kukat.", "Vältät stressiä.",
  "Vesi tunkeutuu taloon.", "Leivot kakkua.", "Et valehtele.",
  "Koira puree.", "Kaivat kuopan.", "Vauva huutaa.", "Peset kätesi.",
  "Koira syö lihaa.", "Kukat tuoksuvat hyvältä.", "Kello heiluu.",
  "Taivutat metallia.", "Tie kääntyy vasemmalle.", "Petät ystäväsi.",
  "Vihellät laulua.", "Ratsastat hevosella.", "Sulatat voita.",
  "Jää sulaa.", "Lainaat rahaa.", "Tuuli puhaltaa voimakkaasti.",
  "Heität pallon.", "Säikähdät helposti.", "Kissa hiipii hiljaa.",
  "Paistat kalaa.", "Vene liukuu veden yli.", "Vannot sen.",
  "Sinulla on kylmä tänään.", "Annat minulle anteeksi.",
  "Sade pilaa ruoan.", "Ruoka pilaantuu nopeasti.", "Et käske mitään.",
  "Vauva ryömii."
)

de_du <- c(
  "Du wirst müde.", "Du hast Zeit.", "Du kannst schwimmen.",
  "Du gibst mir Wasser.", "Du sollst lernen.", "Du musst arbeiten.",
  "Du kommst morgen.", "Du gehst nach Hause.", "Du willst schlafen.",
  "Du stehst hier.", "Du siehst ein Auto.", "Du bleibst zu Hause.",
  "Du lässt das Fenster offen.", "Du findest den Schlüssel.",
  "Das Buch liegt hier.", "Du bringst Brot.", "Du nimmst den Bus.",
  "Du sprichst Deutsch.", "Du triffst deinen Freund.", "Du hältst die Tür.",
  "Du heißt Anna.", "Das Ticket gilt heute.", "Du tust viel.", "Du weißt das.",
  "Du darfst gehen.", "Ihr bietet Kaffee an.", "Du schreibst eine E-Mail.",
  "Du ziehst den Tisch.", "Du ziehst nach Berlin.", "Du läufst im Park.",
  "Du fährst nach Turku.", "Du fährst das Auto.", "Das Glas fällt runter.",
  "Du beginnst jetzt.", "Du verlierst dein Handy.", "Du gewinnst das Spiel.",
  "Du steigst aus.", "Du hilfst deiner Mutter.", "Du schaffst das.",
  "Du schließt die Tür.", "Du trägst eine Tasche.", "Du nennst ihn Max.",
  "Die Sonne scheint.", "Du denkst an mich.", "Du trittst ein.",
  "Du schreitest langsam.", "Das gelingt dir.", "Du schlägst den Ball.",
  "Du kennst ihn.", "Du wirfst den Ball.", "Du bittest um Hilfe.",
  "Die Pflanze stirbt.", "Du sitzt hier.", "Du isst Brot.",
  "Du lädst das Handy.", "Du greifst nach dem Glas.", "Du liest ein Buch.",
  "Du rufst deinen Freund.", "Das Kind wächst schnell.", "Du weist den Weg.",
  "Du rätst mir.", "Du lädst mich ein.", "Du rennst schnell.",
  "Du bindest die Schuhe.", "Das Schiff sinkt.", "Das Bild hängt dort.",
  "Du magst Kaffee.", "Das klingt gut.", "Du fliegst nach Deutschland.",
  "Du empfiehlst das Buch.", "Du genießt den Urlaub.", "Du brichst das Brot.",
  "Der Ast bricht.", "Was geschieht hier?", "Du stößt die Tür.",
  "Du stößt gegen den Tisch.", "Du leidest an Kopfschmerzen.",
  "Du treibst Sport.", "Du schneidest das Brot.", "Du gleichst deinem Vater.",
  "Du ringst mit dem Problem.", "Der Hund verschwindet.", "Du stiehlst Geld.",
  "Du schießt ein Foto.", "Du streichst die Wand.", "Du misst den Tisch.",
  "Du hebst die Kiste.", "Du vergisst den Namen.",
  "Das Wetter zwingt dich zu Hause zu bleiben.", "Du singst ein Lied.",
  "Das Wasser fließt schnell.", "Du fängst den Ball.", "Du springst hoch.",
  "Du trinkst Wasser.", "Das Feuer brennt.", "Du reißt das Papier.",
  "Du wendest das Fleisch.", "Du weichst zurück.", "Du schiebst den Wagen.",
  "Du schläfst lange.", "Ihr preist das Produkt.", "Die Katze flieht.",
  "Du schwimmst gern.", "Du schweigst jetzt.", "Du sendest eine Nachricht.",
  "Die Biene sticht dich.", "Du streitest mit deinem Bruder.",
  "Du gießt die Blumen.", "Du meidest Stress.", "Wasser dringt ins Haus.",
  "Du backst Kuchen.", "Du lügst nicht.", "Der Hund beißt.",
  "Du gräbst ein Loch.", "Das Baby schreit.", "Du wäschst deine Hände.",
  "Der Hund frisst Fleisch.", "Die Blumen riechen gut.", "Die Glocke schwingt.",
  "Du biegst das Metall.", "Die Straße biegt nach links.",
  "Du betrügst deine Freunde.", "Du pfeifst ein Lied.", "Du reitest ein Pferd.",
  "Du schmilzt Butter.", "Das Eis schmilzt.", "Du leihst Geld.",
  "Der Wind bläst stark.", "Du schmeißt den Ball.", "Du erschrickst leicht.",
  "Die Katze schleicht leise.", "Du brätst Fisch.",
  "Das Boot gleitet über das Wasser.", "Du schwörst es.", "Du frierst heute.",
  "Du verzeihst mir.", "Der Regen verdirbt das Essen.",
  "Das Essen verdirbt schnell.", "Du befiehlst nichts.", "Das Baby kriecht."
)

fi_er <- c(
  "Hänestä tulee väsynyt.", "Hänellä on aikaa.", "Hän osaa uida.",
  "Hän antaa minulle vettä.", "Hänen pitää opiskella.", "Hänen täytyy työskennellä.",
  "Hän tulee huomenna.", "Hän menee kotiin.", "Hän haluaa nukkua.", "Hän seisoo täällä.",
  "Hän näkee auton.", "Hän jää kotiin.", "Hän jättää ikkunan auki.", "Hän löytää avaimen.",
  "Kirja on täällä.", "Hän tuo leipää.", "Hän ottaa bussin.", "Hän puhuu saksaa.",
  "Hän tapaa ystävänsä.", "Hän pitää ovea.", "Hänen nimensä on Anna.",
  "Lippu on voimassa tänään.", "Hän tekee paljon.", "Hän tietää sen.", "Hän saa mennä.",
  "Hän tarjoaa kahvia.", "Hän kirjoittaa sähköpostin.", "Hän vetää pöytää.",
  "Hän muuttaa Berliiniin.", "Hän juoksee puistossa.", "Hän matkustaa Turkuun.",
  "Hän ajaa autoa.", "Lasi putoaa alas.", "Hän aloittaa nyt.", "Hän kadottaa puhelimen.",
  "Hän voittaa pelin.", "Hän nousee pois kyydistä.", "Hän auttaa äitiään.", "Hän selviää siitä.",
  "Hän sulkee oven.", "Hän kantaa laukkua.", "Hän kutsuu häntä Maxiksi.", "Aurinko paistaa.",
  "Hän ajattelee sinua.", "Hän astuu sisään.", "Hän astelee hitaasti.",
  "Se onnistuu hänelle.", "Hän lyö palloa.", "Hän tuntee hänet.", "Hän heittää pallon.",
  "Hän pyytää apua.", "Kasvi kuolee.", "Hän istuu täällä.", "Hän syö leipää.",
  "Hän lataa puhelimen.", "Hän tarttuu lasiin.", "Hän lukee kirjaa.",
  "Hän soittaa ystävälleen.", "Lapsi kasvaa nopeasti.", "Hän osoittaa tien.",
  "Hän neuvoo sinua.", "Hän kutsuu sinut.", "Hän juoksee nopeasti.", "Hän sitoo kengät.",
  "Laiva uppoaa.", "Taulu roikkuu siellä.", "Hän pitää kahvista.",
  "Se kuulostaa hyvältä.", "Hän lentää Saksaan.", "Hän suosittelee kirjaa.",
  "Hän nauttii lomasta.", "Hän katkaisee leivän.", "Oksa katkeaa.",
  "Mitä täällä tapahtuu?", "Hän työntää ovea.", "Hän törmää pöytään.",
  "Hän kärsii päänsärystä.", "Hän harrastaa urheilua.", "Hän leikkaa leivän.",
  "Hän näyttää isältään.", "Hän kamppailee ongelman kanssa.", "Koira katoaa.",
  "Hän varastaa rahaa.", "Hän ottaa valokuvan.", "Hän maalaa seinän.",
  "Hän mittaa pöydän.", "Hän nostaa laatikon.", "Hän unohtaa nimen.",
  "Sää pakottaa hänet jäämään kotiin.", "Hän laulaa laulun.",
  "Vesi virtaa nopeasti.", "Hän ottaa pallon kiinni.", "Hän hyppää korkealle.",
  "Hän juo vettä.", "Tuli palaa.", "Hän repii paperin.", "Hän kääntää lihan.",
  "Hän väistyy taaksepäin.", "Hän työntää kärryä.", "Hän nukkuu pitkään.",
  "He ylistävät tuotetta.", "Kissa pakenee.", "Hän ui mielellään.",
  "Hän on nyt hiljaa.", "Hän lähettää viestin.", "Mehiläinen pistää häntä.",
  "Hän riitelee veljensä kanssa.", "Hän kastelee kukat.", "Hän välttää stressiä.",
  "Vesi tunkeutuu taloon.", "Hän leipoo kakkua.", "Hän ei valehtele.",
  "Koira puree.", "Hän kaivaa kuopan.", "Vauva huutaa.", "Hän pesee kätensä.",
  "Koira syö lihaa.", "Kukat tuoksuvat hyvältä.", "Kello heiluu.",
  "Hän taivuttaa metallia.", "Tie kääntyy vasemmalle.", "Hän pettää ystäviään.",
  "Hän viheltää laulua.", "Hän ratsastaa hevosella.", "Hän sulattaa voita.",
  "Jää sulaa.", "Hän lainaa rahaa.", "Tuuli puhaltaa voimakkaasti.",
  "Hän heittää pallon.", "Hän säikkyy helposti.", "Kissa hiipii hiljaa.",
  "Hän paistaa kalaa.", "Vene liukuu veden yli.", "Hän vannoo sen.",
  "Hänellä on kylmä tänään.", "Hän antaa minulle anteeksi.",
  "Sade pilaa ruoan.", "Ruoka pilaantuu nopeasti.", "Hän ei käske mitään.",
  "Vauva ryömii."
)

de_er <- c(
  "Er wird müde.", "Er hat Zeit.", "Er kann schwimmen.",
  "Er gibt mir Wasser.", "Er soll lernen.", "Er muss arbeiten.",
  "Er kommt morgen.", "Er geht nach Hause.", "Er will schlafen.",
  "Er steht hier.", "Er sieht ein Auto.", "Er bleibt zu Hause.",
  "Er lässt das Fenster offen.", "Er findet den Schlüssel.",
  "Das Buch liegt hier.", "Er bringt Brot.", "Er nimmt den Bus.",
  "Er spricht Deutsch.", "Er trifft seinen Freund.", "Er hält die Tür.",
  "Er heißt Anna.", "Das Ticket gilt heute.", "Er tut viel.", "Er weiß das.",
  "Er darf gehen.", "Er bietet Kaffee an.", "Er schreibt eine E-Mail.",
  "Er zieht den Tisch.", "Er zieht nach Berlin.", "Er läuft im Park.",
  "Er fährt nach Turku.", "Er fährt das Auto.", "Das Glas fällt runter.",
  "Er beginnt jetzt.", "Er verliert sein Handy.", "Er gewinnt das Spiel.",
  "Er steigt aus.", "Er hilft seiner Mutter.", "Er schafft das.",
  "Er schließt die Tür.", "Er trägt eine Tasche.", "Er nennt ihn Max.",
  "Die Sonne scheint.", "Er denkt an dich.", "Er tritt ein.",
  "Er schreitet langsam.", "Es gelingt ihm.", "Er schlägt den Ball.",
  "Er kennt ihn.", "Er wirft den Ball.", "Er bittet um Hilfe.",
  "Die Pflanze stirbt.", "Er sitzt hier.", "Er isst Brot.",
  "Er lädt das Handy.", "Er greift nach dem Glas.", "Er liest ein Buch.",
  "Er ruft seinen Freund.", "Das Kind wächst schnell.", "Er weist den Weg.",
  "Er rät dir.", "Er lädt dich ein.", "Er rennt schnell.",
  "Er bindet die Schuhe.", "Das Schiff sinkt.", "Das Bild hängt dort.",
  "Er mag Kaffee.", "Das klingt gut.", "Er fliegt nach Deutschland.",
  "Er empfiehlt das Buch.", "Er genießt den Urlaub.", "Er bricht das Brot.",
  "Der Ast bricht.", "Was geschieht hier?", "Er stößt die Tür.",
  "Er stößt gegen den Tisch.", "Er leidet an Kopfschmerzen.",
  "Er treibt Sport.", "Er schneidet das Brot.", "Er gleicht seinem Vater.",
  "Er ringt mit dem Problem.", "Der Hund verschwindet.", "Er stiehlt Geld.",
  "Er schießt ein Foto.", "Er streicht die Wand.", "Er misst den Tisch.",
  "Er hebt die Kiste.", "Er vergisst den Namen.",
  "Das Wetter zwingt ihn zu Hause zu bleiben.", "Er singt ein Lied.",
  "Das Wasser fließt schnell.", "Er fängt den Ball.", "Er springt hoch.",
  "Er trinkt Wasser.", "Das Feuer brennt.", "Er reißt das Papier.",
  "Er wendet das Fleisch.", "Er weicht zurück.", "Er schiebt den Wagen.",
  "Er schläft lange.", "Sie preisen das Produkt.", "Die Katze flieht.",
  "Er schwimmt gern.", "Er schweigt jetzt.", "Er sendet eine Nachricht.",
  "Die Biene sticht ihn.", "Er streitet mit seinem Bruder.",
  "Er gießt die Blumen.", "Er meidet Stress.", "Wasser dringt ins Haus.",
  "Er backt Kuchen.", "Er lügt nicht.", "Der Hund beißt.",
  "Er gräbt ein Loch.", "Das Baby schreit.", "Er wäscht seine Hände.",
  "Der Hund frisst Fleisch.", "Die Blumen riechen gut.", "Die Glocke schwingt.",
  "Er biegt das Metall.", "Die Straße biegt nach links.",
  "Er betrügt seine Freunde.", "Er pfeift ein Lied.", "Er reitet ein Pferd.",
  "Er schmilzt Butter.", "Das Eis schmilzt.", "Er leiht Geld.",
  "Der Wind bläst stark.", "Er schmeißt den Ball.", "Er erschrickt leicht.",
  "Die Katze schleicht leise.", "Er brät Fisch.",
  "Das Boot gleitet über das Wasser.", "Er schwört es.", "Er friert heute.",
  "Er verzeiht mir.", "Der Regen verdirbt das Essen.",
  "Das Essen verdirbt schnell.", "Er befiehlt nichts.", "Das Baby kriecht."
)

# wir (1. pers. pl.) — user batch; ranks 73, 76, 121, 125, 138, 139 filled to match ranked duplicates
fi_wir_u <- c(
  "Me tulemme opettajiksi.", "Meillä on aikaa.", "Me osaamme uida.",
  "Me annamme kirjan.", "Meidän pitää lähteä.", "Meidän täytyy oppia.",
  "Me tulemme kotiin.", "Me menemme kouluun.", "Me haluamme jäätelöä.",
  "Me seisomme tässä.", "Me näemme sinut.", "Me jäämme kotiin.",
  "Me jätämme sen.", "Me löydämme sen.", "Me makaamme sängyllä.",
  "Me tuomme kirjan.", "Me otamme bussin.", "Me puhumme saksaa.",
  "Me tapaamme sinut.", "Me pidämme tauon.", "Meidän nimi on Anna ja Tom.",
  "Nämä säännöt ovat voimassa.", "Me teemme sen.", "Me tiedämme sen.",
  "Me saamme mennä ulos.", "Me tarjoamme apua.", "Me kirjoitamme kirjeen.",
  "Me vedämme laatikkoa.", "Me muutamme uuteen kotiin.", "Me juoksemme puistossa.",
  "Me matkustamme Berliiniin.", "Me ajamme autoa.", "Me kaadumme.",
  "Me aloitamme nyt.", "Me häviämme pelin.", "Me voitamme pelin.",
  "Me nousemme ylös.", "Me autamme sinua.", "Me luomme jotain.",
  "Me suljemme oven.", "Me kannamme laukkua.", "Me kutsumme häntä Tomiksi.",
  "Aurinko paistaa.", "Me ajattelemme sitä.", "Me astumme sisään.",
  "Me astumme hitaasti.", "Me onnistumme.", "Me lyömme palloa.",
  "Me tunnemme hänet.", "Me heitämme pallon.", "Me pyydämme apua.",
  "Me emme kuole nyt.", "Me istumme täällä.", "Me syömme pizzaa.",
  "Me lataamme akun.", "Me tartumme siihen.", "Me luemme kirjaa.",
  "Me huudamme sinua.", "Me kasvamme nopeasti.", "Me osoitamme tietä.",
  "Me neuvomme sinua.", "Me kutsumme sinut.", "Me juoksemme nopeasti.",
  "Me sidomme köyden.", "Me vajoamme alas.", "Me roikumme täällä.",
  "Me pidämme tästä.", "Tämä kuulostaa hyvältä.", "Me lennämme Roomaan.",
  "Me suosittelemme tätä.", "Me nautimme tästä.", "Me rikomme lasin.",
  "Mitä tapahtuu?", "Me työnnämme oven.", "Me kärsimme nyt.",
  "Me harrastamme urheilua.", "Me leikkaamme leipää.", "Me muistutamme häntä.",
  "Me kamppailemme.", "Me katoamme.", "Me varastamme sen.",
  "Me ammutaan palloa.", "Me maalaamme seinän.", "Me mittaamme sen.",
  "Me nostamme sen.", "Me unohdamme sen.", "Me pakotamme hänet.",
  "Me laulamme laulun.", "Vesi virtaa.", "Me pyydystämme kalan.",
  "Me hyppäämme.", "Me juomme vettä.", "Talo palaa.",
  "Me revimme paperin.", "Me käännämme auton.", "Me väistämme.",
  "Me työnnämme pöytää.", "Me nukumme.", "Me ylistämme häntä.",
  "Me pakenemme.", "Me uimme.", "Me olemme hiljaa.",
  "Me lähetämme kirjeen.", "Me pistämme neulan.", "Me riitelemme.",
  "Me kaadamme vettä.", "Me vältämme sitä.", "Me tunkeudumme sisään.",
  "Me leivomme leipää.", "Me valehtelemme.", "Me puremme.",
  "Me kaivamme kuopan.", "Me huudamme.", "Me pesemme kädet.",
  "Eläimet syövät.", "Me haistamme sen.", "Me heilutamme käsiä.",
  "Me taivutamme sen.", "Me petämme.", "Me vihellemme.",
  "Me ratsastamme.", "Lumi sulaa.", "Me lainaamme kirjan.",
  "Me puhallamme.", "Me heitämme sen.", "Me säikähdämme.",
  "Me hiivimme.", "Me paistamme lihaa.", "Me liukuumme.",
  "Me vannomme.", "Me palellumme.", "Me annamme anteeksi.",
  "Me pilaamme ruoan.", "Me ryömimme."
)

de_wir_u <- c(
  "Wir werden Lehrer.", "Wir haben Zeit.", "Wir können schwimmen.",
  "Wir geben das Buch.", "Wir sollen gehen.", "Wir müssen lernen.",
  "Wir kommen nach Hause.", "Wir gehen zur Schule.", "Wir wollen Eis.",
  "Wir stehen hier.", "Wir sehen dich.", "Wir bleiben zu Hause.",
  "Wir lassen das.", "Wir finden das.", "Wir liegen im Bett.",
  "Wir bringen das Buch.", "Wir nehmen den Bus.", "Wir sprechen Deutsch.",
  "Wir treffen dich.", "Wir halten Pause.", "Wir heißen Anna und Tom.",
  "Diese Regeln gelten.", "Wir tun das.", "Wir wissen das.",
  "Wir dürfen rausgehen.", "Wir bieten Hilfe.", "Wir schreiben einen Brief.",
  "Wir ziehen die Kiste.", "Wir ziehen um.", "Wir laufen im Park.",
  "Wir fahren nach Berlin.", "Wir fahren das Auto.", "Wir fallen.",
  "Wir beginnen jetzt.", "Wir verlieren das Spiel.", "Wir gewinnen das Spiel.",
  "Wir steigen auf.", "Wir helfen dir.", "Wir schaffen etwas.",
  "Wir schließen die Tür.", "Wir tragen die Tasche.", "Wir nennen ihn Tom.",
  "Die Sonne scheint.", "Wir denken daran.", "Wir treten ein.",
  "Wir schreiten langsam.", "Uns gelingt es.", "Wir schlagen den Ball.",
  "Wir kennen ihn.", "Wir werfen den Ball.", "Wir bitten um Hilfe.",
  "Wir sterben nicht jetzt.", "Wir sitzen hier.", "Wir essen Pizza.",
  "Wir laden den Akku.", "Wir greifen danach.", "Wir lesen ein Buch.",
  "Wir rufen dich.", "Wir wachsen schnell.", "Wir weisen den Weg.",
  "Wir raten dir.", "Wir laden dich ein.", "Wir rennen schnell.",
  "Wir binden das Seil.", "Wir sinken.", "Wir hängen hier.",
  "Wir mögen das.", "Das klingt gut.", "Wir fliegen nach Rom.",
  "Wir empfehlen das.", "Wir genießen das.", "Wir brechen das Glas.",
  "Was geschieht?", "Wir stoßen die Tür.", "Wir leiden jetzt.",
  "Wir treiben Sport.", "Wir schneiden Brot.", "Wir gleichen ihm.",
  "Wir ringen.", "Wir verschwinden.", "Wir stehlen das.",
  "Wir schießen den Ball.", "Wir streichen die Wand.", "Wir messen das.",
  "Wir heben das.", "Wir vergessen das.", "Wir zwingen ihn.",
  "Wir singen ein Lied.", "Das Wasser fließt.", "Wir fangen einen Fisch.",
  "Wir springen.", "Wir trinken Wasser.", "Das Haus brennt.",
  "Wir reißen das Papier.", "Wir wenden das Auto.", "Wir weichen aus.",
  "Wir schieben den Tisch.", "Wir schlafen.", "Wir preisen ihn.",
  "Wir fliehen.", "Wir schwimmen.", "Wir schweigen.",
  "Wir senden den Brief.", "Wir stechen die Nadel.", "Wir streiten.",
  "Wir gießen Wasser.", "Wir meiden das.", "Wir dringen ein.",
  "Wir backen Brot.", "Wir lügen.", "Wir beißen.",
  "Wir graben ein Loch.", "Wir schreien.", "Wir waschen die Hände.",
  "Wir fressen.", "Wir riechen das.", "Wir schwingen die Arme.",
  "Wir biegen das.", "Wir betrügen.", "Wir pfeifen.",
  "Wir reiten.", "Der Schnee schmilzt.", "Wir leihen ein Buch.",
  "Wir blasen.", "Wir schmeißen das.", "Wir erschrecken.",
  "Wir schleichen.", "Wir braten Fleisch.", "Wir gleiten.",
  "Wir schwören.", "Wir frieren.", "Wir verzeihen.",
  "Wir verderben das Essen.", "Wir kriechen."
)

fi_wir_fill <- c(
  "73" = "Oksat katkeavat.",
  "76" = "Me törmäämme pöytään.",
  "121" = "Tie kääntyy vasemmalle.",
  "125" = "Me sulatamme voita.",
  "138" = "Ruoka pilaantuu nopeasti.",
  "139" = "Me emme käske mitään."
)
de_wir_fill <- c(
  "73" = "Die Äste brechen.",
  "76" = "Wir stoßen gegen den Tisch.",
  "121" = "Die Straße biegt nach links.",
  "125" = "Wir schmelzen Butter.",
  "138" = "Das Essen verdirbt schnell.",
  "139" = "Wir befehlen nichts."
)

stopifnot(length(fi_wir_u) == 134L, length(fi_wir_u) == length(de_wir_u))

fi_wir <- character(140)
de_wir <- character(140)
j <- 1L
for (i in seq_len(140)) {
  rk <- as.character(i)
  if (rk %in% names(fi_wir_fill)) {
    fi_wir[i] <- fi_wir_fill[[rk]]
    de_wir[i] <- de_wir_fill[[rk]]
  } else {
    fi_wir[i] <- fi_wir_u[j]
    de_wir[i] <- de_wir_u[j]
    j <- j + 1L
  }
}

# ihr (2. pers. pl.) — user batch; ranks 73, 76, 121, 125, 138, 139 filled
fi_ihr_u <- c(
  "Te tulette opettajiksi.", "Teillä on aikaa.", "Te osaatte uida.",
  "Te annatte kirjan.", "Teidän pitää lähteä.", "Teidän täytyy oppia.",
  "Te tulette kotiin.", "Te menette kouluun.", "Te haluatte jäätelöä.",
  "Te seisotte tässä.", "Te näette minut.", "Te jäätte kotiin.",
  "Te jätätte sen.", "Te löydätte sen.", "Te makaatte sängyllä.",
  "Te tuotatte kirjan.", "Te otatte bussin.", "Te puhutte saksaa.",
  "Te tapaatte hänet.", "Te pidätte tauon.", "Teidän nimenne on…",
  "Nämä säännöt ovat voimassa teille.", "Te teette sen.", "Te tiedätte sen.",
  "Te saatte mennä ulos.", "Te tarjoatte apua.", "Te kirjoitatte kirjeen.",
  "Te vedätte laatikkoa.", "Te muutatte uuteen kotiin.", "Te juoksette puistossa.",
  "Te matkustatte Berliiniin.", "Te ajatte autoa.", "Te kaadutte.",
  "Te aloitte nyt.", "Te häviätte pelin.", "Te voitatte pelin.",
  "Te nousette ylös.", "Te autatte minua.", "Te luotte jotain.",
  "Te suljette oven.", "Te kannatte laukkua.", "Te kutsutte häntä Tomiksi.",
  "Aurinko paistaa teille.", "Te ajattelette sitä.", "Te astutte sisään.",
  "Te astutte hitaasti.", "Te onnistutte.", "Te lyötte palloa.",
  "Te tunnette hänet.", "Te heitätte pallon.", "Te pyydätte apua.",
  "Te ette kuole nyt.", "Te istutte täällä.", "Te syötte pizzaa.",
  "Te lataatte akun.", "Te tartutte siihen.", "Te luette kirjaa.",
  "Te huudatte minua.", "Te kasvatte nopeasti.", "Te osoitatte tietä.",
  "Te neuvotte minua.", "Te kutsutte minut.", "Te juoksette nopeasti.",
  "Te sidotte köyden.", "Te vajoatte alas.", "Te roikutte täällä.",
  "Te pidätte tästä.", "Tämä kuulostaa teistä hyvältä.", "Te lennätte Roomaan.",
  "Te suosittelette tätä.", "Te nautitte tästä.", "Te rikotte lasin.",
  "Mitä teille tapahtuu?", "Te työnnätte ovea.", "Te kärsitte nyt.",
  "Te harrastatte urheilua.", "Te leikkaatte leipää.", "Te muistutatte häntä.",
  "Te kamppailette.", "Te katoatte.", "Te varastatte sen.",
  "Te ammutte palloa.", "Te maalaatte seinän.", "Te mittaatte sen.",
  "Te nostatte sen.", "Te unohdatte sen.", "Te pakotatte hänet.",
  "Te laulatte laulun.", "Vesi virtaa teidän luonanne.", "Te pyydystätte kalan.",
  "Te hyppäätte.", "Te juotte vettä.", "Talo palaa teillä.",
  "Te revitte paperin.", "Te käännätte auton.", "Te väistätte.",
  "Te työnnätte pöytää.", "Te nukutte.", "Te ylistätte häntä.",
  "Te pakenette.", "Te uitte.", "Te olette hiljaa.",
  "Te lähetätte kirjeen.", "Te pistätte neulan.", "Te riitelette.",
  "Te kaadatte vettä.", "Te vältätte sitä.", "Te tunkeudutte sisään.",
  "Te leivotte leipää.", "Te valehtelette.", "Te purette.",
  "Te kaivatte kuopan.", "Te huudatte.", "Te pesette kädet.",
  "Eläimet syövät (teidän ympärillä).", "Te haistatte sen.", "Te heilutatte käsiä.",
  "Te taivutatte sen.", "Te petätte.", "Te vihellätte.",
  "Te ratsastatte.", "Lumi sulaa teidän luona.", "Te lainaatte kirjan.",
  "Te puhallatte.", "Te heitätte sen.", "Te säikähdätte.",
  "Te hiivitte.", "Te paistatte lihaa.", "Te liukuutte.",
  "Te vannotte.", "Te palellette.", "Te annatte anteeksi.",
  "Te pilaatte ruoan.", "Te ryömitte."
)

de_ihr_u <- c(
  "Ihr werdet Lehrer.", "Ihr habt Zeit.", "Ihr könnt schwimmen.",
  "Ihr gebt das Buch.", "Ihr sollt gehen.", "Ihr müsst lernen.",
  "Ihr kommt nach Hause.", "Ihr geht zur Schule.", "Ihr wollt Eis.",
  "Ihr steht hier.", "Ihr seht mich.", "Ihr bleibt zu Hause.",
  "Ihr lasst das.", "Ihr findet das.", "Ihr liegt im Bett.",
  "Ihr bringt das Buch.", "Ihr nehmt den Bus.", "Ihr sprecht Deutsch.",
  "Ihr trefft ihn.", "Ihr haltet Pause.", "Ihr heißt…",
  "Diese Regeln gelten für euch.", "Ihr tut das.", "Ihr wisst das.",
  "Ihr dürft rausgehen.", "Ihr bietet Hilfe.", "Ihr schreibt einen Brief.",
  "Ihr zieht die Kiste.", "Ihr zieht um.", "Ihr lauft im Park.",
  "Ihr fahrt nach Berlin.", "Ihr fahrt das Auto.", "Ihr fallt.",
  "Ihr beginnt jetzt.", "Ihr verliert das Spiel.", "Ihr gewinnt das Spiel.",
  "Ihr steigt auf.", "Ihr helft mir.", "Ihr schafft etwas.",
  "Ihr schließt die Tür.", "Ihr tragt die Tasche.", "Ihr nennt ihn Tom.",
  "Die Sonne scheint euch.", "Ihr denkt daran.", "Ihr tretet ein.",
  "Ihr schreitet langsam.", "Euch gelingt es.", "Ihr schlagt den Ball.",
  "Ihr kennt ihn.", "Ihr werft den Ball.", "Ihr bittet um Hilfe.",
  "Ihr sterbt nicht jetzt.", "Ihr sitzt hier.", "Ihr esst Pizza.",
  "Ihr ladet den Akku.", "Ihr greift danach.", "Ihr lest ein Buch.",
  "Ihr ruft mich.", "Ihr wachst schnell.", "Ihr weist den Weg.",
  "Ihr ratet mir.", "Ihr ladet mich ein.", "Ihr rennt schnell.",
  "Ihr bindet das Seil.", "Ihr sinkt.", "Ihr hängt hier.",
  "Ihr mögt das.", "Das klingt euch gut.", "Ihr fliegt nach Rom.",
  "Ihr empfehlt das.", "Ihr genießt das.", "Ihr brecht das Glas.",
  "Was geschieht euch?", "Ihr stoßt die Tür.", "Ihr leidet jetzt.",
  "Ihr treibt Sport.", "Ihr schneidet Brot.", "Ihr gleicht ihm.",
  "Ihr ringt.", "Ihr verschwindet.", "Ihr stehlt das.",
  "Ihr schießt den Ball.", "Ihr streicht die Wand.", "Ihr messt das.",
  "Ihr hebt das.", "Ihr vergesst das.", "Ihr zwingt ihn.",
  "Ihr singt ein Lied.", "Das Wasser fließt bei euch.", "Ihr fangt einen Fisch.",
  "Ihr springt.", "Ihr trinkt Wasser.", "Das Haus brennt bei euch.",
  "Ihr reißt das Papier.", "Ihr wendet das Auto.", "Ihr weicht aus.",
  "Ihr schiebt den Tisch.", "Ihr schlaft.", "Ihr preist ihn.",
  "Ihr flieht.", "Ihr schwimmt.", "Ihr schweigt.",
  "Ihr sendet den Brief.", "Ihr stecht die Nadel.", "Ihr streitet.",
  "Ihr gießt Wasser.", "Ihr meidet das.", "Ihr dringt ein.",
  "Ihr backt Brot.", "Ihr lügt.", "Ihr beißt.",
  "Ihr grabt ein Loch.", "Ihr schreit.", "Ihr wascht die Hände.",
  "Tiere fressen.", "Ihr riecht das.", "Ihr schwingt die Arme.",
  "Ihr biegt das.", "Ihr betrügt.", "Ihr pfeift.",
  "Ihr reitet.", "Der Schnee schmilzt bei euch.", "Ihr leiht ein Buch.",
  "Ihr blast.", "Ihr schmeißt das.", "Ihr erschreckt.",
  "Ihr schleicht.", "Ihr bratet Fleisch.", "Ihr gleitet.",
  "Ihr schwört.", "Ihr friert.", "Ihr verzeiht.",
  "Ihr verdirbt das Essen.", "Ihr kriecht."
)

fi_ihr_fill <- c(
  "73" = "Oksat katkeavat.",
  "76" = "Te törmäätte pöytään.",
  "121" = "Tie kääntyy vasemmalle.",
  "125" = "Te sulatatte voita.",
  "138" = "Ruoka pilaantuu nopeasti.",
  "139" = "Te ette käske mitään."
)
de_ihr_fill <- c(
  "73" = "Die Äste brechen.",
  "76" = "Ihr stoßt gegen den Tisch.",
  "121" = "Die Straße biegt nach links.",
  "125" = "Ihr schmilzt Butter.",
  "138" = "Das Essen verdirbt schnell.",
  "139" = "Ihr befiehlt nichts."
)

stopifnot(length(fi_ihr_u) == 134L, length(fi_ihr_u) == length(de_ihr_u))

fi_ihr <- character(140)
de_ihr <- character(140)
j <- 1L
for (i in seq_len(140)) {
  rk <- as.character(i)
  if (rk %in% names(fi_ihr_fill)) {
    fi_ihr[i] <- fi_ihr_fill[[rk]]
    de_ihr[i] <- de_ihr_fill[[rk]]
  } else {
    fi_ihr[i] <- fi_ihr_u[j]
    de_ihr[i] <- de_ihr_u[j]
    j <- j + 1L
  }
}

# sie (3. pers. pl.) — user batch; ranks 73, 76, 121, 125, 138, 139 filled
fi_sie_u <- c(
  "He tulevat opettajiksi.", "Heillä on aikaa.", "He osaavat uida.",
  "He antavat kirjan.", "Heidän pitää lähteä.", "Heidän täytyy oppia.",
  "He tulevat kotiin.", "He menevät kouluun.", "He haluavat jäätelöä.",
  "He seisovat tässä.", "He näkevät minut.", "He jäävät kotiin.",
  "He jättävät sen.", "He löytävät sen.", "He makaavat sängyllä.",
  "He tuovat kirjan.", "He ottavat bussin.", "He puhuvat saksaa.",
  "He tapaavat hänet.", "He pitävät tauon.", "Heidän nimensä ovat Anna ja Tom.",
  "Nämä säännöt ovat voimassa.", "He tekevät sen.", "He tietävät sen.",
  "He saavat mennä ulos.", "He tarjoavat apua.", "He kirjoittavat kirjeen.",
  "He vetävät laatikkoa.", "He muuttavat uuteen kotiin.", "He juoksevat puistossa.",
  "He matkustavat Berliiniin.", "He ajavat autoa.", "He kaatuvat.",
  "He aloittavat nyt.", "He häviävät pelin.", "He voittavat pelin.",
  "He nousevat ylös.", "He auttavat minua.", "He luovat jotain.",
  "He sulkevat oven.", "He kantavat laukkua.", "He kutsuvat häntä Tomiksi.",
  "Aurinko paistaa.", "He ajattelevat sitä.", "He astuvat sisään.",
  "He astelevat hitaasti.", "He onnistuvat.", "He lyövät palloa.",
  "He tuntevat hänet.", "He heittävät pallon.", "He pyytävät apua.",
  "He eivät kuole nyt.", "He istuvat täällä.", "He syövät pizzaa.",
  "He lataavat akun.", "He tarttuvat siihen.", "He lukevat kirjaa.",
  "He huutavat minua.", "He kasvavat nopeasti.", "He osoittavat tietä.",
  "He neuvovat minua.", "He kutsuvat minut.", "He juoksevat nopeasti.",
  "He sitovat köyden.", "He vajoavat alas.", "He roikkuvat täällä.",
  "He pitävät tästä.", "Tämä kuulostaa hyvältä.", "He lentävät Roomaan.",
  "He suosittelevat tätä.", "He nauttivat tästä.", "He rikkovat lasin.",
  "Mitä tapahtuu?", "He työntävät ovea.", "He kärsivät nyt.",
  "He harrastavat urheilua.", "He leikkaavat leipää.", "He muistuttavat häntä.",
  "He kamppailevat.", "He katoavat.", "He varastavat sen.",
  "He ampuvat palloa.", "He maalaavat seinän.", "He mittaavat sen.",
  "He nostavat sen.", "He unohtavat sen.", "He pakottavat hänet.",
  "He laulavat laulun.", "Vesi virtaa.", "He pyydystävät kalan.",
  "He hyppäävät.", "He juovat vettä.", "Talo palaa.",
  "He repivät paperin.", "He kääntävät auton.", "He väistävät.",
  "He työntävät pöytää.", "He nukkuvat.", "He ylistävät häntä.",
  "He pakenevat.", "He uivat.", "He ovat hiljaa.",
  "He lähettävät kirjeen.", "He pistävät neulan.", "He riitelevät.",
  "He kaatavat vettä.", "He välttävät sitä.", "He tunkeutuvat sisään.",
  "He leipovat leipää.", "He valehtelevat.", "He purevat.",
  "He kaivavat kuopan.", "He huutavat.", "He pesevät kädet.",
  "Eläimet syövät.", "He haistavat sen.", "He heiluttavat käsiä.",
  "He taivuttavat sen.", "He pettävät.", "He viheltävät.",
  "He ratsastavat.", "Lumi sulaa.", "He lainaavat kirjan.",
  "He puhaltavat.", "He heittävät sen.", "He säikähtävät.",
  "He hiipivät.", "He paistavat lihaa.", "He liukuvat.",
  "He vannovat.", "He palelevat.", "He antavat anteeksi.",
  "He pilaavat ruoan.", "He ryömivät."
)

de_sie_u <- c(
  "Sie werden Lehrer.", "Sie haben Zeit.", "Sie können schwimmen.",
  "Sie geben das Buch.", "Sie sollen gehen.", "Sie müssen lernen.",
  "Sie kommen nach Hause.", "Sie gehen zur Schule.", "Sie wollen Eis.",
  "Sie stehen hier.", "Sie sehen mich.", "Sie bleiben zu Hause.",
  "Sie lassen das.", "Sie finden das.", "Sie liegen im Bett.",
  "Sie bringen das Buch.", "Sie nehmen den Bus.", "Sie sprechen Deutsch.",
  "Sie treffen ihn.", "Sie halten Pause.", "Sie heißen Anna und Tom.",
  "Diese Regeln gelten.", "Sie tun das.", "Sie wissen das.",
  "Sie dürfen rausgehen.", "Sie bieten Hilfe.", "Sie schreiben einen Brief.",
  "Sie ziehen die Kiste.", "Sie ziehen um.", "Sie laufen im Park.",
  "Sie fahren nach Berlin.", "Sie fahren das Auto.", "Sie fallen.",
  "Sie beginnen jetzt.", "Sie verlieren das Spiel.", "Sie gewinnen das Spiel.",
  "Sie steigen auf.", "Sie helfen mir.", "Sie schaffen etwas.",
  "Sie schließen die Tür.", "Sie tragen die Tasche.", "Sie nennen ihn Tom.",
  "Die Sonne scheint.", "Sie denken daran.", "Sie treten ein.",
  "Sie schreiten langsam.", "Ihnen gelingt es.", "Sie schlagen den Ball.",
  "Sie kennen ihn.", "Sie werfen den Ball.", "Sie bitten um Hilfe.",
  "Sie sterben nicht jetzt.", "Sie sitzen hier.", "Sie essen Pizza.",
  "Sie laden den Akku.", "Sie greifen danach.", "Sie lesen ein Buch.",
  "Sie rufen mich.", "Sie wachsen schnell.", "Sie weisen den Weg.",
  "Sie raten mir.", "Sie laden mich ein.", "Sie rennen schnell.",
  "Sie binden das Seil.", "Sie sinken.", "Sie hängen hier.",
  "Sie mögen das.", "Das klingt gut.", "Sie fliegen nach Rom.",
  "Sie empfehlen das.", "Sie genießen das.", "Sie brechen das Glas.",
  "Was geschieht?", "Sie stoßen die Tür.", "Sie leiden jetzt.",
  "Sie treiben Sport.", "Sie schneiden Brot.", "Sie gleichen ihm.",
  "Sie ringen.", "Sie verschwinden.", "Sie stehlen das.",
  "Sie schießen den Ball.", "Sie streichen die Wand.", "Sie messen das.",
  "Sie heben das.", "Sie vergessen das.", "Sie zwingen ihn.",
  "Sie singen ein Lied.", "Das Wasser fließt.", "Sie fangen einen Fisch.",
  "Sie springen.", "Sie trinken Wasser.", "Das Haus brennt.",
  "Sie reißen das Papier.", "Sie wenden das Auto.", "Sie weichen aus.",
  "Sie schieben den Tisch.", "Sie schlafen.", "Sie preisen ihn.",
  "Sie fliehen.", "Sie schwimmen.", "Sie schweigen.",
  "Sie senden den Brief.", "Sie stechen die Nadel.", "Sie streiten.",
  "Sie gießen Wasser.", "Sie meiden das.", "Sie dringen ein.",
  "Sie backen Brot.", "Sie lügen.", "Sie beißen.",
  "Sie graben ein Loch.", "Sie schreien.", "Sie waschen die Hände.",
  "Tiere fressen.", "Sie riechen das.", "Sie schwingen die Arme.",
  "Sie biegen das.", "Sie betrügen.", "Sie pfeifen.",
  "Sie reiten.", "Der Schnee schmilzt.", "Sie leihen ein Buch.",
  "Sie blasen.", "Sie schmeißen das.", "Sie erschrecken.",
  "Sie schleichen.", "Sie braten Fleisch.", "Sie gleiten.",
  "Sie schwören.", "Sie frieren.", "Sie verzeihen.",
  "Sie verderben das Essen.", "Sie kriechen."
)

fi_sie_fill <- c(
  "73" = "Oksat katkeavat.",
  "76" = "He törmäävät pöytään.",
  "121" = "Tie kääntyy vasemmalle.",
  "125" = "He sulattavat voita.",
  "138" = "Ruoka pilaantuu nopeasti.",
  "139" = "He eivät käske mitään."
)
de_sie_fill <- c(
  "73" = "Die Äste brechen.",
  "76" = "Sie stoßen gegen den Tisch.",
  "121" = "Die Straße biegt nach links.",
  "125" = "Sie schmelzen Butter.",
  "138" = "Das Essen verdirbt schnell.",
  "139" = "Sie befhehlen nichts."
)

stopifnot(length(fi_sie_u) == 134L, length(fi_sie_u) == length(de_sie_u))

fi_sie <- character(140)
de_sie <- character(140)
j <- 1L
for (i in seq_len(140)) {
  rk <- as.character(i)
  if (rk %in% names(fi_sie_fill)) {
    fi_sie[i] <- fi_sie_fill[[rk]]
    de_sie[i] <- de_sie_fill[[rk]]
  } else {
    fi_sie[i] <- fi_sie_u[j]
    de_sie[i] <- de_sie_u[j]
    j <- j + 1L
  }
}

stopifnot(
  nrow(ranked) == length(fi),
  length(fi) == length(de),
  length(fi) == length(fi_du),
  length(fi) == length(de_du),
  length(fi) == length(fi_er),
  length(fi) == length(de_er),
  length(fi) == length(fi_wir),
  length(fi) == length(de_wir),
  length(fi) == length(fi_ihr),
  length(fi) == length(de_ihr),
  length(fi) == length(fi_sie),
  length(fi) == length(de_sie)
)

meta <- ranked[, c("rank", "infinitive", "suomi")]

out <- rbind(
  data.frame(meta, tense = "praesens", person = "ich", sentence_fi = fi, sentence_de = de),
  data.frame(meta, tense = "praesens", person = "du", sentence_fi = fi_du, sentence_de = de_du),
  data.frame(meta, tense = "praesens", person = "er", sentence_fi = fi_er, sentence_de = de_er),
  data.frame(meta, tense = "praesens", person = "wir", sentence_fi = fi_wir, sentence_de = de_wir),
  data.frame(meta, tense = "praesens", person = "ihr", sentence_fi = fi_ihr, sentence_de = de_ihr),
  data.frame(meta, tense = "praesens", person = "sie", sentence_fi = fi_sie, sentence_de = de_sie)
)

dir.create("cleanup/archive", recursive = TRUE, showWarnings = FALSE)
write_csv(out, "cleanup/archive/saksa_epasaannolliset_verbit_lauseet_praesens.csv")

message("Wrote ", nrow(out), " rows to cleanup/archive/saksa_epasaannolliset_verbit_lauseet_praesens.csv")
