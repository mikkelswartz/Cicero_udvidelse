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
import shutil

def write():
    st.header("Stregkodegenererator til delehold")
    
    if st.checkbox("Vis hjælp til at lokalisere elevoversigt fra Cicero og Lectio"):
        st.info(
            "__Elevoversigt fra Cicero:__  \n"
            "Start med at uploade en elevoversigt fra cicero.  \n"
            "Åben Cicero og gå til 'Cirkulation' --> 'Låner'.  \n"
            "Angiv alle klasser under 'Lånergrupper' og søg.  \n"
            "Tryk på 'Print og eksporter' i venstre hjørne og vælg 'Eksporter viste: CSV'.  \n"
            "  \n"
            "__Elevoversigt fra Lectio:__  \n"
            "Log ind på Lectio.  \n"
            "Gå til 'Hovedmenu' og vælg 'Importer/Eksporter data'.  \n"
            "Tryk på 'Excel' under kolonnen 'Eksporter' ud fra rækken 'Elever'."
            )

    # upload fra Cicero
    st.write("__Upload elevoversigt fra Cicero__")
    Elever_Cicero_file = st.file_uploader("Uploade eksport af fuld elevoversigt fra Cicero i csv-format", type="csv") 


    if Elever_Cicero_file is not None:
        Elever_Cicero_data = pd.read_csv(Elever_Cicero_file, sep=';', na_filter=False)
        Elever_Cicero_data.drop([
            "Adresse", 
            "Postnummer & by", 
            "Telefon",
            "E-mail"
            ], axis=1, inplace=True)
        Elever_Cicero_data = Elever_Cicero_data.rename(columns={"Lånergrupper" : "Stamklasse"})
        
        if st.checkbox("Vis elevoversigt fra Cicero"):
            st.write(Elever_Cicero_data)


    # upload fra Lectio
    st.write("__Upload elevoversigt fra Lectio__")
    Elever_Lectio_file = st.file_uploader("Uploade eksport af fuld elevoversigt fra Lectio i xlsx-format", type="xlsx") 

    if Elever_Lectio_file is not None:
        Elever_Lectio_data = pd.read_excel(Elever_Lectio_file, sep=';', na_filter=False)
        Elever_Lectio_data.drop([
            "Id", 
            "PNr", 
            "Afdeling", 
            "Brugernavn", 
            "CPR-NUMMER", 
            "TELEFON 1", 
            "TELEFON 2", 
            "Adresse CO",
            "Adresse",
            "Stednavn",
            "Postnummer",
            "Kommunenr",
            "Email"
            ], axis=1, inplace=True)
        Elever_Lectio_data = Elever_Lectio_data.rename(columns={"KaldeNavn" : "Navn"})
        
        if st.checkbox("Vis elevoversigt fra Lectio"):
            st.write(Elever_Lectio_data)

        st.write("__Hvilke holdoversigter ønskes genereret?__")
        # Lav oversigt over alle delehold
        Hold = set()
        for line in Elever_Lectio_data["Hold"]:
            Hold_temp = line.split(",")
            for elem in Hold_temp:
                if elem.startswith(" "):
                    Hold.add(elem[1:])
                else:
                    Hold.add(elem)
        Hold = list(Hold)
        Hold.sort()
        Valgte_hold = st.multiselect("Du kan vælge flere hold på én gang.", options=Hold)

        st.write("__Hvilke stamklasseoversigter ønskes genereret?__")
        # Lav oversigt over alle stamklasser
        Stamklasse = set()
        for line in Elever_Lectio_data["Stamklasse"]:
            Stamklasse_temp = line.split(",")
            for elem in Stamklasse_temp:
                if elem.startswith(" "):
                    Stamklasse.add(elem[1:])
                else:
                    Stamklasse.add(elem)
        Stamklasse = list(Stamklasse)
        Stamklasse.sort()
        Valgte_Stamklasse = st.multiselect("Du kan vælge flere stamklasser på én gang.", options=Stamklasse)

        
    # Generer stregkoder
    if Elever_Cicero_file and Elever_Lectio_file is not None and len(Hold) != 0:
        #generate_barcodes(Elever_Cicero_data, Elever_Lectio_data, Valgte_hold)

        # Lav en sammensat dataframe af de to uploadede filer
        Elever_merged_data = pd.merge(Elever_Cicero_data,Elever_Lectio_data, on=["Navn"])
        #Elever_merged_data = pd.merge(Elever_Cicero_data,Elever_Lectio_data, on=["Navn", "Stamklasse"])
        Elever_merged_data = Elever_merged_data.sort_values("Navn", axis=0)
        #Elever_merged_data = Elever_merged_data.sort_values("Navn", axis=0, ignore_index=True)
        if st.checkbox("Vis samlet elevoversigt"):
            st.write(Elever_merged_data)

        # Find elever som ikke eksisterer i begge filer
        Elever_med_fejl = pd.concat([Elever_Cicero_data,Elever_Lectio_data]).drop_duplicates(subset = ['Navn'], keep=False)
        #Elever_med_fejl = pd.concat([Elever_Cicero_data,Elever_Lectio_data]).drop_duplicates(subset = ['Navn','Stamklasse'], keep=False)

        if len(Elever_med_fejl) == 0:
            st.info("Der var ingen elever som kun var at finde i en enkelt fil.")
        elif len(Elever_med_fejl) != 0:
            st.warning("__Følgende elever var ikke at finde i begge filer:__")
            st.write(Elever_med_fejl)

        # Den resterende kode sættes i gang når brugeren ønsker det
        if st.button("Generer filer med stregkoder for de valgte hold"):
            # Genereate folder to barcodes
            try:
                os.mkdir('Barcodes')
            except OSError:
                print ("Creation of the directory %s failed" % path)

            # Generer stregkodeark for hvert af de valgte hold
            for hold in range(0,len(Valgte_Stamklasse)):

                # Generer dataframe hvor hvert af de valgte hold
                Valgt_hold_temp = pd.DataFrame(columns=["Navn", "Lånernummer", "Stamklasse", "Hold"])
                for row in range(0,len(Elever_merged_data["Stamklasse_y"])):
                    if Valgte_Stamklasse[hold] in Elever_merged_data["Stamklasse_y"][row]:
                        if len(Valgt_hold_temp) == 0:
                            Valgt_hold_temp = Elever_merged_data.loc[[row]]
                        elif len(Valgt_hold_temp) != 0:
                            Valgt_hold_temp = Valgt_hold_temp.append(Elever_merged_data.loc[[row]], sort=False, ignore_index=True)

                

                # Generer stregkolder for hvert af de valgte hold
                code39_class = barcode.get_barcode_class('code39')
                opts = {'module_width': 0.2, 'module_height':8.0 ,'font_size': 15, 'text_distance': 1}
                for elem in range(0, len(Valgt_hold_temp['Lånernummer'])):
                    Loannumber = Valgt_hold_temp['Lånernummer'][elem]
                    code39 = code39_class(str(Loannumber), writer=ImageWriter(), add_checksum=False)
                    save_code = code39.save('Barcodes/' + str(Loannumber), options=opts)


                ### Generer tom PDF ###
                dato = dt.date.today()
                Filnavn = str(Valgte_Stamklasse[hold]) + ' - ' + str(dato) + '.pdf'
                save_name = os.path.join(os.path.expanduser("~"), "Desktop", Filnavn)
                pdf = SimpleDocTemplate(
                    save_name,
                    pagesize=A4,
                    rightMargin=15, 
                    leftMargin=15, 
                    topMargin=15, 
                    bottomMargin=15
                )

                # Data for header
                header_data = [['Antal elever: ' + str(len(Valgt_hold_temp)), str(dato), str(Valgte_Stamklasse[hold])]]
                
                # List of list med navne og barcodes
                names = []
                images = []
                for elem in range(0, len(Valgt_hold_temp['Lånernummer'])):
                    # Data om navne
                    Navn =  Valgt_hold_temp["Navn"][elem]
                    names.append(Navn)
                    # Data om barcodes
                    Loannumber = Valgt_hold_temp['Lånernummer'][elem]
                    image = PIL.Image.open('Barcodes/' + str(Loannumber) + '.png')
                    width, height = image.size
                    image_Loannumber = Image('Barcodes/' + str(Loannumber) + '.png')
                    image_Loannumber.drawWidth = width/4
                    image_Loannumber.drawHeight = height/4
                    images.append(image_Loannumber)
           
                # Generer tabel ud fra List of list med navne og barcodes
                data = []
                start = 0
                slut = 3
                for elem in range(0, len(names),3):
                    data += [names[start:slut],images[start:slut]] 
                    start += 3
                    slut += 3 
                
                # Generer tabeller
                header = Table(header_data, colWidths = 2.55*inch)
                table = Table(data, colWidths = 2.55*inch)

                # table style header
                ts = TableStyle(
                    [
                    ('FONTSIZE',(0, 0), (-1, -1), 12),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('LEFTPADDING',(0,0),(-1,-1), 1),
                    ('RIGHTPADDING',(0,0),(-1,-1), 1),
                    ('BOTTOMPADDING',(0,0),(-1,-1), 10),
                    ('TOPPADDING',(0,0),(-1,-1), 5)
                    ]
                )
                header.setStyle(ts)

                # table style til stregkoder og navne
                ts = TableStyle(
                    [
                    ('FONTSIZE',(0, 0), (-1, -1), 9),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('LEFTPADDING',(0,0),(-1,-1), 1),
                    ('RIGHTPADDING',(0,0),(-1,-1), 1),
                    ('BOTTOMPADDING',(0,0),(-1,-1), 1),
                    ('TOPPADDING',(0,0),(-1,-1), 1)
                    ]
                )
                table.setStyle(ts)
                
                # Tilføj elemter til pdf
                elems = []
                elems.append(header)
                elems.append(table)
                pdf.build(elems)
            
            if len(Valgte_Stamklasse) == 1:
                st.success('Succes!  \n' + str(len(Valgte_Stamklasse)) + ' PDF-fil er genereret. Filerne er placeret på skrivebordet.')
            elif len(Valgte_Stamklasse) > 1:
                st.success('Succes!  \n' + str(len(Valgte_Stamklasse)) + ' PDF-filer er genereret. Filerne er placeret på skrivebordet.')
            elif len(Valgte_Stamklasse) == 0:
                st.error('Du mangler at vælge hvilke holdoversigter som ønskes genereret.')

            # Delete barcodes
            shutil.rmtree('Barcodes')








