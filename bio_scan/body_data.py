class BodyData:
    def __init__(self, name):
        self.name: str = name
        self.type: str = ""
        self.id: int = -1
        self.atmosphere: str = ""
        self.volcanism: str = ""
        self.distance: float = 0.0
        self.gravity: float = 0.0
        self.temp: float = 0.0
        self.bio_signals: int = 0
        self.flora: dict[str, tuple[str, int]] = {}
        self.mapped: bool = False

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def set_type(self, value: str):
        self.type = value
        return self

    def get_id(self):
        return self.id

    def set_id(self, value: int):
        self.id = value
        return self

    def get_atmosphere(self):
        return self.atmosphere

    def set_atmosphere(self, value: str):
        self.atmosphere = value
        return self

    def get_volcanism(self):
        return self.volcanism

    def set_volcanism(self, value: int):
        self.volcanism = value
        return self

    def get_distance(self):
        return self.distance

    def set_distance(self, value: float):
        self.distance = value
        return self

    def get_gravity(self):
        return self.gravity

    def set_gravity(self, value: float):
        self.gravity = value
        return self

    def get_temp(self):
        return self.temp

    def set_temp(self, value: float):
        self.temp = value
        return self

    def get_bio_signals(self):
        return self.bio_signals

    def set_bio_signals(self, value: int):
        self.bio_signals = value
        return self

    def get_flora(self, genus: str = None):
        if genus:
            if genus in self.flora:
                return self.flora[genus]
            else:
                return None
        return self.flora

    def add_flora(self, genus: str, species: str = ""):
        scan = 0
        if genus in self.flora:
            scan = self.flora[genus][1]
        self.flora[genus] = (species, scan)
        return self

    def set_flora(self, genus: str, species: str, scan: int):
        self.flora[genus] = (species, scan)
        return self

    def clear_flora(self):
        self.flora = {}
        return self

    def is_mapped(self):
        return self.mapped

    def set_mapped(self, value: bool):
        self.mapped = value
        return self

def get_body_shorthand(type: str):
    match type:
        case 'Icy body':
            return " (I)"
        case 'Rocky body':
            return " (R)"
        case 'Rocky ice body':
            return " (RI)"
        case 'Metal rich body':
            return " (M)"
        case 'High metal content body':
            return " (HMC)"
        case _:
            return ''