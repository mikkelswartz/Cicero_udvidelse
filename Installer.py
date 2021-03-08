import streamlit as st

import pip


def install_func(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])

    else:
        pip._internal.main(['install', package])

import subprocess
import sys

try:
    import pdftotext
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", 'install', 'pdftotext'])
finally:
    import pdftotext