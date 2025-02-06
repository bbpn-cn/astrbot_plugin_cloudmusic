# AstrBot 网易云音乐插件

这是一个用于 AstrBot 的插件，提供网易云音乐搜索、热评和歌词功能。

## 功能

- 搜索音乐并以精美的图片卡片输出，附带热评
- 搜索音乐并输出前 3 条文本的歌曲信息

## 使用方法

### 搜索音乐并以精美的图片卡片输出，附带热评

命令：`/songp song_name`

示例：
```
/songp 海阔天空
```

### 搜索音乐并输出前 3 条文本的歌曲信息

命令：`/song song_name`

示例：
```
/song 海阔天空
```

### LLM 函数调用 

默认支持通过自然语言搜歌，比如: `搜索 all my life 这首歌`

需要模型支持函数调用，推荐 `gpt-4o-mini`

关闭这个功能 `/tool off search_music`

## 支持

[帮助文档](https://astrbot.soulter.top/center/docs/%E5%BC%80%E5%8F%91/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91/)
