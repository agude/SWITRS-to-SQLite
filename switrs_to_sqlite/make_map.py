from enum import Enum, unique


@unique
class Make(Enum):
    ACADIAN                 = "acadian"
    ACURA                   = "acura"
    ALFA_ROMERO             = "alfa romera"
    AMC                     = "american motors"
    AMERICAN_LAFRANCE       = "american lafrance"
    AUDI                    = "audi"
    AUTOCAR                 = "autocar"
    BENTLEY                 = "bentley"
    BLUEBIRD                = "bluebird"
    BMW                     = "bmw"
    BUICK                   = "buick"
    CADILLAC                = "cadillac"
    CHEVROLET               = "chevrolet"
    CHRYSLER                = "chrysler"
    CROWN                   = "crown"
    DAEWOO                  = "daewoo"
    DATSUN                  = "datsun"
    DELOREAN                = "delorean"
    DODGE                   = "dodge"
    DUCATI                  = "ducati"
    FERRARI                 = "ferrari"
    FIAT                    = "fiat"
    FORD                    = "ford"
    FREIGHTLINER            = "freightliner"
    GEO                     = "geo"
    GILLIG                  = "gillig"
    GMC                     = "gmc"
    GRUMMAN                 = "grumman"
    HARLEY                  = "harley-davidson"
    HINO                    = "hino"
    HONDA                   = "honda"
    HUMMER                  = "hummer"
    HYUNDAI                 = "hyundai"
    INFINITI                = "infiniti"
    INTERNATIONAL_HARVESTER = "international harvester"
    ISUZU                   = "isuzu"
    JAGUAR                  = "jaguar"
    JEEP                    = "jeep"
    JOHN_DEERE              = "john deere"
    KAWASAKI                = "kawasaki"
    KENWORTH                = "kenworth"
    KIA                     = "kia"
    LAND_ROVER              = "land rover"
    LEXUS                   = "lexus"
    LINCOLN                 = "lincoln"
    MACK                    = "mack"
    MASERATI                = "maserati"
    MAZDA                   = "mazda"
    MERCEDES_BENZ           = "mercedes-benz"
    MERCURY                 = "mercury"
    MINI                    = "mini"
    MITSUBISHI              = "mitsubishi"
    NISSAN                  = "nissan"
    NONE                    = None
    OLDSMOBILE              = "oldsmobile"
    PETERBILT               = "peterbilt"
    PLYMOUTH                = "plymouth"
    PONTIAC                 = "pontiac"
    PORSCHE                 = "porsche"
    RADPOWER                = "rad power bikes"
    RAM                     = "ram"
    SAAB                    = "saab"
    SATURN                  = "saturn"
    SCHWINN                 = "schwinn"
    SCION                   = "scion"
    SMART                   = "smart"
    STERLING                = "sterling"
    SUBARU                  = "subaru"
    SUZUKI                  = "suzuki"
    TESLA                   = "tesla"
    THOMAS                  = "thomas"
    TOYOTA                  = "toyota"
    TREK                    = "trek"
    TRIUMPH                 = "triumph"
    VESPA                   = "vespa"
    VOLKSWAGEN              = "volkswagen"
    VOLVO                   = "volvo"
    WHITE                   = "white"
    WINNEBAGO               = "winnebago"
    YAMAHA                  = "yamaha"


MAKE_MAP = {
    "(UNK)": Make.NONE.value,
    "--": Make.NONE.value,
    "---": Make.NONE.value,
    "/": Make.NONE.value,
    "ACAD": Make.ACADIAN.value,
    "ACADIAN": Make.ACADIAN.value,
    "ACCURA": Make.ACURA.value,
    "ACRU": Make.ACURA.value,
    "ACRUA": Make.ACURA.value,
    "ACU": Make.ACURA.value,
    "ACUA": Make.ACURA.value,
    "ACUR /": Make.ACURA.value,
    "ACUR": Make.ACURA.value,
    "ACURA": Make.ACURA.value,
    "ACURA/": Make.ACURA.value,
    "ALFA ROMEO": Make.ALFA_ROMERO.value,
    "ALFA ROMERO": Make.ALFA_ROMERO.value,
    "ALFA": Make.ALFA_ROMERO.value,
    "ALFR": Make.ALFA_ROMERO.value,
    "AMER": Make.AMC.value,
    "AMERI": Make.AMC.value,
    "AMERICAN LA FRANCE": Make.AMERICAN_LAFRANCE.value,
    "AMERICAN MOTORS (AMC)": Make.AMC.value,
    "AMERICAN MOTORS": Make.AMC.value,
    "AMERICAN": Make.AMC.value,
    "AUD": Make.AUDI.value,
    "AUDI /": Make.AUDI.value,
    "AUDI": Make.AUDI.value,
    "AUDI/": Make.AUDI.value,
    "AUDU": Make.AUDI.value,
    "AUID": Make.AUDI.value,
    "AUIDI": Make.AUDI.value,
    "AUTOCAR": Make.AUTOCAR.value,
    "BENT": Make.BENTLEY.value,
    "BENTL": Make.BENTLEY.value,
    "BENTLEY": Make.BENTLEY.value,
    "BENZ": Make.MERCEDES_BENZ.value,
    "BLU BIRD": Make.BLUEBIRD.value,
    "BLU": Make.BLUEBIRD.value,
    "BLUB": Make.BLUEBIRD.value,
    "BLUBD": Make.BLUEBIRD.value,
    "BLUBI": Make.BLUEBIRD.value,
    "BLUBIRD": Make.BLUEBIRD.value,
    "BLUBR": Make.BLUEBIRD.value,
    "BLUBRD": Make.BLUEBIRD.value,
    "BLUE BIR": Make.BLUEBIRD.value,
    "BLUE BIRD": Make.BLUEBIRD.value,
    "BLUE": Make.BLUEBIRD.value,
    "BLUEB": Make.BLUEBIRD.value,
    "BLUEBIR": Make.BLUEBIRD.value,
    "BLUEBIRD (BUS)": Make.BLUEBIRD.value,
    "BLUEBIRD": Make.BLUEBIRD.value,
    "BMW /": Make.BMW.value,
    "BMW": Make.BMW.value,
    "BMW/": Make.BMW.value,
    "BMW1": Make.BMW.value,
    "BMW`": Make.BMW.value,
    "BUCIK": Make.BUICK.value,
    "BUCK": Make.BUICK.value,
    "BUI": Make.BUICK.value,
    "BUIC": Make.BUICK.value,
    "BUICK": Make.BUICK.value,
    "BUICK/": Make.BUICK.value,
    "BUIK": Make.BUICK.value,
    "BWM": Make.BMW.value,
    "BWW": Make.BMW.value,
    "CADI": Make.CADILLAC.value,
    "CADI/": Make.CADILLAC.value,
    "CADIL": Make.CADILLAC.value,
    "CADILA": Make.CADILLAC.value,
    "CADILAC": Make.CADILLAC.value,
    "CADILL": Make.CADILLAC.value,
    "CADILLA": Make.CADILLAC.value,
    "CADILLAC": Make.CADILLAC.value,
    "CEHV": Make.CHEVROLET.value,
    "CEHVY": Make.CHEVROLET.value,
    "CHEROLET": Make.CHEVROLET.value,
    "CHEV /": Make.CHEVROLET.value,
    "CHEV": Make.CHEVROLET.value,
    "CHEV/": Make.CHEVROLET.value,
    "CHEVE": Make.CHEVROLET.value,
    "CHEVER": Make.CHEVROLET.value,
    "CHEVEROL": Make.CHEVROLET.value,
    "CHEVEY": Make.CHEVROLET.value,
    "CHEVOLET": Make.CHEVROLET.value,
    "CHEVR": Make.CHEVROLET.value,
    "CHEVRLET": Make.CHEVROLET.value,
    "CHEVRLT": Make.CHEVROLET.value,
    "CHEVRO": Make.CHEVROLET.value,
    "CHEVROEL": Make.CHEVROLET.value,
    "CHEVROET": Make.CHEVROLET.value,
    "CHEVROL": Make.CHEVROLET.value,
    "CHEVROLE": Make.CHEVROLET.value,
    "CHEVROLET": Make.CHEVROLET.value,
    "CHEVROLT": Make.CHEVROLET.value,
    "CHEVT": Make.CHEVROLET.value,
    "CHEVY": Make.CHEVROLET.value,
    "CHEVY/": Make.CHEVROLET.value,
    "CHEV`": Make.CHEVROLET.value,
    "CHRS": Make.CHRYSLER.value,
    "CHRSLER": Make.CHRYSLER.value,
    "CHRSY": Make.CHRYSLER.value,
    "CHRY": Make.CHRYSLER.value,
    "CHRY/": Make.CHRYSLER.value,
    "CHRYL": Make.CHRYSLER.value,
    "CHRYLER": Make.CHRYSLER.value,
    "CHRYLSER": Make.CHRYSLER.value,
    "CHRYS": Make.CHRYSLER.value,
    "CHRYS/": Make.CHRYSLER.value,
    "CHRYSER": Make.CHRYSLER.value,
    "CHRYSL": Make.CHRYSLER.value,
    "CHRYSLE": Make.CHRYSLER.value,
    "CHRYSLER": Make.CHRYSLER.value,
    "CHRYSLR": Make.CHRYSLER.value,
    "CHRYST": Make.CHRYSLER.value,
    "CHRYSTLE": Make.CHRYSLER.value,
    "CHV": Make.CHEVROLET.value,
    "CHVROLET": Make.CHEVROLET.value,
    "CHVY": Make.CHEVROLET.value,
    "CHY": Make.CHRYSLER.value,
    "CHYRSLER": Make.CHRYSLER.value,
    "CHYSLER": Make.CHRYSLER.value,
    "CROW": Make.CROWN.value,
    "CROWN (BUS)": Make.CROWN.value,
    "CROWN": Make.CROWN.value,
    "CRY": Make.CHRYSLER.value,
    "CRYS": Make.CHRYSLER.value,
    "CRYSLER": Make.CHRYSLER.value,
    "D0DGE": Make.DODGE.value,
    "DAEW": Make.DAEWOO.value,
    "DAEWO": Make.DAEWOO.value,
    "DAEWOO": Make.DAEWOO.value,
    "DATS": Make.DATSUN.value,
    "DATSU": Make.DATSUN.value,
    "DATSUN": Make.DATSUN.value,
    "DATSUN/NISSAN": Make.NISSAN.value,
    "DDGE": Make.DODGE.value,
    "DDOGE": Make.DODGE.value,
    "DELOREAN": Make.DELOREAN.value,
    "DOD": Make.DODGE.value,
    "DODDGE": Make.DODGE.value,
    "DODE": Make.DODGE.value,
    "DODEG": Make.DODGE.value,
    "DODG /": Make.DODGE.value,
    "DODG": Make.DODGE.value,
    "DODG/": Make.DODGE.value,
    "DODGE /": Make.DODGE.value,
    "DODGE": Make.DODGE.value,
    "DODGE/": Make.DODGE.value,
    "DODGER": Make.DODGE.value,
    "DODGE`": Make.DODGE.value,
    "DODGW": Make.DODGE.value,
    "DOG": Make.DODGE.value,
    "DOGDE": Make.DODGE.value,
    "DOGE": Make.DODGE.value,
    "DOGGE": Make.DODGE.value,
    "DUCA": Make.DUCATI.value,
    "DUCAT": Make.DUCATI.value,
    "DUCATI (MOTORCYCLE)": Make.DUCATI.value,
    "DUCATI": Make.DUCATI.value,
    "DUCTI": Make.DUCATI.value,
    "FERRARA": Make.FERRARI.value,
    "FERRARI": Make.FERRARI.value,
    "FIAT": Make.FIAT.value,
    "FIAT-ABARTH": Make.FIAT.value,
    "FOR": Make.FORD.value,
    "FORC": Make.FORD.value,
    "FORD /": Make.FORD.value,
    "FORD": Make.FORD.value,
    "FORD/": Make.FORD.value,
    "FORDE": Make.FORD.value,
    "FORD`": Make.FORD.value,
    "FORE": Make.FORD.value,
    "FORED": Make.FORD.value,
    "FORF": Make.FORD.value,
    "FORN": Make.NONE.value,
    "FORR": Make.FORD.value,
    "FORRD": Make.FORD.value,
    "FORS": Make.FORD.value,
    "FRD": Make.FORD.value,
    "FREHT": Make.FREIGHTLINER.value,
    "FREI /": Make.FREIGHTLINER.value,
    "FREI": Make.FREIGHTLINER.value,
    "FREIG": Make.FREIGHTLINER.value,
    "FREIGH": Make.FREIGHTLINER.value,
    "FREIGHT LINER": Make.FREIGHTLINER.value,
    "FREIGHT": Make.FREIGHTLINER.value,
    "FREIGHTL": Make.FREIGHTLINER.value,
    "FREIGHTLINER CORP": Make.FREIGHTLINER.value,
    "FREIGHTLINER": Make.FREIGHTLINER.value,
    "FREIGT": Make.FREIGHTLINER.value,
    "FREIHT": Make.FREIGHTLINER.value,
    "FREIT": Make.FREIGHTLINER.value,
    "FREITLIN": Make.FREIGHTLINER.value,
    "FREITLNR": Make.FREIGHTLINER.value,
    "FRGH": Make.FREIGHTLINER.value,
    "FRGHT": Make.FREIGHTLINER.value,
    "FRGHT.": Make.FREIGHTLINER.value,
    "FRGHTLNR": Make.FREIGHTLINER.value,
    "FRGT": Make.FREIGHTLINER.value,
    "FRGTH": Make.FREIGHTLINER.value,
    "FRGTLNR": Make.FREIGHTLINER.value,
    "FRH": Make.FREIGHTLINER.value,
    "FRHGT": Make.FREIGHTLINER.value,
    "FRHI": Make.FREIGHTLINER.value,
    "FRHK": Make.FREIGHTLINER.value,
    "FRHT /": Make.FREIGHTLINER.value,
    "FRHT": Make.FREIGHTLINER.value,
    "FRHT.": Make.FREIGHTLINER.value,
    "FRHT/": Make.FREIGHTLINER.value,
    "FRHTL": Make.FREIGHTLINER.value,
    "FRHTLINE": Make.FREIGHTLINER.value,
    "FRHTLINR": Make.FREIGHTLINER.value,
    "FRHTLN": Make.FREIGHTLINER.value,
    "FRHTLNR": Make.FREIGHTLINER.value,
    "FRI": Make.FREIGHTLINER.value,
    "FRIE": Make.FREIGHTLINER.value,
    "FRIEGH": Make.FREIGHTLINER.value,
    "FRIEGHT": Make.FREIGHTLINER.value,
    "FRIEGHTL": Make.FREIGHTLINER.value,
    "FRIET": Make.FREIGHTLINER.value,
    "FRIGH": Make.FREIGHTLINER.value,
    "FRIGHT": Make.FREIGHTLINER.value,
    "FROD": Make.FORD.value,
    "FRT": Make.FREIGHTLINER.value,
    "FRTH": Make.FREIGHTLINER.value,
    "FRTL": Make.FREIGHTLINER.value,
    "FRTLINER": Make.FREIGHTLINER.value,
    "FRTLN": Make.FREIGHTLINER.value,
    "FRTLNR": Make.FREIGHTLINER.value,
    "FTL": Make.FREIGHTLINER.value,
    "FTLR": Make.FREIGHTLINER.value,
    "GENERAL MOTORS CORP": Make.GMC.value,
    "GENERAL": Make.GMC.value,
    "GEO": Make.GEO.value,
    "GILG": Make.GILLIG.value,
    "GILIG": Make.GILLIG.value,
    "GILL": Make.GILLIG.value,
    "GILLI": Make.GILLIG.value,
    "GILLIC": Make.GILLIG.value,
    "GILLIG (BUS)": Make.GILLIG.value,
    "GILLIG BUS": Make.GILLIG.value,
    "GILLIG": Make.GILLIG.value,
    "GM": Make.GMC.value,
    "GMA": Make.GMC.value,
    "GMC (GENERAL MOTORS)": Make.GMC.value,
    "GMC /": Make.GMC.value,
    "GMC": Make.GMC.value,
    "GMC/": Make.GMC.value,
    "GMG": Make.GMC.value,
    "GMS": Make.GMC.value,
    "GMV": Make.GMC.value,
    "GMX": Make.GMC.value,
    "GMZ": Make.GMC.value,
    "GNC": Make.GMC.value,
    "GRUM": Make.GRUMMAN.value,
    "GRUMAN": Make.GRUMMAN.value,
    "GRUMANN": Make.GRUMMAN.value,
    "GRUMIN": Make.GRUMMAN.value,
    "GRUMM": Make.GRUMMAN.value,
    "GRUMMAN MOTOR HOME": Make.GRUMMAN.value,
    "GRUMMAN": Make.GRUMMAN.value,
    "H0NDA": Make.HONDA.value,
    "HANDA": Make.HONDA.value,
    "HARL /": Make.HARLEY.value,
    "HARL DAV": Make.HARLEY.value,
    "HARL": Make.HARLEY.value,
    "HARLE": Make.HARLEY.value,
    "HARLEY D": Make.HARLEY.value,
    "HARLEY DAVIDSON": Make.HARLEY.value,
    "HARLEY": Make.HARLEY.value,
    "HARLEY-D": Make.HARLEY.value,
    "HARLEY-DAVIDSON": Make.HARLEY.value,
    "HARLEYD": Make.HARLEY.value,
    "HARLY": Make.HARLEY.value,
    "HD": Make.HARLEY.value,
    "HD/": Make.HARLEY.value,
    "HINO": Make.HINO.value,
    "HINO/": Make.HINO.value,
    "HIOND": Make.HONDA.value,
    "HIONDA": Make.HONDA.value,
    "HODNA": Make.HONDA.value,
    "HOINDA": Make.HONDA.value,
    "HON": Make.HONDA.value,
    "HONA": Make.HONDA.value,
    "HONAD": Make.HONDA.value,
    "HOND /": Make.HONDA.value,
    "HOND": Make.HONDA.value,
    "HOND/": Make.HONDA.value,
    "HONDA /": Make.HONDA.value,
    "HONDA MC": Make.HONDA.value,
    "HONDA": Make.HONDA.value,
    "HONDA/": Make.HONDA.value,
    "HONDAS": Make.HONDA.value,
    "HONDAY": Make.HONDA.value,
    "HONDA`": Make.HONDA.value,
    "HONDS": Make.HONDA.value,
    "HONE": Make.HONDA.value,
    "HONF": Make.HONDA.value,
    "HONG": Make.HONDA.value,
    "HONS": Make.HONDA.value,
    "HONSA": Make.HONDA.value,
    "HUMM": Make.HUMMER.value,
    "HUMME": Make.HUMMER.value,
    "HUMMER": Make.HUMMER.value,
    "HUMVEE": Make.HUMMER.value,
    "HUN": Make.HYUNDAI.value,
    "HUNDAI": Make.HYUNDAI.value,
    "HUYN": Make.HYUNDAI.value,
    "HUYNDAI": Make.HYUNDAI.value,
    "HYN": Make.HYUNDAI.value,
    "HYND": Make.HYUNDAI.value,
    "HYNDAI": Make.HYUNDAI.value,
    "HYNU": Make.HYUNDAI.value,
    "HYNUDAI": Make.HYUNDAI.value,
    "HYU N": Make.HYUNDAI.value,
    "HYU": Make.HYUNDAI.value,
    "HYUAN": Make.HYUNDAI.value,
    "HYUANDAI": Make.HYUNDAI.value,
    "HYUD": Make.HYUNDAI.value,
    "HYUDAI": Make.HYUNDAI.value,
    "HYUIN": Make.HYUNDAI.value,
    "HYUM": Make.HYUNDAI.value,
    "HYUN /": Make.HYUNDAI.value,
    "HYUN": Make.HYUNDAI.value,
    "HYUN/": Make.HYUNDAI.value,
    "HYUNA": Make.HYUNDAI.value,
    "HYUNAI": Make.HYUNDAI.value,
    "HYUND": Make.HYUNDAI.value,
    "HYUNDA": Make.HYUNDAI.value,
    "HYUNDAI": Make.HYUNDAI.value,
    "HYUNDAI/": Make.HYUNDAI.value,
    "HYUNDAU": Make.HYUNDAI.value,
    "HYUNDAY": Make.HYUNDAI.value,
    "HYUNDI": Make.HYUNDAI.value,
    "HYUNDIA": Make.HYUNDAI.value,
    "HYUU": Make.HYUNDAI.value,
    "HYUUN": Make.HYUNDAI.value,
    "INF": Make.INFINITI.value,
    "INFI /": Make.INFINITI.value,
    "INFI": Make.INFINITI.value,
    "INFIN": Make.INFINITI.value,
    "INFIN/": Make.INFINITI.value,
    "INFINI": Make.INFINITI.value,
    "INFINIT": Make.INFINITI.value,
    "INFINITE": Make.INFINITI.value,
    "INFINITI": Make.INFINITI.value,
    "INFINITY": Make.INFINITI.value,
    "INFINT": Make.INFINITI.value,
    "INFINTI": Make.INFINITI.value,
    "INFINTY": Make.INFINITI.value,
    "INFIT": Make.INFINITI.value,
    "INIF": Make.INFINITI.value,
    "INIFI": Make.INFINITI.value,
    "INIFINIT": Make.INFINITI.value,
    "INIFNITI": Make.INFINITI.value,
    "INTER": Make.INTERNATIONAL_HARVESTER.value,
    "INTERNAT": Make.INTERNATIONAL_HARVESTER.value,
    "INTERNATIONAL HARVESTER": Make.INTERNATIONAL_HARVESTER.value,
    "INTL": Make.NONE.value,
    "ISU": Make.ISUZU.value,
    "ISUZ": Make.ISUZU.value,
    "ISUZU": Make.ISUZU.value,
    "JAG": Make.JAGUAR.value,
    "JAGA": Make.JAGUAR.value,
    "JAGU": Make.JAGUAR.value,
    "JAGUA": Make.JAGUAR.value,
    "JAGUAR": Make.JAGUAR.value,
    "JDEER": Make.JOHN_DEERE.value,
    "JEE": Make.JEEP.value,
    "JEEEP": Make.JEEP.value,
    "JEEF": Make.JEEP.value,
    "JEEO": Make.JEEP.value,
    "JEEP /": Make.JEEP.value,
    "JEEP": Make.JEEP.value,
    "JEEP/": Make.JEEP.value,
    "JEPP": Make.JEEP.value,
    "JOHN DEE": Make.JOHN_DEERE.value,
    "JOHN DEER": Make.JOHN_DEERE.value,
    "JOHN DEERE": Make.JOHN_DEERE.value,
    "JOHN": Make.JOHN_DEERE.value,
    "JOHND": Make.JOHN_DEERE.value,
    "JOHNDEER": Make.JOHN_DEERE.value,
    "KAWA": Make.KAWASAKI.value,
    "KAWAI": Make.KAWASAKI.value,
    "KAWAK": Make.KAWASAKI.value,
    "KAWAS": Make.KAWASAKI.value,
    "KAWASA": Make.KAWASAKI.value,
    "KAWASAK": Make.KAWASAKI.value,
    "KAWASAKI": Make.KAWASAKI.value,
    "KAWASKI": Make.KAWASAKI.value,
    "KAWI": Make.KAWASAKI.value,
    "KAWK": Make.KAWASAKI.value,
    "KENW": Make.KENWORTH.value,
    "KENWO": Make.KENWORTH.value,
    "KENWOR": Make.KENWORTH.value,
    "KENWORT": Make.KENWORTH.value,
    "KENWORTH": Make.KENWORTH.value,
    "KENWRTH": Make.KENWORTH.value,
    "KIA /": Make.KIA.value,
    "KIA": Make.KIA.value,
    "KIA/": Make.KIA.value,
    "KIO": Make.KIA.value,
    "KIS": Make.KIA.value,
    "LAND ROVER": Make.LAND_ROVER.value,
    "LAND RVR": Make.LAND_ROVER.value,
    "LAND": Make.LAND_ROVER.value,
    "LANDR": Make.LAND_ROVER.value,
    "LANDRO": Make.LAND_ROVER.value,
    "LANDROVE": Make.LAND_ROVER.value,
    "LANDROVER": Make.LAND_ROVER.value,
    "LANDRVR": Make.LAND_ROVER.value,
    "LES": Make.LEXUS.value,
    "LESU": Make.LEXUS.value,
    "LEX": Make.LEXUS.value,
    "LEXAS": Make.LEXUS.value,
    "LEXI": Make.LEXUS.value,
    "LEXIS": Make.LEXUS.value,
    "LEXS /": Make.LEXUS.value,
    "LEXS": Make.LEXUS.value,
    "LEXSS": Make.LEXUS.value,
    "LEXSUS": Make.LEXUS.value,
    "LEXU /": Make.LEXUS.value,
    "LEXU": Make.LEXUS.value,
    "LEXUS": Make.LEXUS.value,
    "LEXUS/": Make.LEXUS.value,
    "LEXUX": Make.LEXUS.value,
    "LEZ": Make.LEXUS.value,
    "LEZUS": Make.LEXUS.value,
    "LICOLN": Make.LINCOLN.value,
    "LIN": Make.LINCOLN.value,
    "LINC /": Make.LINCOLN.value,
    "LINC": Make.LINCOLN.value,
    "LINCL": Make.LINCOLN.value,
    "LINCO": Make.LINCOLN.value,
    "LINCOL": Make.LINCOLN.value,
    "LINCOLN CONTINENTAL": Make.LINCOLN.value,
    "LINCOLN": Make.LINCOLN.value,
    "LINCOLN/": Make.LINCOLN.value,
    "LINCON": Make.LINCOLN.value,
    "LND RVR": Make.LAND_ROVER.value,
    "LNDR": Make.LAND_ROVER.value,
    "LNDRVR": Make.LAND_ROVER.value,
    "LUXUS": Make.LEXUS.value,
    "LXS": Make.LEXUS.value,
    "MACK": Make.MACK.value,
    "MADA": Make.MAZDA.value,
    "MADZA": Make.MAZDA.value,
    "MASE": Make.MASERATI.value,
    "MASER": Make.MASERATI.value,
    "MASERATI": Make.MASERATI.value,
    "MASERATT": Make.MASERATI.value,
    "MASI": Make.MASERATI.value,
    "MAXDA": Make.MAZDA.value,
    "MAZ": Make.MAZDA.value,
    "MAZA": Make.MAZDA.value,
    "MAZAD": Make.MAZDA.value,
    "MAZADA": Make.MAZDA.value,
    "MAZD /": Make.MAZDA.value,
    "MAZD": Make.MAZDA.value,
    "MAZDA /": Make.MAZDA.value,
    "MAZDA 3": Make.MAZDA.value,
    "MAZDA 6": Make.MAZDA.value,
    "MAZDA": Make.MAZDA.value,
    "MAZDA/": Make.MAZDA.value,
    "MAZDZ": Make.MAZDA.value,
    "MAZERATI": Make.MASERATI.value,
    "MERB /": Make.MERCEDES_BENZ.value,
    "MERB": Make.MERCEDES_BENZ.value,
    "MERB.": Make.MERCEDES_BENZ.value,
    "MERB/": Make.MERCEDES_BENZ.value,
    "MERBENZ": Make.MERCEDES_BENZ.value,
    "MERBNZ": Make.MERCEDES_BENZ.value,
    "MERC": Make.MERCURY.value,
    "MERCE": Make.MERCEDES_BENZ.value,
    "MERCED": Make.MERCEDES_BENZ.value,
    "MERCEDE": Make.MERCEDES_BENZ.value,
    "MERCEDES BENZ": Make.MERCEDES_BENZ.value,
    "MERCEDES": Make.MERCEDES_BENZ.value,
    "MERCEDES-BENZ": Make.MERCEDES_BENZ.value,
    "MERCEDEZ": Make.MERCEDES_BENZ.value,
    "MERCEDS": Make.MERCEDES_BENZ.value,
    "MERCU": Make.MERCURY.value,
    "MERCUR": Make.MERCURY.value,
    "MERCURY": Make.MERCURY.value,
    "MERD": Make.MERCURY.value,
    "MERZ /": Make.MERCEDES_BENZ.value,
    "MERZ BNZ": Make.MERCEDES_BENZ.value,
    "MERZ": Make.MERCEDES_BENZ.value,
    "MERZ/": Make.MERCEDES_BENZ.value,
    "MERZB": Make.MERCEDES_BENZ.value,
    "MINI COOPER": Make.MINI.value,
    "MINI": Make.MINI.value,
    "MINN": Make.MINI.value,
    "MINNI": Make.MINI.value,
    "MISCELLANEOUS": Make.NONE.value,
    "MISSAN": Make.NISSAN.value,
    "MIST": Make.MITSUBISHI.value,
    "MISTU": Make.MITSUBISHI.value,
    "MIT": Make.MITSUBISHI.value,
    "MITI": Make.MITSUBISHI.value,
    "MITS /": Make.MITSUBISHI.value,
    "MITS": Make.MITSUBISHI.value,
    "MITS.": Make.MITSUBISHI.value,
    "MITS/": Make.MITSUBISHI.value,
    "MITSH": Make.MITSUBISHI.value,
    "MITSU": Make.MITSUBISHI.value,
    "MITSUB": Make.MITSUBISHI.value,
    "MITSUBI": Make.MITSUBISHI.value,
    "MITSUBIS": Make.MITSUBISHI.value,
    "MITSUBISHI": Make.MITSUBISHI.value,
    "MITT": Make.MITSUBISHI.value,
    "MITTS": Make.MITSUBISHI.value,
    "MITU": Make.MITSUBISHI.value,
    "MITZ": Make.MITSUBISHI.value,
    "MNI": Make.MINI.value,
    "MNICP": Make.MINI.value,
    "MNNI": Make.MINI.value,
    "MZD": Make.MAZDA.value,
    "MZDA": Make.MAZDA.value,
    "N/A": Make.NONE.value,
    "NII": Make.NISSAN.value,
    "NIIS": Make.NISSAN.value,
    "NIISAN": Make.NISSAN.value,
    "NIISS": Make.NISSAN.value,
    "NIISSAN": Make.NISSAN.value,
    "NIS": Make.NISSAN.value,
    "NISA": Make.NISSAN.value,
    "NISAA": Make.NISSAN.value,
    "NISAAN": Make.NISSAN.value,
    "NISAN": Make.NISSAN.value,
    "NISAS": Make.NISSAN.value,
    "NISS /": Make.NISSAN.value,
    "NISS": Make.NISSAN.value,
    "NISS/": Make.NISSAN.value,
    "NISSA N": Make.NISSAN.value,
    "NISSA": Make.NISSAN.value,
    "NISSAM": Make.NISSAN.value,
    "NISSAN /": Make.NISSAN.value,
    "NISSAN": Make.NISSAN.value,
    "NISSAN/": Make.NISSAN.value,
    "NISSANA": Make.NISSAN.value,
    "NISSAN`": Make.NISSAN.value,
    "NISSAS": Make.NISSAN.value,
    "NISSASN": Make.NISSAN.value,
    "NISSI": Make.NISSAN.value,
    "NISSIAN": Make.NISSAN.value,
    "NISSN": Make.NISSAN.value,
    "NISSNA": Make.NISSAN.value,
    "NISSS": Make.NISSAN.value,
    "NISSSAN": Make.NISSAN.value,
    "NOT STATED": Make.NONE.value,
    "ODYSSEY": Make.HONDA.value,
    "OLDS": Make.OLDSMOBILE.value,
    "OLDSM": Make.OLDSMOBILE.value,
    "OLDSMO": Make.OLDSMOBILE.value,
    "OLDSMOBI": Make.OLDSMOBILE.value,
    "OLDSMOBILE": Make.OLDSMOBILE.value,
    "OLS": Make.OLDSMOBILE.value,
    "OTHER - ATV": Make.NONE.value,
    "OTHER - AUTO": Make.NONE.value,
    "OTHER - BUS": Make.NONE.value,
    "OTHER - DOMESTIC": Make.NONE.value,
    "OTHER - MOPED": Make.NONE.value,
    "OTHER - MOTORCYCLE": Make.NONE.value,
    "OTHER - MOTORHOME": Make.NONE.value,
    "OTHER - PICKUP": Make.NONE.value,
    "OTHER - SCHOOL BUS": Make.NONE.value,
    "OTHER - TRUCK": Make.NONE.value,
    "OTHER DOMESTICS": Make.NONE.value,
    "OTHER FOREIGN": Make.NONE.value,
    "OTHER": Make.NONE.value,
    "PETE": Make.PETERBILT.value,
    "PETEBILT": Make.PETERBILT.value,
    "PETER": Make.PETERBILT.value,
    "PETERB": Make.PETERBILT.value,
    "PETERBI": Make.PETERBILT.value,
    "PETERBIL": Make.PETERBILT.value,
    "PETERBILT": Make.PETERBILT.value,
    "PETERBL": Make.PETERBILT.value,
    "PETERBLT": Make.PETERBILT.value,
    "PETERBU": Make.PETERBILT.value,
    "PETERBUI": Make.PETERBILT.value,
    "PETERBUILT": Make.PETERBILT.value,
    "PETERBUL": Make.PETERBILT.value,
    "PETKT": Make.PETERBILT.value,
    "PETR": Make.PETERBILT.value,
    "PETRB": Make.PETERBILT.value,
    "PETRBILT": Make.PETERBILT.value,
    "PETRBLT": Make.PETERBILT.value,
    "PLY": Make.PLYMOUTH.value,
    "PLYM": Make.PLYMOUTH.value,
    "PLYMO": Make.PLYMOUTH.value,
    "PLYMOTH": Make.PLYMOUTH.value,
    "PLYMOU": Make.PLYMOUTH.value,
    "PLYMOUTH": Make.PLYMOUTH.value,
    "PONI": Make.PONTIAC.value,
    "PONIT": Make.PONTIAC.value,
    "PONITAC": Make.PONTIAC.value,
    "PONT": Make.PONTIAC.value,
    "PONTAIC": Make.PONTIAC.value,
    "PONTI": Make.PONTIAC.value,
    "PONTIA": Make.PONTIAC.value,
    "PONTIAC": Make.PONTIAC.value,
    "PONTIAC/": Make.PONTIAC.value,
    "PONTIC": Make.PONTIAC.value,
    "POR": Make.PORSCHE.value,
    "PORC": Make.PORSCHE.value,
    "PORCH": Make.PORSCHE.value,
    "PORCHE": Make.PORSCHE.value,
    "PORS": Make.PORSCHE.value,
    "PORSC": Make.PORSCHE.value,
    "PORSCE": Make.PORSCHE.value,
    "PORSCH": Make.PORSCHE.value,
    "PORSCHE": Make.PORSCHE.value,
    "PORSCHE/": Make.PORSCHE.value,
    "PORSE": Make.PORSCHE.value,
    "PORSH": Make.PORSCHE.value,
    "PORSHE": Make.PORSCHE.value,
    "PRIUS": Make.TOYOTA.value,
    "PRTB": Make.PETERBILT.value,
    "PTB": Make.PETERBILT.value,
    "PTBL": Make.PETERBILT.value,
    "PTBLT": Make.PETERBILT.value,
    "PTBR": Make.PETERBILT.value,
    "PTBT": Make.PETERBILT.value,
    "PTE": Make.PETERBILT.value,
    "PTER": Make.PETERBILT.value,
    "PTR": Make.PETERBILT.value,
    "PTRB /": Make.PETERBILT.value,
    "PTRB": Make.PETERBILT.value,
    "PTRB/": Make.PETERBILT.value,
    "PTRBILT": Make.PETERBILT.value,
    "PTRBL": Make.PETERBILT.value,
    "PTRBLT": Make.PETERBILT.value,
    "PTRBT": Make.PETERBILT.value,
    "PTRBUILT": Make.PETERBILT.value,
    "RAD CITY": Make.RADPOWER.value,
    "RAD POWE": Make.RADPOWER.value,
    "RAD": Make.RADPOWER.value,
    "RADPOWER": Make.RADPOWER.value,
    "RADROVER": Make.RADPOWER.value,
    "RAM 2500": Make.RAM.value,
    "RAM": Make.RAM.value,
    "RAM/": Make.RAM.value,
    "RAN": Make.RAM.value,
    "RANG": Make.LAND_ROVER.value,
    "RANGE RO": Make.LAND_ROVER.value,
    "RANGE ROVER": Make.LAND_ROVER.value,
    "RANGE RV": Make.LAND_ROVER.value,
    "RANGE": Make.LAND_ROVER.value,
    "RANGER": Make.LAND_ROVER.value,
    "RANGEROV": Make.LAND_ROVER.value,
    "RNG ROVR": Make.LAND_ROVER.value,
    "RNG RVR": Make.LAND_ROVER.value,
    "RNGRV": Make.LAND_ROVER.value,
    "RNGRVR": Make.LAND_ROVER.value,
    "RORD": Make.FORD.value,
    "ROVER": Make.LAND_ROVER.value,
    "SAAB": Make.SAAB.value,
    "SATN": Make.SATURN.value,
    "SATR": Make.SATURN.value,
    "SATRN": Make.SATURN.value,
    "SATRU": Make.SATURN.value,
    "SATRUN": Make.SATURN.value,
    "SATU": Make.SATURN.value,
    "SATUN": Make.SATURN.value,
    "SATUR": Make.SATURN.value,
    "SATURN": Make.SATURN.value,
    "SATURN/": Make.SATURN.value,
    "SATY": Make.SATURN.value,
    "SCHW": Make.SCHWINN.value,
    "SCHWIN": Make.SCHWINN.value,
    "SCHWINN": Make.SCHWINN.value,
    "SCHWYNN": Make.SCHWINN.value,
    "SCIO": Make.SCION.value,
    "SCIOIN": Make.SCION.value,
    "SCION": Make.SCION.value,
    "SCOIN": Make.SCION.value,
    "SCWHINN": Make.SCHWINN.value,
    "SCWINN": Make.SCHWINN.value,
    "SHWIN": Make.SCHWINN.value,
    "SHWINN": Make.SCHWINN.value,
    "SMAR": Make.SMART.value,
    "SMART": Make.SMART.value,
    "STERLI": Make.STERLING.value,
    "STERLIN": Make.STERLING.value,
    "STERLING": Make.STERLING.value,
    "STRN /": Make.SATURN.value,
    "STRN": Make.SATURN.value,
    "STURN": Make.SATURN.value,
    "SUB": Make.SUBARU.value,
    "SUBA /": Make.SUBARU.value,
    "SUBA": Make.SUBARU.value,
    "SUBAR": Make.SUBARU.value,
    "SUBARA": Make.SUBARU.value,
    "SUBARAU": Make.SUBARU.value,
    "SUBARI": Make.SUBARU.value,
    "SUBARU": Make.SUBARU.value,
    "SUBARU/": Make.SUBARU.value,
    "SUBARY": Make.SUBARU.value,
    "SUBI": Make.SUBARU.value,
    "SUBN": Make.SUBARU.value,
    "SUBR": Make.SUBARU.value,
    "SUBRA": Make.SUBARU.value,
    "SUBRARU": Make.SUBARU.value,
    "SUBRAU": Make.SUBARU.value,
    "SUBRU": Make.SUBARU.value,
    "SUBU": Make.SUBARU.value,
    "SUBUARU": Make.SUBARU.value,
    "SUBUR": Make.SUBARU.value,
    "SUBURA": Make.SUBARU.value,
    "SUBURU": Make.SUBARU.value,
    "SUS": Make.SUZUKI.value,
    "SUSUKI": Make.SUZUKI.value,
    "SUV": Make.NONE.value,
    "SUZ": Make.SUZUKI.value,
    "SUZI": Make.SUZUKI.value,
    "SUZIKI": Make.SUZUKI.value,
    "SUZK": Make.SUZUKI.value,
    "SUZKI": Make.SUZUKI.value,
    "SUZU /": Make.SUZUKI.value,
    "SUZU": Make.SUZUKI.value,
    "SUZUK": Make.SUZUKI.value,
    "SUZUKI MC": Make.SUZUKI.value,
    "SUZUKI": Make.SUZUKI.value,
    "SUZUKI/": Make.SUZUKI.value,
    "T0Y": Make.TOYOTA.value,
    "T0YOTA": Make.TOYOTA.value,
    "TAHOE": Make.GMC.value,
    "TAOTA": Make.TOYOTA.value,
    "TAOTAO": Make.TOYOTA.value,
    "TESL": Make.TESLA.value,
    "TESLA MOTORS": Make.TESLA.value,
    "TESLA": Make.TESLA.value,
    "TESLA/": Make.TESLA.value,
    "THOM": Make.THOMAS.value,
    "THOMA": Make.THOMAS.value,
    "THOMAS (BUS)": Make.THOMAS.value,
    "THOMAS B": Make.THOMAS.value,
    "THOMAS": Make.THOMAS.value,
    "TOT": Make.TOYOTA.value,
    "TOTA": Make.TOYOTA.value,
    "TOTO": Make.TOYOTA.value,
    "TOTOTA": Make.TOYOTA.value,
    "TOTOYA": Make.TOYOTA.value,
    "TOTOYTA": Make.TOYOTA.value,
    "TOTY": Make.TOYOTA.value,
    "TOTYOA": Make.TOYOTA.value,
    "TOTYOTA": Make.TOYOTA.value,
    "TOY": Make.TOYOTA.value,
    "TOY/SCIO": Make.TOYOTA.value,
    "TOY0": Make.TOYOTA.value,
    "TOY0TA": Make.TOYOTA.value,
    "TOYA": Make.TOYOTA.value,
    "TOYAT": Make.TOYOTA.value,
    "TOYATA": Make.TOYOTA.value,
    "TOYI": Make.TOYOTA.value,
    "TOYO /": Make.TOYOTA.value,
    "TOYO": Make.TOYOTA.value,
    "TOYO/": Make.TOYOTA.value,
    "TOYO/SCI": Make.TOYOTA.value,
    "TOYOA": Make.TOYOTA.value,
    "TOYOAT": Make.TOYOTA.value,
    "TOYORA": Make.TOYOTA.value,
    "TOYOT": Make.TOYOTA.value,
    "TOYOTA": Make.TOYOTA.value,
    "TOYOTA/": Make.TOYOTA.value,
    "TOYOTAS": Make.TOYOTA.value,
    "TOYOTA`": Make.TOYOTA.value,
    "TOYOTO": Make.TOYOTA.value,
    "TOYOTOA": Make.TOYOTA.value,
    "TOYOTR": Make.TOYOTA.value,
    "TOYOTRA": Make.TOYOTA.value,
    "TOYOTS": Make.TOYOTA.value,
    "TOYOTYA": Make.TOYOTA.value,
    "TOYOY": Make.TOYOTA.value,
    "TOYOYA": Make.TOYOTA.value,
    "TOYOYTA": Make.TOYOTA.value,
    "TOYO`": Make.TOYOTA.value,
    "TOYR": Make.TOYOTA.value,
    "TOYT /": Make.TOYOTA.value,
    "TOYT": Make.TOYOTA.value,
    "TOYT.": Make.TOYOTA.value,
    "TOYT/": Make.TOYOTA.value,
    "TOYT/SCI": Make.TOYOTA.value,
    "TOYTA": Make.TOYOTA.value,
    "TOYTO": Make.TOYOTA.value,
    "TOYTOA": Make.TOYOTA.value,
    "TOYTOTA": Make.TOYOTA.value,
    "TOYTT": Make.TOYOTA.value,
    "TOYY": Make.TOYOTA.value,
    "TREC": Make.TREK.value,
    "TRECK": Make.TREK.value,
    "TREK": Make.TREK.value,
    "TREK.value, INC.": Make.TREK.value,
    "TRIPH": Make.TRIUMPH.value,
    "TRIU": Make.TRIUMPH.value,
    "TRIUM": Make.TRIUMPH.value,
    "TRIUMP": Make.TRIUMPH.value,
    "TRIUMPH": Make.TRIUMPH.value,
    "TRIUPH": Make.TRIUMPH.value,
    "TRUIMPH": Make.TRIUMPH.value,
    "TRUM": Make.TRIUMPH.value,
    "TSLA": Make.TESLA.value,
    "TSMR": Make.TESLA.value,
    "TUNDRA": Make.TOYOTA.value,
    "TYOT": Make.TOYOTA.value,
    "TYOTA": Make.TOYOTA.value,
    "UBER": Make.NONE.value,
    "UKN": Make.NONE.value,
    "UKNONWN": Make.NONE.value,
    "UKNOWN": Make.NONE.value,
    "UNK /": Make.NONE.value,
    "UNK": Make.NONE.value,
    "UNK.": Make.NONE.value,
    "UNK/": Make.NONE.value,
    "UNKN": Make.NONE.value,
    "UNKN/": Make.NONE.value,
    "UNKNONW": Make.NONE.value,
    "UNKNOW": Make.NONE.value,
    "UNKNOWN": Make.NONE.value,
    "UNKNOWN/": Make.NONE.value,
    "UNKNWN": Make.NONE.value,
    "UNKNWON": Make.NONE.value,
    "UNKOWN": Make.NONE.value,
    "UNKWN": Make.NONE.value,
    "UNNKNOWN": Make.NONE.value,
    "UNNOWN": Make.NONE.value,
    "V & W": Make.VOLKSWAGEN.value,
    "V W": Make.VOLKSWAGEN.value,
    "V.W.": Make.VOLKSWAGEN.value,
    "V/W": Make.VOLKSWAGEN.value,
    "VESP": Make.VESPA.value,
    "VESPA": Make.VESPA.value,
    "VOK": Make.VOLKSWAGEN.value,
    "VOKS": Make.VOLKSWAGEN.value,
    "VOLCO": Make.VOLVO.value,
    "VOLK /": Make.VOLKSWAGEN.value,
    "VOLK": Make.VOLKSWAGEN.value,
    "VOLK/": Make.VOLKSWAGEN.value,
    "VOLKD": Make.VOLKSWAGEN.value,
    "VOLKL": Make.VOLKSWAGEN.value,
    "VOLKS": Make.VOLKSWAGEN.value,
    "VOLKS/": Make.VOLKSWAGEN.value,
    "VOLKSW": Make.VOLKSWAGEN.value,
    "VOLKSWA": Make.VOLKSWAGEN.value,
    "VOLKSWAG": Make.VOLKSWAGEN.value,
    "VOLKSWAGEN": Make.VOLKSWAGEN.value,
    "VOLKSWAGON": Make.VOLKSWAGEN.value,
    "VOLKSWGN": Make.VOLKSWAGEN.value,
    "VOLKS`": Make.VOLKSWAGEN.value,
    "VOLKW": Make.VOLKSWAGEN.value,
    "VOLKWA": Make.VOLKSWAGEN.value,
    "VOLKWAGE": Make.VOLKSWAGEN.value,
    "VOLKWGN": Make.VOLKSWAGEN.value,
    "VOLLK": Make.VOLKSWAGEN.value,
    "VOLLKS": Make.VOLKSWAGEN.value,
    "VOLO": Make.VOLVO.value,
    "VOLOV": Make.VOLVO.value,
    "VOLOVO": Make.VOLVO.value,
    "VOLS": Make.VOLKSWAGEN.value,
    "VOLSWAGE": Make.VOLKSWAGEN.value,
    "VOLSWGN": Make.VOLKSWAGEN.value,
    "VOLV /": Make.VOLVO.value,
    "VOLV": Make.VOLVO.value,
    "VOLV0": Make.VOLVO.value,
    "VOLVA": Make.VOLVO.value,
    "VOLVE": Make.VOLVO.value,
    "VOLVL": Make.VOLVO.value,
    "VOLVO": Make.VOLVO.value,
    "VOLVO/": Make.VOLVO.value,
    "VOLW": Make.VOLKSWAGEN.value,
    "VOLX": Make.VOLKSWAGEN.value,
    "VOVL": Make.VOLVO.value,
    "VOVLO": Make.VOLVO.value,
    "VOVLVO": Make.VOLVO.value,
    "VOVO": Make.VOLVO.value,
    "VOYAGER": Make.PLYMOUTH.value,
    "VW": Make.VOLKSWAGEN.value,
    "WHITE GMC": Make.GMC.value,
    "WHITE VOLVO": Make.VOLVO.value,
    "WHITE": Make.WHITE.value,
    "WHITEGMC": Make.GMC.value,
    "WINN": Make.WINNEBAGO.value,
    "WINNE": Make.WINNEBAGO.value,
    "WINNEBAG": Make.WINNEBAGO.value,
    "WINNEBAGO": Make.WINNEBAGO.value,
    "WINNI": Make.WINNEBAGO.value,
    "WNBG": Make.WINNEBAGO.value,
    "WNBGO": Make.WINNEBAGO.value,
    "YAH": Make.YAMAHA.value,
    "YAHA": Make.YAMAHA.value,
    "YAHAMA": Make.YAMAHA.value,
    "YAHMA": Make.YAMAHA.value,
    "YAM": Make.YAMAHA.value,
    "YAMA": Make.YAMAHA.value,
    "YAMAH": Make.YAMAHA.value,
    "YAMAHA": Make.YAMAHA.value,
    "YAMAMA": Make.YAMAHA.value,
    "YAMH": Make.YAMAHA.value,
    "________": Make.NONE.value,
}
