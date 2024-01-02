# PhantomHarmony 幻音諧侶

accompaniment generation AI for a science fair project.

如何抓資料：

**注意：目前因為 windows 路徑字元格式問題，有些程式只能跑在 linux 上，因此沒裝 linux 了話建議用 wsl 跑**

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

把 windows_data_dir 或 linux_data_dir 改成你想要放抓下來資料的地方：

```yaml
# -- config.yaml
windows_data_dir: "D:/data"
linux_data_dir: "/mnt/d/data"
```

在 music_scraper.py 的一開始，設定抓資料的設定：

```python
link_src: str = "maharshipandya/spotify-tracks-dataset"
output_dir: str = os.path.join(DATA_DIR, "dataset", "spotify_114k")  # 抓取資料相對於 DATA_DIR 的存放位置
shuffle: bool = True  # 是否以隨機順序抓取 (隨機抓取都是使用相同的隨機種子，因此跑數次順序都會是一樣的)
start_index: int = 0
end_index: int = -1  # -1 表示抓到最後一個項
exclude_genre: list[str] = ["classical", "sleep", "study"]  # 不抓的音樂類型
min_duration_ms = 2 * 60 * 1000
max_duration_ms = 7 * 60 * 1000
```