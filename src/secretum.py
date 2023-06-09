import getpass
import logging as log
import os
import os.path as Path
import sys

from cypher import Cypher

database_path = f"/home/{os.getlogin()}/.config/Secretum/encrypted.db"

def loadDatabase(CYPHER):
    chances = 4
    while True:
        if chances == 0:
            log.critical("password was wrong multiple times. exiting the program.")
            sys.exit(1)
        
        CYPHER.setPassword(getpass.getpass(prompt="Please enter password: "))
        
        try:
            CYPHER.decrypt()
            break
        except Exception:
            chances -= 1
            log.warning(f"passwords is not correct. ({chances} entries left).")
            continue
    return CYPHER.getContent()

def setupDatabase(CYPHER):
    chances = 4
    while True:
        CYPHER.setPassword(getpass.getpass(prompt="Please enter new password: "))
        if CYPHER.getPassword() != getpass.getpass(prompt="Please enter new password (confirmation): "):
            chances -= 1
            log.warning(f"password do not match. ({chances} entries left).")
            continue
        break

    CYPHER.encrypt()
    return CYPHER.getContent()

def getNewEntry():
    service_name = input("\nPlease enter service name: ")

    while True:
        service_password = getpass.getpass(prompt="Please enter service password: ")

        if service_password == getpass.getpass(prompt="Please enter service password (confirmation): "):
            return service_name, service_password
        else:
            log.warning("passwords do not match. try again.")
            continue
    
if __name__ == "__main__":
    log.basicConfig(level = log.DEBUG, datefmt = "%H:%M:%S", format = "%(asctime)s.%(msecs)02d -- %(levelname)s: %(message)s")
    # os.system("clear")

    cypher = Cypher(database_path)

    database_exists = Path.exists(database_path)
    log.debug("database {}".format("exists" if database_exists else "doesn't exist"))
    
    if database_exists:
        database = loadDatabase(cypher)
    else:
        database = setupDatabase(cypher)
    
    while True:
        print(database)

        if input("\nAdd new entry?\n> ") in ('y', "yes"):
            service_name, service_password = getNewEntry()
            database[service_name] = service_password
            cypher.setContent(database)
            cypher.encrypt()
        else:
            sys.exit(0)