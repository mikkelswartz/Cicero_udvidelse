#!/usr/bin/env python3

import streamlit as st
from basics import *

import pdfplumber
# Hvis pdftotext skal benyttes, så se her: https://www.activestate.com/resources/quick-reads/how-to-install-python-packages-using-a-script/

def write():
    st.header("Velkommen til cicero udvidelse")
    
    pdf_file = st.file_uploader("Uploade din PDF-fil med laanerudskrifter", type="pdf")
    #pdf_file = "AUdvikling/Udskift-2020-05-27.pdf"
    #pdf_file = open('AUdvikling/sample6.pdf', "r")

    if pdf_file is not None:
        pdf_text = pdftotext.PDF(pdf_file)
        pdflines = PDF_to_list_of_strings(pdf_text)
        Inputdata = extract_data_from_pdflines(pdflines)

        # #st.write(Inputdata)

        # #st.write(pdflines)
        # #printerfunction_by_class(Inputdata)
        printerfunction_by_class_pandas(Inputdata)
        # #st.write(Inputdata[1][1])




        # pdf = pdfplumber.open(pdf_file)
        # st.write(pdf)
        # with pdfplumber.open(r"AUdvikling/sample6.pdf") as pdf:
        #     first_page = pdf.pages[0]
        #     print(first_page.extract_text())

        # with pdfplumber.open(pdf_file) as pdf:
        #     page = pdf.pages[0]
        #     text = page.extract_text()
        #     st.write(text)  


