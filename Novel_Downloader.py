# from www.wenku8.net link get novel txt
# Yu-An Chen by 2020/04/26

# pip install BeautifulSoup4 Flask requests 

from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests

##############################
# web Server 
##############################

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    link = request.form['link']
    novel_list = get_novel_info(link)
    return download_page(novel_list)

def download_page(link_list):
    htmltext = "<html><head><title>Novel Downloader by Yu-An Chen</title></head><body><h2 style=\"color: #2e6c80;\">Novel Downloader</h2>"
    
    for l in link_list:

        tital,id = l.split(',')
        #link = "https://www.wenku8.net/novel/" + ph_id + "/" + novel_id + "/" + id + ".htm"
        download_link = link_decode(id)
        htmltext += "<p>" + tital + "</p><a href=\"" + download_link + "\" class=\"button\">Download</a>"
        
    htmltext += "</body></html>"
    return htmltext


##############################
# novel process 
##############################

def get_novel_info(link):

    global novel_id #,ph_id
    #print("get:%s" % (link))

    # get Publishing house id      V 
    # https://www.wenku8.net/novel/0/471/index.htm
    #index = link.find("/novel/") + 7
    #ph_id = link[index:index+1]

    # get novel id                    V
    # https://www.wenku8.net/novel/0/471/index.htm
    index = link.find("/novel/") + 9
    tmp = link[index:]
    novel_id = tmp[:tmp.find("/")]

    re = requests.get(link)
    re.encoding = 'GBK'
    htmltext = re.text

    soup = BeautifulSoup(htmltext,features="lxml")          # from html text get url
    t = soup.find_all("table", class_= "css")

    t_list = str(t).split("<td class=\"vcss\"")             # using tital to split t
    t_list.remove(t_list[0])                                # cut t_list[0]
    re_list = list()
    for l in t_list:
        #print(l)
        tital = l[l.find(">")+1:l.find("</td>")]            # get tital
        id = l[l.find("a href=\"")+8:l.find(".htm\">")]     # get book number
        re_list.append(tital + "," + id)
    return re_list

def link_decode(id):
    Link = "http://dl.wenku8.com/packtxt.php?aid=" + novel_id + "&vid=" + id + "&charset=big5"
    return Link

##############################
# main function 
##############################

def main():
    app.run(host='127.0.0.1', port=8888)

if __name__ == "__main__":
    main()

