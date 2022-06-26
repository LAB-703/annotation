import streamlit as st
import streamlit.components.v1 as components
from urllib import parse
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import clipboard
import random
import pandas as pd

#@st.cache(allow_output_mutation=True, persist=True)
#def get_data(): #사용자로부터 데이터를 받을 때 
#    return []

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
    initial_sidebar_state="collapsed",
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
font-weight: 400;
font-display: swap;
src: local('Pretendard Regular'), url('./woff2/Pretendard-Regular.woff2') format('woff2'), url('./woff/Pretendard-Regular.woff') format('woff');
}
html, body, [class*="css"]  {
    font-family: 'Pretendard';
    font-size: 20px;
    }
    </style>""",unsafe_allow_html=True)

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

# 메인메뉴 없애고, 
hide_menu='''
<style>
#MainMenu {
    visibility:hidden;
}


footer {
    content: 'SPDX-FileCopyrightText: © 2022 Lee Jeong Min SPDX-License-Identifier: BSD-3-Clause';
    visibility:visible;
    font-size: 10%;
}

footer:after{
    content: 'SPDX-FileCopyrightText: © 2022 Lee Jeong Min SPDX-License-Identifier: BSD-3-Clause';
    font-size: 10%;
    display:block;
    position:relative;
    color:silver;
}

</style>
'''


st.markdown(hide_menu, unsafe_allow_html=True)

select_event = st.sidebar.selectbox("🎈", ("👀 기사 인용 도우미", "📜 학술지 목록","📌 개발"))
#page1#######################################################################################################
if select_event == "👀 기사 인용 도우미":
    st.markdown('<p align="center" style=" font-size: 140%;"><b>👀 척척 석박들을 위한 기사 인용 도우미</b></p>', unsafe_allow_html=True)

    URL=st.text_input("네이버/다음 뉴스 url을 입력해주세요.")
    col1,col2=st.columns([5,5])  
    with col1:
        STYLE=st.radio("인용 스타일을 선택해주세요.",
             ('APA', 'CHICAGO','by JOURNAL              ⏳개발 중'))
        final_search=st.checkbox('최종 검색일(오늘) 추가')
        submit=st.button('복사')
 #   with col2:
  #      if STYLE=="by JOURNAL":
  #          st.markdown('<p style=" font-size: 100%; color:silver"> ⏳개발 중', unsafe_allow_html=True)
            #journal_list=['Email', 'Home phone', 'Mobile phone']
            #option = st.selectbox('찾으시는 학술지가 있나요?',journal_list)
            #st.markdown('<p style=" font-size: 70%; color:silver"> 학술지가 없다면, 📜 학술지 목록 페이지에서 추가에 동참해 주세요.</p>', unsafe_allow_html=True)
            
    if submit==True:
#---------------------------------------------------------------------------------------------        
            if URL.find("n.news.naver.com/")>0: 
                req =requests.get(URL,headers=headers)
                html_doc = req.text  
                soup = bs(html_doc, 'html.parser')
                TITLE=soup.find("h2",{"class":"media_end_head_headline"}).get_text()
                DATE_retrieve=datetime.now().strftime("%Y.%m.%d")
                DATE_write=soup.find("span",{"class":"media_end_head_info_datestamp_time _ARTICLE_DATE_TIME"}).get_text()[:10]
                #DATE_modify=soup.find("span",{"class":"media_end_head_info_datestamp_time _ARTICLE_MODIFY_DATE_TIME"}).get_text()[:10]
                AUTHOR=soup.find("em",{"class":"media_end_head_journalist_name"}).get_text().split()[0]
                COMPANY=soup.find("em",{"class":"media_end_linked_more_point"}).get_text()
            elif URL.find("v.daum.net/")>0 :
                    header = {
                        'authority' : 'comment.daum.net',
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                        'accept' : "*/*",
                        'accept-encoding' : 'gzip, deflate, br',
                        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                        'referer' : URL,
                        }
                    html = requests.get(URL, headers = header)
                    test_text= html.text  
                    soup = bs(test_text, 'html.parser')
                    DATE_retrieve=datetime.now().strftime("%Y.%m.%d")
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
            FINAL=str(datetime.now().strftime("%Y.%m.%d."))
            if final_search==True:
                APA=APA+", 최종검색일: "+FINAL
                CHICAGO=CHICAGO+", 최종검색일: "+FINAL
            if STYLE=="APA":
                title='''
                    <style>
                    #Copy to clipboard {
                        color:red;
                    }
                    </style>
                    '''
                st.markdown(title, unsafe_allow_html=True)
                st.code(APA,language="Markdown")
                #clipboard.copy(APA)
                st.write('오른쪽 복사버튼을 클릭하세요.')
            elif STYLE=="CHICAGO":
                st.code(CHICAGO,language="Markdown")
                #clipboard.copy(CHICAGO)
                st.write('오른쪽 복사버튼을 클릭하세요.')
            else:
                st.markdown('<p style=" font-size: 100%; color:silver"> ⏳개발 중', unsafe_allow_html=True)
                
    def random_emoji():
        st.session_state.emoji = random.choice(emojis)

    # initialize emoji as a Session State variable
    #if "emoji" not in st.session_state:
    #    st.session_state.emoji = "🤍"

   # emojis = ["💖","🧡","💛","💚","💙","💜","🤎","🖤"]

    #st.button(f" 좋아요 {st.session_state.emoji}", on_click=random_emoji)

#page2#######################################################################################################     
if select_event == "📜 학술지 목록":
    st.subheader("⏳ 개발 중")
#    st.markdown('<p align="center" style=" font-size: 140%;"><b>📜 등재된 학술지 목록</b></p>', unsafe_allow_html=True)
#    LIST=['Email', 'Home phone', 'Mobile phone']
#    journal = st.selectbox('학술지를 찾아보세요!',LIST)
#    st.write("---")
#    st.write('학술지 추가를 원하신다면, 더보기 버튼을 클릭하세요.')
#    expander = st.expander("더보기")
#    expander.text_input("추가할 학술지의 정식 한글 명칭을 입력해 주세요.")
#    expander.markdown('<p style=" font-size: 80%; color:silver"> 🔍학술지 검색이 가능합니다.</p>', unsafe_allow_html=True)
#    expander.markdown("[![Foo](https://www.kci.go.kr/kciportal/resources/newkci/image/kor/title/h1_logo.png)](https://www.kci.go.kr/kciportal/main.kci)")
#    dic = {'AUTHOR':'기자',
#       'TITLE': '기사 제목',
#       'COMPANY': '언론사', 
#       'DATE_write':'기사작성일',
#       'URL' :'기사 URL',
#       'FINAL_SEARCH':'최종검색일',
#           'COMMA':',',
#           'LEFT':'(',
#        'RIGHT':')',
#          'DOT':'.'}
#     
#    multiselect= expander.multiselect('순서대로 놓아주세요.',
#                                list(dic.values()), 
#                                list(dic.values())[:2]) #default
#    annotation=""
#    for selection in multiselect:
#        if selection in list(dic.values())[:6]:
#            annotation+=selection+". "
#        elif selection in list(dic.values())[6]:
#            annotation+=selection+" "
#        else :
#            annotation+=selection
#    expander.markdown(annotation)
#    add=expander.button("추가")
#    if add:
#        expander.write("추가되었습니다! 👀 기사 인용 도우미 페이지에서 확인할 수 있습니다.")
#page3#######################################################################################################
if select_event == "📌 개발":
    st.header("👩🏻‍💻 개발자")
    st.markdown("---")
    st.header("📆 개발 기록")
  #  st.markdown("1️⃣ 2022. 06. 26. beta 1.0 배포")
    st.markdown('<p align="left" style=" font-size: 70%;"><b>1️⃣ 2022. 06. 26. beta 1.0 배포</b></p>', unsafe_allow_html=True)
#    #즐겨찾기 추가인데 윈도우에서만 먹혀
#    a='''
#    <a href="JavaScript:window.external.AddFavorite('https://blog.naver.com/hyoyeol/70152225558','늑대털쓴양 홈페이지')">
#    '''
#    st.markdown(a)
#    st.markdown("[![Foo](https://postfiles.pstatic.net/MjAyMjA2MjZfOTgg/MDAxNjU2MjM0OTkwMjU5.OGRjH6YMCvGKy6AtjnTDjbGh-3MVP5yUsQmKHTlljNsg.6qk6L05rB42FP4F7P5M-TsF4gzRLKI23hIHBv_aW0nkg.PNG.faraway10/SE-f1959757-e2c6-4df0-85a5-1f2987b88c5d.png?type=w773)](https://postfiles.pstatic.net/MjAyMjA2MjZfMzYg/MDAxNjU2MjM1MDM1NDUz.hDsSoeeQATTXFBzlJ9DKBLoYS5rrYTLm8WekqElLNDAg.WqSp45bEruil_YHoScx-y_ZcF1t6Rub4DtJ7ObGGLiAg.PNG.faraway10/SE-9886a95b-a8ad-4edb-99b5-78bff09acb9d.png?type=w773)")