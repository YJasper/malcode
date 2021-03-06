# coding=utf-8

import sys
import os
import codecs
import urllib
import urllib2
import re
import time
import base64
from BeautifulSoup import BeautifulSoup


def WriteRes(malName, malTitle, malDesc, malAuthor, malDate, malSrc):
    if not os.path.exists('malcode'):
        os.makedirs('malcode')

    malTitle = malTitle.replace('<em>', '').replace('</em>', '').replace('<strong>', '').replace('</strong>', '')
    malDesc = malDesc.replace('<em>', '').replace('</em>', '').replace('<strong>', '').replace('</strong>', '')
    malAuthor = malAuthor.replace('<em>', '').replace('</em>', '').replace('<strong>', '').replace('</strong>', '')
    malDate = malDate.replace('<em>', '').replace('</em>', '').replace('<strong>', '').replace('</strong>', '')

    content = '\n'.join([malName, malTitle, malDesc, malAuthor, malDate, malSrc])

    file_path = os.path.join('malcode', malName)

    with codecs.open(file_path, 'w', 'utf-8') as file:
        file.write(content)
    # file = codecs.open(file_path, 'a+', 'utf-8')
    # file.write(content + '\n')
    # file.close


def GetPage(url):
    htmlpage = urllib2.urlopen(url).read()
    soup = BeautifulSoup(htmlpage)

    return soup


def GetFile(url, file):
    # url = ''.join(['http://vxheaven.org/dl/', file])

    if not os.path.exists('resource/zeustracker'):
        os.makedirs('resource/zeustracker')

    file_path = os.path.join('resource/zeustracker', file)

    print '[+] start downloading ', file
    urllib.urlretrieve(url, file_path)


'''
def GetMalInfo(url):
    soup = GetPage(url)
    # print soup

    malName = url[33:-4]

    result = soup.find('div', {'class': 's2'})
    # print result

    tmp = result.find('h2')
    if tmp:
        malTitle = tmp.renderContents()

    malDesc = ''
    malAuthor = ''
    malDate = ''

    tmp = result.findAll('p')
    lenth = len(tmp)

    if (lenth > 0):
        malDesc = tmp[0].renderContents()

        if (lenth > 1):
            malAuthor = tmp[1].renderContents()

            if (lenth > 2):
                malDate = tmp[2].renderContents()

    # tmp = result.find('form')
    tmp = result.find('input', {'type': 'hidden'}, {
                      'name': 'file'}).get('value')
    tmp = tmp.replace('@', '=')
    malFile = base64.b64decode(tmp)
    malSrc = ''.join(['http://vxheaven.org/dl/', malFile])

    WriteRes(malName, malTitle, malDesc, malAuthor, malDate, malSrc)
    GetFile(malSrc, malFile)
'''


def GetMalcode(url):
    soup = GetPage(url)
    # print soup

    results = soup.findAll('a', {'title': 'download file'}, {'href': re.compile(r'monitor.php?show=(.+)')})
    for result in results:
        tmp = result.get('href')

        index_show = tmp.index('show=')
        index_hash = tmp.index('&hash=')
        index_down = tmp.index('&download')
        file_suffix = tmp[index_show + 5: index_hash]
        file_name = tmp[index_hash + 6: index_down]
        file = '.'.join([file_name, file_suffix])

        src_url = ''.join(['https://zeustracker.abuse.ch/', tmp])
        # GetMalInfo(src_url)
        GetFile(src_url, file)


if __name__ == '__main__':
    baseurl = "https://zeustracker.abuse.ch/monitor.php?browse=binaries"
    # SearchNews()
    GetMalcode(baseurl)
