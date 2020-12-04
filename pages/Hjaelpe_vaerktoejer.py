#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import numpy as np

import datetime as dt
from basics import *


def write():
    st.header("Ekstra hjælpeværktøjer")
    st.subheader("Dage til 1. juni")

    # Define dates
    today = dt.date.today()
    today_year = dt.datetime.today().year
    june_first = dt.date(today_year, 6, 1)
    
    # Check if before or after june first
    if (june_first-today).days > 0:
        year = today_year
    else:
        year = today_year+1
    
    # define the next three june first
    day_to_one = dt.date(year, 6, 1)
    day_to_two = dt.date(year+1, 6, 1)
    day_to_three = dt.date(year+2, 6, 1)

    # find dtfference between dates
    diff_one = (day_to_one-today).days
    diff_two = (day_to_two-today).days
    diff_three = (day_to_three-today).days

    #print difference
    st.info(
        "Dage til 1. juni "+ str(year)+": "+ str(diff_one)+ "  \n"
        "Dage til 1. juni "+ str(year+1)+": "+ str(diff_two)+ "  \n"
        "Dage til 1. juni "+ str(year+2)+": "+ str(diff_three)
        )

    st.subheader("Antal indregistrerede bøger")
    st.write("Her kan du beregne hvor mange bøger der er indregistreret af samme sæt ved at indsate første og sidste påsatte stregkode.")
    First_barcode = st.number_input("Første stregkode:", min_value=10000, max_value=999999, step=1)
    Last_barcode = st.number_input("Sidste stregkode:", min_value=10000, max_value=999999, step=1)
    Diff_barcode = Last_barcode-First_barcode+1
    st.info("Antal bøger indregistreret: " + str(Diff_barcode))
