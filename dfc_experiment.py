import itertools
import json
import random
import subprocess
import time
import os

from math import floor, log10

import numpy as np


def random_experiment(options):
    line = ""
    for arg, vals in options.items():
        is_range = type(vals[0]) != str and len(vals) == 2
        if is_range:
            if isinstance(vals[0], int):
                val = int(random.uniform(vals[0], vals[1] + 1))
            elif isinstance(vals[0], float):
                loglow, loghigh = np.log(vals[0]), np.log(vals[1])
                val = np.exp(random.uniform(loglow, loghigh))
                val = round(val, 1 - int(floor(log10(abs(val)))))
        else:
            val = random.choice(vals)
        line += f"{arg} {val} "
    return line


def options_to_lines(options, option="grid", num_lines=64):
    if option == "grid":
        arg_strings = [
            [f"{arg} {val}" for val in vals] for arg, vals in options.items()
        ]
        lines = [" ".join(arg_list) for arg_list in itertools.product(*arg_strings)]

    elif option == "random":
        lines = [random_experiment(options) for _ in range(num_lines)]
    return lines


def save_json(discrete_options):
    # archieve json file as header name
    header = discrete_options['--header'][0]

    save_dir = "runs/save_runs/" + header

    os.makedirs(save_dir, exist_ok=True)

    with open(os.path.join(save_dir, header + ".json"),"w") as f:
        json.dump(discrete_options, f)

    return save_dir


json_file = "gogo.json"
option = "grid"
MAX_EXPS = 8

with open(f"runs/{json_file}", "r") as f:
    discrete_options = json.load(f)

lines = options_to_lines(discrete_options, option=option, num_lines=MAX_EXPS)
save_dir = save_json(discrete_options)


# commands = [f"dfc start main.py {line}" for line in lines]
# commands = [f"dfc start vggprune.py {line}" for line in lines]
commands = [f"dfc start main_finetune.py {line}" for line in lines]

#print(commands)
#print(lines[:3])
#print("example command: \n", commands[0])

processes = list()
for command in commands:
    process = subprocess.Popen(command, shell=True)
    time.sleep(5)
    processes.append(process)
output = [p.wait() for p in processes]
