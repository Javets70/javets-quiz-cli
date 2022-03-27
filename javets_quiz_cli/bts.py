from rich.console import Console
from cryptography.fernet import Fernet
import os
import json
import sys

class QuizCli:
    console = Console()
    config_path = './QuizCli/config.json'
    if os.path.isfile('./QuizCli/user.key'):
        user_key = open('./QuizCli/user.key').read()
    else:
        user_key = None

    def __init__(self) -> None:
        try:
            os.mkdir("./QuizCli")
        except OSError:
            QuizCli.console.print("[bold yellow] \n:warning: Directory already exists , skipping mkdir[/]")

        if not os.path.isfile(self.config_path):
            with open(self.config_path , 'w+') as config_file:
                json.dump({"save key" : True , 'path1' : 'None' , 'path2' : 'None' , '+points' : 10 , '-points' : 5} ,fp=config_file, indent=4)
                
        
    def gen_key(self) -> "User key":
        if not os.path.isfile('./QuizCli/user.key'):
            config = json.loads(open('./QuizCli/config.json').read())
            if config['save key']:
                with open('./QuizCli/user.key','wb') as self.keyfile:
                    self.user_key = Fernet.generate_key()
                    self.keyfile.write(self.user_key)
                    QuizCli.user_key = self.user_key
                    return self.user_key
            else:
                self.user_key = Fernet.generate_key()
                QuizCli.console.print(f"[bold yellow] Key hasnt been saved in user.key , Your key is {self.user_key}")
                QuizCli.user_key = self.user_key
                return self.user_key
        else:
            QuizCli.console.print("[bold yellow] \n:warning: user.key already exists , skipping gen_key [/]")

    def encrypt_data(self , path , key ) -> None:
        self.path = path
        self.data = open(self.path).read().encode()
        self.key = key

        if key == 'None':
            self.key = QuizCli.user_key

        self.fernet = Fernet(self.key)
        self.encrypted_data = self.fernet.encrypt(self.data)
        self.encrypted_file_path = './QuizCli/' +"_encrypted_" +  os.path.basename(self.path)
        if not os.path.isfile(self.path):
            QuizCli.console.print("File not found , check your file path :pensive: ")
            sys.exit()       
        elif os.path.isfile(self.encrypted_file_path):
            QuizCli.console.print("[bold yellow]\n:warning: File already exists , rename your data file [/]")
            sys.exit()
        else:
            with open('./QuizCli/' +"_encrypted_" +  os.path.basename(self.path) , 'wb') as encrypted_file:
                encrypted_file.write(self.encrypted_data)

    def decrypt_data(self , path , key ) -> "Decrypted Data": 
        if os.path.isfile(path):
            self.path = path
            self.key = QuizCli.user_key

            if self.key != 'None':
                self.key = self.key

            self.fernet = Fernet(self.key)
            self.data = open(self.path , 'rb').read()
            self.decrypted_data = self.fernet.decrypt(self.data)
            return self.decrypted_data
        else:
            QuizCli.console.print("[bold yellow]\n:warning: File not found , please check the file path[/]")
            sys.exit()
    
    def filter_data(self , data) -> "Filtered Data":
        with open('tempfile.txt' , 'w+') as temp:
            temp.write(data.decode('utf-8'))

        self.raw_data = open('./tempfile.txt').readlines()
        self.dash_indexes = [i for i in range(len(self.raw_data)) if "---" in self.raw_data[i]]
        self.data = []
        self.prev_index = -1
        for index in self.dash_indexes:
            self.data.append("".join(self.raw_data[1 + self.prev_index : index]))
            self.prev_index = index
        os.remove("./tempfile.txt")
        return self.data

