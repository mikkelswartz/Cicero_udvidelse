#!/usr/bin/env python3

import streamlit as st
from basics import *


import pdfplumber
import PyPDF2
# Hvis pdftotext skal benyttes, så se her: https://www.activestate.com/resources/quick-reads/how-to-install-python-packages-using-a-script/

import datetime as datetime

def write():    
    st.header("Udlånsoversigt per klasse")

    st.subheader("Her kan du uploade en samlet udlånsoversigt for alle elever, "
        "hvorefter der genereres en oversigt over hvor mange bøger der lånt i alt "
        "og hvor mange bøger der er forgamle for hver enkelt klasse."
        )
    if st.checkbox("Vis hjælp til at lokalisere udlånsoversigt fra Cicero"):
        st.info(
            "__Ændre printeropsætning__"
            "Åben Cicero og gå til 'Admin' --> 'Klientopsætning' --> 'Printer'. \n"
            "Sæt 'A4 print' til at være 'Microsoft Print to PDF'. \n\n"

            "__Eksporter udlånsliste__ \n"
            "Gå til 'Liser' --> 'Udlån'.  \n"
            "Angiv alle klasser under 'Lånergrupper'. \n"
            "Sørg for at der Ikke er flueben ved 'Inkludér kun overskedne lån' "
            "og at der er flueben ved 'Medtag langtidslån'.  \n"
            "Tryk 'Print' og gem filen et sted hvor du kan finde den."
            )


    pdf_file_name = st.file_uploader("Uploade din PDF-fil med laanerudskrifter", type="pdf")
    #pdf_file_name = "AUdvikling/Udskift-2020-05-27.pdf"
    #pdf_file_name = 'AUdvikling/sample6.pdf'

    threshold_date = st.date_input("Hvilken dage skal sættes som grænse for 'for gamle' bøger?")
    
    if pdf_file_name is not None:
        
        # The next function is cached to speed up the reading 
        # and formatting of the raw input.
        @st.cache
        def load_and_clean_data(pdf_file_name):
            """
            The function takes the pdf_file_name as input and reads the file.
            The data is formatted and collected in two dataframes.
            The dataframe (Inputdata_pandas_by_class) contains data for each class.
            """
            pdf_text = pdftotext.PDF(pdf_file_name)
            pdflines = PDF_to_list_of_strings(pdf_text)
            
            Inputdata_pandas = extract_data_from_pdflines_pandas(pdflines)

            # Convert dates to datetime format
            Inputdata_pandas["Afleveringsdato"] = pd.to_datetime(Inputdata_pandas["Afleveringsdato"]).dt.date
            Inputdata_pandas["Udlånsdato"] = pd.to_datetime(Inputdata_pandas["Udlånsdato"]).dt.date

            ### test
            #st.write(Inputdata_pandas)
            ### test

            # Make new columns for "old" and all books
            Inputdata_pandas["For gamle"] = np.where(Inputdata_pandas['Afleveringsdato'] < threshold_date, 1, 0)
            Inputdata_pandas["I alt"] = 1

            ### test
            #st.write(Inputdata_pandas)
            ### test

            # Make new dataframe grouped by class
            Inputdata_pandas_by_class = Inputdata_pandas.groupby(['Klasse'])['I alt', 'For gamle'].agg(['sum'])
            Inputdata_pandas_by_class.columns = Inputdata_pandas_by_class.columns.droplevel(1)

            # Calculate and format percentage for old books
            Inputdata_pandas_by_class["Procent for gamle"] = Inputdata_pandas_by_class["For gamle"]/Inputdata_pandas_by_class["I alt"]*100
            Inputdata_pandas_by_class["Procent for gamle"] = Inputdata_pandas_by_class["Procent for gamle"].map('{:,.2f}'.format)

            return Inputdata_pandas_by_class

        Loans_by_class = load_and_clean_data(pdf_file_name)

        # Show overview for all classes
        st.markdown("Det er er muligt at sortere rækkerne efter kolonne ved at trykke på kolonnenavnet.")
        st.dataframe(Loans_by_class, width=1000, height=2000)
        if st.checkbox("Hvis kopieringsvenlig tabel",key="Loans_by_class"):
            st.table(Loans_by_class)
        

        def calculate_sum(classes_to_sum_df, index_name):
            """
            This function calculate the sum for the loans in each column.
            The classes_to_sum_df is the dataframe to be summarized.
            The index_name is the index name the will be used in the index.
            """
            # Calculate the sum for each column
            Loan_old = classes_to_sum_df["For gamle"].sum()
            Loan_sum = classes_to_sum_df["I alt"].sum()
            Percentage_old_sum = '{:,.2f}'.format((Loan_old/Loan_sum)*100)

            # Show the summed overview (total)
            Sum_by_class_columns= ["I alt", "For gamle", "Procent for gamle"]
            Sum_by_class = pd.DataFrame(np.array([[Loan_sum,Loan_old,Percentage_old_sum]]))
            Sum_by_class.columns = Sum_by_class_columns
            Sum_by_class.index = [str(index_name)]
            #st.write(Summariced_by_class)
            return Sum_by_class


        # Find the names of each class and find years and lines 
        Classes_all = sorted(set(Loans_by_class.index))
        Classes_years = sorted(set([i[:-1] for i in Classes_all]))
        Classes_lines = sorted(set([i[-1:] for i in Classes_all]))

        # Select which lines that are HF classes
        HF = st.multiselect("Hvilke klasser er HF-klasser?", Classes_lines)
        st.markdown("Hvis HF klasser ikke er angivet, men er tilstede i udlånslisten, vil klassen blive " 
            "indregnet som en del af den årgang som matcher."
            )

        # Find STX lines (the ones that is not selected as HF)
        STX = []
        for i in Classes_lines:
            STX.append(i)
        if len(HF) != 0:
            for i in HF:
                STX.remove(i)

        # Find HF class names
        HF_classes = list()
        for year in Classes_years:
            HF_classes.append([year+i for i in HF if year+i in Classes_all])
        # Flatten list
        HF_classes = [item for sublist in HF_classes for item in sublist]

        # Find STX class names
        STX_classes = list()
        for year in Classes_years:
            STX_classes.append([year+i for i in STX if year+i in Classes_all])
        # Flatten list
        STX_classes = [item for sublist in STX_classes for item in sublist]

        # Make dataframe for STX classes
        Loans_by_class_STX = Loans_by_class
        if len(HF_classes) != 0:
            for i in HF_classes:
                #st.write(i)
                Loans_by_class_STX = Loans_by_class_STX.drop(index=i)

        # Make dataframe for HF classes
        Loans_by_class_HF = Loans_by_class
        for i in STX_classes:
            #st.write(i)
            Loans_by_class_HF = Loans_by_class_HF.drop(index=i)


        # summarize by year for STX
        Summariced_by_year_STX = pd.DataFrame(columns=["I alt", "For gamle", "Procent for gamle"])
        for year in Classes_years:
            temp_year_df = pd.DataFrame(columns=["I alt", "For gamle", "Procent for gamle"])
            for row in Loans_by_class_STX.index:
                if row[:-1] == year:
                    temp_year_df = temp_year_df.append(Loans_by_class_STX.loc[[row]])

            Summariced_by_year_STX = Summariced_by_year_STX.append(calculate_sum(temp_year_df, str(year)))
        
        # summarize by year for HF
        Summariced_by_year_HF = calculate_sum(Loans_by_class_HF, "HF")

        # summarize for alle
        Summariced_Total = calculate_sum(Loans_by_class, "Total")
                    
        # dataframe for summarized
        Summariced = Summariced_by_year_STX
        if len(HF_classes) != 0:
            Summariced = Summariced.append(Summariced_by_year_HF)
        Summariced = Summariced.append(Summariced_Total)
        st.dataframe(Summariced)
        if st.checkbox("Hvis kopieringsvenlig tabel",key="Summariced"):
            st.table(Summariced)














        # PDFplumber
        """
        pdf = pdfplumber.open(pdf_file_name)
        st.write(pdf)
        
        with pdfplumber.open(r"AUdvikling/sample6.pdf") as pdf:
            first_page = pdf.pages[0]
            st.write(first_page.extract_text())
        
        with pdfplumber.open(pdf_file_name) as pdf:
            for i in range(0,len(pdf.pages)):
                page = pdf.pages[i]
                text = page.extract_text()
                st.write(text)
        """
            
        # PyPDF2
        """
        pdf = open(pdf_file)
        read_pdf = PyPDF2.PdfFileReader(pdf, 'rb')
        number_of_pages = read_pdf.getNumPages()
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        st.write(page_content)
        """
        
        # PyPDF2
        """
        pdf_file = open(pdf_file_name, 'rb')
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        #number_of_pages = read_pdf.getNumPages()
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        st.write(page_content.encode('utf-8'))
        st.write("Stop")
        """


