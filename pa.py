import requests
from bs4 import BeautifulSoup


def get_title_by_id(problem_id):
    url = f"https://www.acwing.com/problem/search/1/?search_content={problem_id}"

    try:
        # 发送 GET 请求
        r = requests.get(url)

        # 解析 HTML
        soup = BeautifulSoup(r.text, "html.parser")

        # 查找搜索结果中的第一个链接，即题目页面链接
        link = soup.select_one("table tbody tr:nth-of-type(1) td:nth-of-type(3) a")

        # 如果找到了链接，则返回链接的文本内容和链接
        if link:
            return {
                "title": link.text.strip(),
                "link": "https://www.acwing.com" + link.get("href")
            }
        else:
            return None
    except Exception as e:
        # 处理异常情况，例如打印错误日志
        print(e)
        return None