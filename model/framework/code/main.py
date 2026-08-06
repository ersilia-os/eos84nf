# imports
import os
import sys
from ersilia_pack_utils.core import read_smiles, write_out

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# genmol's sampler resolves its bundled assets (fragment length distribution)
# relative to a module-level ROOT_DIR; the pip package does not ship that
# asset, so we bundle a copy under ./data and repoint ROOT_DIR at this folder
import genmol.sampler as genmol_sampler
genmol_sampler.ROOT_DIR = root
from genmol.sampler import Sampler

CHECKPOINT_PATH = os.path.join(root, "..", "..", "checkpoints", "model.ckpt")
NUM_SAMPLES = 100
SOFTMAX_TEMP = 1.2
RANDOMNESS = 2
GAMMA = 0.3

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# load model once
sampler = Sampler(CHECKPOINT_PATH)


# my model
def my_model(smiles_list):
    outputs = []
    for smi in smiles_list:
        try:
            samples = sampler.fragment_completion(
                smi, NUM_SAMPLES, softmax_temp=SOFTMAX_TEMP, randomness=RANDOMNESS, gamma=GAMMA
            )
        except Exception:
            samples = []
        samples = list(samples[:NUM_SAMPLES]) + [""] * (NUM_SAMPLES - len(samples))
        outputs.append(samples)
    return outputs


# read SMILES from .csv file, assuming one column with header
_, smiles_list = read_smiles(input_file)

# run model
outputs = my_model(smiles_list)

# check input and output have the same length
input_len = len(smiles_list)
output_len = len(outputs)
assert input_len == output_len

header = [f"smi_{str(i).zfill(2)}" for i in range(NUM_SAMPLES)]

# write output in a .csv file
write_out(outputs, header, output_file, str)
