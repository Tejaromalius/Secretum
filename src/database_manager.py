# Copyright (c) 2023 tejaromalius
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import getpass
import logging as log
import os
import os.path as Path
import sys

class DatabaseManager:
    def __init__(self, CYPHER):
        self.database = None
        self.cypher = CYPHER

    def setupDatabase(self):
        while True:
            self.cypher.setPassword(getpass.getpass(prompt="Please enter new password: "))
            if self.cypher.getPassword() != getpass.getpass(prompt="Please enter new password (confirmation): "):
                log.warning(f"password do not match. ({chances} entries left).")
                continue
            break

        self.cypher.encrypt()
        self.__updateDatabase()

    def loadDatabase(self):
        chances = 4
        while True:    
            if chances == 0:
                log.critical("password was wrong multiple times. exiting the program.")
                sys.exit(1)

            self.cypher.setPassword(getpass.getpass(prompt="Please enter password: "))  
                
            try:
                self.cypher.decrypt()
                break

            except Exception:
                chances -= 1
                log.warning(f"passwords is not correct. ({chances} entries left).")
                continue

        self.__updateDatabase()

    def appendNewEntry(self):
        service_name = input("\nPlease enter service name: ")

        while True:
            service_password = getpass.getpass(prompt="Please enter service password: ")

            if service_password == getpass.getpass(prompt="Please enter service password (confirmation): "):
                self.database[service_name] = service_password
                self.cypher.setContent(self.database)
                self.cypher.encrypt()
                break
            else:
                log.warning("passwords do not match. try again.")
                continue
    
    def __updateDatabase(self):
        self.database = self.cypher.getContent()