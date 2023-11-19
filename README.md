# PhantomHarmony 幻音諧侶
accompaniment generation AI for a science fair project.

如何抓資料：

**注意：目前因為 windows 路徑字元格式問題，程式只能跑在 linux 上**

用 git clone 下來的資料夾裡：

建一個虛擬環境：

```commandline
sudo apt-get update
sudo apt-get install python3.9
pip3 install virtualenv
virtualenv --python python3.9 venv
```

啟用虛擬環境：
```commandline
source venv/bin/activate
```

裝需要的東西：
```commandline
pip install -r requirements.txt
```
不過說實在如果你只需要抓資料只需要裝這兩個即可：
```commandline
pip install -e ytmdl
pip install datasets
```

把 DATA_DIR 改成你想要放抓下來資料的地方：
```python
# -- config.py
DATA_DIR = '資料存放位置'
```


在 music_scraper.py 的最下面，設定抓資料的開始與結束：
```python
dataset = Dataset(
    link_src='maharshipandya/spotify-tracks-dataset',
    track_name_col='track_name',
    artists_col='artists',
    output_dir=f'{DATA_DIR}/dataset/spotify_114k',
    start_index='開始',
    end_index='結束'
)
```