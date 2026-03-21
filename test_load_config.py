from pprint import pprint

from src.turboprint_logger import ConfigManager, get_logger

config = ConfigManager().load_file("./config.json")

root_logger = get_logger()
app_logger = get_logger("app")
app_api_logger = get_logger("app.api")

pprint(repr(root_logger))
print()
pprint(repr(app_logger))
print()
pprint(repr(app_api_logger))
