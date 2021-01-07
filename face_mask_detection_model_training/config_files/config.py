# import the necessary packages
import os

# initialize the path to the *original* input directory of images
ORIG_INPUT_DATASET = "Raw_Dataset"

# initialize the base path to the *new* directory that will contain
# our images after computing the training and testing split
BASE_PATH = "Organized_Dataset"

# derive the training, validation, and testing directories
TRAIN_PATH = os.path.sep.join([BASE_PATH, "Train"])
VAL_PATH = os.path.sep.join([BASE_PATH, "Validation"])
TEST_PATH = os.path.sep.join([BASE_PATH, "Test"])


# define the amount of data that will be used training
TRAIN_SPLIT = 0.75
# the amount of validation data will be a percentage of the
# *training* data
VAL_SPLIT = 0.1

# define the names of the classes
CLASSES = ["Wearing Mask", "Incorrect or No Mask"]

# initialize the initial learning rate, batch size, and number of
# epochs to train for
INIT_LR = 1e-4
BS = 32
NUM_EPOCHS = 20
# define the path to the serialized output model after training
MODEL_PATH = "face_mask_detection_model"