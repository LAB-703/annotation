import streamlit as st
import streamlit.components.v1 as components
from urllib import parse
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import clipboard
import random
import pandas as pd
import google_auth_httplib2
import httplib2
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from dateutil import tz

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1Ym2nbTDvApMRUErsPoT4frr_-6TAZY2gzrX2sfgaWLg"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
SHEET_NAME = ["Database", "reaction"]
timezone = tz.tzlocal()


@st.experimental_singleton(show_spinner=False, suppress_st_warning=True) #구글 시트 연결
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
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME[0]}!A:C",
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
        range=f"{SHEET_NAME[0]}!A:B",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()
    
def random_emoji():
    emojis = ["💖","🧡","💛","💚","💙","💜","🤎","🖤"]  
    st.session_state.emoji = random.choice(emojis)

gsheet_connector = connect_to_gsheet()

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}


#전체 페이지
st.set_page_config(page_title="척척 석박의 기사 인용 도우미",          
    page_icon="👀",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/LAB-703',
        'Report a bug': "https://github.com/LAB-703",
        'About': '''SPDX-FileCopyrightText: © 2022 LAB-703 SPDX-License-Identifier: MIT'''
    }
)

#전체 폰트 

st.markdown("""
        <style>
@font-face {
  font-family: 'Pretendard';
  font-style: normal;
  font-weight: 800;
  src: url(https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard-dynamic-subset.css) format('woff');
}
    html, body, [class*="css"]  {
    font-family: 'Pretendard';
    font-size: 20px;
    }
    </style>""",unsafe_allow_html=True)

#버튼
st.markdown("""
<style>
div.stButton > button:first-child {
  font-family: 'Pretendard';
  font-size:70%;
    background-color: #FCF9F6;
    font-color: #C0504D;
}
</style>""", unsafe_allow_html=True)

#st.markdown("""        <style>
#        
#@font-face {
#  font-family: 'Pretendard';
#  font-style: normal;
#  font-weight: 400;
#  src: url(https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css) format('woff');
#}
#    html, body, [class*="css"]  {
#    font-family: 'Pretendard';
#    font-size: 20px;
#    }
#    </style>""",unsafe_allow_html=True)

# 메인메뉴 없애고, 저작권 표시
hide_menu='''
<style>
#MainMenu {
    visibility:hidden;
}
footer {
    visibility:visible;
    size: 10%;
    font-family: 'Pretendard';
}
footer:after{
    content: 'SPDX-FileCopyrightText: © 2022 LAB-703 SPDX-License-Identifier: MIT';
    font-size: 15px;
    display:block;
    position:relative;
    color:silver;
    font-family: 'Pretendard';
}
</style>
'''
st.markdown(hide_menu, unsafe_allow_html=True)

select_event = st.sidebar.selectbox("🎈", ("👀 기사 인용 도우미", "📜 학술지 목록","📌 개발"))
if "emoji" not in st.session_state:
    st.session_state.emoji = "🤍"
st.sidebar.button(f" 좋아요 {st.session_state.emoji}", on_click=random_emoji)
#page1#######################################################################################################
if select_event == "👀 기사 인용 도우미":
    st.markdown('<p align="center" style=" font-size: 120%;"><b>👀 척척 석박들을 위한 기사 인용 도우미</b></p>', unsafe_allow_html=True)

    URL=st.text_input("네이버/다음 뉴스 url을 입력해주세요.")
    col1,col2=st.columns([5,5])  
    with col1:

        STYLE=st.radio("인용 스타일을 선택해주세요.",
             ("APA", 
              'CHICAGO',
              'by JOURNAL')) # : ⏳ 개발 중'))        
        final_search=st.checkbox('최종 검색일(오늘) 추가')
        submit=st.button('인용')
    with col2:
        if STYLE=="by JOURNAL":
            #st.markdown('<p style=" font-size: 100%; color:silver"> ⏳개발 중', unsafe_allow_html=True)
            journal_list=['Email', 'Home phone', 'Mobile phone']
            st.table(list(get_data(gsheet_connector)['학술지']))
            option = st.selectbox('찾으시는 학술지가 있나요?',journal_list)
            st.markdown('<p style=" font-size: 70%; color:silver"> 학술지가 없다면, 📜 학술지 목록 페이지에서 추가에 동참해 주세요.</p>', unsafe_allow_html=True)
            
    if submit==True:
#---------------------------------------------------------------------------------------------        
            if URL.find("n.news.naver.com/")>0: 
                req =requests.get(URL,headers=headers)
                html_doc = req.text  
                soup = bs(html_doc, 'html.parser')
                TITLE=soup.find("h2",{"class":"media_end_head_headline"}).get_text()
                DATE_write=soup.find("span",{"class":"media_end_head_info_datestamp_time _ARTICLE_DATE_TIME"}).get_text()[:10]
                #DATE_modify=soup.find("span",{"class":"media_end_head_info_datestamp_time _ARTICLE_MODIFY_DATE_TIME"}).get_text()[:10]
                
                AUTHOR=soup.find("em",{"class":"media_end_head_journalist_name"}).get_text().split()[0]
                COMPANY=soup.find("em",{"class":"media_end_linked_more_point"}).get_text()
            elif URL.find("v.daum.net/")>0 :
                    # header = {
                    #     'authority' : 'comment.daum.net',
                    #     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                    #     'accept' : "*/*",
                    #     'accept-encoding' : 'gzip, deflate, br',
                    #     'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                    #     'referer' : URL,
                    #     }
                    html = requests.get(URL, headers = headers)
                    test_text= html.text  
                    soup = bs(test_text, 'html.parser')
                    DATE_write=soup.find("span",{"class":"num_date"}).get_text()[:12].replace(" ","")
                    COMPANY=soup.select_one('meta[property="og:article:author"]')['content']
                    TITLE=soup.find("h3",{"class":"tit_view"}).get_text()#.replace("\'",'"')
                    #--------------------기자 이름 
                    if soup.find("span",{"class":"txt_info"}).get_text().startswith("입력")==True:
                        AUTHOR="" #없을 시 빈칸
                    else: #기자가 붙어있으면 떼고, 앞에 언론사 붙어있으면 리스트로 분리해서 마지막 행만 가져오도록 
                        AUTHOR=soup.find("span",{"class":"txt_info"}).get_text().split()[0]
#---------------------------------------------------------------------------------------------------------
            else :
                st.error('링크가 없거나 네이버/다음 포털뉴스의 링크가 아닙니다!')
                st.stop()
            APA=AUTHOR+". "+"("+DATE_write+"). "+TITLE+". "+COMPANY+". "+URL
            CHICAGO=AUTHOR+', "'+TITLE+'" '+COMPANY+", "+DATE_write+", "+URL
            FINAL=str(datetime.now().astimezone(timezone).strftime("%Y.%m.%d."))
            if final_search==True:
                APA=APA+", 최종검색일: "+FINAL
                CHICAGO=CHICAGO+", 최종검색일: "+FINAL
            if STYLE=="APA":
                st.code(APA,language="Markdown")
                #clipboard.copy(APA)
                st.write('오른쪽 복사버튼을 클릭하세요.')
            elif STYLE=="CHICAGO":
                st.code(CHICAGO,language="Markdown")
                #clipboard.copy(CHICAGO)
                st.write('오른쪽 복사버튼을 클릭하세요.')
            else:
                st.markdown('<p style=" font-size: 100%; color:silver"> ⏳개발 중', unsafe_allow_html=True)
                

#page2#######################################################################################################     
if select_event == "📜 학술지 목록":
    #st.subheader("⏳ 개발 중")
    st.markdown('<p align="center" style=" font-size: 140%;"><b>📜 등재된 학술지 목록</b></p>', unsafe_allow_html=True)
    LIST=['Email', 'Home phone', 'Mobile phone']
    journallist = st.selectbox('',LIST)
    st.write("---")
    #st.write('학술지 추가를 원하신다면, 더보기 버튼을 클릭하세요.')
    expander = st.expander("학술지 추가를 원하신다면 클릭하세요.")
    journal=expander.text_input("추가할 학술지의 정식 한글 명칭을 입력해 주세요.")
    col1,col2=expander.columns([5,5])  
    with col1:
        st.markdown("[![Foo](https://www.kci.go.kr/kciportal/resources/newkci/image/kor/title/h1_logo.png)](https://www.kci.go.kr/kciportal/main.kci)")
    with col2:
        st.markdown('<p style=" font-size: 80%; color:silver"> 🔍학술지 검색이 가능합니다.</p>', unsafe_allow_html=True)
    dic = {'AUTHOR':'기자',
       'TITLE': '기사 제목',
       'COMPANY': '언론사', 
       'DATE_write':'기사작성일',
       'URL' :'기사 URL',
       'FINAL_SEARCH':'최종검색일',
           'COMMA':',',
           'LEFT':'(',
        'RIGHT':')',
          'DOT':'.'}
     
    multiselect= expander.multiselect('순서대로 놓아주세요.',
                                list(dic.values()), 
                                list(dic.values())[:2]) #default
    annotation=""
    for selection in multiselect:
        if selection in list(dic.values())[:6]:
            annotation+=selection+". "
        elif selection in list(dic.values())[6]:
            annotation+=selection+" "
        else :
            annotation+=selection
    expander.markdown(annotation)
    today=str(datetime.now().astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"))
    submitted = expander.button("추가")
    if submitted:
        add_row_to_gsheet(
            gsheet_connector,
            [[journal, annotation,today]],
        )
        expander.success("추가되었습니다! 👀 기사 인용 도우미 페이지에서 확인할 수 있습니다.")
        expander.balloons()
#page3#######################################################################################################
if select_event == "📌 개발":
    st.header("👩🏻‍💻 개발자")
    col1,col2=st.columns([3,7])
    with col1 :
        st.markdown('<a href="http://m.site.naver.com/0Z7nr"><img src="https://qrcodethumb-phinf.pstatic.net/20220702_173/1656698540984dDVVY_PNG/0Z7nr.png"/></a>', unsafe_allow_html=True)
    with col2 :
        st.markdown("<br>개발자에게 커피 한잔은 큰 힘이 됩니다☕️<br>후원은 익명으로 가능합니다🎭", unsafe_allow_html=True)
    st.markdown("---")
    st.header("📆 개발 기록")
    st.markdown("`📌 배포 완료` `🐞 버그 수정`")
    beta1_0=st.expander("1️⃣ 2022. 06. 28. beta 1.0 배포")
    beta1_0.markdown('''<p align="left" style="font-size: 70%; text-indent : 20px;"> 📌 네이버/다음 뉴스 APA, CHICAGO 스타일 인용 기능 추가</p>''', unsafe_allow_html=True)
    beta2_0=st.expander("1️⃣ 2022. 07. 02. beta 2.0 배포")
    beta2_0.markdown('''<p align="left" style="font-size: 70%; text-indent : 20px;"> 🐞 타임존 UTC → KST 수정 </p>''', unsafe_allow_html=True)
    beta2_0.markdown('''<p align="left" style="font-size: 70%; text-indent : 20px;"> 📌 개발자 커피 후원 기능 추가 </p>''', unsafe_allow_html=True)
    
    
    
#    #즐겨찾기 추가인데 윈도우에서만 먹혀
#    a='''
#    <a href="JavaScript:window.external.AddFavorite('https://blog.naver.com/hyoyeol/70152225558','늑대털쓴양 홈페이지')">
#    '''
#    st.markdown(a)
#    st.markdown("[![Foo](https://postfiles.pstatic.net/MjAyMjA2MjZfOTgg/MDAxNjU2MjM0OTkwMjU5.OGRjH6YMCvGKy6AtjnTDjbGh-3MVP5yUsQmKHTlljNsg.6qk6L05rB42FP4F7P5M-TsF4gzRLKI23hIHBv_aW0nkg.PNG.faraway10/SE-f1959757-e2c6-4df0-85a5-1f2987b88c5d.png?type=w773)](https://postfiles.pstatic.net/MjAyMjA2MjZfMzYg/MDAxNjU2MjM1MDM1NDUz.hDsSoeeQATTXFBzlJ9DKBLoYS5rrYTLm8WekqElLNDAg.WqSp45bEruil_YHoScx-y_ZcF1t6Rub4DtJ7ObGGLiAg.PNG.faraway10/SE-9886a95b-a8ad-4edb-99b5-78bff09acb9d.png?type=w773)")

####################
