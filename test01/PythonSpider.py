import requests
from bs4 import BeautifulSoup
import time
import os

if __name__ == "__main__":

    # 定义存放文件的文件夹名称
    folder_name = '蛊真人'
    # 如果文件夹不存在，则创建文件夹
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 目标小说的首页 URL
    url = 'https://www.bqgui.cc/book/10457/'
    # 请求头，模拟浏览器访问
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ''(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
    # 创建一个会话
    session = requests.session()

    # 循环爬取每一章节的内容
    for i in range(1, 2381):
        # 构造当前章节的URL
        detail_url = f'https://www.bqgui.cc/book/10457/{i}.html'
        print(detail_url)
        while True:
            try:
                # 发起请求获取章节页面内容
                detail_response = session.get(url=detail_url, headers=headers)
                # 设置编码方式
                detail_response.encodings = detail_response.apparent_encoding
                # 获取页面文本
                detail_page_text = detail_response.text
                # 使用 BeautifulSoup 解析页面
                detail_soup = BeautifulSoup(detail_page_text, 'lxml')

                # 获取章节标题
                h1_tag = detail_soup.find('h1', class_='wap_none')
                title = h1_tag.text

                # 获取章节内容
                div_tag = detail_soup.find('div', id='chaptercontent')
                br_tags = div_tag.find_all('br')
                for br_tag in br_tags:
                    br_tag.replace_with('\n')
                content = div_tag.text

                # 构造文件路径，将章节内容写入文件
                file_path = os.path.join(folder_name, f'{title}.txt')
                with open(file_path, 'w', encoding='utf-8') as fp:
                    fp.write(title + "\n" + content + "\n")

                # 打印爬取成功信息，并休眠2秒
                print(title, "爬取成功")
                time.sleep(2)
                break
            except Exception as e:
                # 捕获异常并打印出来
                print(e)
