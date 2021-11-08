


from src.utils.all_utils import read_yaml, create_directory
#from src.utils.callbacks import create_and_save_tensorboard_callback, create_and_save_checkpoint_callback
import argparse
import os
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")



def prepare_callbacks(config_path,params_path):
    pass 








if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default = "config/config.yaml")
    args.add_argument("--params","-p", default= "params.yaml")

    parsed_args = args.parse_args()

    #print("hi")

    try:

        logging.info(">>>>> stage three started ")

        prepare_base_model(config_path= parsed_args.config,params_path =parsed_args.params) 
        

        #get_data(config_path=parsed_args.config)
        #print("*"*50)

        logging.info("stage three completed and call backs are prepared and saved as binary >>>>>")

    except Exception as e:
        logging.exception(e)
        raise e