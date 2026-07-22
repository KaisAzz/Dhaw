# -*- coding: utf-8 -*-
"""
Gazetteer Tunisie : zone/délégation -> gouvernorat.
Clés normalisées (minuscules, sans accents). Extensible librement :
plus on ajoute de quartiers/localités, meilleur est le matching.
"""

GAZETTEER = {
    # ---- Tunis ----
    "el menzah": "Tunis", "el manar": "Tunis", "bab souika": "Tunis",
    "la marsa": "Tunis", "el omrane": "Tunis", "sidi hassine": "Tunis",
    "le bardo": "Tunis", "bardo": "Tunis", "le kram": "Tunis", "kram": "Tunis",
    "la goulette": "Tunis", "carthage": "Tunis", "jardins de carthage": "Tunis",
    "sidi bou said": "Tunis", "el ouardia": "Tunis", "el kabaria": "Tunis",
    "cite el khadra": "Tunis", "montplaisir": "Tunis", "lafayette": "Tunis",
    "bab el bhar": "Tunis", "medina": "Tunis", "sejoumi": "Tunis",
    "hraira": "Tunis", "ezzouhour": "Tunis", "el menzah 6": "Tunis",
    # ---- Ariana ----
    "ariana": "Ariana", "l ariana": "Ariana", "cite ennasr": "Ariana",
    "ennasr": "Ariana", "raoued": "Ariana", "la soukra": "Ariana",
    "soukra": "Ariana", "mnihla": "Ariana", "ettadhamen": "Ariana",
    "cite ettadhamen": "Ariana", "kalaat el andalous": "Ariana",
    "kalaat andalouss": "Ariana", "sidi thabet": "Ariana", "borj touil": "Ariana",
    "ain zaghouan": "Tunis", "borj louzir": "Ariana", "ghazela": "Ariana",
    # ---- Ben Arous ----
    "ben arous": "Ben Arous", "rades": "Ben Arous", "ezzahra": "Ben Arous",
    "ez zahra": "Ben Arous", "megrine": "Ben Arous", "hammam lif": "Ben Arous",
    "hammam chott": "Ben Arous", "boumhal": "Ben Arous", "bou mhel": "Ben Arous",
    "mornag": "Ben Arous", "fouchana": "Ben Arous", "mohamedia": "Ben Arous",
    "el mourouj": "Ben Arous", "mourouj": "Ben Arous", "borj cedria": "Ben Arous",
    "el mghria": "Ben Arous", "birine": "Ben Arous", "khalidia": "Ben Arous",
    # ---- Manouba ----
    "manouba": "Manouba", "la manouba": "Manouba", "douar hicher": "Manouba",
    "oued ellil": "Manouba", "tebourba": "Manouba", "jedaida": "Manouba",
    "battan": "Manouba", "borj el amri": "Manouba", "mornaguia": "Manouba",
    "den den": "Manouba",
    # ---- Nabeul ----
    "nabeul": "Nabeul", "hammamet": "Nabeul", "korba": "Nabeul",
    "kelibia": "Nabeul", "menzel temime": "Nabeul", "menzel temine": "Nabeul",
    "beni khalled": "Nabeul", "beni khiar": "Nabeul", "bou argoub": "Nabeul",
    "dar allouche": "Nabeul", "dar chaabane": "Nabeul", "el haouaria": "Nabeul",
    "el mida": "Nabeul", "grombalia": "Nabeul", "hammam ghzez": "Nabeul",
    "menzel bouzelfa": "Nabeul", "soliman": "Nabeul", "takelsa": "Nabeul",
    "zaouiet djedidi": "Nabeul", "yasmine hammamet": "Nabeul",
    # ---- Zaghouan ----
    "zaghouan": "Zaghouan", "el fahs": "Zaghouan", "zriba": "Zaghouan",
    "nadhour": "Zaghouan", "saouaf": "Zaghouan", "bir mcherga": "Zaghouan",
    "jebel oust": "Zaghouan", "djebel el ouest": "Zaghouan", "jradou": "Zaghouan",
    "bou achir": "Zaghouan",
    # ---- Bizerte ----
    "bizerte": "Bizerte", "menzel bourguiba": "Bizerte", "mateur": "Bizerte",
    "ras jebel": "Bizerte", "sejnane": "Bizerte", "joumine": "Bizerte",
    "metline": "Bizerte", "menzel abderrahamane": "Bizerte",
    "menzel abderrahmane": "Bizerte", "el alia": "Bizerte",
    "ghar el melh": "Bizerte", "menzel jemil": "Bizerte", "menzel jmill": "Bizerte",
    "tinja": "Bizerte", "utique": "Bizerte", "ghezala": "Bizerte", "zarzouna": "Bizerte",
    # ---- Béja ----
    "beja": "Béja", "medjez el bab": "Béja", "mjez elbeb": "Béja",
    "medjez elbab": "Béja", "testour": "Béja", "nefza": "Béja",
    "teboursouk": "Béja", "goubellat": "Béja", "amdoun": "Béja",
    "thibar": "Béja", "ouachtata": "Béja", "maagoula": "Béja",
    # ---- Jendouba ----
    "jendouba": "Jendouba", "tabarka": "Jendouba", "ain draham": "Jendouba",
    "bou salem": "Jendouba", "bousalem": "Jendouba", "ghardimaou": "Jendouba",
    "fernana": "Jendouba", "balta bou aouane": "Jendouba", "oued mliz": "Jendouba",
    "ben bechir": "Jendouba",
    # ---- El Kef ----
    "le kef": "El Kef", "el kef": "El Kef", "kef": "El Kef",
    "dahmani": "El Kef", "tajerouine": "El Kef", "tejerouine": "El Kef",
    "le sers": "El Kef", "sers": "El Kef", "djerissa": "El Kef",
    "jerissa": "El Kef", "kalaat senan": "El Kef", "kalaat khasba": "El Kef",
    "nebeur": "El Kef", "sakiet sidi youssef": "El Kef", "touiref": "El Kef",
    # ---- Siliana ----
    "siliana": "Siliana", "makthar": "Siliana", "makther": "Siliana",
    "bou arada": "Siliana", "gaafour": "Siliana", "el krib": "Siliana",
    "bourouis": "Siliana", "bargou": "Siliana", "kesra": "Siliana",
    "rouhia": "Siliana", "sidi bou rouis": "Siliana",
    # ---- Sousse ----
    "sousse": "Sousse", "msaken": "Sousse", "m saken": "Sousse",
    "kalaa kebira": "Sousse", "kalaa sghira": "Sousse", "enfidha": "Sousse",
    "hammam sousse": "Sousse", "akouda": "Sousse", "hergla": "Sousse",
    "bouficha": "Sousse", "kondar": "Sousse", "sidi bou ali": "Sousse",
    "sidi el hani": "Sousse", "zaouiet sousse": "Sousse", "chott meriem": "Sousse",
    "quartier universitaire": "Sousse", "port el kantaoui": "Sousse",
    # ---- Monastir ----
    "monastir": "Monastir", "ksar hellal": "Monastir", "ksar helal": "Monastir",
    "moknine": "Monastir", "jemmal": "Monastir", "sahline": "Monastir",
    "bembla": "Monastir", "teboulba": "Monastir", "sayada": "Monastir",
    "ksibet el mediouni": "Monastir", "lamta": "Monastir", "ksar lemta": "Monastir",
    "bekalta": "Monastir", "zeramdine": "Monastir", "beni hassen": "Monastir",
    "menzel kamel": "Monastir", "bouhjar": "Monastir", "ouerdanine": "Monastir",
    # ---- Mahdia ----
    "mahdia": "Mahdia", "ksour essef": "Mahdia", "chebba": "Mahdia",
    "el jem": "Mahdia", "bou merdes": "Mahdia", "chorbane": "Mahdia",
    "essouassi": "Mahdia", "souassi": "Mahdia", "hebira": "Mahdia",
    "melloulech": "Mahdia", "ouled chamekh": "Mahdia", "aouled chamekh": "Mahdia",
    "rejiche": "Mahdia", "sidi alouane": "Mahdia", "kerker": "Mahdia",
    # ---- Sfax ----
    "sfax": "Sfax", "sakiet ezzit": "Sfax", "sakiet eddaier": "Sfax",
    "thyna": "Sfax", "mahres": "Sfax", "kerkennah": "Sfax",
    "jebeniana": "Sfax", "el amra": "Sfax", "el amara": "Sfax",
    "agareb": "Sfax", "bir ali": "Sfax", "bir ali ben khalifa": "Sfax",
    "menzel chaker": "Sfax", "skhira": "Sfax", "graiba": "Sfax",
    "el ghraiba": "Sfax", "el hancha": "Sfax", "ghraba": "Sfax",
    "centre ville de sfax": "Sfax", "sfax ville": "Sfax",
    # ---- Kairouan ----
    "kairouan": "Kairouan", "haffouz": "Kairouan", "sbikha": "Kairouan",
    "bou hajla": "Kairouan", "bouhajla": "Kairouan", "hajeb el ayoun": "Kairouan",
    "nasrallah": "Kairouan", "echrarda": "Kairouan", "oueslatia": "Kairouan",
    "chebika": "Kairouan", "el ala": "Kairouan", "ain jalloula": "Kairouan",
    "menzel mehiri": "Kairouan", "ragada": "Kairouan", "raccada": "Kairouan",
    "dar el jamiaa": "Kairouan", "ouled achour": "Kairouan",
    "essouilehat": "Kairouan",
    # ---- Kasserine ----
    "kasserine": "Kasserine", "sbeitla": "Kasserine", "feriana": "Kasserine",
    "thala": "Kasserine", "sbiba": "Kasserine", "foussana": "Kasserine",
    "foussana cite el ferid": "Kasserine", "majel bel abbes": "Kasserine",
    "jedelienne": "Kasserine", "el ayoun": "Kasserine", "laayoune": "Kasserine",
    "ezzouhour kasserine": "Kasserine", "hassi el ferid": "Kasserine",
    "hidra": "Kasserine", "khamouda boudris": "Kasserine", "khamouda": "Kasserine",
    # ---- Sidi Bouzid ----
    "sidi bouzid": "Sidi Bouzid", "regueb": "Sidi Bouzid",
    "meknassy": "Sidi Bouzid", "jilma": "Sidi Bouzid",
    "bir el hafey": "Sidi Bouzid", "menzel bouzaiane": "Sidi Bouzid",
    "mezzouna": "Sidi Bouzid", "ouled haffouz": "Sidi Bouzid",
    "aouled haffouz": "Sidi Bouzid", "cebbala": "Sidi Bouzid",
    "souk jedid": "Sidi Bouzid", "sou ejdid": "Sidi Bouzid",
    "sidi ali ben aoun": "Sidi Bouzid",
    # ---- Gabès ----
    "gabes": "Gabès", "mareth": "Gabès", "el hamma": "Gabès",
    "metouia": "Gabès", "ghannouch": "Gabès", "matmata": "Gabès",
    "nouvelle matmata": "Gabès", "menzel habib": "Gabès",
    "bouchamma": "Gabès", "bouchemma": "Gabès", "chenini nahal": "Gabès",
    "cite el izdihar": "Gabès", "chentech": "Gabès", "cite el hana": "Gabès",
    "matrech": "Gabès", "teboulbou": "Gabès",
    # ---- Médenine ----
    "medenine": "Médenine", "djerba": "Médenine", "houmt souk": "Médenine",
    "houmet essouk": "Médenine", "midoun": "Médenine", "ajim": "Médenine",
    "zarzis": "Médenine", "ben gardane": "Médenine", "ben guerdane": "Médenine",
    "beni khedache": "Médenine", "sidi makhlouf": "Médenine",
    "el jamila": "Médenine", "route de ras jedir": "Médenine",
    "zarzis ville": "Médenine",
    # ---- Tataouine ----
    "tataouine": "Tataouine", "ghomrassen": "Tataouine", "remada": "Tataouine",
    "bir lahmar": "Tataouine", "dehiba": "Tataouine", "smar": "Tataouine",
    "nouvelle tataouine": "Tataouine", "cite oued el kamh": "Tataouine",
    "cite mahrajene": "Tataouine", "borj bourguiba": "Tataouine",
    # ---- Gafsa ----
    "gafsa": "Gafsa", "metlaoui": "Gafsa", "el ksar": "Gafsa",
    "redeyef": "Gafsa", "moulares": "Gafsa", "el guettar": "Gafsa",
    "sened": "Gafsa", "belkhir": "Gafsa", "mdhilla": "Gafsa",
    "sidi aich": "Gafsa", "sidi yaich": "Gafsa", "ksar gafsa": "Gafsa",
    "el saida": "Gafsa", "aouled ahmed": "Gafsa", "makarem": "Gafsa",
    # ---- Tozeur ----
    "tozeur": "Tozeur", "nefta": "Tozeur", "degache": "Tozeur",
    "tamerza": "Tozeur", "hazoua": "Tozeur", "hamet jerid": "Tozeur",
    # ---- Kébili ----
    "kebili": "Kébili", "douz": "Kébili", "souk lahad": "Kébili",
    "el golaa": "Kébili", "jemna": "Kébili", "faouar": "Kébili",
    "rahmet": "Kébili", "cite route de gabes": "Kébili",
}

# Noms officiels des 24 gouvernorats (pour matching direct "gouvernorat de X")
GOVERNORATS = [
    "Tunis", "Ariana", "Ben Arous", "Manouba", "Nabeul", "Zaghouan",
    "Bizerte", "Béja", "Jendouba", "El Kef", "Siliana", "Sousse",
    "Monastir", "Mahdia", "Sfax", "Kairouan", "Kasserine", "Sidi Bouzid",
    "Gabès", "Médenine", "Tataouine", "Gafsa", "Tozeur", "Kébili",
]
