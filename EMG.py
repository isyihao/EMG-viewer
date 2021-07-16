# @author:      Yi Hao
# @email:       isyihao@163.com
# @datetime:    2021/7/16 16:27
from typing import List


class EMG:
    # 文件名
    file_name: str = 'Test-EMG'
    # 数据长度
    length: int = 0
    # 拆图偏移量
    offset: int = 0
    # emg数据
    emg: List[float] = []
    # pred1数据
    pred1: List[float] = []
    # pred2数据
    pred2: List[float] = []
