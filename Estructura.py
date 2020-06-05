class Estructura:
    # Initializer / Instance Attributes
    def __init__(self):
        self.compiler = {}
        self.characters = {}
        self.keywords = {}
        self.tokens = {}
        self.productions  = {}
        self.end = {}

    def add_component(self, dic, key, value):
        self.dic[key] = value
    
    def get_value(self, dic, key):
        return self.dic[key]