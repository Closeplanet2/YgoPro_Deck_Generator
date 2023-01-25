from Controller.WebsiteController import RequestController
import os
import json

class FileDirectoryController:
    def open_file(self, dir_path, file_name):
        osCommandString = f"notepad.exe {dir_path}/{file_name}"
        os.system(osCommandString)

    def does_path_exist(self, file_path):
        return os.path.exists(file_path)

    def create_directory(self, dir_path):
        if not self.does_path_exist(dir_path):
            os.makedirs(dir_path)

    def write_file(self, dir_path, file_name):
        self.create_directory(dir_path)
        if not os.path.exists(f"{dir_path}/{file_name}"):
            open(f"{dir_path}/{file_name}", "w").close()

    def read_and_write_file(self, dir_path, file_name):
        self.write_file(dir_path, file_name)
        return open(f"{dir_path}/{file_name}",'r')

    def is_file_empty(self, dir_path, file_name):
        return os.stat(f"{dir_path}/{file_name}").st_size == 0

    def is_dir_empty(self, dir_path):
        return not os.listdir(dir_path)

    def count_files_in_dir(self, dir_path):
        return len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])

    def delete_file(self, dir_path, file_name):
        if os.path.exists(f"{dir_path}/{file_name}"):
            os.remove(f"{dir_path}/{file_name}")

    def delete_and_write_file(self, dir_path, file_name):
        self.delete_file(dir_path, file_name)
        self.write_file(dir_path, file_name)

    def write_array_to_file(self, dir_path, file_name, list):
        self.write_file(dir_path, file_name)
        with open(f"{dir_path}/{file_name}", 'w') as data_file:
            for item in list:
                data_file.write(f"{item}\n")

    def read_array_from_file(self, dir_path, file_name):
        self.write_file(dir_path, file_name)
        data = []
        with open(f"{dir_path}/{file_name}", 'r') as data_file:
            for line in data_file:
                data.append(line.replace("\n", ""))
        return data

class JSONController:
    def dump_webpage_to_json(self, dir_path, file_name, webpage_url, external_key=None):
        external_webpage = RequestController().pull_website(webpage_url=webpage_url)
        json_webpage = json.loads(external_webpage.text)
        if not external_key is None:
            json_webpage = json.loads(external_webpage.text)[external_key]
        self.dump_dict_to_json(dir_path, file_name, json_webpage)

    def dump_dict_to_json(self, dir_path, file_name, dict):
        with open(f"{dir_path}/{file_name}", 'w') as data_file:
            json.dump(dict, data_file)

    def load_json(self, dir_path, file_name):
        with open(f"{dir_path}/{file_name}", "r") as data_file:
            return json.load(data_file)








