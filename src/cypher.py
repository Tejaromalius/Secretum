# Copyright (c) 2023 tejaromalius
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import base64
import json
import logging as log
import secrets
import sys

from cryptography.fernet import InvalidToken as InvalidTokenError
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

class Cypher:
    def __init__(self, PATH):
        self.encrypted_content = None
        self.decrypted_content = {}
        self.seed = secrets.token_bytes(16)
        self.key = None
        self.path = PATH
        self.password = None
    
    def setPassword(self, PASSWORD):
        self.password = PASSWORD
        log.debug("new password is set.")
    
    def getPassword(self):
        return self.password
    
    def setContent(self, CONTENT: dict):
        self.decrypted_content = CONTENT
        log.debug("new content is set.")
    
    def getContent(self):
        return self.decrypted_content
    
    def encrypt(self):
        self.__bakeKey()
        self.__fernetContent(encrypt=1)
        self.__writeContent()
        log.info("file is encrypted.")
    
    def decrypt(self):
        self.__readContent()
        self.__bakeKey()
        self.__fernetContent(decrypt=1)

    def __writeContent(self):
        with open(self.path, "wb") as FILE:
            log.debug(f"\"{self.path}\" file is opened.")
            FILE.write(self.encrypted_content)
            log.debug("encrypted content is written to file.")
            FILE.write(b'\n')
            FILE.write(self.seed)
            log.debug("seed is written to file.")

    def __readContent(self):
        with open(self.path, "rb") as FILE:
            log.debug(f"\"{self.path}\" file is opened.")
            file_content = FILE.readlines()
            self.encrypted_content = file_content[0].replace(b'\n', b'')
            log.debug("encrypted content is read from file.")
            self.seed = file_content[1]
            log.debug("seed is read from file.")
    
    def __bakeKey(self):
        generator = Scrypt(salt=self.seed, length=32, n=2**14, r=8, p=1)
        log.debug("generator is configured.")
        decoded_key = generator.derive(self.password.encode())
        log.debug("key derived from password.")
        self.key = base64.urlsafe_b64encode(decoded_key)
        log.debug("key is baked.")

    def __fernetContent(self, encrypt=0, decrypt=0):
        try:
            oven = Fernet(self.key)
            log.debug("oven is prepared.")
            if encrypt:
                self.encrypted_content = oven.encrypt(bytes(json.dumps(self.decrypted_content).encode("utf-8")))
                log.debug("content encryption is complete.")
            elif decrypt:
                self.decrypted_content = json.loads(oven.decrypt(self.encrypted_content).decode("utf-8"))
                log.debug("password matches. content decryption is complete.")
        except InvalidTokenError:
            raise Exception("password is wrong.")
        except Exception:
            log.critical("unexpected error is raised.")
            sys.exit(1)