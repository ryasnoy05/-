import requests
from bs4 import BeautifulSoup as BS
import csv
from multiprocessing import Pool


def csv_write(data): #Записываем словарь с данными в CSV файл
    with open("E:/work/data.csv",'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        for post in data:
            writer.writerow((post['title'],post['time'],post['href']))
            


def get_html(url):
    r = requests.get(url) #Отправляем HTTP запрос и получаем результат
    return r.text


def all_links(): # Получаеи ссылки всех страниц для парсинга и записываем их в массив, для дальнейшего взаимодействия
    links = list()
    for i in range(1, 51):
        links.append("https://habr.com/ru/page" + str(i))
    return links


def get_pages_info(html): #Берем с сайта нужную нам информацию и записываем в словарь, для дальнейшей записи в CSV файл
    data = []
    soup = BS(html, "html.parser")
    user = soup.findAll("a", class_= "post__user-info user-info")
    title = soup.findAll("a", class_= "post__title_link")
    time = soup.findAll("span", class_= "post__time")
    for i in range(len(title)):
        data.append({
            'title' : str(title[i].text),
            'time' : str(time[i].text),
            'href' : str(user[i].get('href'))
        })
        print(str(title[i].text))
    print("pars")
    return data

def head(link): #Эта функция создана для удобства пользования пакетом multiprocessing
    html = get_html(link)
    data = get_pages_info(html)
    csv_write(data)


def main(): #Основная функция кода
    links = all_links()
    with Pool(15) as pars:
        pars.map(head, links)


if __name__ == "__main__":
    main()
