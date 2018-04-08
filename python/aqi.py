"""
    aqi爬虫抓取练习
"""

import requests
from bs4 import BeautifulSoup
import csv
import pandas
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_city_list():
    """
    获取所有城市列表
    :return: 城市列表的拼音和中文列表
    """
    r = requests.get('http://pm25.in/')
    soup = BeautifulSoup(r.text, 'html.parser')
    div_list = soup.find_all('div', {'class': 'bottom'})[1]
    city_a = div_list.find_all('a')

    city_list = []
    for item in city_a:
        city_name = item.text.strip()
        city_pinyin = item['href'][1:]
        city_list.append((city_pinyin, city_name))

    return city_list


def get_city_aqi(city):
    """
    获取指定城市的空气质量指标
    :param city: 城市拼音,如:beijing
    :return: 返回该城市的空气指标列表
    """
    url = 'http://pm25.in/' + city
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    div_list = soup.find_all("div", {"class": "span1"})

    # print(type(div_list))
    city_aqi_caption = []
    city_aqi_value = []
    for i in range(8):
        div = div_list[i]
        caption = div.find('div', {'class': 'caption'}).text.strip()
        value = div.find('div', class_='value').text.strip()
        city_aqi_caption.append(caption)
        city_aqi_value.append(value)

    return city_aqi_value,city_aqi_caption


def save_aqi_to_csv(file_name, city_list):
    """
    保存数据到csv文件
    :param file_name:文件名称
    :param city_list:城市列表
    :return:
    """
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        io = csv.writer(f)
        for i, city in enumerate(city_list):
            aqi, header = get_city_aqi(city[0])
            if i == 0:
                header = ['City'] + header
                io.writerow(header)

            data = [city[1]] + aqi
            io.writerow(data)
            print(data)
        return i


def main():
    # city_list = get_city_list()
    # count = save_aqi_to_csv('china_city_aqi_data.csv', city_list)

    # print("共写入{}条数据".format(count))

    aqi_csv_data = pandas.read_csv('china_city_aqi_data.csv')
    # print(aqi_csv_data.tail(5))
    # print(aqi_csv_data.info())

    print('AQI最大值:', aqi_csv_data['AQI'].max())
    print('AQI最小值:', aqi_csv_data['AQI'].min())
    print('AQI平均值:', aqi_csv_data['AQI'].mean())

    # AQI最差的前50个城市
    last_50_city = aqi_csv_data.sort_values(by=['AQI'], ascending=False).head(50)
    last_50_city.to_csv('last_50_city.csv', index=False)

    last_50_city.plot(kind='bar', x='City', y='AQI', title='空气质量', figsize=(20, 10))

    plt.savefig('top_50.png')
    plt.show()


if __name__ == '__main__':
    main()
