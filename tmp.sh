#!/bin/bash

# Check if the environment 'genomeVarAPI_pyenv_3.9' exists
if conda env list | grep -q 'genomeVarAPI_pyenv_3.90'; then
  echo 'The environment "genomeVarAPI_pyenv_3.9" already exists.'
else
  echo 'The environment "genomeVarAPI_pyenv_3.9" does not exist. Creating it now...'
fi