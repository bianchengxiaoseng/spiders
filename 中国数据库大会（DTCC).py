# encoding: utf-8
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
 
 
def visit(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "st_user_token=798e0f7985d5137259ba45c398a76024; account_user=70001331|XU_JUNQI|http://img.account.itpub.net/head/user.jpg?x-oss-process=style/m; Hm_lvt_07e252e5a1f7f0397d666cafe06db6c8=1622549131,1622549259; Hm_lpvt_07e252e5a1f7f0397d666cafe06db6c8=1622550997",  
        "referer": "",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
    }
 
    res = requests.get(url,headers=headers)
    bsObj = BeautifulSoup(res.text, "html.parser")
    return bsObj
 
 
def visit_homepage(url):
    bsObj = visit(url)
    content = bsObj.find('div', class_="content")
    content_list = content.select("p")
 
    category = []
    for i in range(4,len(content_list)):
        try:
            urls = content_list[i].a['href']
            name = content_list[i].get_text("|").split("|")[0].replace(' ','').replace('\xa0','')
            category.append([name,urls])
        except:
            pass
    print(category)
    return category
 
 
def download_pdf(conf,path):
    category_name = conf[0]
    category_url = conf[1]
    bsObj = visit(category_url)
 
    res = re.search(r'(.*)token:(.*?),',str(bsObj) ,re.M|re.I)
    token = res.group(2).replace('"','').replace(' ','')
 
    arts = re.findall(r'(.*)li data-docinfo=(.*?)}',str(bsObj) ,re.M|re.I)
    for art in arts:
        art_str = "{"+str(art).split('{')[1].replace("')","}")
        art_dic = json.loads(art_str)
        id = art_dic['id']
        name = art_dic['name']
        download_url = "https://api.z.itpub.net/download/file?st-usertoken=%s&id=%s"%(token,str(id))
        print(download_url)
        data = urlopen(download_url).read()
        with open(path+category_name+'__'+name, 'wb') as f:
            f.write(data)
            print("finish download  ")
 
 
if __name__ == '__main__':
    homepage = "https://z.itpub.net/article/detail/5260C494873379BAA63BAB7C5CBD7A95"
    path = "/Users/gs59567/books/"
 
    # download
    category = visit_homepage(homepage)
    for i in category:
        download_pdf(i,path)
