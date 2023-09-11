#!/usr/bin/env fish

rm -r dist
pip uninstall nbdump -y
python -m build

# pip install dist/*  # cant to this, install just one (whl or tar)
pip install dist/*.whl
