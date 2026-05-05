GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
MODEL = "gemini-2.5-flash-preview-05-20"

PAGES_DIR = "pages"
OUTPUT_DIR = "output"

MIN_PAGES_CHARS = 500
REQUEST_DELAY = 3

HOTELS = [
    {"Property ID": "98435", "Nome account": "The Vincent Boutique Hotel, BW Premier Collection", "Brand": "BW Premier Collection", "Sito Web": "www.thevincenthotelmalta.com"},
    {"Property ID": "98438", "Nome account": "Modica Inn Centro, BW Premier Collection", "Brand": "BW Premier Collection", "Sito Web": "www.hotelprincipedaragona.it"},
    {"Property ID": "98177", "Nome account": "WorldHotel Casati 18, WorldHotels Elite", "Brand": "Worldhotels Elite", "Sito Web": "www.worldhotelcasati18.com"},
    {"Property ID": "77742", "Nome account": "Collini Hotel Mykonos, WorldHotels Elite", "Brand": "Worldhotels Elite", "Sito Web": "www.collinihotelmykonos.com"},
    {"Property ID": "98445", "Nome account": "Best Western Hotel Garda", "Brand": "Best Western", "Sito Web": "www.hotel-garda.it"},
    {"Property ID": "98447", "Nome account": "Matilde Boutique Hotel, WorldHotels Elite", "Brand": "Worldhotels Elite", "Sito Web": "www.matildeboutiquehotel.it"},
    {"Property ID": "98449", "Nome account": "Hotel Savoia & Jolanda, WorldHotels Elite", "Brand": "Worldhotels Elite", "Sito Web": "www.hotelsavoiajolanda.com"},
    {"Property ID": "77713", "Nome account": "Best Western Premier Ark Hotel", "Brand": "Best Western Premier", "Sito Web": "www.arkhotel.al"},
    {"Property ID": "77734", "Nome account": "Adriatik Hotel, BW Premier Collection", "Brand": "BW Premier Collection", "Sito Web": "www.adriatikhotel.com"},
    {"Property ID": "77587", "Nome account": "Best Western Bohemian Resort", "Brand": "Best Western", "Sito Web": ""},
    {"Property ID": "77739", "Nome account": "Local Stay Hotel, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.localstay.bg/en/home/"},
    {"Property ID": "77704", "Nome account": "Best Western Plus Paradise Hotel Dilijan", "Brand": "Best Western Plus", "Sito Web": ""},
    {"Property ID": "77720", "Nome account": "Best Western Plus Lozenetz Hotel", "Brand": "Best Western Plus", "Sito Web": "www.lozenetzhotel.com/en/"},
    {"Property ID": "77579", "Nome account": "Best Western Plus Congress Hotel", "Brand": "Best Western Plus", "Sito Web": "www.congresshotelyerevan.com"},
    {"Property ID": "77737", "Nome account": "Pino Nature Hotel, BW Premier Collection", "Brand": "BW Premier Collection", "Sito Web": "https://www.pino-hotel.com/"},
    {"Property ID": "77736", "Nome account": "Dorian Inn, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "https://www.dorianinnhotel.com"},
    {"Property ID": "77735", "Nome account": "Makedonia Palace, WorldHotels Luxury", "Brand": "WorldHotels Luxury", "Sito Web": "https://www.makedoniapalace.com"},
    {"Property ID": "77723", "Nome account": "Best Western Plus Premium Inn", "Brand": "Best Western Plus", "Sito Web": "www.premiuminn.bg"},
    {"Property ID": "77733", "Nome account": "Chryssi Akti, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.hotel-chryssiakti.gr"},
    {"Property ID": "77706", "Nome account": "Best Western Plus Bristol Hotel", "Brand": "Best Western Plus", "Sito Web": "www.bristolhotel.bg/en/"},
    {"Property ID": "77597", "Nome account": "Best Western Plus Embassy Hotel", "Brand": "Best Western Plus", "Sito Web": "www.embassyhotel.gr"},
    {"Property ID": "77738", "Nome account": "Best Western Plus Olives City Hotel", "Brand": "Best Western Plus", "Sito Web": "www.oliveshotel.com/en/"},
    {"Property ID": "77728", "Nome account": "Best Western Premier Plovdiv Hills", "Brand": "Best Western Premier", "Sito Web": "www.hotelpremierplovdiv.com/en"},
    {"Property ID": "77522", "Nome account": "Best Western Plus Hotel Plaza", "Brand": "Best Western Plus", "Sito Web": "www.rhodesplazahotel.com"},
    {"Property ID": "77729", "Nome account": "Best Western Terminus Hotel", "Brand": "Best Western", "Sito Web": "www.hotelterminus.bg"},
    {"Property ID": "77519", "Nome account": "Zante Park Resort & Spa, BW Premier Collection", "Brand": "BW Premier Collection", "Sito Web": "www.zanteparkhotels.gr/en/"},
    {"Property ID": "77740", "Nome account": "Sokio Attiki Hotel, BW Premier Collection", "Brand": "BW Premier Collection", "Sito Web": "www.sokiohotels.com/hotel/sokio-attiki-bw-premier-collection"},
    {"Property ID": "77547", "Nome account": "Best Western Central Hotel", "Brand": "Best Western", "Sito Web": "www.bwcentral.ro/en/"},
    {"Property ID": "77724", "Nome account": "Best Western Hotel Galla", "Brand": "Best Western", "Sito Web": ""},
    {"Property ID": "77726", "Nome account": "Best Western Premier Natalija Residence", "Brand": "Best Western Premier", "Sito Web": "www.natalijaresidence.com/en/"},
    {"Property ID": "77703", "Nome account": "Galaxy Beach Resort, BW Premier Collection", "Brand": "BW Premier Collection", "Sito Web": "www.galaxybeachresort.gr/en/"},
    {"Property ID": "77705", "Nome account": "Best Western Silva Hotel", "Brand": "Best Western", "Sito Web": "www.hotelsilvasibiu.com"},
    {"Property ID": "77552", "Nome account": "Best Western Bucovina-Club De Munte", "Brand": "Best Western", "Sito Web": "www.bestwesternbucovina.ro"},
    {"Property ID": "77741", "Nome account": "Sokio Piraeus, BW Premier Collection", "Brand": "BW Premier Collection", "Sito Web": ""},
    {"Property ID": "98000", "Nome account": "Best Western Plus Hotel Aurora", "Brand": "Best Western Plus", "Sito Web": "https://www.bestwestern.it"},
    {"Property ID": "98426", "Nome account": "Best Western Plus Sabaudia Hotel", "Brand": "Best Western Plus", "Sito Web": "www.sabaudiahotel.com"},
    {"Property ID": "98427", "Nome account": "Best Western Hotel dei Mille", "Brand": "Best Western", "Sito Web": "www.hoteldeimillenapoli.it"},
    {"Property ID": "98428", "Nome account": "Best Western Premier Malta", "Brand": "Best Western Premier", "Sito Web": "www.bestwesternmalta.com"},
    {"Property ID": "98429", "Nome account": "Best Western Hotel Green City", "Brand": "Best Western", "Sito Web": "www.hotelgreencity.it"},
    {"Property ID": "98430", "Nome account": "Best Western Plus The Hub Hotel", "Brand": "Best Western Plus", "Sito Web": "www.thehubhotel.com"},
    {"Property ID": "98431", "Nome account": "Hotel Al Caminetto, WorldHotels Crafted", "Brand": "Worldhotels Crafted", "Sito Web": "www.alcaminetto.com"},
    {"Property ID": "98432", "Nome account": "Hotel Shelley e Delle Palme, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.hotelshelley.it"},
    {"Property ID": "98433", "Nome account": "Antico Sipario Boutique Hotel, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.anticosipario.com"},
    {"Property ID": "98434", "Nome account": "Muraless Art Hotel, WorldHotels Crafted", "Brand": "Worldhotels Crafted", "Sito Web": "www.muralessarthotel.com"},
    {"Property ID": "98436", "Nome account": "Le Dune Resort, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.leduneresortsicilia.it"},
    {"Property ID": "98437", "Nome account": "Sure Hotel by Best Western Turin City Centre", "Brand": "Sure Hotel", "Sito Web": "www.hotelturincitycentre.com"},
    {"Property ID": "98439", "Nome account": "Best Western Hotel Nevada", "Brand": "Best Western", "Sito Web": "www.hotelnevadasanvito.com"},
    {"Property ID": "98440", "Nome account": "Best Western Plus Hotel Dimora del Monaco", "Brand": "Best Western Plus", "Sito Web": "www.dimoradelmonaco.it"},
    {"Property ID": "98441", "Nome account": "Best Western Hotel Colaiaco", "Brand": "Best Western", "Sito Web": "www.hotelcolaiaco.it"},
    {"Property ID": "56300", "Nome account": "Hotel De La Pace, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.hoteldelapace.it"},
    {"Property ID": "56303", "Nome account": "Hotel La Villa, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.ivrealavilla.com"},
    {"Property ID": "56304", "Nome account": "Etrusco Arezzo Hotel, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.etruscohotel.it"},
    {"Property ID": "56305", "Nome account": "Hotel San Giorgio, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.hotelsangiorgioforli.it"},
    {"Property ID": "56310", "Nome account": "San Severino Park Hotel & SPA, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.sanseverinoparkhotel.com"},
    {"Property ID": "56312", "Nome account": "Hotel Casena dei Colli, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.casenadeicolli.it"},
    {"Property ID": "56314", "Nome account": "The Regency Hotel, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.hotelregency.it"},
    {"Property ID": "56316", "Nome account": "Blu Hotel, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.bluhoteltorino.it"},
    {"Property ID": "56317", "Nome account": "Hotel Cristallo Relais, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.hotelcristallotivoli.it"},
    {"Property ID": "56318", "Nome account": "Hotel Sirio, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.hotelsiriobergamo.it"},
    {"Property ID": "56319", "Nome account": "Residence Le Axidie, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.leaxidie.it"},
    {"Property ID": "56320", "Nome account": "Hotel Raffaello, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.hotelraffaello.it"},
    {"Property ID": "56324", "Nome account": "Hotel Bellevue, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.bellevuehotel.net"},
    {"Property ID": "56326", "Nome account": "Sure Hotel by Best Western Hotel Milano", "Brand": "Sure Hotel", "Sito Web": "www.milanohotelpadova.it"},
    {"Property ID": "86142", "Nome account": "Parkhotel Laurin, WorldHotels Elite", "Brand": "Worldhotels Elite", "Sito Web": "www.laurin.it"},
    {"Property ID": "98024", "Nome account": "Best Western Plus Hotel Universo", "Brand": "Best Western Plus", "Sito Web": "www.hoteluniverso.com"},
    {"Property ID": "98025", "Nome account": "Best Western Hotel Piccadilly", "Brand": "Best Western", "Sito Web": "www.hotelpiccadillyroma.it"},
    {"Property ID": "98033", "Nome account": "Best Western Hotel Genio", "Brand": "Best Western", "Sito Web": "www.hotelgenio.it"},
    {"Property ID": "98041", "Nome account": "Best Western Hotel Rivoli", "Brand": "Best Western", "Sito Web": "www.hotelrivoliroma.com"},
    {"Property ID": "98050", "Nome account": "Hotel Paradiso, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.hotelparadisonapoli.it"},
    {"Property ID": "98058", "Nome account": "BW Premier Collection Hotel Canada", "Brand": "BW Premier Collection", "Sito Web": "www.hotelcanadaroma.com"},
    {"Property ID": "98080", "Nome account": "Best Western Hotel Regina Elena", "Brand": "Best Western", "Sito Web": "www.reginaelena.it"},
    {"Property ID": "98088", "Nome account": "Best Western Plus Hotel De' Capuleti", "Brand": "Best Western Plus", "Sito Web": "www.hotelcapuleti.it"},
    {"Property ID": "98094", "Nome account": "Best Western Hotel City", "Brand": "Best Western", "Sito Web": "www.hotelcitymilano.it"},
    {"Property ID": "98097", "Nome account": "Best Western Plus City Hotel", "Brand": "Best Western Plus", "Sito Web": "www.hotelcitygenova.it"},
    {"Property ID": "98103", "Nome account": "Best Western Hotel Crimea", "Brand": "Best Western", "Sito Web": "www.hotelcrimea.it"},
    {"Property ID": "98105", "Nome account": "Best Western Plus Hotel Genova", "Brand": "Best Western Plus", "Sito Web": "www.albergogenova.it"},
    {"Property ID": "98107", "Nome account": "Best Western Hotel Piemontese", "Brand": "Best Western", "Sito Web": "www.hotelpiemontese.it"},
    {"Property ID": "98108", "Nome account": "Best Western Hotel Artdeco", "Brand": "Best Western", "Sito Web": "www.hotelartdecorome.com"},
    {"Property ID": "98119", "Nome account": "Best Western Hotel Nazionale", "Brand": "Best Western", "Sito Web": "www.hotelnazionalesanremo.com"},
    {"Property ID": "98124", "Nome account": "Best Western City Hotel", "Brand": "Best Western", "Sito Web": "www.cityhotelbologna.it"},
    {"Property ID": "98125", "Nome account": "Best Western Hotel Metropoli", "Brand": "Best Western", "Sito Web": "www.hotelmetropoli.it"},
    {"Property ID": "98130", "Nome account": "Best Western Hotel Cristallo", "Brand": "Best Western", "Sito Web": "www.cristallorovigo.com"},
    {"Property ID": "98133", "Nome account": "Best Western Hotel Biri", "Brand": "Best Western", "Sito Web": "www.hotelbiri.com"},
    {"Property ID": "98134", "Nome account": "Best Western Grand Hotel Guinigi", "Brand": "Best Western", "Sito Web": "www.grandhotelguinigi.it"},
    {"Property ID": "98144", "Nome account": "Best Western Hotel Major", "Brand": "Best Western", "Sito Web": "www.bwhotelmajor-mi.it"},
    {"Property ID": "98150", "Nome account": "Best Western Hotel Solaf", "Brand": "Best Western", "Sito Web": "www.hotelsolaf.it"},
    {"Property ID": "98152", "Nome account": "Best Western Plus Hotel Bologna", "Brand": "Best Western Plus", "Sito Web": "www.hotelbologna.com"},
    {"Property ID": "98154", "Nome account": "Best Western Hotel Residence Italia", "Brand": "Best Western", "Sito Web": "www.residenceitaliahotel.it"},
    {"Property ID": "98159", "Nome account": "Best Western Hotel Luxor", "Brand": "Best Western", "Sito Web": "www.hoteluxor.it"},
    {"Property ID": "98161", "Nome account": "Best Western Park Hotel", "Brand": "Best Western", "Sito Web": "www.parkhotelpiacenza.it"},
    {"Property ID": "98163", "Nome account": "Best Western Plus Park Hotel Pordenone", "Brand": "Best Western Plus", "Sito Web": "www.parkhotelpordenone.it"},
    {"Property ID": "98166", "Nome account": "Hotel Cappello D'Oro, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.bwhotelcappellodoro-bg.it"},
    {"Property ID": "98182", "Nome account": "Best Western Park Hotel", "Brand": "Best Western", "Sito Web": "www.parkhotelromanord.it"},
    {"Property ID": "98191", "Nome account": "Best Western Hotel Globus City", "Brand": "Best Western", "Sito Web": "www.hotelglobuscity.com"},
    {"Property ID": "98195", "Nome account": "Best Western Classic Hotel", "Brand": "Best Western", "Sito Web": "www.classic-hotel.it"},
    {"Property ID": "98204", "Nome account": "Hotel Astoria, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.astoriahotelmilano.com"},
    {"Property ID": "98206", "Nome account": "Best Western Hotel Mediterraneo", "Brand": "Best Western", "Sito Web": "www.hotelmediterraneoct.com"},
    {"Property ID": "98207", "Nome account": "Best Western Hotel Dei Cavalieri", "Brand": "Best Western", "Sito Web": "www.hoteldeicavalieri.net"},
    {"Property ID": "98213", "Nome account": "Albergo Roma, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.albergoroma.com"},
    {"Property ID": "98215", "Nome account": "Best Western Hotel Ferrari", "Brand": "Best Western", "Sito Web": "www.hotelferrari.it"},
    {"Property ID": "98217", "Nome account": "Best Western Plus Hotel Farnese", "Brand": "Best Western Plus", "Sito Web": "www.farnesehotel.it"},
    {"Property ID": "98219", "Nome account": "Best Western Hotel Tre Torri", "Brand": "Best Western", "Sito Web": "www.hoteltretorri.it"},
    {"Property ID": "98221", "Nome account": "Jet Hotel, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.jethotel.com"},
    {"Property ID": "98222", "Nome account": "Best Western Hotel La Solara", "Brand": "Best Western", "Sito Web": "www.lasolara.com"},
    {"Property ID": "98229", "Nome account": "Best Western Hotel Acqua Novella", "Brand": "Best Western", "Sito Web": "www.acquanovella.it"},
    {"Property ID": "98233", "Nome account": "Best Western Ai Cavalieri Hotel", "Brand": "Best Western", "Sito Web": "www.aicavalierihotel.it"},
    {"Property ID": "98234", "Nome account": "Best Western Hotel Porto Antico", "Brand": "Best Western", "Sito Web": "www.hotelportoantico.it"},
    {"Property ID": "98235", "Nome account": "Best Western Hotel Cavalieri della Corona", "Brand": "Best Western", "Sito Web": "www.cavalieridellacorona.com"},
    {"Property ID": "98236", "Nome account": "Best Western Cesena Hotel", "Brand": "Best Western", "Sito Web": "www.cesena-hotel.it"},
    {"Property ID": "98237", "Nome account": "Best Western Hotel Libertà", "Brand": "Best Western", "Sito Web": "www.hotelliberta.it"},
    {"Property ID": "98241", "Nome account": "Best Western Hotel La Conchiglia", "Brand": "Best Western", "Sito Web": "www.hotellaconchiglia.it"},
    {"Property ID": "98242", "Nome account": "Best Western Plus Globus Hotel", "Brand": "Best Western Plus", "Sito Web": "www.globushotel.com"},
    {"Property ID": "98244", "Nome account": "Best Western Hotel Quattrotorri Perugia", "Brand": "Best Western", "Sito Web": "www.hotelquattrotorriperugia.com"},
    {"Property ID": "98247", "Nome account": "Best Western Plus Hotel Plaza", "Brand": "Best Western Plus", "Sito Web": "www.hotelplazanapoli.it"},
    {"Property ID": "98252", "Nome account": "Best Western Hotel Viterbo", "Brand": "Best Western", "Sito Web": "www.hotelviterbo.com"},
    {"Property ID": "98254", "Nome account": "Best Western Gorizia Palace Hotel", "Brand": "Best Western", "Sito Web": "www.goriziapalace.com"},
    {"Property ID": "98257", "Nome account": "Best Western Hotel Stella D'Italia", "Brand": "Best Western", "Sito Web": "www.hotelstelladitalia.it"},
    {"Property ID": "98261", "Nome account": "Hotel Olimpia Venice, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.hotel-olimpia.com"},
    {"Property ID": "98264", "Nome account": "Best Western Plus Soave Hotel", "Brand": "Best Western Plus", "Sito Web": "www.soavehotel.it"},
    {"Property ID": "98265", "Nome account": "Best Western Hotel I Triangoli", "Brand": "Best Western", "Sito Web": "www.itriangoli.com"},
    {"Property ID": "98274", "Nome account": "Best Western Plus Hotel Monza e Brianza Palace", "Brand": "Best Western Plus", "Sito Web": "www.monzaebrianzapalace.it"},
    {"Property ID": "98276", "Nome account": "Best Western Park Hotel Continental", "Brand": "Best Western", "Sito Web": "www.parkhotelcontinental.it"},
    {"Property ID": "98280", "Nome account": "Best Western Plus Tigullio Royal Hotel", "Brand": "Best Western Plus", "Sito Web": "www.hoteltigullioroyal.it"},
    {"Property ID": "98281", "Nome account": "Best Western Falck Village Hotel", "Brand": "Best Western", "Sito Web": "www.falckvillagehotel.it"},
    {"Property ID": "98282", "Nome account": "Best Western Hotel Astrid", "Brand": "Best Western", "Sito Web": "www.hotelastrid.com"},
    {"Property ID": "98284", "Nome account": "Best Western Hotel Cristallo", "Brand": "Best Western", "Sito Web": "www.hotelcristallomantova.it"},
    {"Property ID": "98286", "Nome account": "Best Western Hotel Parco Paglia", "Brand": "Best Western", "Sito Web": "www.parcopagliahotel.it"},
    {"Property ID": "98289", "Nome account": "Best Western Blu Hotel Roma", "Brand": "Best Western", "Sito Web": "www.bluhotelrome.it"},
    {"Property ID": "98291", "Nome account": "Best Western Premier Villa Fabiano Palace Hotel", "Brand": "Best Western Premier", "Sito Web": "www.villafabiano.it"},
    {"Property ID": "98293", "Nome account": "Best Western Palace Inn Hotel", "Brand": "Best Western", "Sito Web": "www.palaceinnferrara.it"},
    {"Property ID": "98295", "Nome account": "Best Western Plus Hotel Galileo Padova", "Brand": "Best Western Plus", "Sito Web": "www.hotelgalileopadova.it"},
    {"Property ID": "98296", "Nome account": "Best Western Premier Hotel Royal Santina", "Brand": "Best Western Premier", "Sito Web": "www.hotelroyalsantina.com"},
    {"Property ID": "98299", "Nome account": "Best Western Hotel Goldenmile Milan", "Brand": "Best Western", "Sito Web": "www.hotelgoldenmile.it"},
    {"Property ID": "98305", "Nome account": "Best Western Plus Hotel Modena Resort", "Brand": "Best Western Plus", "Sito Web": "www.modenaresort.it"},
    {"Property ID": "98306", "Nome account": "Best Western Hotel Madison", "Brand": "Best Western", "Sito Web": "www.madisonhotelmilano.com"},
    {"Property ID": "98307", "Nome account": "Best Western Hotel Modena District", "Brand": "Best Western", "Sito Web": "www.modenadistrict.it"},
    {"Property ID": "98316", "Nome account": "Best Western Plus Hotel Le Favaglie", "Brand": "Best Western Plus", "Sito Web": "www.hotelfavaglie.it"},
    {"Property ID": "98317", "Nome account": "Best Western Hotel Continental", "Brand": "Best Western", "Sito Web": "www.hotelcontinental-ud.it"},
    {"Property ID": "98320", "Nome account": "Best Western Titian Inn Hotel Treviso", "Brand": "Best Western", "Sito Web": "www.titianinntreviso.com"},
    {"Property ID": "98321", "Nome account": "Best Western Plus BorgoLecco Hotel", "Brand": "Best Western Plus", "Sito Web": "www.borgoleccohotel.it"},
    {"Property ID": "98323", "Nome account": "Best Western Premier BHR Treviso Hotel", "Brand": "Best Western Premier", "Sito Web": "www.bhrtrevisohotel.com"},
    {"Property ID": "98325", "Nome account": "Best Western Plus Hotel Perla del Porto", "Brand": "Best Western Plus", "Sito Web": "www.hotelperladelporto.it"},
    {"Property ID": "98326", "Nome account": "Best Western CTC Hotel Verona", "Brand": "Best Western", "Sito Web": "www.ctchotelverona.com"},
    {"Property ID": "98327", "Nome account": "Best Western Premier CHC Airport", "Brand": "Best Western Premier", "Sito Web": "www.chcairport.it"},
    {"Property ID": "98334", "Nome account": "Best Western Titian Inn Hotel Venice Airport", "Brand": "Best Western", "Sito Web": "www.titianinnvenice.com"},
    {"Property ID": "98336", "Nome account": "Best Western Hotel Rome Airport", "Brand": "Best Western", "Sito Web": "www.hotelromeairport.it"},
    {"Property ID": "98339", "Nome account": "Best Western Hotel Rocca", "Brand": "Best Western", "Sito Web": "www.hotelrocca.it"},
    {"Property ID": "98342", "Nome account": "Best Western Hotel Moderno Verdi", "Brand": "Best Western", "Sito Web": "www.modernoverdi.it"},
    {"Property ID": "98343", "Nome account": "Best Western Hotel Piemontese", "Brand": "Best Western", "Sito Web": "www.hotelpiemontese.com"},
    {"Property ID": "98346", "Nome account": "Best Western Plus Leone di Messapia Hotel & Conference", "Brand": "Best Western Plus", "Sito Web": "www.leonedimessapia.it"},
    {"Property ID": "98347", "Nome account": "Best Western Hotel Anthurium", "Brand": "Best Western", "Sito Web": "www.hotelanthurium.it"},
    {"Property ID": "98351", "Nome account": "Best Western Premier Milano Palace Hotel", "Brand": "Best Western Premier", "Sito Web": "www.milanopalacehotel.it"},
    {"Property ID": "98353", "Nome account": "Best Western Hotel I Colli", "Brand": "Best Western", "Sito Web": "www.hotelicolli.com"},
    {"Property ID": "98354", "Nome account": "Best Western Plus Hotel Le Rondini", "Brand": "Best Western Plus", "Sito Web": "www.hotellerondini.it"},
    {"Property ID": "98356", "Nome account": "Best Western Hotel Turismo", "Brand": "Best Western", "Sito Web": "www.hotelturismo.it"},
    {"Property ID": "98359", "Nome account": "Best Western Hotel Armando", "Brand": "Best Western", "Sito Web": "www.hotelarmando.it"},
    {"Property ID": "98361", "Nome account": "Best Western Plus Tower Hotel Bologna", "Brand": "Best Western Plus", "Sito Web": "www.towerhotelbologna.com"},
    {"Property ID": "98363", "Nome account": "Best Western Plus Hotel Terre di Eolo", "Brand": "Best Western Plus", "Sito Web": "www.terredieolo.it"},
    {"Property ID": "98364", "Nome account": "Best Western Mirage Hotel Fiera", "Brand": "Best Western", "Sito Web": "www.mirage-hotel.it"},
    {"Property ID": "98365", "Nome account": "Best Western Crystal Palace Hotel", "Brand": "Best Western", "Sito Web": "www.hotelcrystalpalace.it"},
    {"Property ID": "98366", "Nome account": "Best Western JFK Hotel", "Brand": "Best Western", "Sito Web": "www.hoteljfknapoli.it"},
    {"Property ID": "98367", "Nome account": "Best Western Plus CHC Florence", "Brand": "Best Western Plus", "Sito Web": "www.chcflorence.it"},
    {"Property ID": "98368", "Nome account": "Best Western Hotel Class", "Brand": "Best Western", "Sito Web": "www.hotelclass.it"},
    {"Property ID": "98373", "Nome account": "Best Western Hotel Adige", "Brand": "Best Western", "Sito Web": "www.adigehotel.it"},
    {"Property ID": "98379", "Nome account": "Best Western Plus Net Tower Hotel Padova", "Brand": "Best Western Plus", "Sito Web": "www.towerhotelpadova.net"},
    {"Property ID": "98380", "Nome account": "Best Western Hotel Tritone", "Brand": "Best Western", "Sito Web": "www.hoteltritonevenice.com"},
    {"Property ID": "98381", "Nome account": "Devero Hotel & SPA, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.deverohotel.it"},
    {"Property ID": "98382", "Nome account": "Best Western Hotel Nettuno", "Brand": "Best Western", "Sito Web": "www.nettunohotel.it"},
    {"Property ID": "98385", "Nome account": "Best Western Hotel San Marco", "Brand": "Best Western", "Sito Web": "www.sanmarcosiena.it"},
    {"Property ID": "98395", "Nome account": "Best Western Plus Hotel Royal Superga", "Brand": "Best Western Plus", "Sito Web": "www.hotelroyalsuperga.it"},
    {"Property ID": "98396", "Nome account": "Best Western Air Hotel Linate", "Brand": "Best Western", "Sito Web": "www.airhotel.it"},
    {"Property ID": "98398", "Nome account": "Best Western Maison B Hotel", "Brand": "Best Western", "Sito Web": "www.maisonbhotel.it"},
    {"Property ID": "98399", "Nome account": "Best Western Hotel Imperiale", "Brand": "Best Western", "Sito Web": "www.hotelimperialenovasiri.it"},
    {"Property ID": "98402", "Nome account": "Best Western Hotel Santa Caterina", "Brand": "Best Western", "Sito Web": "www.santacaterinahotel.com"},
    {"Property ID": "98404", "Nome account": "La Dimora di Spartivento, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.dimoradispartivento.it"},
    {"Property ID": "98407", "Nome account": "Aiden by Best Western @ JHD Dunant Hotel", "Brand": "Aiden by Best Western", "Sito Web": "www.dunanthotel.it"},
    {"Property ID": "98408", "Nome account": "Best Western Hotel Corsi", "Brand": "Best Western", "Sito Web": "www.hotelcorsi.it"},
    {"Property ID": "98410", "Nome account": "Horizon Wellness & Spa Resort, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.hotelspavarese.it"},
    {"Property ID": "98411", "Nome account": "Hotel Villa delle Fate, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.hotelvilladellefate.it"},
    {"Property ID": "98412", "Nome account": "Europalace Hotel, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.europalacehotel.com"},
    {"Property ID": "98413", "Nome account": "Hotel Le Ancore, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.leancorehotel.com"},
    {"Property ID": "98414", "Nome account": "Hotel Le Axidie, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.leaxidie.it"},
    {"Property ID": "98415", "Nome account": "Hotel Blumarea, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.hotelblumarea.it"},
    {"Property ID": "98416", "Nome account": "Hotel Cima Rosetta, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.hotelcimarosetta.com"},
    {"Property ID": "98417", "Nome account": "BW Premier Collection Palazzo Gatto Art Hotel & SPA", "Brand": "BW Premier Collection", "Sito Web": "www.palazzogatto.it"},
    {"Property ID": "98418", "Nome account": "Hotel Agorà, Sure Hotel Collection by Best Western", "Brand": "Sure Hotel Collection", "Sito Web": "www.hotelagora.net"},
    {"Property ID": "98419", "Nome account": "Hotel Mulino di Firenze, WorldHotels Crafted", "Brand": "Worldhotels Crafted", "Sito Web": "www.mulinodifirenze.com"},
    {"Property ID": "98421", "Nome account": "Best Western Hotel Principe di Lampedusa", "Brand": "Best Western", "Sito Web": "www.principedilampedusa.it"},
    {"Property ID": "98422", "Nome account": "Best Western Hotel Martello", "Brand": "Best Western", "Sito Web": "www.hotelmartello.it"},
    {"Property ID": "98423", "Nome account": "Hotel Centrale, BW Signature Collection", "Brand": "BW Signature Collection", "Sito Web": "www.hotelcentraletirano.it"},
    {"Property ID": "98424", "Nome account": "Best Western Hotel Massafra", "Brand": "Best Western", "Sito Web": "www.hotelmassafra.it"},
    {"Property ID": "98425", "Nome account": "Best Western Hotel Fiera Verona", "Brand": "Best Western", "Sito Web": "www.hotelfieraverona.biz"},
    {"Property ID": "98443", "Nome account": "Collini Rooms, WorldHotels Crafted", "Brand": "Worldhotels Crafted", "Sito Web": "www.collinirooms.it"},
    {"Property ID": "98442", "Nome account": "Best Western Grand Hotel Catanzaro", "Brand": "Best Western", "Sito Web": "www.grandhotelcatanzaro.it"},
    {"Property ID": "98444", "Nome account": "Best Western Hotel Arya", "Brand": "Best Western", "Sito Web": "www.hotelarya.it"},
    {"Property ID": "98446", "Nome account": "Grand Hotel Della Posta, WorldHotels Distinctive", "Brand": "Worldhotels Distinctive", "Sito Web": "www.grandhoteldellapostasondrio.it"},
    {"Property ID": "98450", "Nome account": "Hotel Terme San Michele & SPA, WorldHotels Distinctive", "Brand": "Worldhotels Distinctive", "Sito Web": "www.hoteltermesanmichele.it"},
]

HOTELS_BY_ID = {h["Property ID"]: h for h in HOTELS}

CSV_COLUMNS = [
    "Property ID",
    "Does the hotel have an on site restaurant?",
    "Restaurant Sequence",
    "Restaurant Name",
    "Restaurant Type",
    "Phone number",
    "Hours Of Operation",
    "Cuisine Type",
    "Dietary Menu Options",
    "Meals Served",
    "Restaurant description",
    "Book a table",
    "View menu",
    "Visit Website",
    "Dining Page Headline",
    "Dining Page Description",
    "Experience Page Dining Headline",
    "Experience Page Dining Description",
]

SYSTEM_PROMPT = """You must extract only verified factual dining information in English for onsite hotel restaurants and bars only. Exclude offsite venues, nearby recommendations, partner venues, and suggested local restaurants. Use a strict output format. Do not add commentary, notes, explanations, source notes, or extra sections.

Allowed Restaurant Type values: Fine dining, Brasserie, Casual dining, Deli, Fast casual, Fast food, Buffet, Cafe / Coffee shop, Coffee bar, Ice cream bar, Snack Bar, Sweet shop, Lounge, Bar/Pub, Bistronomique

Allowed Cuisine Type values: American, BBQ, Chinese, Continental, French, Greek, Indian, International, Italian, Japanese, Korean, Mediterranean, Mexican, Middle Eastern, Seafood, Steakhouse, Thai, Vietnamese

Allowed Dietary Menu Options values: Vegan, Vegetarian, Gluten free, None of the above

Allowed Meals Served values: Breakfast, Brunch, Lunch, Dinner

GENERAL RULES
Only include information that is explicitly available. Do not infer, assume, speculate, estimate, or invent missing details. Do not invent amenities, treatments, pricing, hours, policies, partnerships, or awards. Do not convert suggestive language into fact. Do not fill gaps with likely or typical hotel information. Do not generalize from brand standards, hotel category, destination, or nearby attractions. Do not infer restaurant type, cuisine, dietary options, meals served, or booking availability unless explicitly supported. If a field cannot be verified, leave it blank. If wording on the site is vague, keep the output conservative and factual. If multiple pages appear to conflict, do not reconcile by guessing. Use only what is directly and clearly supported.

Normalize hours into clear English format such as: Mon - Fri 12:30pm - 2:00pm; Mon - Fri 7:30pm - 10:00pm; Sat - Sun 7:30pm - 10:00pm

For Meals Served, include all that apply, separated by commas. For Dietary Menu Options, include one or more supported values separated by commas. If none are explicitly supported, write None of the above. For Cuisine Type, choose only one from the allowed list. For Restaurant Type, choose only one from the allowed list. Phone number must be the restaurant phone number only. If unavailable, leave blank. Restaurant description must be a concise factual summary in English of the website description. Book a table must contain the booking URL only, if available. Visit Website must contain the specific restaurant or restaurant page URL only, if available.

OUTPUT RULES
Always begin with:
Property ID: [propid]
Does the hotel have an on site restaurant? Yes or No

If the hotel has no onsite restaurant or bar, output only:
Property ID: [propid]
Does the hotel have an on site restaurant? No

If the hotel has one or more onsite restaurants or bars, create one complete block for each venue. Use exactly this format and field order:

Property ID: [propid]
Does the hotel have an on site restaurant? Yes or No
Restaurant Sequence: [number]
Restaurant Name: [name of restaurant or bar]
Restaurant Type: [value]
Phone number: [restaurant phone number]
Hours Of Operation: [normalized English hours]
Cuisine Type: [value]
Dietary Menu Options: [values]
Meals Served: [values]
Restaurant description: [summary]
Book a table: [URL]
View menu: [URL]
Visit Website: [URL]
Dining Page Headline: [write in English]
Dining Page Description: [write in English]
Experience Page Dining Headline: [write in English]
Experience Page Dining Description: [write in English]

WRITING RULES FOR Dining Page Headline: Write in English. Use a warm, welcoming, witty, and wise tone with light wit. Keep the voice polished and quietly confident. Be concise, inviting, and expressive. Reflect the personality of that specific restaurant or bar. Stay grounded in verified facts only. Avoid clichés, hype, slang, sarcasm, jokes, and region specific idioms. Do not use hyphens or dashes.

WRITING RULES FOR Dining Page Description: Write in English for a hotel dining overview section. Use a warm, welcoming, witty, and wise tone with light wit. Maintain a polished and quietly confident voice. Be expressive yet controlled, focusing on atmosphere and personality. Write in smooth, flowing sentences. Stay grounded in verified facts only. Avoid clichés, hype, slang, sarcasm, jokes, and region specific idioms. Do not use hyphens or dashes.

WRITING RULES FOR Experience Page Dining Headline: Write in English for a hotel dining experience page. Use a warm, welcoming, witty, and wise tone. Keep the voice polished, evocative, and quietly confident. Be concise and focused on the feeling of the experience. Reflect the identity of that specific restaurant or bar. Stay grounded in verified facts only. Avoid clichés, hype, slang, sarcasm, jokes, and region specific idioms. Do not use hyphens or dashes.

WRITING RULES FOR Experience Page Dining Description: Write in English for a hotel dining experience page. Use a warm, welcoming, witty, and wise tone. Maintain a polished and quietly confident voice. Focus on how the dining experience feels and what makes it distinctive. Be vivid but controlled. Reflect the personality of that specific restaurant or bar. Stay grounded in verified facts only. Avoid clichés, hype, slang, sarcasm, jokes, and region specific idioms. Do not use hyphens or dashes.

ANTI HALLUCINATION GUARDRAILS: Use only explicit information. Absence of evidence is not evidence. Do not infer dietary options from generic menu language. Do not infer bookable status from a contact form or general hotel booking engine unless it clearly applies to the restaurant. Do not infer phone number from the hotel main number. When in doubt, leave the field blank."""
