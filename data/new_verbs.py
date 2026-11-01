"""Authored learning content for newly researched verb candidates.
German stems are checked separately in irregular_candidates.tsv and ranking code.
Stable source_rank values above 1000 are independent of the display order.
"""
PEOPLE=['ich','du','er','wir','ihr','sie']
# lemma | Finnish meaning | six Finnish finite cues | English meaning | English cue
CONTENT='''sein|olla|olen,olet,on,olemme,olette,ovat|be|be
verstehen|ymmärtää|ymmärrän,ymmärrät,ymmärtää,ymmärrämme,ymmärrätte,ymmärtävät|understand|understand
bestehen|olla olemassa; läpäistä|läpäisen,läpäiset,läpäisee,läpäisemme,läpäisette,läpäisevät|exist; pass a test|pass
erhalten|saada; säilyttää|saan,saat,saa,saamme,saatte,saavat|receive; preserve|receive
entscheiden|ratkaista; päättää|ratkaisen,ratkaiset,ratkaisee,ratkaisemme,ratkaisette,ratkaisevat|decide; resolve|decide
anfangen|aloittaa|aloitan,aloitat,aloittaa,aloitamme,aloitatte,aloittavat|begin; start|begin
anbieten|tarjota|tarjoan,tarjoat,tarjoaa,tarjoamme,tarjoatte,tarjoavat|offer|offer
bekommen|saada|saan,saat,saa,saamme,saatte,saavat|get; receive|get
verlassen|jättää; poistua|jätän,jätät,jättää,jätämme,jätätte,jättävät|leave|leave
erfahren|saada tietää; kokea|saan tietää,saat tietää,saa tietää,saamme tietää,saatte tietää,saavat tietää|learn; experience|learn
entstehen|syntyä; muodostua|,,syntyy,,,syntyvät|arise; develop|arise
teilnehmen|osallistua|osallistun,osallistut,osallistuu,osallistumme,osallistutte,osallistuvat|take part|take part
stattfinden|tapahtua; toteutua|,,tapahtuu,,,tapahtuvat|take place|take place
geraten|joutua|joudun,joudut,joutuu,joudumme,joudutte,joutuvat|get into a situation|get into a situation
bergen|pelastaa; ottaa talteen|pelastan,pelastat,pelastaa,pelastamme,pelastatte,pelastavat|rescue; recover|rescue'''

# Subject / complement / separable particle / Finnish present, past, perfect /
# English present, past, perfect. Generated German sentences use verified tables.
EXAMPLES={
'sein': ('Ich','zu Hause','', ['Olen kotona.','Olin kotona.','Olen ollut kotona.'],['I am at home.','I was at home.','I have been at home.']),
'verstehen': ('Ich','die Frage','',['Ymmärrän kysymyksen.','Ymmärsin kysymyksen.','Olen ymmärtänyt kysymyksen.'],['I understand the question.','I understood the question.','I have understood the question.']),
'bestehen': ('Ich','die Prüfung','',['Läpäisen kokeen.','Läpäisin kokeen.','Olen läpäissyt kokeen.'],['I pass the exam.','I passed the exam.','I have passed the exam.']),
'erhalten': ('Ich','eine Antwort','',['Saan vastauksen.','Sain vastauksen.','Olen saanut vastauksen.'],['I receive an answer.','I received an answer.','I have received an answer.']),
'entscheiden': ('Ich','den Streit','',['Ratkaisen riidan.','Ratkaisin riidan.','Olen ratkaissut riidan.'],['I settle the dispute.','I settled the dispute.','I have settled the dispute.']),
'anfangen': ('Ich','mit der Arbeit','an',['Aloitan työn.','Aloitin työn.','Olen aloittanut työn.'],['I start work.','I started work.','I have started work.']),
'anbieten': ('Ich','dir Hilfe','an',['Tarjoan sinulle apua.','Tarjosin sinulle apua.','Olen tarjonnut sinulle apua.'],['I offer you help.','I offered you help.','I have offered you help.']),
'bekommen': ('Ich','ein Geschenk','',['Saan lahjan.','Sain lahjan.','Olen saanut lahjan.'],['I get a present.','I got a present.','I have received a present.']),
'verlassen': ('Ich','das Haus','',['Lähden talosta.','Lähdin talosta.','Olen lähtenyt talosta.'],['I leave the house.','I left the house.','I have left the house.']),
'erfahren': ('Ich','die Wahrheit','',['Saan tietää totuuden.','Sain tietää totuuden.','Olen saanut tietää totuuden.'],['I learn the truth.','I learned the truth.','I have learned the truth.']),
'entstehen': ('Ein Problem','','',['Ongelma syntyy.','Ongelma syntyi.','Ongelma on syntynyt.'],['A problem arises.','A problem arose.','A problem has arisen.']),
'geraten': ('Ich','in Schwierigkeiten','',['Joudun vaikeuksiin.','Jouduin vaikeuksiin.','Olen joutunut vaikeuksiin.'],['I get into trouble.','I got into trouble.','I have got into trouble.']),
'stattfinden': ('Das Treffen','hier','statt',['Tapaaminen pidetään täällä.','Tapaaminen pidettiin täällä.','Tapaaminen on pidetty täällä.'],['The meeting takes place here.','The meeting took place here.','The meeting has taken place here.']),
 'teilnehmen': ('Ich','am Kurs','teil',['Osallistun kurssille.','Osallistuin kurssille.','Olen osallistunut kurssille.'],['I take part in the course.','I took part in the course.','I have taken part in the course.']),
 'bergen': ('Ich','den Verletzten','',['Pelastan loukkaantuneen.','Pelastin loukkaantuneen.','Olen pelastanut loukkaantuneen.'],['I rescue the injured person.','I rescued the injured person.','I have rescued the injured person.'])
}

CONTENT += '''
verbinden|yhdistää|yhdistän,yhdistät,yhdistää,yhdistämme,yhdistätte,yhdistävät|connect|connect
aufnehmen|ottaa vastaan; hyväksyä joukkoon; tallentaa|tallennan,tallennat,tallentaa,tallennamme,tallennatte,tallentavat|receive; admit to a group; record|record
versprechen|luvata|lupaan,lupaat,lupaa,lupaamme,lupaatte,lupaavat|promise|promise
beschreiben|kuvata, selostaa, luonnehtia|kuvaan,kuvaat,kuvaa,kuvaamme,kuvaatte,kuvaavat|describe|describe
beschließen|päättää|päätän,päätät,päättää,päätämme,päätätte,päättävät|decide|decide
verbringen|viettää|vietän,vietät,viettää,vietämme,vietätte,viettävät|spend time|spend time
angreifen|hyökätä|hyökkään,hyökkäät,hyökkää,hyökkäämme,hyökkäätte,hyökkäävät|attack|attack
besitzen|omistaa|omistan,omistat,omistaa,omistamme,omistatte,omistavat|own|own
annehmen|olettaa|oletan,oletat,olettaa,oletamme,oletatte,olettavat|assume; accept|assume
ankommen|saapua|saavun,saavut,saapuu,saavumme,saavutte,saapuvat|arrive|arrive
anrufen|soittaa|soitan,soitat,soittaa,soitamme,soitatte,soittavat|phone; call|phone
aufstehen|nousta ylös|nousen ylös,nouset ylös,nousee ylös,nousemme ylös,nousette ylös,nousevat ylös|get up|get up
einsteigen|astua kyytiin|astun kyytiin,astut kyytiin,astuu kyytiin,astumme kyytiin,astutte kyytiin,astuvat kyytiin|board; get in|board
aussteigen|poistua kyydistä|poistun kyydistä,poistut kyydistä,poistuu kyydistä,poistumme kyydistä,poistutte kyydistä,poistuvat kyydistä|get out; get off|get out
umsteigen|vaihtaa kulkuneuvoa, vaihtaa toiseen yhteyteen|vaihdan kulkuneuvoa,vaihdat kulkuneuvoa,vaihtaa kulkuneuvoa,vaihdamme kulkuneuvoa,vaihdatte kulkuneuvoa,vaihtavat kulkuneuvoa|change transport|change transport'''
EXAMPLES.update({
'verbinden': ('Ich','die Kabel','',['Yhdistän johdot.','Yhdistin johdot.','Olen yhdistänyt johdot.'],['I connect the cables.','I connected the cables.','I have connected the cables.']),
'aufnehmen': ('Ich','ein Lied','auf',['Tallennan laulun.','Tallensin laulun.','Olen tallentanut laulun.'],['I record a song.','I recorded a song.','I have recorded a song.']),
'versprechen': ('Ich','dir Hilfe','',['Lupaan sinulle apua.','Lupasin sinulle apua.','Olen luvannut sinulle apua.'],['I promise you help.','I promised you help.','I have promised you help.']),
'beschreiben': ('Ich','den Weg','',['Kuvaan reitin.','Kuvasin reitin.','Olen kuvannut reitin.'],['I describe the route.','I described the route.','I have described the route.']),
'beschließen': ('Ich','den Kauf','',['Päätän ostosta.','Päätin ostosta.','Olen päättänyt ostosta.'],['I decide on the purchase.','I decided on the purchase.','I have decided on the purchase.']),
'verbringen': ('Ich','den Sommer hier','',['Vietän kesän täällä.','Vietin kesän täällä.','Olen viettänyt kesän täällä.'],['I spend the summer here.','I spent the summer here.','I have spent the summer here.']),
'angreifen': ('Ich','die Festung','an',['Hyökkään linnoitukseen.','Hyökkäsin linnoitukseen.','Olen hyökännyt linnoitukseen.'],['I attack the fortress.','I attacked the fortress.','I have attacked the fortress.']),
'besitzen': ('Ich','ein Fahrrad','',['Omistan polkupyörän.','Omistin polkupyörän.','Olen omistanut polkupyörän.'],['I own a bicycle.','I owned a bicycle.','I have owned a bicycle.']),
'annehmen': ('Ich','das','an',['Oletan niin.','Oletin niin.','Olen olettanut niin.'],['I assume that.','I assumed that.','I have assumed that.']),
'ankommen': ('Ich','am Bahnhof','an',['Saavun asemalle.','Saavuin asemalle.','Olen saapunut asemalle.'],['I arrive at the station.','I arrived at the station.','I have arrived at the station.']),
'anrufen': ('Ich','dich','an',['Soitan sinulle.','Soitin sinulle.','Olen soittanut sinulle.'],['I phone you.','I phoned you.','I have phoned you.']),
'aufstehen': ('Ich','früh','auf',['Nousen aikaisin.','Nousin aikaisin.','Olen noussut aikaisin.'],['I get up early.','I got up early.','I have got up early.']),
'einsteigen': ('Ich','in den Zug','ein',['Astun junaan.','Astuin junaan.','Olen astunut junaan.'],['I board the train.','I boarded the train.','I have boarded the train.']),
'aussteigen': ('Ich','aus dem Bus','aus',['Poistun bussista.','Poistuin bussista.','Olen poistunut bussista.'],['I get off the bus.','I got off the bus.','I have got off the bus.']),
'umsteigen': ('Ich','in Köln','um',['Vaihdan junaa Kölnissä.','Vaihdoin junaa Kölnissä.','Olen vaihtanut junaa Kölnissä.'],['I change trains in Cologne.','I changed trains in Cologne.','I have changed trains in Cologne.'])
})

def entries():
    out={}
    for i,line in enumerate(CONTENT.splitlines(),1001):
        inf,fi,forms,en,base=line.split('|')
        out[inf]=dict(source_rank=str(i),suomi=fi,fi_forms=forms.split(','),english=en,english_base=base,example=EXAMPLES[inf])
    return out
