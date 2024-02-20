# 從 0 開始直到 0.5，持續把臨界值加 0.001
for threshold in np.arange(0, 0.5, 0.001):
    writer.writerow(
        [
            detect_blank_music(os.path.join(EXAMPLE_DIR, "vocals_full.mp3"), threshold=threshold),
            detect_blank_music(os.path.join(EXAMPLE_DIR, "vocals_blank.mp3"), threshold=threshold),
        ]
    )
