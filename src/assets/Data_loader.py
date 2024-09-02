import os
import json
from tqdm import tqdm

class MTSS_data_loader:

    @staticmethod
    def load_data():

        f = open('config.json'); data_file_descriptor = json.load(f)["mtss_data_path"]; f.close()
        f = open(data_file_descriptor,'r'); data = '\n'.join(f.read().splitlines()); f.close()
        data = ''.join(ch for ch in data if (ch.isalnum() or str(ch) in [' ','.',',',';'])).strip()
        return data

    @staticmethod
    def load_symbolic_data():

        f = open('config.json'); json_files_folder_path = json.load(f)["mtss_qa_path"]; f.close()
        qa_file_names = [os.path.join(json_files_folder_path,item) for item in os.listdir(json_files_folder_path)]
        QAs = []
        for qa_file in tqdm(qa_file_names):
            try:
                with open(qa_file) as f:
                    QAs += list(json.load(f))

            except ValueError as error:

                print (qa_file, error)
                continue

        print (len(QAs))
        
