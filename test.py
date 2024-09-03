import sys
import json

def from_string_to_json(string):
    return json.loads(string)

if __name__ == "__main__":
    corret_form = sys.argv[1].replace("'","\"")
    json_input_download = from_string_to_json(corret_form)