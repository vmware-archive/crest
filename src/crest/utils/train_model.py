# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT

# Install simpletransformers library using pip install simpletransformers
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import logging
from crest.config import *
import os

logging.basicConfig(level=logging.DEBUG)


def check_input():
    logging.debug("Inside check input")
    file_name = global_args["model_params"]["training_data_input_file_name"]
    if os.path.exists(file_name):
        logging.debug("Inout data does exists")
        return True
    else:
        logging.debug("Inout data does not exists")
        return False


def load_dataset():
    logging.debug("Load Dataset")
    dataset = pd.read_csv(global_args["model_params"]["training_data_input_file_name"])
    dataset.rename(
        columns={"Title": "text_a", "Description": "text_b", "Result": "labels"},
        inplace=True,
    )
    dataset = dataset[:-1]
    dataset.dropna(inplace=True)
    try:
        dataset.drop(columns=["URL"], inplace=True)
    except:
        pass
    return dataset


def data_preprocess(dataset):
    logging.debug("Data Preprocess started")
    enc = LabelEncoder()
    dataset["labels"] = enc.fit_transform(dataset["labels"])

    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2)
    for train_index, valid_index in sss.split(dataset, dataset["labels"]):
        # print(type(train_index), type(valid_index))
        train_dataset = dataset.iloc[train_index].reset_index(drop=True)
        valid_dataset = dataset.iloc[valid_index].reset_index(drop=True)
    logging.debug("Data splitted into training and validation data")
    return train_dataset, valid_dataset


def train(train_dataset, valid_dataset):
    logging.debug("Training is going to start")
    args = {}
    args.update(global_args["model_params"])
    model = ClassificationModel(
        "roberta",
        "models/best_model/",
        use_cuda=False,
        args=global_args["model_params"],
    )
    model.train_model(train_dataset, eval_df=valid_dataset)
    logging.debug("Training is done")


def run_script():
    logging.debug("Inside run script")
    if check_input():
        dataset = load_dataset()
        train_dataset, validation_dataset = data_preprocess(dataset)
        train(train_dataset, validation_dataset)
    else:
        pass


if __name__ == "__main__":
    run_script()
