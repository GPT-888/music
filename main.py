import streamlit as st
import requests
import inscode

st.set_page_config(page_title='神码观察音乐百宝箱')

# 页面标题
st.title("欢迎使用神码观察音乐百宝箱")

# 接收用户输入的关键词
search = st.text_input("请输入歌曲关键词进行搜索")

# 搜索歌曲
if search:
    url = 'http://music.163.com/api/search/get/web'
    headers = {
        'Referer': 'http://music.163.com',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    params = {
        's': search,
        'type': 1,
        'offset': 0,
        'limit': 10
    }

    response = requests.get(url, headers=headers, params=params)

    result = response.json()

    if result and result['code'] == 200:
        songs = result['result']['songs']
        song_name_list = []
        for song in songs:
            name = song['name']
            artist = song['artists'][0]['name']
            song_name_list.append(name + '-' + artist)
        # 展示搜索结果
        st.write('搜索结果：')
        selected_song = st.selectbox('请选择歌曲', song_name_list)
        song_id = songs[song_name_list.index(selected_song)]['id']

        # 获取歌曲的url
        url = 'http://music.163.com/api/song/enhance/player/url'
        params = {
            'ids': '[' + str(song_id) + ']',
            'br': 320000
        }
        response = requests.get(url, headers=headers, params=params)
        song_url = response.json()['data'][0]['url']
        st.audio(song_url)

# 推荐歌曲
st.markdown("## 推荐歌曲")
liked_songs = st.text_input("请输入您喜欢的歌曲名称，多个歌曲以逗号隔开")
if liked_songs:
    songs = liked_songs.split(',')
    artists = []
    for song in songs:
        inscode_result = inscode.ai('艺术家', song)
        if inscode_result:
            artists.append(inscode_result)
    if artists:
        url = 'http://music.163.com/api/v1/discovery/recommend/songs'
        headers = {
            'Referer': 'http://music.163.com',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Cookie': 'appver=2.0.2'
        }
        params = {
            'songids': '',
            'alg': 'itembased',
            'userid': '1001',
            'page': 0,
            'pagesize': 30
        }
        for artist in artists:
            params['songids'] += get_song_id_by_artist(artist) + ','
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        if result and result['code'] == 200:
            recommend_songs = result['recommend']
            song_name_list = []
            for song in recommend_songs:
                name = song['name']
                artist = song['artists'][0]['name']
                song_name_list.append(name + '-' + artist)
            # 展示推荐结果
            st.write('推荐结果：')
            selected_song = st.selectbox('请选择歌曲', song_name_list)
            song_id = recommend_songs[song_name_list.index(selected_song)]['id']
            # 获取歌曲的url
            url = 'http://music.163.com/api/song/enhance/player/url'
            headers['Cookie'] = 'appver=2.0.2'
            params = {
                'ids': '[' + str(song_id) + ']',
                'br': 320000
            }
            response = requests.get(url, headers=headers, params=params)
            song_url = response.json()['data'][0]['url']
            st.audio(song_url)
    else:
        st.write("没有找到相关的艺术家")

def get_song_id_by_artist(artist):
    '''
    根据艺术家获取歌曲id
    '''
    url = 'http://music.163.com/api/artist/' + str(get_artist_id(artist))
    headers = {
        'Referer': 'http://music.163.com',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    if result and result['code'] == 200:
        hot_songs = result['hotSongs']
        song_ids = []
        for song in hot_songs:
            song_ids.append(str(song['id']))
        return ','.join(song_ids)
    else:
        return ''

def get_artist_id(artist):
    '''
    根据艺术家获取艺术家id
    '''
    url = f'http://music.163.com/api/search/get/web?s={artist}&type=100'
    headers = {
        'Referer': 'http://music.163.com',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    if result and result['code'] == 200:
        artist_id = result['result']['artists'][0]['id']
        return artist_id
    else:
        return ''