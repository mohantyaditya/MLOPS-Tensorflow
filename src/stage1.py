from genericpath import exists
import os

from src.utils.all_utils import read_yaml, create_directory

import argparse

import pandas as pd 
import shutil
from tqdm import tqdm 
import shutil

import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s " 
log_dir = "logs"
os.makedirs(log_dir,exist_ok = True)
logging.basicConfig(filename=os.path.join(log_dir,"running_logs.log"),level = logging.INFO,format = logging_str,filemode = 'a')


def copy_file(source_download_dir,local_data_dir):

    list_of_files = os.listdir(source_download_dir)

    N = len(list_of_files)

    for file in tqdm(list_of_files,total = N,desc = f"copying file from {source_download_dir} to {local_data_dir}",colour = "green"):

        src = os.path.join(source_download_dir,file)

        dest = os.path.join(local_data_dir,file)

        shutil.copy(src,dest)





def get_data(config_path):
    config = read_yaml(config_path)

    source_download_dirs = config["source_download_paths"]

    print(source_download_dirs)

    local_data_dir = config["local_data_path"]


    for source_download_dir,local_dir in tqdm(zip(source_download_dirs,local_data_dir),total = 2,desc = "list of folder"):

        create_directory([local_dir])

        print(source_download_dir)
        copy_file(source_download_dir,local_dir)


    







if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default = "config/config.yaml")

    parsed_args = args.parse_args()

    print("hi")

    try:

        logging.info(">>>>> stage 1 started ")

        get_data(config_path=parsed_args.config)
        print("*"*50)

        logging.info("stage 1 completed and all data are saved in local >>>>>")

    except Exception as e:
        logging.exception(e)
        raise e


