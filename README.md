# minuofans

## todo

- __添加artist.\*图片，可能仍要调整目录结构__

- 排查问题，检查下载失败的情况（估计是歌曲以外的信息报错，没有继续处理而是直接raise了）
    - IncompleteRead 只能retry
    - not a mp4 file 存在mp3和wav
    

- 按时间倒序导入，否则recently added会很乱

- ->重构pull逻辑，将Pull作为Song的代理类

- 根据[文档](https://www.navidrome.org/docs/usage/artwork/)，应该是 歌手/专辑/歌曲 的形式，在歌手一级下放置artist.*

- coverUrl和thumbnailUrl并用

- 试试vmiss hk
    - 效果很差，内存太小？

## 目录结构

```
Data/
├── 2022-07
├── 2022-08
├── 2022-09
├── 2022-10
├── 2022-11
├── 2022-12
├── 2023-01
├── 2023-02
├── 2023-03
├── 2023-04
├── 2023-05
└── artist.png
```

## m4a文件tag

```py
>>> m.tags.keys()
dict_keys(['©nam', '©ART', '©wrt', '©alb', '©gen', '©day', '©too', 'covr', 'aART', '©cmt'])
```