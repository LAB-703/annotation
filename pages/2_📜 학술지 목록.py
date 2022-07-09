import streamlit as st
import streamlit.components.v1 as components
from urllib import parse
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import clipboard
import random
import pandas as pd
from pytz import timezone
import google_auth_httplib2
import httplib2
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from googleapiclient import discovery

st.markdown('<p align="center" style=" font-size: 140%;"><b>📜 등재된 학술지 목록</b></p>', unsafe_allow_html=True)
journal_df=get_data(gsheet_connector)
journal_list = st.selectbox('',list(journal_df['학술지']))                    #-1 때문에 마지막 열 받아올 수 있었음 🟡
st.markdown(str(journal_df.iat[journal_df.loc[journal_df.학술지==journal_list].index[0]-1,1]), unsafe_allow_html=True)
#if journal_list==
st.write("---")
st.write(" ")
expander = st.expander("학술지 추가를 원하신다면 클릭하세요.")
journal=expander.text_input("추가할 학술지의 정식 한글 명칭을 입력해 주세요.")
col1,col2=expander.columns([5,5])  
with col1:
    st.markdown("[![Foo](https://www.kci.go.kr/kciportal/resources/newkci/image/kor/title/h1_logo.png)](https://www.kci.go.kr/kciportal/po/search/poSereSear.kci)")
with col2:
    st.markdown('<p style=" font-size: 90%; color:silver"> 🔍 학술지 검색이 가능합니다.</p>', unsafe_allow_html=True)
dic = {'AUTHOR':'기자',
   'TITLE': '기사 제목',
   'COMPANY': '언론사', 
   'DATE_write':'기사작성일',
   'URL' :'기사 URL',
   'FINAL_SEARCH':'최종검색일',
       'LEFT':'(',
    'RIGHT':')',
       'COMMA1':',',
       'COMMA2':',',
       'COMMA3':',',
      'DOT1':'.',
      'DOT2':'.',
      'DOT3':'.',
      'DOT4':'.'}
multiselect= expander.multiselect('순서대로 놓아주세요.',
                            list(dic.values()), 
                            list(dic.values())[:2]) #default
annotation=""
for selection in multiselect:
    if selection in list(dic.values())[:6]:
        annotation+=selection
    elif selection in list(dic.values())[6]:
        annotation+=" "+selection
    else :
        annotation+=selection+" "
expander.markdown(annotation)
TODAY = str(datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S"))
submitted = expander.button("추가")

if submitted:
    if journal=="":
        expander.error('❗ 학술지 한글 명칭을 입력해 주세요.')
        st.stop()
    else:   
        add_row_to_gsheet(
        gsheet_connector,
        [[journal, annotation,TODAY]],
        )
        gsheet_connector = connect_to_gsheet()
        expander.success("추가되었습니다! 👀 기사 인용 도우미 페이지에서 확인할 수 있습니다.")
        expander.balloons()    

    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(gsheet_connector))
