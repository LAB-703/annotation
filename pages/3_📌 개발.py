import streamlit as st
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
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
</style>
'''

st.markdown(hide_menu, unsafe_allow_html=True)

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
