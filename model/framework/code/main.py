# imports
import os
import sys
from rdkit import Chem
from ersilia_pack_utils.core import read_smiles, write_out

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# genmol's sampler resolves its bundled assets (fragment length distribution)
# relative to a module-level ROOT_DIR; the pip package does not ship that
# asset, so we bundle a copy under ./data and repoint ROOT_DIR at this folder
import genmol.sampler as genmol_sampler
genmol_sampler.ROOT_DIR = root
from genmol.sampler import Sampler
import genmol.model as genmol_model
from safe.tokenizer import SAFETokenizer

CHECKPOINT_PATH = os.path.join(root, "..", "..", "checkpoints", "model.ckpt")
TOKENIZER_PATH = os.path.join(root, "..", "..", "checkpoints", "tokenizer.json")
NUM_SAMPLES = 100  # outputs per input
ROUND_SIZE = 100  # samples GenMol draws per call
MAX_ROUNDS = 5
SOFTMAX_TEMP = 1.2
RANDOMNESS = 2
GAMMA = 0.3

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]


def _local_tokenizer():
    # genmol's get_tokenizer() downloads datamol-io/safe-gpt from the Hugging Face
    # Hub every time the model is built; the same tokenizer.json is kept next to
    # the checkpoint instead, with the two bracket tokens genmol adds to it
    tokenizer = SAFETokenizer.load(TOKENIZER_PATH).get_pretrained()
    tokenizer.add_tokens(["<", ">"])
    return tokenizer


genmol_model.get_tokenizer = _local_tokenizer

# load model once
sampler = Sampler(CHECKPOINT_PATH)


# my model
def _canonical_no_stereo(smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None
    return Chem.MolToSmiles(Chem.MolFromSmiles(Chem.MolToSmiles(mol, isomericSmiles=False)))


def my_model(smiles_list):
    outputs = []
    for smi in smiles_list:
        # For an input without `*`, GenMol adds one to three `*` attachment points at
        # random hydrogen-bearing atoms of the whole input (once per call) and keeps only
        # samples that contain the input as a substructure, so every output extends the
        # whole input. It can still return the unchanged input or repeat a completion
        # (39/97 valid outputs for one benchmark compound were the unchanged input), so a
        # call gives about 64 distinct outputs of 100. A larger request keeps the same
        # attachment points; a new call draws new ones, so calls are repeated until
        # NUM_SAMPLES distinct outputs are collected or MAX_ROUNDS is reached.
        input_key = _canonical_no_stereo(smi)
        seen = set()
        filtered = []
        for _ in range(MAX_ROUNDS):
            try:
                samples = sampler.fragment_completion(
                    smi, ROUND_SIZE, softmax_temp=SOFTMAX_TEMP, randomness=RANDOMNESS, gamma=GAMMA
                )
            except Exception as e:
                # keep what earlier rounds gave; the cause (unparsable SMILES, no atom
                # bearing a hydrogen, a model error) is reported instead of swallowed
                print(f"GenMol failed for {smi!r}: {type(e).__name__}: {e}", file=sys.stderr)
                break
            for s in samples:
                key = _canonical_no_stereo(s)
                if key is None or key == input_key or key in seen:
                    continue
                seen.add(key)
                filtered.append(s)
            if len(filtered) >= NUM_SAMPLES:
                break

        samples = list(filtered[:NUM_SAMPLES]) + [""] * (NUM_SAMPLES - len(filtered))
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
