

from tensorflow.python.module.module import valid_identifier
from src.utils.all_utils import read_yaml, create_directory
from src.utils.models import load_full_model
from src.utils.datamanagement import train_valid_generator
from src.utils.callbacks import create_and_save_tensorboard_callback, create_and_save_checkpoint_callback, get_callbacks
import argparse
import os
import time
import logging

from utils.models import get_unique_path_to_save_model

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")




def train_model(config_path,params_path):

    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts = config["artifacts"]
 
    artifacts_dir = artifacts["ARTIFACTS_DIR"]

    train_model_dir_path = os.path.join(artifacts_dir,artifacts["TRAINED_MODEL_DIR"])

    create_directory([train_model_dir_path])


    untrain_full_model_path = os.path.join(artifacts_dir,artifacts
    ["BASE_MODEL_DIR"],artifacts["UPDATED_BASE_MODEL_NAME"])

    
    model = load_full_model(untrain_full_model_path)

    callback_dir_path = os.path.join(artifacts_dir,artifacts["CALLBACKS_DIR"])

    callbacks = get_callbacks(callback_dir_path)


    train_generator, valid_generator = train_valid_generator(
        data_dir = artifacts["DATA_DIR"],
        IMAGE_SIZE = tuple(params["IMAGE_SIZE"][:-1]),
        BATCH_SIZE = params["BATCH_SIZE"],
        do_data_augmentation = params["AUGMENTATION"]
    )

    steps_per_epoch = train_generator.samples // train_generator.batch_size
    validation_steps = valid_generator.samples // valid_generator.batch_size

    model.fit(
        train_generator,
        validation_data = valid_generator,
        epochs = params["EPOCHS"],
        steps_per_epoch = steps_per_epoch,
        validation_steps = validation_steps,
        callbacks = callbacks

    )
    logging.info(f"training completed")

    train_model_dir = os.path.join(artifacts_dir,artifacts["TRAINED_MODEL_DIR"])
    create_directory([train_model_dir])

    model_file_path = get_unique_path_to_save_model(train_model_dir)
    model.save(model_file_path)
    logging.info(f"trained model is saved at :{model_file_path}")





if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default = "config/config.yaml")
    args.add_argument("--params","-p", default= "params.yaml")

    parsed_args = args.parse_args()

    #print("hi")

    try:

        logging.info(">>>>> stage four started ")

        train_model(config_path= parsed_args.config,params_path =parsed_args.params) 
        

        #get_data(config_path=parsed_args.config)
        #print("*"*50)

        logging.info("stage four completed and model is saved >>>>>")

    except Exception as e:
        logging.exception(e)
        raise e