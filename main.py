# @author:      Yi Hao
# @email:       isyihao@163.com
# @datetime:    2021/7/16 10:19
import numpy as np
from viewer import generate_emg

from EMG import EMG

# 载入数据
testData = np.load('./data/testData.npz')
EMGData = testData['EMGdata'].flatten().tolist()
pred_1 = testData['pred_1'].flatten().tolist()
pred_2 = testData['pred_2'].flatten().tolist()
total_len = len(EMGData)

# 组建EMG数据
emg = EMG()
emg.file_name = '改成你要保存的文件名'
emg.emg = EMGData
emg.pred1 = pred_1
emg.pred2 = pred_2
emg.length = len(EMGData)

# 绘制EMG图
generate_emg(emg)

