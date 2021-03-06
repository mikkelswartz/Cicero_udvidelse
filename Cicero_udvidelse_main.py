#!/usr/bin/env python3


# Author:	    Mikkel Swartz
# Date:		    2-07-2019
# Institution:  Marie Kruses Skole
# Version:      2.0
# Function:     This program analyse data from Ciceo

# import libraries
import streamlit as st
import re
import string

from basics import *
import pages.Startside
import pages.Stregkode_generator_delehold
import pages.Konvertering_af_bogbestillinger
import pages.Reoloversigt
import pages.Hjaelpe_vaerktoejer


# import kvantitativ udlaanssnslyse
#from quantitative_book_lending_analysis_by_class import *;
#from quantitative_book_lending_analysis_by_book import *; 

PAGES = {
    "Startside" : pages.Startside,
    "Stregkodegenerator til delehold" : pages.Stregkode_generator_delehold,
    "Konvertering af bogbestillinger" : pages.Konvertering_af_bogbestillinger,
    "Reoloversigt" : pages.Reoloversigt,
    "Ekstra hjælpevæktøjer" : pages.Hjaelpe_vaerktoejer
    #"Forhydrering" : pages.Forhydering,
    #"MTX infusion" : pages.MTX_infusion,
    #"Monitorering af toksicitet" : pages.Monitorering_af_toksicitet
}

def main():
    
    st.sidebar.title("Navigation")
    page_selection = st.sidebar.radio('', options=list(PAGES.keys()))

    page = PAGES[page_selection]
    #testing
    #before = dt.datetime.now()
    #testing
    
    write_page(page)
    

    # customize width of the content
    sidebar_settings()

    # remove the steamlit footer and the hamburger menu in top right cornor
    #hide_streamlit_style()
    # display costum footer
    custom_footer()

    #testing
    #after = dt.datetime.now()
    #st.write(after-before)
    #testing

if __name__ == "__main__":
    main()




