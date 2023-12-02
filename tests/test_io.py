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
    metadata = {"can": "be", "anything": "really"}
    extracted = extract_metadata(sio)
    assert extracted == metadata


def test_extract_no_metadata():
    ipynb_string = """{
        "nbformat_minor": 4,
        "nbformat": 4,
        "cells": []
    }"""
    sio = StringIO(ipynb_string)
    metadata = {}
    extracted = extract_metadata(sio)
    assert extracted == metadata
