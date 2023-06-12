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
    def __init__(self, DB_MANAGER):
        self.db_manager = DB_MANAGER
    
    def run(self):
        log.info("UI loop initiated.")
        while True:
            self.__displayMenu()

    def __displayMenu(self):
        print("Select an option:\n\t1) Display passwords\n\t2) Register new password\n\t3) Delete password\n\t4) Exit\n")
        selected_option = None
        while selected_option not in (1, 2, 3, 4):
            try:
                selected_option = int(input("> "))
                break
            except Exception:
                pass
            log.warning("selected option is invalid.")

        self.__callSelected(selected_option)
    
    def __callSelected(self, SELECTION):
        if SELECTION == 1:
            self.db_manager.displayDatabase()
            log.debug("returning to menu.")
        elif SELECTION == 2:
            self.db_manager.appendEntry()
            log.debug("returning to menu.")
        elif SELECTION == 3:
            self.db_manager.deleteEntry()
            log.debug("returning to menu.")
        else:
            log.info("exiting the program safely.")
            sys.exit(0)