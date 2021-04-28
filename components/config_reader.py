import json

class ConfigReader:
    def __init__(self):
      self.config_settings = {}
      self.config_file_path = ""

    def load_config_from_file(self, configfilepath):
        """Reads config values from .json file
        Input:
            configfilepath: file path to the config.json file

        Returns:
            json dictionary: dictionary parsed from json containing config values
        """
        # loads config from .json file
        f = open(configfilepath)
        config_values = json.load(f)
        

        f.close()
        self.config_file_path = configfilepath
        self.config_values = config_values
        return config_values


    
        


if __name__ == "__main__":

    # Tests

    # Test 1 - read config file and pring values
    config_file_path = "config.json"
    cf = ConfigReader()

    config_values = cf.load_config_from_file(config_file_path)
    print(config_values)
    for i in config_values:
            print(i)
    
    # Test 2 - 
