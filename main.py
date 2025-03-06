from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from .api import NeteaseCloudMusicAPI
from astrbot.api.message_components import Forward

HTML_TMPL = """
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <title>{{ song_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #ffffff; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background-color: #1e1e1e; padding: 40px; box-sizing: border-box; display: flex; border-radius: 10px; }
        .song { flex: 1; text-align: center; }
        .song img { max-width: 100%; border-radius: 10px; }
        .song h1 { font-size: 48px; margin: 20px 0; }
        .comments { flex: 2; margin-left: 40px; }
        .comment { margin-bottom: 20px; padding: 20px; border-bottom: 1px solid #333; }
        .comment p { margin: 0; font-size: 28px; }
        .comment strong { color: #ffffff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="song">
            <img src="{{ album_img1v1Url }}" alt="Album Cover">
            <h1>{{ song_name }}</h1>
        </div>
        <div class="comments">
            <h2>热评:</h2>
            {% for comment in comments %}
            <div class="comment">
                <p><strong>{{ comment.user_nickname }}:</strong> {{ comment.content }} (Likes: {{ comment.likedCount }})</p>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""


@register("astrbot_plugin_cloudmusic", "mika", "网易云音乐搜索、热评", "1.0.0", "https://github.com/AstrBot-Devs/astrbot_plugin_cloudmusic")
class CloudMusicPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.command("音乐热评")
    async def get_song(self, event: AstrMessageEvent):
        '''搜索音乐并以精美的图片卡片输出，附带热评。'''
        tokens = self.parse_commands(event.message_str)
        if tokens.len < 2:
            yield event.plain_result("请输入音乐名。")
            return
        song_name = " ".join(tokens.tokens[1:])
        
        api = NeteaseCloudMusicAPI()
        try:
            songs = await api.fetch_song_data(song_name, limit=1)
            if not songs:
                yield event.plain_result("未找到相关音乐。")
                return

            song = songs[0]
            song_id = song['id']
            song_name = song['name']
            album_img1v1Url = song['album_img1v1Url']
            comments = await api.fetch_song_comments(song_id, limit=3)
            if comments:
                comments_data = [{'user_nickname': c['user_nickname'], 'content': c['content'], 'likedCount': c['likedCount']} for c in comments]
            else:
                comments_data = []

            url = await self.html_render(HTML_TMPL, {
                "song_name": song_name, 
                "album_img1v1Url": album_img1v1Url,
                "comments": comments_data
            }, return_url=True)
            yield event.image_result(url)
        except Exception as e:
            yield event.plain_result(f"发生错误: {e}")
        finally:
            await api.close()
                        
    @filter.command("音乐")
    async def get_song_list(self, event: AstrMessageEvent):
        '''搜索音乐并输出前 3 条文本的歌曲信息。'''
        tokens = self.parse_commands(event.message_str)
        if tokens.len < 2:
            yield event.plain_result("请输入音乐名。")
            return
        song_name = " ".join(tokens.tokens[1:])
        
        api = NeteaseCloudMusicAPI()
        try:
            songs = await api.fetch_song_data(song_name, limit=3, pic=False)
            if not songs:
                yield event.plain_result("未找到相关音乐。")
                return

            result = "🎵 搜索结果：\n"
            for idx, song in enumerate(songs, start=1):
                result += f"{idx}. 🎤 歌曲名: {song['name']}\n"
                result += f"   🆔 歌曲ID: {song['id']}\n"
                result += f"   🎙️ 歌手: {', '.join(song['artists'])}\n"
                result += f"   📀 专辑: {song['album']}\n"
                result += f"   🔗 链接: https://music.163.com/#/song?id={song['id']}\n"
            result = event.plain_result(result)
            result.use_t2i(False)
            yield result
        except Exception as e:
            yield event.plain_result(f"搜索过程中出现错误: {e}")

    @filter.llm_tool("search_music")
    async def search_music(self, event: AstrMessageEvent, keyword: str):
        '''根据关键词搜索音乐
        
        Args:
            keyword(string): 音乐名或者关键词
        '''
        song_name = keyword
        
        api = NeteaseCloudMusicAPI()
        try:
            songs = await api.fetch_song_data(song_name, limit=3, pic=False)
            if not songs:
                return event.plain_result("未找到相关音乐。")
            result = "🎵 搜索结果(网易云音乐)：\n"
            for idx, song in enumerate(songs, start=1):
                result += f"{idx}. 🎤 歌曲名: {song['name']}\n"
                result += f"   🆔 歌曲ID: {song['id']}\n"
                result += f"   🎙️ 歌手: {', '.join(song['artists'])}\n"
                result += f"   📀 专辑: {song['album']}\n"
                result += f"   链接: https://music.163.com/#/song?id={song['id']}\n"
            return result
        except Exception as e:
            return event.plain_result(f"搜索过程中出现错误: {e}")
