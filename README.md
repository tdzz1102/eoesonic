# eoesonic

## 部署

以docker为例，其他方式可以参考[安装指南](https://www.navidrome.org/docs/installation/)。


初次安装

```bash
pip install -r requirements.txt

# 同步数据库
python main.py sync

# 下载歌曲
python main.py pull

# 启动navidrome服务
docker run -d --name navidrome --restart=unless-stopped  -v `pwd`/Data/music:/music -v `pwd`/Data/data:/data -v `pwd`/navidrome.toml:/navidrome.toml -p 4533:4533 -e ND_CONFIGFILE=/navidrome.toml  deluan/navidrome:develop
```

更新

```bash
python main.py sync
python main.py pull
```

sync会调用eoebeat api，获取歌曲信息（包括下载地址）并插入数据库，pull会下载歌曲到本地，并处理ID3标签。sync和pull都会检查已有的数据，若已存在不会覆盖写入。

docker启动后，访问 http://你的服务器ip:4533/ 进入播放器ui。subsonic api也是这个地址，可以用它登录各种客户端。

## 说明

navidrome的配置选项可以参考[配置指南](https://www.navidrome.org/docs/usage/configuration-options/)。

方便起见，数据默认放在项目文件夹下。项目自用的sqlite文件放在./database.db，navidrome的数据目录为./Data，可以根据需要在`config.ini`中自行更改。

代码更改比较频繁，暂时没有封镜像和加cron的打算，需要手动同步数据。
