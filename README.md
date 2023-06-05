# eoesonic

```bash
docker run -d --name navidrome --restart=unless-stopped  -v `pwd`/Data/music:/music -v `pwd`/Data/data:/data -v `pwd`/navidrome.toml:/navidrome.toml -v `pwd`/static:/static -p 8080:4533 -e ND_CONFIGFILE=/navidrome.toml  deluan/navidrome:develop
```