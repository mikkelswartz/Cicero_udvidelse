#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import barcode
from barcode.writer import ImageWriter

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors
import PIL 
from reportlab.lib.units import inch

import datetime as dt
from basics import *

import csv
import os

def write():
    st.header("Stregkodegenererator til delehold")
    
    if st.checkbox("Vis hjælp til at lokalisere bogbestillinger"):
        st.info(
            "Log ind på Microsoft Forms via dette link (https://forms.office.com/Pages/DesignPage.aspx#Analysis=true&FormId=E1UM0AXnJ0mrbkz9VaG8DlYxe7oFYvNOq2Q32K2uqmRUODdENzdGRDhFTUpJUEYzMExNSjFBOTkxMy4u) "
            "og tryk på knappen 'Åben i Excel'.  \n"
            )
    
    if st.checkbox("Vis hjælp til at indsætte konverteret dokument i samlede bogbestillinger"):
        st.info(
            "Åben det konvertede dokument på skrivebordet. Marker hele dokumentet og kopier.  \n"
            "Åben arket med samlede bestillinger: (https://docs.google.com/spreadsheets/d/1PxQQbC3Ib8tcMGtE4okmi-KRGhHwuGYfSWzRxlUV55I/edit?usp=sharing)  \n"
            "Indsæt (Indsæt speciel --> kun værdier) (cmd + shift + V) ved en første ledige celle i kolonne A'."
            )

    # upload fra Cicero
    st.write("__Upload bogbestillinger__")
    Bogbestillinger_file = st.file_uploader("Uploade eksport bogbestillinger fra Microsoft Forms i xlsx-format", type="xlsx") 

    
    if Bogbestillinger_file is not None:
        Bogbestillinger_data = pd.read_excel(Bogbestillinger_file, sep=';', na_filter=False)

        # Angivelse af start på konvertering af bruger
        min_value = Bogbestillinger_data["ID"][0]
        start_ID = st.number_input("Ved hvilken bogbestilling skal konverteringen starte?", min_value=min_value, value=min_value)

        # Fjerner bestillinger indtil angivede star
        for elem in range (0, len(Bogbestillinger_data)):
            if Bogbestillinger_data["ID"][elem] == start_ID:
                start_position = elem

        start_set = [x for x in range(0, start_position)]
        Bogbestillinger_data = Bogbestillinger_data.drop(start_set, axis=0)

        # Fjerner unødvendige kolonner
        Bogbestillinger_data.drop([
            "Færdiggørelsestidspunkt", 
            "Mail", 
            "Navn"
            ], axis=1, inplace=True)

        # Omdøber kolonner
        Bogbestillinger_data = Bogbestillinger_data.rename(columns={
            "Lærers initialer:" : "Lærer", 
            "Hvilken klasse/hold er klassesættet til?" : "Klasse",
            "Titel på bogen:" : "Titel",
            "Evt. bogens forfatter:" : "Forfatter",
            "Hvornår skal eleverne aflevere klassesættet? (Sæt en så realistisk afleveringsdato som muligt)" : "Afleveringsdato",
            "Hvornår skal klassesættet være klar til udlevering?" : "Udleveringsdato",
            "Yderligere kommentarer/ønsker:" : "Lærer kommentar"
            })
        
            
        for elem in range(start_position, len(Bogbestillinger_data)):
            Udleveringsdato = Bogbestillinger_data["Udleveringsdato"][elem]
            if Udleveringsdato == "Klassesættet skal være klar til skolestart i august":
                Bogbestillinger_data.loc[elem,"Udleveringsdato"] = "12/08/2020"
            elif Udleveringsdato == "Klassesættet skal være klar når de nye 1.g klasser træder i kraft efter grundforløbet":
                Bogbestillinger_data.loc[elem,"Udleveringsdato"] = "30/10/2020"
            

        # Indstætter kolonne til senere indtastning
        tom_kolonne = ['' for x in range(0, len(Bogbestillinger_data))]
        Bogbestillinger_data.insert(8, 'Udlånt', tom_kolonne)

        # finder sidste ID
        slut_position = Bogbestillinger_data["ID"][len(Bogbestillinger_data)-1]
        
        # Eksporter til skrivebord
        st.write(Bogbestillinger_data)
        if st.button("Gem konverterede bogbestillinger på skrivebordet."): 
            Filnavn = 'Bogbestillinger(' + str(start_ID) +'-'+ str(slut_position) + ').xlsx'
            save_name = os.path.join(os.path.expanduser("~"), "Desktop", Filnavn)
            Bogbestillinger_data.to_excel(save_name,header=False, index=False, merge_cells=False)

            st.success("Dokumentet er gemt på skrivebodet med navnet: '" + str(Filnavn) + "'")


            # Ændrer kolonnebredden i kolonnen med tidspunkt (https://stackoverflow.com/questions/13197574/openpyxl-adjust-column-width-size)
            import openpyxl as xl
            work_book = xl.load_workbook(save_name)
            sheet = work_book['Sheet1']
            column_number = 2
            column = str(chr(64 + column_number))
            sheet.column_dimensions[column].width = 20
            work_book.save(save_name)