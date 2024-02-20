blank = int(torch.count_nonzero(torch.abs(y) < threshold))  # 計算音樂數值絕對值超過臨界值的數量

avg = blank / torch.numel(y)  # 將超過臨界值的數值數量 / 總數值數量，得到超過臨界值的數值比例
