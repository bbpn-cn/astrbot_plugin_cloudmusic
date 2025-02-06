import aiohttp
import asyncio

class NeteaseCloudMusicAPI:
    def __init__(self):
        self.baseurls = ["https://netease-music.api.harisfox.com/", "https://neteasecloudmusicapi.vercel.app", ]
        self.session = aiohttp.ClientSession()

    async def fetch_song_detail(self, song_id):
        for baseurl in self.baseurls:
            try:
                detail_url = f"{baseurl}/song/detail?ids={song_id}"
                async with self.session.get(detail_url) as detail_response:
                    if detail_response.status == 200:
                        detail_data = await detail_response.json()
                        return detail_data['songs'][0]
            except Exception as e:
                print(f"Error with {baseurl}: {e}")
        return None

    async def fetch_song_data(self, keywords, limit=5, pic=True):
        for baseurl in self.baseurls:
            try:
                url = f"{baseurl}/search?keywords={keywords}"
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = []
                        cnt = 0
                        for song in data['result']['songs']:
                            song_id = song['id']
                            
                            artists = [artist['name'] for artist in song['artists']]
                            song_info = {
                                'id': song_id,
                                'name': song['name'],
                                'artists': artists,
                                'album': song['album']['name'],
                            }
                            if pic:
                                song_detail = await self.fetch_song_detail(song_id)
                                song_info['album_img1v1Url']= song_detail['al']['picUrl']
                            result.append(song_info)
                            cnt += 1
                            if cnt >= limit:
                                break
                        return result
            except Exception as e:
                print(f"Error with {baseurl}: {e}")
        return []

    async def fetch_song_comments(self, song_id, limit=5):
        for baseurl in self.baseurls:
            try:
                url = f"{baseurl}/comment/music?id={song_id}"
                async with self.session.get(url, ) as response:
                    if response.status == 200:
                        data = await response.json()
                        comments = []
                        cnt = 0
                        for comment in data['hotComments']:
                            comment_info = {
                                'user_nickname': comment['user']['nickname'],
                                'content': comment['content'],
                                'likedCount': comment['likedCount']
                            }
                            comments.append(comment_info)
                            cnt += 1
                            if cnt >= limit:
                                break
                        return comments
            except Exception as e:
                print(f"Error with {baseurl}: {e}")
        return []

    async def fetch_song_lyrics(self, song_id):
        for baseurl in self.baseurls:
            try:
                url = f"{baseurl}/lyric?id={song_id}"
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('lrc', {}).get('lyric', '歌词未找到')
            except Exception as e:
                print(f"Error with {baseurl}: {e}")
        return '歌词未找到'

    async def close(self):
        await self.session.close()