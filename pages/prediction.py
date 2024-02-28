import streamlit as st
from streamlit_sortables import sort_items
from google.oauth2.service_account import Credentials
import gspread


service_account_info = st.secrets["google_service_account"]

st.subheader('アムオスF1順位予想2024')

#st.write(f"カーナンバー: {st.session_state['car_number']}")


if 'car_number' in st.session_state:
    st.write(f"参加者名: {st.session_state['name']}")
    st.write(f"レース名: {st.session_state['race']}")
else:
    st.write("入力ページにて必要な情報を入力してください")
    
    

original_items_q = [
    {'header': '予選順位：', 'items':['フェルスタッペン', 'ペレス', 'ハミルトン', 'ラッセル', 'ルクレール', 'サインツ', 'ノリス', 'ピアストリ', 'アロンソ','ストロール','ガスリー','オコン','アルボン','サージェント','角田','リカルド','ボッタス','周','ヒュルケンベルグ','マグヌッセン']},
]
sorted_items_q = sort_items(original_items_q, multi_containers=True, direction='vertical')

original_items_r = [
    {'header': '決勝順位：', 'items':['フェルスタッペン', 'ペレス', 'ハミルトン', 'ラッセル', 'ルクレール', 'サインツ', 'ノリス', 'ピアストリ', 'アロンソ','ストロール','ガスリー','オコン','アルボン','サージェント','角田','リカルド','ボッタス','周','ヒュルケンベルグ','マグヌッセン']},
    {'header': '決勝リタイア：',
        'items': []}
]
sorted_items_r = sort_items(original_items_r, multi_containers=True, direction='vertical')

# 予選順位のリストを取得
sorted_qual = sorted_items_q[0]["items"]
# 決勝順位のリストを取得
sorted_race = sorted_items_r[0]["items"]
# 決勝リタイアのリストを取得 (もし決勝でリタイアした車があれば)
sorted_ret = sorted_items_r[1]["items"]

driver_number = {'フェルスタッペン':1, 'ペレス':11, 'ハミルトン':44, 'ラッセル':63, 'ルクレール':16, 'サインツ':55, 'ノリス':4, 'ピアストリ':81, 'アロンソ':14,'ストロール':18,'ガスリー':10,'オコン':31,'アルボン':23,'サージェント':2,'角田':22,'リカルド':3,'ボッタス':77,'周':24,'ヒュルケンベルグ':27,'マグヌッセン':20}

if st.button('提出'):
    # ここでカーナンバー、レース選択、並び替えられた順位などの情報を取得します
    # 実際のspreadsheetへの書き込み処理をここに追加します
    
    scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(service_account_info,scopes=scopes)
    client = gspread.authorize(creds)
    
    spreadsheet = client.open('F1順位予想企画2024')
    worksheet = spreadsheet.worksheet('参加者予想')
    data_qual = list(map(lambda item: driver_number[item], sorted_qual))
    data_race = list(map(lambda item: driver_number[item], sorted_race))
    data_ret = list(map(lambda item: driver_number[item], sorted_ret))
   
   
    all_values = worksheet.get_all_values()
    max_col = max(len(row) for row in all_values)  # 最大列数を取得

    
    search_car_number = st.session_state['car_number']
    search_race = st.session_state['race']

    all_values = worksheet.get_all_values()

    # 条件を満たす列が存在するかどうかのフラグ
    column_exists = False

    # 全列を走査して条件を満たすか確認
    for col_index, col_values in enumerate(zip(*all_values), start=1):
        try:
            # 1行目を整数として、2行目を文字列として比較
            if int(col_values[0]) == int(search_car_number) and col_values[1] == search_race:
                column_exists = True
                #print(f"条件に合致する列は {col_index} 列目に存在します。")
                break  # 条件を満たす列が見つかったらループを抜ける
        except ValueError:
            # int変換できない場合は、この列は無視（整数でないため条件に合わない）
            continue
    if column_exists:
            st.write('すでに提出済みです')
        # ここに特定の値が含まれている場合の処理を書く
    else:
        st.write('このままお待ちください')
        
        # dataリストの値を縦に入れる列を指定（最右列の次）
        target_col = max_col + 1

        worksheet.update_cell(1, target_col, st.session_state['car_number'])
        worksheet.update_cell(1, target_col+1, st.session_state['car_number'])
        worksheet.update_cell(1, target_col+2, st.session_state['car_number'])

        worksheet.update_cell(2, target_col, st.session_state['race'])
        worksheet.update_cell(2, target_col+1, st.session_state['race'])
        worksheet.update_cell(2, target_col+2, st.session_state['race'])

        worksheet.update_cell(3, target_col, '予選')
        worksheet.update_cell(3, target_col+1, '決勝')
        worksheet.update_cell(3, target_col+2, '決勝リタイア')


        # dataリストの値を指定した列に縦に入れる
      # このリストを必要に応じて調整してください
        for i, value in enumerate(data_qual, start=4):
            worksheet.update_cell(i, target_col, value)

        for i, value in enumerate(data_race, start=4):
            worksheet.update_cell(i, target_col+1, value)

        for i, value in enumerate(data_ret, start=4):
            worksheet.update_cell(i, target_col+2, value)
        
        st.write('提出完了しました')
