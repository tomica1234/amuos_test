import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe

st.session_state['name'] = 'このカーナンバーは申請されていません。公式SNSのDMにて参加申請をしてください。'
service_account_info = st.secrets["google_service_account"]

# 認証情報オブジェクトを生成


# 認証情報を設定
scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_info(service_account_info,scopes=scopes)
client = gspread.authorize(creds)

st.subheader('アムオスF1順位予想2024')

spreadsheet = client.open('F1順位予想企画2024')

# 最初のワークシートを選択
sheet1 = client.open('F1順位予想企画2024').worksheet("エントリークラスⅠ")

data1 = sheet1.get_all_values()
headers = data1.pop(0)
df1 = pd.DataFrame(data1)

sheet2 = client.open('F1順位予想企画2024').worksheet("エントリークラスⅡ")

data2 = sheet2.get_all_values()
headers = data2.pop(0)
df2 = pd.DataFrame(data2)

car_number = st.number_input('あなたのカーナンバーを半角で入力してください', min_value=0, max_value=200, step=1)
class_number =  st.selectbox('あなたのクラスを選択してください',('クラスⅠ', 'クラスⅡ'))

if class_number == 'クラスⅠ':
    if (df1.loc[: ,1] == str(int(car_number))).any():
        filtered_rows = df1[df1.loc[: ,1] == str(int(car_number))]
        name = filtered_rows[2].iloc[0]
    else:
        name = 'このカーナンバーは申請されていません。公式SNSのDMにて参加申請をしてください。'

elif class_number == 'クラスⅡ':
    if (df2.loc[: ,1] == str(int(car_number))).any():
        filtered_rows = df2[df2.loc[: ,1] == str(int(car_number))]
        name = filtered_rows[2].iloc[0]
    else:
        name = 'このカーナンバーは申請されていません。公式SNSのDMにて参加申請をしてください。'
st.write(f'参加者名:{name}')

race_selection = st.selectbox(
    'レースを選択してください',
    ['バーレーン', 'サウジアラビア', 'オーストラリア','鈴鹿','中国','マイアミ','エミリアロマーニャ','モナコ','カナダ','スペイン','オーストリア','イギリス','ハンガリー','ベルギー','オランダ','モンツァ','アゼルバイジャン','シンガポール','COTA','メキシコ','サンパウロ','ラスベガス','カタール','アブダビ'])

if st.button('確定'):
    
    st.session_state['car_number'] = car_number
    st.session_state['class'] = class_number
    st.session_state['race'] = race_selection
    st.session_state['name'] = name
    if name == 'このカーナンバーは申請されていません。公式SNSのDMにて参加申請をしてください。':
        st.write('最初からやり直してください')
    else:
        st.write('予想ページへ進んでください')

    


