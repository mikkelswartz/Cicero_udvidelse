import streamlit as st
#import pdftotext
import re
import pandas as pd

Destination_main_file = "MTX-dataark.xlsx"
Destination_st_file = "df_selected_treatment.xlsx"

class MTX:
    def MTX_pandas_main_file(Destination_main_file):
        """
        Function:   Imports data from main excelark to a dataframe

        Input:
            [str]	A string that contains the destination of the main file.

        Output:
            [pandas.dataframe]	Pandas dataframe that contains the data from the excelark
        """
        # Reads dataframe from excel
        df = pd.read_excel(Destination_main_file, na_filter=False)

        # Remove "Unnamed: 0" collums from dataframe
        df.drop(["Unnamed: 0"], axis=1, inplace=True)

        return df






# This function is copyed from the awesome_streamlit package by Marc Skov Madsen
# https://github.com/MarcSkovMadsen/awesome-streamlit/blob/master/package/awesome_streamlit/shared/components.py
def write_page(page):  # pylint: disable=redefined-outer-name
    """Writes the specified page/module
    Our multipage app is structured into sub-files with a `def write()` function
    Arguments:
        page {module} -- A module with a 'def write():' function
    """
    # _reload_module(page)
    page.write()

def hide_streamlit_style():
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def custom_footer():
    """ Makes a custom footer """ 
    custom_footer = """
        <style>
            body { 
                margin: 0; 
                font-family: Arial, Helvetica, sans-serif;
            } 
            .footer {
                position: fixed;
                padding: 10px;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #fafafa;
                color: #262730;
                text-align: center;
                font-size: small;
                z-index: 95
            }
        </style>

        <div class="footer">
            Cicero Udvidelse - Et program udviklet Mikkel Swartz
        </div>
    """
    st.markdown(custom_footer, unsafe_allow_html=True) 

# The two following functions makes is possible to change the width of the content.
def sidebar_settings():
    """Add selection section for setting setting the max-width and padding
    of the main block container"""
    max_width_100_percent = st.sidebar.checkbox("Maks bredde?", False)
    if not max_width_100_percent:
        max_width = st.sidebar.slider("Vælg maks bredde i px", 100, 2500, 900, 100)
    else:
        max_width = 900

    _set_block_container_style(max_width, max_width_100_percent)


def _set_block_container_style(max_width: int = 900, max_width_100_percent: bool = False):
    """## Helper Function to set the max width of the main block container"""
    if max_width_100_percent:
        max_width_str = f"max-width: 95%;"
    else:
        max_width_str = f"max-width: {max_width}px;"
    st.markdown(
        f"""
        <style>
        .reportview-container .main .block-container{{
            {max_width_str}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )






def PDF_to_list_of_strings(pdf):
    ################################################
    ### Read pdf and convert to a list of strings ###
    #################################################
    # Initialize 
    pdflines = list()       # List to contain lines from pdf
    templine = ""               # Temporary string to 'pdflines'
    
    # Iterate over all the pages
    for page in pdf:
        # Iterate over characters 
        for elem in page:
        
            # Add next character if tempeary line is not empty 
            if templine != "":
                
                # If the last character in the tempeary line is not a whitespace
                # then append the the character to the tempeary line
                if templine[-1] != " ":
                    templine += elem
                
                # If the last character in the tempeary line is a whitespace and the character
                # is not a whitespace then append the the character to the tempeary line
                if templine[-1] == " ":
                    if elem != " ":
                        templine += elem
            
            # Skip first character if it is a whitespace
            if templine == "":
                if elem != " ":
                    templine += elem
    
        # Append temporary line to the list 'pdflines' and reset temporary line
            if elem == "\n":
                pdflines.append(templine[:-1])
                templine = ""
    return pdflines


def extract_data_from_pdflines(pdflines):
    Inputdata = [[], [], [], dict()] #klasse - laan - for gamle laan - book titles
    Class_counter = -1
    Return_date = 20200701
    
    # Iterate over all the lines
    for line in pdflines:
        
        # Find Student name and class
        Class_name_search = re.search(r"^(20\d{2}[eimst]),\s(.+)", line)
        Entry_Class_name_search = re.search(r"^(GF\d),\s(.+)", line)
        Class_udgaaet_search = re.search(r"^(Udgaaet),\s(.+)(\s\\)", line)
        
        # Finds out what type of class the student haves and
        # Make the an universal studen data variable
        if Class_name_search is not None:
            Student_data_search = Class_name_search
        elif Entry_Class_name_search is not None:
            Student_data_search = Entry_Class_name_search
        elif Class_udgaaet_search is not None:
            Student_data_search = Class_udgaaet_search
        
        
        """
        student_data_contracter(Class_name_search)
        print(Inputdata)
        
        """
        # If line contains student name and class:
        if Class_name_search is not None:
            # Make variable with student name and class
            Class_name = Class_name_search.group(1)
            student_name = Class_name_search.group(2)[:-2]
            
            #################### for testing ####################
            #print(student_name)
            ####################             ####################
            
            # If it is the first student in a class, expent the Inputdata to make room for a new class
            if Class_name not in Inputdata[0]:
                Inputdata[0].append(Class_name)
                Inputdata[1].append(0)
                Inputdata[2].append(0)
                Class_counter += 1
        
        
        # If class is "udgaaet"
        elif Class_udgaaet_search is not None:
            # Make variable with student name and class
            Class_name = Class_udgaaet_search.group(1)
            student_name = Class_udgaaet_search.group(2)
            
            #################### for testing ####################
            #print(student_name)
            ####################             ####################
            
            
            # If it is the first student in a class, expent the Inputdata to make room for a new class
            if Class_name not in Inputdata[0]:
                Inputdata[0].append(Class_name)
                Inputdata[1].append(0)
                Inputdata[2].append(0)
                Class_counter += 1
        
    
        # Find books
        book = re.search(r"^(.+)\s(\d{5,6})\s([sk0-9\.]*\s)?(\d{2}-\d{2}-20\d{2})\s((\d{2})-(\d{2})-(20\d{2}))", line)
        if book is not None:
            dato_check = int(book.group(8) + book.group(7) + book.group(6))
            # Add 1 to the klasse and navn laan
            Inputdata[1][Class_counter] += 1
            # Add 1 to old laan
            if dato_check <= Return_date:
                Inputdata[2][Class_counter] += 1
            # Add booktitle to dict of books
            book_title = book.group(1)
            if book_title in Inputdata[3]:
                Inputdata[3][book_title] += 1 # [student_name]
            else:
                Inputdata[3][book_title] = 1 #= 1 #[student_name]
    return Inputdata


def printerfunction_by_class(Inputdata):
    #print(Inputdata[2])
    
    st.write("Klasse \tLaan \tFor gamle laan\t% for gamle")
    for aagang in range(0, 14, 5):
        for k in range(0, 5):
            st.write(Inputdata[0][aagang+k], Inputdata[1][aagang+k], Inputdata[2][aagang+k], "", round((Inputdata[2][aagang+k]/Inputdata[1][aagang+k])*100,2), sep="\t")
        
        Klasse_laan  = Inputdata[1][aagang+k-4]+Inputdata[1][aagang+k-3]+Inputdata[1][aagang+k-2]+Inputdata[1][aagang+k-1]+Inputdata[1][aagang+k]
        Klasse_gamle = Inputdata[2][aagang+k-4]+Inputdata[2][aagang+k-3]+Inputdata[2][aagang+k-2]+Inputdata[2][aagang+k-1]+Inputdata[2][aagang+k]
        Klasse_procent = round((Klasse_gamle/Klasse_laan)*100,2)
        st.write("Sum:", Klasse_laan, Klasse_gamle, "", Klasse_procent, sep="\t")
        st.write()
    
    st.write("Gym laan:\t", sum(Inputdata[1]))
    st.write("Gamle Gym laan:\t", sum(Inputdata[2]))
    st.write("% for gamle:\t", round((sum(Inputdata[2])/sum(Inputdata[1]))*100,2))

def printerfunction_by_class_pandas(Inputdata):
    pass
    #print(Inputdata[2])
    
    df_klasser = pd.DataFrame(columns=['Klasse', 'Lån', 'For gamle lån', '% for gamle'])
    
    for Klasse in range(0, len(Inputdata[0])):

        # st.write(Inputdata[0][aagang], Inputdata[1][aagang], Inputdata[2][aagang], round((Inputdata[2][aagang]/Inputdata[1][aagang])*100,2), sep="\t")

        df_klasser.loc[Klasse, "Klasse"] = Inputdata[0][Klasse]
        df_klasser.loc[Klasse, "Lån"] = Inputdata[1][Klasse]
        df_klasser.loc[Klasse, "For gamle lån"] = Inputdata[2][Klasse]
        df_klasser.loc[Klasse, "% for gamle"] = round((Inputdata[2][Klasse]/Inputdata[1][Klasse])*100,2)

    df_årgange = pd.DataFrame(columns=['Årgang', 'Lån', 'For gamle lån', '% for gamle']) 
    Klassetæller = 0

    #st.write(df_årgange["Årgang"])
    #st.write(df_klasser["Klasse"])
    # if "2017e" in df_klasser["Klasse"][0]:
    #     st.success("")

    st.table(df_klasser)



    # # st.error("")
    # # Laver en sum for hver årgang
    # for klasse in range(0, len(df_klasser["Klasse"])):
    #     årgang = ((str(df_klasser["Klasse"][klasse])[:-1]))
        #st.write(årgang)
        # if klasse == 0:
        #     df_årgange.loc[klasse, 'Årgang'] = årgang
        # else:
        #     st.write(df_årgange["Årgang"])
        #     #ast.write(klasse)
        #     #st.write(klasse)
        #     #st.write(df_årgange.isin({'Årgang':[årgang]}))
        #     #if årgang not in df_klasser["Klasse"][klasse]:
        #     if df_årgange.isin({'Årgang':[årgang]}) is True:
        #         st.write(årgang)
        #         #st.write(df_klasser["Klasse"][klasse])
        #         #df_årgange.loc[klasse, "Årgang"] = årgang




        #st.write(årgang)

        # if årgang not in df_årgange["Årgang"][Klassetæller]:
        #     df_årgange.loc[Klassetæller, "Årgang"] = årgang

        #     st.write(Klassetæller)
        #     st.write(årgang)

        #     Klassetæller += 1
            


    #st.write(df_årgange)


    # Klasse_laan  = Inputdata[1][årgang+k-4]+Inputdata[1][årgang+k-3]+Inputdata[1][årgang+k-2]+Inputdata[1][årgang+k-1]+Inputdata[1][årgang+k]
    # Klasse_gamle = Inputdata[2][årgang+k-4]+Inputdata[2][årgang+k-3]+Inputdata[2][årgang+k-2]+Inputdata[2][årgang+k-1]+Inputdata[2][årgang+k]
    # Klasse_procent = round((Klasse_gamle/Klasse_laan)*100,2)
    # st.write("Sum:", Klasse_laan, Klasse_gamle, "", Klasse_procent, sep="\t")
    # st.write()
    
    #st.write(df_klasser)

    st.write("Gym lån:\t", sum(Inputdata[1]))
    st.write("Gamle Gym lån:\t", sum(Inputdata[2]))
    st.write("% for gamle:\t", round((sum(Inputdata[2])/sum(Inputdata[1]))*100,2))


def generate_barcodes(Elever_Cicero_data, Elever_Lectio_data, Selected_hold):
    pass
    
