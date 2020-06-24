#!/usr/bin/env python3

import streamlit as st
from basics import *

def write():
    st.header("Velkommen til cicero udvidelse")
    
    pdf_file = st.file_uploader("Uploade din PDF-fil med laanerudskrifter", type="pdf")
    if pdf_file is not None:
        pdf_text = pdftotext.PDF(pdf_file)
        pdflines = PDF_to_list_of_strings(pdf_text)
        Inputdata = extract_data_from_pdflines(pdflines)

        #st.write(Inputdata)

        #st.write(pdflines)
        #printerfunction_by_class(Inputdata)
        printerfunction_by_class_pandas(Inputdata)
        #st.write(Inputdata[1][1])
    

