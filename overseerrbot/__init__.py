import ast
import logging
from configparser import ConfigParser
from logging.handlers import TimedRotatingFileHandler

from overseerrbot.bot import OverseerrBot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        TimedRotatingFileHandler('logs/overseerrbot.log', when="midnight", encoding=None,
                                 delay=False, backupCount=10),
        logging.StreamHandler()
    ]
)
LOGS = logging.getLogger(__name__)

__author__ = 'Athfan Khaleel'

OverseerrBot = OverseerrBot()

config = ConfigParser()
config.read('config.ini')

# Get from config file.
ADMINS = ast.literal_eval(config.get('overseerrbot', 'admins'))
# LOG_GROUP = config.get('overseerrbot', 'log_group')

client = None

