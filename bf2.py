import unittest
import re
from bs4 import BeautifulSoup
import os


def parse(path_to_file):
    with open(path_to_file, encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")
        body = soup.find(id="bodyContent")

    # количество картинок (img) с шириной (width) не меньше 200
    imgs = len(body.find_all('img', width=lambda x: int(x or 0) > 199))

    # количество заголовков (h1, h2, h3, h4, h5, h6), первая буква текста внутри которых
    # соответствует заглавной букве E, T или C
    headers = sum(1 for tag in body.find_all(
        ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if tag.get_text()[0] in "ETC")

    # количество списков (ul, ol), не вложенных в другие списки
    lists = sum(
        1 for tag in body.find_all(['ol', 'ul']) if not tag.find_parent(['ol', 'ul']))

    # Длину максимальной последовательности ссылок, между которыми нет других тегов
    linkslen = 0

    for a in body.find_all('a'):
        current_streak = 1

        for tag in a.find_next_siblings():
            if tag.name == 'a':
                current_streak += 1
            else:
                break

        linkslen = current_streak if current_streak > linkslen else linkslen

    return [imgs, headers, linkslen, lists]

def get_nodes(path, start_page):
    with open(os.path.join(path, start_page), encoding="utf-8") as file:
        links = re.findall(r"(?<=[\"\']/wiki/)[\w()]+[\"\']", file.read())
        links = [re.sub(r"[\"\']", "", i) for i in links]
        if start_page in  links:
            links.remove(start_page)
    return links
def bfs(wiki,start_page,end_page):

    d = {}
    level = {}
    queue = []
    queue.append([start_page])
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end_page:
            return path
        if node in level:
            continue
        level[node]=1
        if(os.path.isfile(os.path.join(wiki,node))):
            d[node] = get_nodes(wiki, node)
        for adjacent in d.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


def build_bridge(path, start_page, end_page):
    short_path= bfs(path,start_page,end_page)
    return short_path



def get_statistics(path, start_page, end_page):


    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    # напишите вашу реализацию логики по сбору статистики здесь
    statistic = {}
    for page in pages:
        statistic[page]=parse(os.path.join(path,page))
    return statistic

if __name__ == '__main__':
    result = get_statistics('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing")
