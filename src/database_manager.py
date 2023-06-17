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

from time import sleep

class DatabaseManager:
    def __init__(self, CYPHER):
        self.database = None
        self.cypher = CYPHER

    def setupDatabase(self):
        while not self.cypher.setPassword(getpass.getpass(prompt="Please enter new master password: ")) and self.cypher.getPassword() != getpass.getpass(prompt="Please enter new master password (confirmation): "):
            sleep(1.5)
            log.warning("entered passwords do not match.")
            print("entered passwords do not match.")

        self.cypher.encrypt()
        self.__updateDatabase()

    def loadDatabase(self):
        log.debug("loading the database.")
        chances = 4
        while chances != 0:
            try:
                self.cypher.setPassword(getpass.getpass(prompt="Please enter master password: "))
                self.cypher.decrypt()
                break
            except Exception:
                sleep(1.5)
                chances -= 1
                
                log.warning(f"passwords is not correct. ({chances} entries left).")
                print(f"passwords is not correct. ({chances} entries left).\n")

        if chances == 0:
            sleep(1.5)
            log.critical("password was wrong multiple times. exiting the program.")
            sys.exit(1)

        self.__updateDatabase()

    def displayDatabase(self):
        sleep(1.5)
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
                sleep(1.5)
                log.warning("service already exists.")
                print("service already exists.")
            else:
                break
        
        while True:
            service_password = getpass.getpass(prompt="Please enter service password: ")
            if service_password.strip() == "":
                sleep(1.5)
                log.debug("no service name provided. returning to menu.")
                return
            elif service_password == getpass.getpass(prompt="Please enter service password (confirmation): "):
                break
            else:
                sleep(1.5)
                log.warning("passwords do not match. try again.")
                print("passwords do not match. try again.\n")
        
        self.database[service_name] = service_password
        log.info("entry appended to the database.")
        self.cypher.setContent(self.database)
        self.cypher.encrypt()
        
    def deleteEntry(self):
        log.debug("deleting an entry..")
        
        service_name = None
        while service_name not in self.database.keys() or service_name == "":
            service_name = input("\nPlease enter service name: ")
            if service_name == "":
                log.debug("no service name provided. returning to menu.")
                return
            elif service_name not in self.database.keys():
                sleep(1.5)
                log.warning("service not found in database. try again.")
                print("service not found in database. try again.")

        validation_password = None
        while validation_password != self.cypher.getPassword():
            validation_password = getpass.getpass(prompt="Please enter master password: ")
            if validation_password.strip() == "":
                log.debug("no service name provided. returning to menu.")
                return
            elif validation_password != self.cypher.getPassword():
                sleep(1.5)
                log.warning("entered password is incorrect. try again.")
                print("entered password is incorrect. try again.\n")
        
        self.database.pop(service_name)
        log.info("entry removed from the database.")
        self.cypher.setContent(self.database)
        self.cypher.encrypt()
    
    def __updateDatabase(self):
        self.database = self.cypher.getContent()
        log.debug("database updated from file.")