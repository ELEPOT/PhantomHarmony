import librosa
#y, sr = librosa.load('/home/pi/PhantomHarmony/example/fiction.mp3',sr=None)
y, sr = librosa.load('/home/pi/PhantomHarmony/test_output/split_by_beat/fiction/00001.mp3',sr=None)
'''
blank=0
print(len(y))
for i in range(len(y)):
    #print(y[i])
    if y[i]==0:
        #print(y[i],i)
        blank=blank+1
print(blank)
avg=blank/len(y)*100
print(avg)
'''
import csv
with open('output.csv', 'w', newline='') as csvfile:
  # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    writer.writerow(y)
