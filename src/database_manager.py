# Copyright (c) 2023 tejaromalius
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import getpass
import logging as log
import os
import os.path as Path
import subprocess
import sys

class DatabaseManager:
    def __init__(self, CYPHER):
        self.database = None
        self.cypher = CYPHER

    def setupDatabase(self):
        while True:
            self.cypher.setPassword(getpass.getpass(prompt="Please enter new master password: "))
            if self.cypher.getPassword() != getpass.getpass(prompt="Please enter new master password (confirmation): "):
                log.warning("entered passwords do not match.")
                continue
            break
        self.cypher.encrypt()
        self.__updateDatabase()

    def loadDatabase(self):
        log.debug("loading the database.")
        chances = 4
        while True:    
            if chances == 0:
                log.critical("password was wrong multiple times. exiting the program.")
                sys.exit(1)
            self.cypher.setPassword(getpass.getpass(prompt="Please enter master password: "))
            try:
                self.cypher.decrypt()
                break
            except Exception:
                chances -= 1
                log.warning(f"passwords is not correct. ({chances} entries left).")
                continue
        self.__updateDatabase()

    def displayDatabase(self):
        process = subprocess.Popen(["less"], stdin=subprocess.PIPE)
        output = "\n".join(f"({ind}) {pair[0]} : {pair[1]}"for ind, pair in enumerate(self.database.items()))
        log.debug("process and pipe are prepared to display.")
        process.communicate(output.encode("utf-8"))

    def appendEntry(self):
        log.debug("registering a new entry..")

        while True:
            service_name = input("\nPlease enter service name: ")
            if service_name == "":
                log.debug("no service name provided. returning to menu.")
                return
            elif self.database.get(service_name, False):
                log.warning("service already exists.")
                continue
            else:
                break
        
        while True:
            service_password = getpass.getpass(prompt="Please enter service password: ")
            if service_password == getpass.getpass(prompt="Please enter service password (confirmation): "):
                self.database[service_name] = service_password
                log.info("entry appended to the database.")
                self.cypher.setContent(self.database)
                self.cypher.encrypt()
                break
            else:
                log.warning("passwords do not match. try again.")
                continue
        
    def deleteEntry(self):
        log.debug("deleting an entry..")
        while True:
            service_name = input("\nPlease enter service name: ")
            if service_name == "":
                log.debug("no service name provided. returning to menu.")
                break
            elif service_name not in self.database.keys():
                log.warning("service not found in database. try again.")
                continue

            if getpass.getpass(prompt="Please enter master password: ") == self.cypher.getPassword():
                self.database.pop(service_name)
                log.info("entry removed from the database.")
                self.cypher.setContent(self.database)
                self.cypher.encrypt()
                break
            else:
                log.warning("entered password is incorrect. try again.")
                continue
    
    def __updateDatabase(self):
        self.database = self.cypher.getContent()
        log.debug("database updated from file.")