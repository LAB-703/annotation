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
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from pytz import timezone
from gsheetsdb import connect

#def likes(gsheet_connector, row) -> None:
#    gsheet_connector.values().append(
#        spreadsheetId=SPREADSHEET_ID,
#        range=f"{SHEET_NAME}!D2",
#        body=dict(values=row),
#        valueInputOption="USER_ENTERED",
#    ).execute()
#    

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

st.markdown("""<style> @font-face {font-family: 'Pretendard';}</style>""", unsafe_allow_html=True)
#전체 폰트 
st.markdown("""
        <style>
@font-face {
font-family: Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
	font-weight: 45 920;
    
	font-style: normal;
	font-display: block;
	src: url('https://tistory1.daumcdn.net/tistory/814207/skin/images/PretendardVariable.subset.blog.woff2') format('woff2-variations');
}
    </style>""",unsafe_allow_html=True)

#전체 버튼
st.markdown("""
<style>
div.stButton > button:first-child {
font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
  font-size:100%;
    background-color: #FCF9F6;
    font-color: #C0504D;
}
</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
.viewerBadge_link__1S137 {
    visibility: hidden;
}
</style>""", unsafe_allow_html=True)

#전체 multiselect


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
#document{
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
}
footer {
    visibility:visible;
    size: 10%;
    font-family: 'Pretendard';
}
footer:after{
    content: 'SPDX-FileCopyrightText: © 2022 LAB-703 SPDX-License-Identifier: MIT';
    font-size: 30%;
    display:block;
    position:relative;
    color:silver;
    font-family: 'Pretendard';
code {
    color: sienna;
    overflow-wrap: break-word;
    background: linen;
    font-family: 'Source Code Pro';
}
}

</style>
'''

st.markdown(hide_menu, unsafe_allow_html=True)

def random_emoji():
    emojis = ["💖","🧡","💛","💚","💙","💜","🤎","🖤"]  
    st.session_state.emoji = random.choice(emojis)
    
if "emoji" not in st.session_state:
    st.session_state.emoji = "🤍"
###################################
select_event = st.sidebar.selectbox("🎈", ("👀 기사 인용 도우미", "📜 학술지 목록","📌 개발"))
likes=st.sidebar.button(f" 좋아요 {st.session_state.emoji}", on_click=random_emoji)
# gsheet_connector = connect_to_gsheet()

#likes_cnt=st.sidebar.markdown(get_data(gsheet_connector)['좋아요'][1])
#if likes:
#    likes=st.sidebar.button(f" 좋아요 {st.session_state.emoji}", on_click=random_emoji)
#############################################################33    

################################################################################################33    
    


#page1#######################################################################################################
if select_event == "👀 기사 인용 도우미":
    st.markdown('<p align="center" style=" font-size: 140%;"><b>👀 척척 석박들을 위한 기사 인용 도우미</b></p>', unsafe_allow_html=True)

    URL=st.text_input("네이버/다음 뉴스 url을 입력해주세요.")
    col1,col2=st.columns([5,5])  
    with col1:
        STYLE=st.radio("인용 스타일을 선택해주세요.",
             ("APA", 
              'CHICAGO',
              'by JOURNAL')) # : ⏳ 개발 중'))        
        
    with col2:
        if STYLE=="by JOURNAL":
            #st.markdown('<p style=" font-size: 100%; color:silver"> ⏳개발 중', unsafe_allow_html=True)
#             st.markdown("""<style>
# div.st-be.st-bf.st-by.st-bz.st-c0.st-b4.st-c1.st-c2.st-bg.st-c3.st-c4.st-c5.st-c6 {visibility: hidden;}
# div.st-be.st-bf.st-by.st-bz.st-c0.st-b4.st-c1.st-c2.st-bg.st-c3.st-c4.st-c5.st-c6:before {content: "찾으시는 학술지가 있나요?"; visibility: visible;}
# </style>
# """, unsafe_allow_html=True)
            gsheet_connector = connect_to_gsheet()
            #option = st.selectbox('찾으시는 학술지가 있나요?',list(get_data(gsheet_connector)['학술지']))
            st.markdown('<p style=" font-size: 90%; color:silver"> 학술지가 없다면, 📜 학술지 목록 페이지에서 추가에 동참해 주세요.</p>', unsafe_allow_html=True)
    final_search=st.checkbox('최종 검색일(오늘) 추가')
    submit=st.button('인용')        
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
            TODAY = str(datetime.now(timezone('Asia/Seoul')).strftime("%Y.%m.%d."))
            if final_search==True:
                APA=APA+", 최종검색일: "+TODAY
                CHICAGO=CHICAGO+", 최종검색일: "+TODAY
            if STYLE=="APA":
                st.code(APA,language="Markdown")
                #clipboard.copy(APA)
                st.write('오른쪽 복사버튼을 클릭하세요.')
            elif STYLE=="CHICAGO":
                st.code(CHICAGO,language="Markdown")
                #clipboard.copy(CHICAGO)
                st.write('오른쪽 복사버튼을 클릭하세요.')
            # else:
            #     st.markdown('<p style=" font-size: 100%; color:silver"> ⏳개발 중', unsafe_allow_html=True)
                

#page2#######################################################################################################     
if select_event == "📜 학술지 목록":
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
    #st.subheader("⏳ 개발 중")
    st.markdown('<p align="center" style=" font-size: 140%;"><b>📜 등재된 학술지 목록</b></p>', unsafe_allow_html=True)
    gsheet_connector = connect_to_gsheet()
    journal_df=get_data(gsheet_connector)
    journal_list = st.selectbox('',list(journal_df['학술지']))
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
            ).get('values', [])
            
            last_row = rows[-1] if rows else None
            last_row_id = len(rows)
            print(last_row_id, last_row)
            
            gsheet_connector = connect_to_gsheet()
            expander.success("추가되었습니다! 👀 기사 인용 도우미 페이지에서 확인할 수 있습니다.")
            expander.balloons()
#page3#######################################################################################################
if select_event == "📌 개발":
    st.markdown('<p align="left" style=" font-size: 140%;"><b>👩🏻‍💻 개발자</b></p>', unsafe_allow_html=True)
    col1,col2=st.columns([3,7])
    with col1 :
        st.markdown('<a href="http://m.site.naver.com/0Z7nr"><img src="https://qrcodethumb-phinf.pstatic.net/20220702_173/1656698540984dDVVY_PNG/0Z7nr.png"/></a>', unsafe_allow_html=True)
    with col2 :
        st.markdown('''<p align="left" style="font-size: 90%;"> <br> ☕️ 개발자에게 커피 한잔은 큰 힘이 됩니다<br><br>
                        🎭 후원은 익명으로 가능합니다<br> <br>
                        👉 QR코드를 스캔하거나 클릭시 <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Toss-logo.svg/800px-Toss-logo.svg.png" height=13px>로 연결됩니다<br> </p>''', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p align="left" style=" font-size: 140%;"><b>📆 개발 기록</b></p>', unsafe_allow_html=True)
    st.markdown('<code>📌 기능 추가</code> <code>🐞 버그 수정</code>', unsafe_allow_html=True)
    beta1_0=st.expander("1️⃣ 2022. 06. 28. beta 1.0 배포")
    beta1_0.markdown('''<p align="left" style="font-size: 70%; text-indent : 20px;"> 📌 네이버/다음 뉴스 APA, CHICAGO 스타일 인용 기능 추가</p>''', unsafe_allow_html=True)
    beta2_0=st.expander("2️⃣ 2022. 07. 05. beta 2.0 배포")
    beta2_0.markdown('''<p align="left" style="font-size: 70%; text-indent : 20px;"> 🐞 최종검색일 타임존 UTC → KST 수정 </p>''', unsafe_allow_html=True)
    beta2_0.markdown('''<p align="left" style="font-size: 70%; text-indent : 20px;"> 📌 학술지 페이지 오픈 <code>new!</code> 새로운 학술지 추가에 동참해주세요! </p>''', unsafe_allow_html=True)
    beta2_0.markdown('''<p align="left" style="font-size: 70%; text-indent : 20px;"> 📌 개발자 커피 후원 기능 추가 </p>''', unsafe_allow_html=True)
   # st.markdown('''<a href="JavaScript:window.external.AddFavorite('http://yes-today.tistory.com', '내일을 만드는 어제와 오늘')"> 즐겨찾기 추가</a>''', unsafe_allow_html=True)
    
