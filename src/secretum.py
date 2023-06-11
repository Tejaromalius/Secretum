# Copyright (c) 2023 tejaromalius
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import getpass
import logging as log
import os
import os.path as Path
import sys

from cypher import Cypher
from database_manager import DatabaseManager
from interface import Interface

log.basicConfig(level = log.CRITICAL, datefmt = "%H:%M:%S", format = "%(asctime)s.%(msecs)02d -- %(levelname)s: %(message)s")
database_path = f"/home/{os.getlogin()}/.config/Secretum/encrypted.db"

if __name__ == "__main__":
    os.system("clear")

    cypher = Cypher(database_path)
    db_manager = DatabaseManager(cypher)
    interface = Interface(db_manager, cypher)
   
    if Path.exists(database_path):
        log.debug("database exists")
        db_manager.loadDatabase()
    else:
        log.debug("database doesn't exist")
        db_manager.setupDatabase()
    
    interface.run()