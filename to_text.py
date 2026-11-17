#change from json format to txt
import json
from pathlib import Path
import  argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, required=True,
                    help="provide path to input json file to be saved as json")
parser.add_argument("output", type=str, required=True,
                    help="provide path to output json file without extension")
args = parser.parse_args()

json_file = Path(f"{args.file}")
json_stem = json_file.stem
output_file = Path(f"{args.file}")

with open(f"{output_file}.txt", "w", encoding="utf-8") as outf:
    with open(json_file, "r", encoding="utf-8") as inf:
        lexicon = json.load(inf)

        for k, v in lexicon.items():
            outf.write(f"{k}\n")