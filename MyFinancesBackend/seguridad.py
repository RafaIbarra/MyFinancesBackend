from dotenv import load_dotenv
import os
from dataclasses import dataclass
load_dotenv()
@dataclass
class ConfiguracionDB:
    PASS : str 
    USER : str
    NAME : str
    DIR_EMAIL :str
    PASS_EMAIL : str
    LOCAL_ALLOW_HOST:str
    
pass_db = os.getenv('DB_PASS')
user_db = os.getenv('DB_USER')
name_db = os.getenv('DB_NAME')

mail=os.getenv('DIR_EMAIL')
mailpass=os.getenv('PASS_EMAIL')
allowhost=os.getenv('LOCAL_ALLOW_HOST')

configuracion=ConfiguracionDB(PASS=pass_db,
                               USER=user_db, 
                               NAME=name_db,
                               DIR_EMAIL=mail,
                               PASS_EMAIL=mailpass,
                               LOCAL_ALLOW_HOST=allowhost
                               )

