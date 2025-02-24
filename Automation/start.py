import os
from API.config import config

print(f'POSIP : {config.Config_machine_ip()} || POSPORT : {config.Config_Indoor_port()} || REQUEST FORMAT : {config.request_format()}')
os.system("python manage.py runserver")