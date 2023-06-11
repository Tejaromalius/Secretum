# Copyright (c) 2023 tejaromalius
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
import logging as log
import os
import subprocess
import sys

class Interface:
    def __init__(self, DB_MANAGER, CYPHER):
        self.db_manager = DB_MANAGER
        self.cypher = CYPHER
    
    def run(self):
        while True:
            self.__displayMenu()

    def __displayMenu(self):
        os.system("clear")
        print("\t1) Display passwords\n\t2) Register new password\n\t3) Delete password\n\t4) Exit\n")
        selected_display = None

        while selected_display not in (1, 2, 3, 4):
            try:
                selected_display = int(input("> "))
            except Exception:
                continue
        
        self.__callSelected(selected_display)
    
    def __callSelected(self, SELECTION):
        if SELECTION == 1:
            self.db_manager.displayDatabase()
        elif SELECTION == 2:
            self.db_manager.appendEntry()
        elif SELECTION == 3:
            self.db_manager.deleteEntry()
        else:
            sys.exit(0)