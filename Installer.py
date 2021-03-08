import streamlit as st

import pip


def install_func(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])

    else:
        pip._internal.main(['install', package])

