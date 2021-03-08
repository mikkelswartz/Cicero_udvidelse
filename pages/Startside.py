#!/usr/bin/env python3

import streamlit as st
from basics import *

def write():
    st.header("Velkommen til Cicero Udvidelse")
    
    st.markdown("Dette program har til formål at automatisere manuelle opgaver, "
        "samt at give mulighed for indsigt i bogadministrationen på måder Cicero "
        "ikke selv er i stand til.\n"
        "\n"
        "I navigationen til venstre er det muligt at vælge "
        "den funktion man ønsker at benytte.  \n" 
        "Hvis navigationen ikke er synlig kan den frembringes ved at "
        "trykke på den lille pil i øverste venster hjørne."
        )

    