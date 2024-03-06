from matplotlib.font_manager import FontProperties as font
import matplotlib

from paths import TEST_OUTPUT_DIR, PROJECT_DIR
import matplotlib.pyplot as plt
import numpy as np

valid_tags = [
    "guitar",
    "techno",
    "electronic",
    "rock",
    "piano",
    "ambient",
    "indian",
    "opera",
    "dance",
    "country",
    "new age",
    "metal",
]

CHtw_f = font(fname=PROJECT_DIR / "NotoSansTC-Medium.ttf")
with open(TEST_OUTPUT_DIR / "test_musicnn.npy", "rb") as f:
    arr = np.load(f)
    arr = np.flip(arr, axis=0)

print(arr)

plt.figure(dpi=300)

plt.subplots_adjust(bottom=0.25, top=0.9)
ax = plt.subplot()
ax.set_title("實際音樂類型與預測音樂類型之關聯熱圖", fontproperties=CHtw_f)
ax.xaxis.set_label_text("預測類型 (musicnn)", fontproperties=CHtw_f)
ax.yaxis.set_label_text("實際類型 (spotify-track-dataset)", fontproperties=CHtw_f)
ax.xaxis.set_ticks(np.arange(len(valid_tags)))
ax.xaxis.set_ticklabels(valid_tags, rotation=90)
valid_tags.reverse()
ax.yaxis.set_ticks(np.arange(len(valid_tags)))
ax.yaxis.set_ticklabels(valid_tags)
ax.imshow(arr)
# plt.xticks(np.arange(len(valid_tags)), valid_tags, rotation=-90, verticalalignment="bottom")
# plt.yticks(np.arange(len(valid_tags)), valid_tags)
# plt.title("")
# plt.xlabel("預測類型 (musicnn)", fontproperties=CHtw_f)
# plt.ylabel("實際類型 (spotify-track-dataset)", fontproperties=CHtw_f)

plt.show()
