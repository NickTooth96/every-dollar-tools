import json



class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        try:
            settings = json.load(open("utillities/settings.json", "r"))
        except FileNotFoundError:
            settings = {}
        self.DEBUG = settings.get("DEBUG", False)
        self.LOG_LEVEL = settings.get("LOG_LEVEL", 4)
        self.ACCOUNT_ZERO = settings.get("ACCOUNT_ZERO", 0.00)
        self.BASE_ACCOUNT = settings.get("BASE_ACCOUNT", "")
        self.ACCOUNT_MAP = settings.get("ACCOUNT_MAP", {})
        self.ACCOUNTS = {k.lower() for k in self.ACCOUNT_MAP.keys()}
        self._initialized = True
        
    def set_debug(self, debug_value: bool):
        self.DEBUG = debug_value
    
    def set_log_level(self, log_level_value: int):
        if log_level_value > 4:
            print(ValueError)
        else:
            self.LOG_LEVEL = log_level_value
    
    def set_account_zero(self, account_zero_value: float):
        self.ACCOUNT_ZERO = account_zero_value
    
    def set_base_account(self, base_account_value: str):
        self.BASE_ACCOUNT = base_account_value
    
    def set_account_map(self, account_map_value: dict):
        self.ACCOUNT_MAP = account_map_value
        self.ACCOUNTS = {k.lower() for k in self.ACCOUNT_MAP.keys()}
                
    def custom_settings(self, settings_file_path):
        # log_msg(f"Loading custom settings from {settings_file_path}", Level.INFO)
        try:
            custom_settings = json.load(open(settings_file_path, "r"))
        except FileNotFoundError:
            print(f"File not found: {settings_file_path}")
            return
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {settings_file_path}")
            return

        # log_msg(f"Custom settings loaded: {custom_settings}", Level.INFO)
        self.set_account_map(custom_settings.get("ACCOUNT_MAP", self.ACCOUNT_MAP))
        self.set_account_zero(custom_settings.get("ACCOUNT_ZERO", self.ACCOUNT_ZERO))
        self.set_base_account(custom_settings.get("BASE_ACCOUNT", self.BASE_ACCOUNT))
        self.set_debug(custom_settings.get("DEBUG", self.DEBUG))
        self.set_log_level(custom_settings.get("LOG_LEVEL", self.LOG_LEVEL))