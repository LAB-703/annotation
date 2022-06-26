import streamlit as st
import streamlit.components.v1 as components
from urllib import parse
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import clipboard
import pandas as pd

@st.cache(allow_output_mutation=True, persist=True)
def get_data(): #사용자로부터 데이터를 받을 때 
    return []

#[theme]
#base="light"
#primaryColor="#4b4bcb"
#secondaryBackgroundColor="#dae4f7"

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'accept' : "*/*",
    'accept-encoding' : 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}


#나중에 배포 전에 손 볼 것들 
st.set_page_config(page_title="척척 석박의 기사 인용 도우미",          
    page_icon="🤪",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/LAB-703',
        'Report a bug': "https://github.com/LAB-703",
        'About': '''SPDX-FileCopyrightText: © 2022 Lee Jeong Min
        SPDX-License-Identifier: BSD-3-Clause'''
    }
)

#전체 폰트 
st.markdown("""
        <style>
@font-face {
  font-family: 'Pretendard';
  font-style: normal;
  font-weight: 400;
  src: url(https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css) format('woff');
}
    html, body, [class*="css"]  {
    font-family: 'Pretendard';
    font-size: 20px;
    }
    </style>""",unsafe_allow_html=True)


with st.sidebar:
    select_event = st.sidebar.selectbox("🎈", ("👀 척척 석박의 기사 인용 도우미", "📜 학술지","⏳ 진행 중"))
if select_event == "👀 척척 석박의 기사 인용 도우미":
    st.markdown('<p align="center" style=" font-size: 140%;"><b>👀 척척 석박들을 위한 기사 인용 도우미</b></p>', unsafe_allow_html=True)

    URL=st.text_input("네이버/다음 뉴스 url을 입력해주세요.")
    col1,col2=st.columns([5,5])  
    with col1:
        STYLE=st.radio("인용 스타일을 선택해주세요.",
             ('APA', 'CHICAGO', 'OTHERS'))
        final_search=st.checkbox('최종 검색일 추가')
        submit=st.button('복사')
    with col2:
        if STYLE=="OTHERS":
            option = st.selectbox('찾으시는 학술지가 있나요?',['Email', 'Home phone', 'Mobile phone'])
    if submit==True:
            if URL.find("n.news.naver.com/")>0 or URL.find("news.v.daum.net/")>0 :
                req =requests.get(URL,headers=headers)
                html_doc = req.text  
                soup = bs(html_doc, 'html.parser')
                TITLE=soup.find("h2",{"class":"media_end_head_headline"}).get_text()
                DATE_retrieve=datetime.now().strftime("%Y.%m.%d")
                DATE_write=soup.find("span",{"class":"media_end_head_info_datestamp_time _ARTICLE_DATE_TIME"}).get_text()[:10]
                DATE_modify=soup.find("span",{"class":"media_end_head_info_datestamp_time _ARTICLE_MODIFY_DATE_TIME"}).get_text()[:10]
                AUTHOR=soup.find("em",{"class":"media_end_head_journalist_name"}).get_text().split()[0]
                COMPANY=soup.find("em",{"class":"media_end_linked_more_point"}).get_text()
                APA=AUTHOR+". "+"("+DATE_write+"). "+TITLE+". "+COMPANY+". "+URL
                CHICAGO=AUTHOR+', "'+TITLE+'" '+COMPANY+", "+DATE_write+", "+URL
                if final_search:
                    APA=APA+", 최종검색일: "+str(datetime.now().strftime("%Y.%m.%d."))
                    CHICAGO=CHICAGO+", 최종검색일: "+str(datetime.now().strftime("%Y.%m.%d."))
                if STYLE=="APA":
                    clipboard.copy(APA)
                    st.write('복사오나료!, 붙여넣기하세요.')
                elif STYLE=="CHICAGO":
                    clipboard.copy(CHICAGO)
                    st.write('복사오나료!, 붙여넣기하세요.')
            else :
                st.error('네이버/다음 포털뉴스의 링크가 아닙니다!')
                    
    
if select_event == "📜 학술지":
    st.write('쿠쿠ㅜ르삥ㅃ오')                                    
if select_event == "⏳ 진행 중":
    st.write('어쩔티비')