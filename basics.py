import streamlit as st
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








def generate_barcodes(Elever_Cicero_data, Elever_Lectio_data, Selected_hold):
    pass
    
