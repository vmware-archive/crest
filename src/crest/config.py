# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT
from os.path import dirname, abspath
import logging

dir_path = dirname(abspath(__file__))
parent_dir_path = dirname(dir_path)

global_args = {
    "server-ip": "0.0.0.0",
    "port": 3000,
    "domain_file_path": dir_path + "/utils/ads_domain.txt", #path to keep an advertisement domain list 
    "failed_screenshot_path": dir_path + "/output/screenshot.png", # Path where the failed KFI elements will be stored
    "log_path": dir_path + "/test.log", # Log file path
    "log_level": logging.INFO, # Logging level
    "reporttype": 3, # reporttype is either xpath(value: 3) or css selector(value: 4)
    "model_params": {
        "training_data_input_file_name": dir_path + "/input/dataset.csv", # Path to training data file
        "num_train_epochs": 1, # num. of epochs to train the model
        "evaluate_during_training": True, # whether to evaluate during the training or not
        "fp16": True, # To restrict float values till 16 decimal places only
        "use_cuda": False, # True if you have GPUs
        "use_multiprocessing": False, # Self-explanatory
        "output_dir": dir_path + "/models/", # Path where trained model will be saved
        "best_model_dir": dir_path + "/models/best_model/", # Path to the model that has least validation loss
        "overwrite_output_dir": True, # True if you want to replace the existing model
    },
}
