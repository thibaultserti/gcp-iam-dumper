import json
import logging
import subprocess
from typing import List


logging.basicConfig(encoding='utf-8', level=logging.INFO)

def retrieve_iam_json(project: str) -> List[dict]:

    command = ["gcloud", "projects", "get-iam-policy", project, "--format=json"]

    logging.debug(f"Command: {' '.join(command)}")

    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    dico = json.loads(result.stdout)['bindings']
    return dico