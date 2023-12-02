# nbdump
Dump files to Jupyter notebook. Restore by running the notebook. Add optional extra commands to run.

# Installation
```bash
# user
pip install -U nbdump

# development
pip install -e .
pip install tests/requirements.txt
pytest
```

# Usage
In this demo, we will use `src_example/` as a fake repo that you want to import to notebook.

```bash
# see help
nbdump -h

# basic usage, this will dump entire `src_example/` to `nb1.ipynb`
nbdump src_example -o nb1.ipynb

# use shell expansion, this will come in handy later
nbdump src_example/**/*.py -o nb2.ipynb

# handle multiple files/dirs, will be deduplicated
nbdump src_example src_example/main.py -o nb3.ipynb

# append extra code cell, e.g. running the `src_example/main.py`
nbdump src_example -c '%run src_example/main.py' -o nb4.ipynb

# extra cells can be more than one
nbdump src_example \
    -c '%run src_example/main.py' \
    -c '!git status' \
    -o nb5.ipynb

# use fd to skip ignored files and hidden files
nbdump $(fd -t f . src_example) -o nb6.ipynb
```
There is a catch, `nbdump` will not respect gitignore because the core functionality is just converting a bunch of files to notebook cells. This means, by using the first example on `nb1.ipynb`, `nbdump` will try to convert all files recursively, regardless of file format. The problem arises when `src_example/` contains binary files such as pictures or even `__pycache__/*`.

Then shell expansion can be used to only select relevant files, such as the example on `nb2.ipynb` (make sure to enable globstar in bash to use `**`). Another solution is to use other tools like [fd](https://github.com/sharkdp/fd) to list the files while respecting gitignore and skipping hidden files automatically.

# Why?
Kaggle kernel with *code competition* type with disabled internet cannot use git clone inside the notebook. `nbdump` allows one to work in a standard environment but the final result can be exported to a single notebook, while still preserving the filesystem tree.

This is different than just zipping and unzipping because by using `%%writefile`, you can see and edit the file inside, even after the notebook creation.
