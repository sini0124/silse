# -*- encoding: utf-8 -*-
# =====================================================================
#  Flask의 값을 보기 위해서 HTML접송릉 하려면
#  http://localhost:5000/?content=(묻고싶은 질문)&userid=a
#  을 입력하면 됩니다.
#  괄호는 미포함!
# =====================================================================
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
import requests
import json
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

local_dic = {"강서구": 1150000000, "강남구": 1168000000, "강북구": 1130500000, "강동구": 1174000000}
foreprise = {"강서구": 1150000000, "강남구": 1168000000, "강북구": 1130500000, "강동구": 1174000000}


def how_much_average(location_data):
    # =====================================================================
    #  지역(location_data)의 정보의 평균 가격을 검색해서 return 하는 함수
    # =====================================================================

    req = requests.get(
        "https://land.naver.com/article/divisionPriceInfo.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cortarNo=" + str(
            local_dic[location_data]) + "&articleOrderCode=")

    html = req.text
    header = req.headers
    status = req.status_code
    is_ok = req.ok

    soup = BeautifulSoup(html, 'html.parser')

    local_prise = soup.select('#rightGraphPrice1')
    for prise in local_prise:
        print(prise.text)
    return prise.text


def how_much_list(location_data):
    # =====================================================================
    #  지역(location_data)의 매물정보를 검색해서 return 하는 함수
    # =====================================================================

    req = requests.get(
        "https://land.naver.com/article/divisionArticleList.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cortarNo=" + str(
            local_dic[location_data]) + "&articleOrderCode=")

    html = req.text
    header = req.headers
    status = req.status_code
    is_ok = req.ok

    soup = BeautifulSoup(html, 'html.parser')

    a = []

    print("====================================")
    x = 0
    for i in range(1, 3):
        types = soup.select("#depth4Tab0Content > div > table > tbody > tr:nth-child(" + str(
            i * 2 - 1) + ") > td.sale_type.bottomline > div")
        for type in types:
            ## Tag안의 텍스트
            print(type.text)
        str_test = "거래 : " + type.text

        types = soup.select("#depth4Tab0Content > div > table > tbody > tr:nth-child(" + str(
            i * 2 - 1) + ") > td.sale_type2.bottomline > div")
        for type in types:
            ## Tag안의 텍스트
            print(type.text)
        str_test = str_test + "<br>종류 : " + type.text

        types = soup.select("#depth4Tab0Content > div > table > tbody > tr:nth-child(" + str(
            i * 2 - 1) + ") > td.align_l.name > div > a")
        for type in types:
            ## Tag안의 텍스트
            print(type.text)
        str_test = str_test + "<br>매물명 : " + type.text

        types = soup.select(
            "#depth4Tab0Content > div > table > tbody > tr:nth-child(" + str(i * 2 - 1) + ") > td:nth-child(6) > div")
        for type in types:
            ## Tag안의 텍스트
            str_type = type.text
            first_place = str_type.find("공")
            last_place = str_type.find("㎡")
            print(type.text[first_place:last_place + 1])
            str_test = str_test + "<br>면적 : " + type.text[first_place:last_place + 1] + " "
            first_place = str_type.find("전", last_place + 2)
            last_place = str_type.find("㎡", last_place + 2)
            print(type.text[first_place:last_place + 1])
            str_test = str_test + type.text[first_place:last_place + 1]

        types = soup.select(
            "#depth4Tab0Content > div > table > tbody > tr:nth-child(" + str(i * 2 - 1) + ") > td.num2 > div")
        for type in types:
            ## Tag안의 텍스트
            print(type.text)
        str_test = str_test + "<br>층 : " + type.text

        types = soup.select(
            "#depth4Tab0Content > div > table > tbody > tr:nth-child(" + str(i * 2 - 1) + ") > td.num.align_r > div")
        for type in types:
            ## Tag안의 텍스트
            print(type.text[1:len(type.text) - 1])
        str_test = str_test + "<br>매물가 : " + type.text[1:len(type.text) - 1] + " 만원"

        types = soup.select("#depth4Tab0Content > div > table > tbody > tr:nth-child(" + str(
            i * 2 - 1) + ") > td.contact.bottomline > div")
        for type in types:
            ## Tag안의 텍스트
            str_type = type.text
            first_place = 10
            last_place = str_type.find("\n", 10)
            print(type.text[10:last_place])
            str_test = str_test + "<br>연락처 : " + type.text[10:last_place] + " : "
            first_place = str_type.find("\n", last_place + 2)
            last_place = len(type.text) - 2
            print(type.text[first_place + 1:last_place])
            str_test = str_test + type.text[first_place + 1:last_place]

        a.append(str_test)
    print(a)
    print("====================================")
    # ==========================================
    #  가격정보를 검색해서 알려줄수 있는 부분
    # ==========================================

    return split_and_make_string(a)


def split_and_make_string(a):
    # =====================================================================
    #  위의 정보 list를 예쁘게 파싱해주는 함수
    # =====================================================================
    str = ""
    for i in a:
        str = str + i + "<br><br>"

    return str


def get_answer(location_data):
    # =============================================================================================
    #  이하 분석 한 값을 출력해 주는 코드
    # =============================================================================================

        #location_data = answer[0:len(answer) - 10]
    print("Aa")
    prise = how_much_average(location_data)
    list_data = how_much_list(location_data)
    more_answer = location_data + "의 정보 알려드릴께요.<br><br>" + location_data + "의 평균 가격은 " + prise + "입니다. <br><br><br>매물정보<br><br>" + list_data

    series = pd.read_csv('Avg_' + str(local_dic[location_data]) + '.csv', header=0, index_col=0, squeeze=True)
    series.plot()

    model = ARIMA(series, order=(1, 0, 1), freq='D')
    model_fit = model.fit(trend='c', full_output=True, disp=1)
    # print(model_fit.summary())
    model_fit.plot_predict()
    fore = model_fit.forecast(steps=1)
    # plt.show()
    print("예측가격 : 1m^3 당 " + str(round(fore[0][0], 2)) + "만 원")

    more_answer = more_answer + "예측가격 : 1m^3 당 " + str(round(fore[0][0], 2)) + "만 원"

    return more_answer


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False



@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    retrunAns = ""
    req = request.get_json(force=True)
    answers = req['queryResult']['fulfillmentText']  # 1
    print(answers)
    if answers == '어디 가격을 알려드릴까요?':
        retrunAns == "어디 가격을 알려드릴까요?"  # 2
    elif answers[len(answers)-10:len(answers)] == " 정보 알려드릴께요":
        print("Dd")
        location_data = answers[0:len(answers) - 10]
        retrunAns = get_answer(location_data)

    return {'fulfillmentText': retrunAns}




if __name__ == '__main__':
    app.run(host='0.0.0.0')
