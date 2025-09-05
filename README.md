# Getting started with my code 

## Getting UV installed

```bash 
# for runai use the following line: 
runai submit cs336-dev \ -p <user> \  -i nvcr.io/nvidia/pytorch:25.06-py3 \  -g 1 --interactive --attach \  --command -- bash # replace -g 1 with -g 4 for 4 GPUs.
cd cs336-assignment2-scaling
git clone https://github.com/damek/cs336-assignment2-systems.git
pip install uv
export PATH="$HOME/.local/bin:$PATH"
uv sync
uv venv
source .venv/bin/activate
```


# CS336 Spring 2025 Assignment 3: Scaling


For a full description of the assignment, see the assignment handout at
[cs336_spring2025_assignment3_scaling.pdf](./cs336_spring2025_assignment3_scaling.pdf)

If you see any issues with the assignment handout or code, please feel free to
raise a GitHub issue or open a pull request with a fix.

## Setup

0. Install uv

1. Add whatever dependencies you need with `uv add <package>`.

2. Run anything in the given environment with

```sh
uv run <command>
```

3. If you need the Python binary (for instance to reference the Python interpreter for VSCode), run
```sh
uv run which python
```

