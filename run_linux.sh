#!/bin/bash

# This script is used to run the model in a linux environment.
# run with: ./run_linux.sh --update when you need to setup the python environment

# config
CONDA_ROOT_PREFIX="../text-generation-webui/installer_files/conda"
INSTALL_ENV_DIR="../text-generation-webui/installer_files/env"



# check if conda environment was actually created
if [ ! -e "$INSTALL_ENV_DIR/bin/python" ]; then
    echo "Conda environment is empty."
    exit
fi

# environment isolation
export PYTHONNOUSERSITE=1
unset PYTHONPATH
unset PYTHONHOME
export CUDA_PATH="$INSTALL_ENV_DIR"
export CUDA_HOME="$CUDA_PATH"

# activate installer env
source "$CONDA_ROOT_PREFIX/etc/profile.d/conda.sh" # otherwise conda complains about 'shell not initialized' (needed when running in a script)
conda activate "$INSTALL_ENV_DIR"

# setup installer env
python runmodel.py $@