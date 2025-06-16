import gspread
import datetime
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_dict = st.secrets["star_organizer_sheet"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(credentials_dict), scope)
client = gspread.authorize(creds)

sheet = client.open('star-organizer').sheet1
data = sheet.get_all_records()

st.set_page_config(page_title="📦 Package Organizer")
st.title("📦 Package Organizer")

tab1, tab2 = st.tabs(["➕ Add to Bin", "➖ Remove from Bin"])

with tab1:
    st.header("Add Package")

    with st.form("form_add"):
        cols = st.columns([2, 1, 2])
        line_number = cols[0].number_input("Line Number :", 1, 13)
        bin_number  = cols[2].number_input("Bin Number :", 1, 3)
        barcode = st.text_input("Scan Barcode :", key="barcode_input", placeholder="e.g., 125303_BLUE/GRAY_48_11")
        submit_add = st.form_submit_button("   Add   ")

        if submit_add:

            if barcode.strip() == '':
                st.error('🚨 Please enter the barcode.')
            elif len(barcode.split('_')) != 11:
                st.error('🚨 Please enter the barcode correctly.')
            elif barcode.strip() in [entry['CODE'] for entry in data]:
                st.error('🚨 You have already entered this barcode.')
            else:
                barcode_split = barcode.strip().split("_")

                now = datetime.datetime.now()
                now_str = now.strftime('%Y-%m-%d %H:%M:%S')  # Format it as string

                CODE = barcode.strip()
                STYLE_NO = barcode_split[0]
                LOT	= barcode_split[1]
                Null_NO = barcode_split[2]
                TAG_NO = barcode_split[3]
                COLOR = barcode_split[4]
                BUNDLE_NO = barcode_split[5]
                PART = barcode_split[6]	
                SIZE = barcode_split[7]	
                QUT	= barcode_split[8]
                START_NO = barcode_split[9]	
                END_NO = barcode_split[10]
                DATE_TIME_IN = now_str
                DATE_TIME_OUT = ''
                LINE_NO = int(line_number)
                BIN_NO = int(bin_number)
                STATUS = True

                row_input = [CODE, STYLE_NO, LOT, Null_NO, TAG_NO, COLOR, BUNDLE_NO, PART, SIZE, QUT, START_NO, END_NO, DATE_TIME_IN, DATE_TIME_OUT, LINE_NO, BIN_NO, STATUS]
                sheet.append_row(row_input) 

                st.success(f"✅ Successfully added the package to Bin {BIN_NO}.")

with tab2:
    st.header("Remove Package")
    
    with st.form("form_remove"):
        barcode_to_remove = st.text_input("Scan Barcode to Remove:", key="barcode_1")
        submit_remove = st.form_submit_button("Submit")

        if submit_remove:
            if barcode_to_remove.strip() == '':
                st.error('🚨 Please enter the barcode.')
            elif len(barcode_to_remove.split('_')) != 11:
                st.error('🚨 Please enter the barcode correctly.')
            elif barcode_to_remove not in [entry['CODE'] for entry in data]:
                st.error('🚨 This barcode is not in a bin.')
            else:
                column_b = sheet.col_values(1)
                row_index = column_b.index(barcode_to_remove) + 1 
                
                if sheet.cell(row_index, 17).value == 'FALSE':
                    st.error('🚨 This lot is already taken out from the bin.')
                else:
                    now = datetime.datetime.now()
                    now_str = now.strftime('%Y-%m-%d %H:%M:%S') 

                    sheet.update_cell(row_index, 14, now_str)
                    sheet.update_cell(row_index, 17, False)
                    st.success("✅ Successfully removed the package from the bin.")

