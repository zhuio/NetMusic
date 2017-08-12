import re
import requests
import os

# http://music.163.com/#/playlist?id=643439691
class PlayList:
    def __init__(self,url):
        self.url = url
        self.dicts = {}
    def generate(self):
        id = re.findall(r'id=(.*)',self.url)[0]
        print(id)
        j = requests.get('https://api.imjad.cn/cloudmusic/?type=playlist&id=' + id).json()
        ll = len(j['privileges'])
        # # 歌手名字列表
        # singer_name = []
        # for i in range(0,ll):
        #     singer_name.append(str(j['playlist']['tracks'][i]['ar'][0]['name']))

        # 歌曲名字列表
        song_name = []
        for i in range(0,ll):
            song_name.append(str(j['playlist']['tracks'][i]['name']))

        #获取歌曲ID
        print('正在获取歌曲id.......')
        song_id = []
        for i in range(0,len(j['privileges'])):
            song_id.append(str(j['privileges'][i]['id']))


        # 获取歌曲列表的URL
        print('整理歌曲列表中......')
        songs_url = []
        for id in song_id:
            songs_url.append('https://api.imjad.cn/cloudmusic/?type=song&id=%s&br=320000' % id)

        #获取下载地址
        print('获取下载地址中......')
        download_urls = []
        for song_url in songs_url:
            url = requests.get(song_url).json()['data'][0]['url']
            download_urls.append(url)

        #生成字典
        print('正在生成字典.........')
        download_dicts = {}
        for i in range(len(song_name)):
            download_dicts[song_name[i]] = download_urls[i]
        self.dicts = download_dicts

    def download(self):
        pwd = os.path.abspath('.')
        directory = pwd+'/'+'music'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for key in self.dicts:
            if self.dicts[key] == None:
                print('这首%s有版权问题' % key)
                # continue
            elif os.path.exists(directory+'/'+'%s.mp3' % key):
                print('已经下载过这首歌曲了，跳过......')
                # continue
            else:
                try:
                    r = requests.get(self.dicts[key])
                except Exception as e:
                    print(self.dicts[key])
                    raise e
                # finally:
                #     continue

                print('开始下载%s到当前的文件夹' % key)
                with open(directory+'/'+'%s.mp3' % key, 'wb') as f:
                    f.write(r.content)
        print('好像下载完成了呢！')


def main():
    print('输入网址')
    p = PlayList(url=input())
    p.generate()
    p.download()
if __name__ == '__main__':
    main()
