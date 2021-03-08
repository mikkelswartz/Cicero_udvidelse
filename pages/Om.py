#!/usr/bin/env python3

import streamlit as st
from basics import *

def write():
    st.header("Information om Cicero Udvidelse")
    
    st.markdown("Dette program er udviklet af Mikkel Swartz og designet "
        "specifikt til brug på Marie Kruses Skole. \n"
        "\n"
        "Programmet er skrevet i programmeringsproget Python og benytter "
        "frameworket Streamlit til den visuelle opsætning og brugergrænseflade."
        )

    st.markdown("Version: 2.1.1  \n"
        "Denne version var tilgængelig: 1. marts 2021."
        )

    st.markdown("Ved spørgsmål kan Mikkel Swartz kontaktes via mail på mikkel.swartz@hotmail.com")

    