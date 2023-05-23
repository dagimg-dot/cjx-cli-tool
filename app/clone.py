import fnmatch
import json
import os
import subprocess
from app.simple import Simple
from app.jfxml import JFXML

class Clone:
    def file_search(self,file_extension,directory_path):
        isFound = False
        for root, dirnames, filenames in os.walk(directory_path):
            for _ in fnmatch.filter(filenames, file_extension):
                isFound = True
                break

        return isFound
    
    def check_repo(self):
        url = self.args.url
        self.repo_name = str(url.split('/')[-1].split('.')[0])
        Clone.clone_repo(self)
            
    def clone_repo(self):
        clone_command = f'git clone {self.args.url}'
        if os.path.exists(self.repo_name):
            print("Error: The repository you entered is already cloned")
            return
        try:
            subprocess.check_output(clone_command, shell = True)
            Clone.check_cloned_repo(self)
        except subprocess.CalledProcessError:
            print("Error: There is an error when cloning")
        
    def check_cloned_repo(self):
        os.chdir(self.repo_name)
        current_dir = os.getcwd()
        java_files_ext = "*.java"
        fxml_files_ext = "*.fxml"
        flag_x = Clone.file_search(self,fxml_files_ext,current_dir)
        flag_j = Clone.file_search(self,java_files_ext,current_dir)
        if flag_x == True and flag_j == True:
            Clone.add_config(self,"jfxml")
        elif flag_j:
            Clone.add_config(self,"simple")
        else:
            print("Error: The repository you cloned is not a javafx project !!")
            os.chdir("..")
            try:
                os.system(f"rmdir /s /q {self.repo_name}")
            except:
                os.system(f"Remove-Item {self.repo_name} -Recurse -Force")

    def add_config(self,project_type):
        if project_type == "simple":
            Simple.vscode_folder(self)
            Simple.create_launch_json(self)
            Simple.create_settings_json(self)

            print("\nJavaFX project cloned and configured successfully 🎇")
        elif project_type == "jfxml":
            JFXML.vscode_folder(self)
            JFXML.create_launch_json(self)
            JFXML.create_settings_json(self)

            Clone.config_packageName(self)

            print("\nJavaFX project cloned and configured successfully 🎇")
            

    def config_packageName(self):
        os.chdir("src/main/java/com")

        # list of directories in the current directory
        directories = os.listdir(os.getcwd())
        
        if len(directories) == 0:
            print("Error: There is an error when configuring the project")
            return
        
        self.package_name = directories[0]

        # change the current directory back to the root directory
        os.chdir("../../../../")

        json_path = ".vscode/launch.json"
        print(json_path)
        
        try:
            with open(json_path,'r') as f:
                datas = json.load(f)

            for data in datas['configurations']:
                data["mainClass"] = f"com.{self.package_name}.App"
            
            with open(json_path,'w') as f:
                json.dump(datas,f,indent=4)
        except:
            print("Error: There is an error when configuring the project")







        

