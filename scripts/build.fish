#!/usr/bin/env fish

rm -r dist
pip uninstall nbdump -y
python -m build
