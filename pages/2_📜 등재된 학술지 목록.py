import streamlit as st
import streamlit.components.v1 as components
from urllib import parse
import requests
from datetime import datetime, timedelta
from pytz import timezone
import google_auth_httplib2
import httplib2
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from googleapiclient import discovery

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
hide_menu='''
<style>
#MainMenu {
    visibility:hidden;
}
#document{
    font-family:'Pretendard JP Variable', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Emoji', sans-serif;
    }
footer {
    visibility:visible;
    size: 10%;
    font-family: 'Pretendard JP Variable';
}
footer:after{
    content: 'SPDX-FileCopyrightText: © 2022 LAB-703 SPDX-License-Identifier: MIT';
    font-size: 30%;
    display:block;
    position:relative;
    color:silver;
    font-family: 'Pretendard JP Variable';
}
code {
    color: #C0504D;
    overflow-wrap: break-word;
    background: linen;
    font-family: 'Source Code Pro';
}
#root > div:nth-child(1) > div > div > a {
    visibility:hidden;
}    
    
    
div.stButton > button:first-child {
font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
  font-size:100%;
    background-color: #FCF9F6;
    font-color: #C0504D;
    
}
button.css-jgupqz.e10mrw3y2 {
    opacity: 0;
    height: 2.5rem;
    padding: 0px;
    width: 2.5rem;
    transition: opacity 300ms ease 150ms, transform 300ms ease 150ms;
    border: none;
    background-color: #C0504D;
    visibility: visible;
    color: rgba(0, 0, 0, 0.6);
    border-radius: 0.75rem;
    transform: scale(0);
}
div.viewerBadge_link__1S137 {
    display:none;
    background-color: #C0504D;
}
div.css-j7qwjs.e1fqkh3o5 {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
}
a.viewerBadge_container__1QSob {
    z-index: 50;
    font-size: .875rem;
    position: fixed;
    bottom: 0;
    right: 0;
    display: none;
}
div.streamlit-expanderHeader.st-ae.st-bq.st-ag.st-ah.st-ai.st-aj.st-br.st-bs.st-bt.st-bu.st-bv.st-bw.st-bx.st-as.st-at.st-by.st-bz.st-c0.st-c1.st-c2.st-b4.st-c3.st-c4.st-c5.st-b5.st-c6.st-c7.st-c8.st-c9 {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
    font-weight: 300;
    font-size: initial;
}
div.st-dc.st-ci.st-dd.st-de.st-df.st-co.st-dg.st-dh.st-di {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
}
div.streamlit-expanderContent.st-ae.st-af.st-ag.st-ah.st-ai.st-aj.st-bt.st-br.st-cf.st-eh.st-bw.st-bx.st-as.st-at.st-by.st-bz.st-c0.st-c1.st-ch.st-ci.st-am.st-ei.st-cl.st-b1.st-cm.st-b3.st-c7.st-c8.st-c9 {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
}
</style>
'''

st.markdown(hide_menu, unsafe_allow_html=True)

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1Ym2nbTDvApMRUErsPoT4frr_-6TAZY2gzrX2sfgaWLg"
SHEET_NAME = "Database"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

#https://docs.google.com/spreadsheets/d/1Ym2nbTDvApMRUErsPoT4frr_-6TAZY2gzrX2sfgaWLg/edit?usp=sharing
@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    service = discovery.build('sheets', 'v4', credentials=credentials)
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df

def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:E",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()

gsheet_connector = connect_to_gsheet()

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
      'DOT4':'.',
      'left quote':'"',
      'right quote':'"'}
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

#    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
#    st.dataframe(get_data(gsheet_connector))
