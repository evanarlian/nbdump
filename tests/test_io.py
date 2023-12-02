from io import StringIO

from nbdump.core import extract_metadata


def test_extract_metadata():
    ipynb_string = """{
        "metadata": {"can": "be", "anything": "really"},
        "nbformat_minor": 4,
        "nbformat": 4,
        "cells": []
    }"""
    sio = StringIO(ipynb_string)
    extracted = extract_metadata(sio)
    assert extracted == {"can": "be", "anything": "really"}


def test_extract_missing_metadata():
    ipynb_string = """{
        "nbformat_minor": 4,
        "nbformat": 4,
        "cells": []
    }"""
    sio = StringIO(ipynb_string)
    extracted = extract_metadata(sio)
    assert extracted == {}
