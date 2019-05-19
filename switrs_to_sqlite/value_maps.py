MOVEMENT_PRECEDING = {
    "A": "stopped",
    "B": "proceeding straight",
    "C": "ran off road",
    "D": "making right turn",
    "E": "making left turn",
    "F": "making u-turn",
    "G": "backing",
    "H": "slowing/stopping",
    "I": "passing other vehicle",
    "J": "changing lanes",
    "K": "parking maneuver",
    "L": "entering traffic",
    "M": "other unsafe turning",
    "N": "crossed into opposing lane",
    "O": "parked",
    "P": "merging",
    "Q": "traveling wrong way",
    "R": "other",
}

STATEWIDE_VEHICLE_TYPE = {
    "A": "passenger car",
    "B": "passenger car with trailer",
    "C": "motorcycle or scooter",
    "D": "pickup or panel truck",
    "E": "pickup or panel truck with trailer",
    "F": "truck or truck tractor",
    "G": "truck or truck tractor with trailer",
    "H": "schoolbus",
    "I": "other bus",
    "J": "emergency vehicle",
    "K": "highway construction equipment",
    "L": "bicycle",
    "M": "other vehicle",
    "N": "pedestrian",
    "O": "moped",
}

DEGREE_OF_INJURY = {
    "0": "no injury",
    "1": "killed",
    "2": "severe injury",
    "3": "other visible injury",
    "4": "complaint of pain",
}

PARTY_TYPE = {
    "1": "driver",
    "2": "pedestrian",
    "3": "parked vehicle",
    "4": "bicyclist",
    "5": "other",
}

SEX = {
    "M": "male",
    "F": "female",
}

WEATHER = {
    "A": "clear",
    "B": "cloudy",
    "C": "raining",
    "D": "snowing",
    "E": "fog",
    "F": "other",
    "G": "wind",
}

CHP_BEAT_TYPE = {
    "0": "not chp",
    "1": "interstate",
    "2": "us highway",
    "3": "state route",
    "4": "county road line",
    "5": "county road area",
    "6": "us highway",
    "7": "state route",
    "8": "county road line",
    "9": "county road area",
    "10": "safety services program",
    "S": "safety services program",
    "11": "administrative",
    "A": "administrative",
}

COLLISION_TYPE = {
    "A": "head-on",
    "B": "sideswipe",
    "C": "rear end",
    "D": "broadside",
    "E": "hit object",
    "F": "overturned",
    "G": "pedestrian",
    "H": "other",
}

INVOLVED_WITH = {
    "A": "non-collision",
    "B": "pedestrian",
    "C": "other motor vehicle",
    "D": "motor vehicle on other roadway",
    "E": "parked motor vehicle",
    "F": "train",
    "G": "bicycle",
    "H": "animal",
    "I": "fixed object",
    "J": "other object",
}

PEDESTRIAN_ACTION = {
    "A": "no pedestrian involved",
    "B": "crossing in intersection crosswalk",
    "C": "crossing non-intersection crosswalk",
    "D": "crossing not in crosswalk",
    "E": "in road",
    "F": "not in road",
    "G": "using school bus",
}

DIRECTION = {
    "N": "north",
    "E": "east",
    "S": "south",
    "W": "west",
}

LOCATION_TYPE = {
    "H": "highway",
    "I": "intersection",
    "R": "ramp",
}

CHP_BEAT_CLASS = {
    "1": "chp primary",
    "2": "chp other",
    "0": "not chp",
}

HIT_AND_RUN = {
    "F": "felony",
    "M": "misdemeanor",
    "N": "not hit and run",
}

ROAD_SURFACE = {
    "A": "dry",
    "B": "wet",
    "C": "snowy",
    "D": "slippery",
}

ROAD_CONDITION = {
    "A": "holes",
    "B": "loose material",
    "C": "obstruction",
    "D": "construction",
    "E": "reduced width",
    "F": "flooded",
    "G": "other",
    "H": "normal",
}

LIGHTING = {
    "A": "daylight",
    "B": "dusk or dawn",
    "C": "dark with street lights",
    "D": "dark with no street lights",
    "E": "dark with street lights not functioning",
}

CONTROL_DEVICE = {
    "A": "functioning",
    "B": "not functioning",
    "C": "obscured",
    "D": "none",
}

SIDE_OF_HIGHWAY = {
    "N": "northbound",
    "S": "southbound",
    "E": "eastbound",
    "W": "westbound",
}

PRIMARY_COLLISION_FACTOR = {
    "A": "vehicle code violation",
    "B": "other improper driving",
    "C": "other than driver",
    "D": "unknown",
    "E": "fell asleep",
}

PCF_VIOLATION_CODE = {
    "B": "business",
    "C": "vehicle",
    "H": "city health",
    "I": "city ordinance",
    "O": "county ordinance",
    "P": "penal",
    "S": "streets",
    "W": "welfare",
}

RACE = {
    "A": "asian",
    "B": "black",
    "H": "hispanic",
    "O": "other",
    "W": "white",
}

COLLISION_SEVERITY = {
    "0": "property damage only",
    "1": "fatal",
    "2": "severe injury",
    "3": "other injury",
    "4": "pain",
}

PCF_VIOLATION_CATEGORY = {
    "00": "unknown",
    "01": "dui",
    "02": "impeding traffic",
    "03": "speeding",
    "04": "following too closely",
    "05": "wrong side of road",
    "06": "improper passing",
    "07": "unsafe lane change",
    "08": "improper turning",
    "09": "automobile right of way",
    "10": "pedestrian right of way",
    "11": "pedestrian violation",
    "12": "traffic signals and signs",
    "13": "hazardous parking",
    "14": "lights",
    "15": "brakes",
    "16": "other equipment",
    "17": "other hazardous violation",
    "18": "other than driver (or pedestrian)",
    "21": "unsafe starting or backing",
    "22": "other improper driving",
    "23": "pedestrian dui",
    "24": "fell asleep",
}

