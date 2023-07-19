# eoesonic

```bash
pip install -r requirements.txt

python main.py auto

docker run -d --name navidrome --restart=unless-stopped  -v `pwd`/Data/music:/music -v `pwd`/Data/data:/data -v `pwd`/navidrome.toml:/navidrome.toml -p 4533:4533 -e ND_CONFIGFILE=/navidrome.toml  deluan/navidrome:develop
```
