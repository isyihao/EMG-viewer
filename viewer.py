# @author:      Yi Hao
# @email:       isyihao@163.com
# @datetime:    2021/6/2 16:08
import numpy as np
import yaml
from matplotlib import pyplot as plt

# 加载配置文件
from EMG import EMG

with open('./config.yaml', encoding='utf-8') as fs:
    config = yaml.load(fs, Loader=yaml.FullLoader)


def config_plate(plt, total_len):
    plt.xticks([])

    # y轴标签 0.1一个刻度
    plt.yticks([index for index in np.arange(-1, 1, 0.1)])

    # 每隔200个点（20秒） 绘制一条灰色竖直分割线
    for index in range(1, int(total_len / 200) + 1):
        plt.vlines(index * 200, -1, 1, colors='#DDDDDD', linestyles='solid', linewidth=0.75)

    # 每隔600个点（1分钟） 绘制一条深灰色竖直分割线
    for index in range(1, int(total_len / 600) + 1):
        plt.vlines(index * 600, -1, 1, colors='#6D6D6D', linestyles='solid', linewidth=1.5)

    # 每隔0.1,绘制一条灰色水平分割线
    for index in np.arange(-1, 1, 0.1):
        plt.hlines(index, 0, total_len, colors='#DDDDDD', linestyles='solid', linewidth=0.75)

    # 每隔0.5,绘制一条深灰色水平分割线
    for index in np.arange(-1, 1, 0.5):
        plt.hlines(index, 0, total_len, colors='#6D6D6D', linestyles='solid', linewidth=2)

    # 绘制-1 -0.8 -0.6 ... 指标文字
    font = dict(fontsize=12, color='#265580', family='SimHei', weight='bold', style='normal')
    for y in np.arange(-1, 1, 0.2):
        for x in range(600, int(total_len), 600):
            plt.text(x + 2, y + 1 / 100, str(round(y, 1)), fontdict=font)


def generate_emg(emg: EMG):
    total_len = emg.length
    limit_len = config['emg']['limit-len'] or 240 * 240
    # 过长则拆分左右两份
    if total_len > limit_len:
        # 组建左半部分数据
        left = EMG()
        left.file_name = emg.file_name
        left.offset = emg.offset
        left.length = limit_len
        left.emg = emg.emg[:limit_len]
        left.pred1 = emg.pred1[:limit_len]
        left.pred2 = emg.pred2[:limit_len]
        generate_emg(left)

        # 组建右半部分数据
        right = EMG()
        right.file_name = emg.file_name
        right.offset = emg.offset + limit_len
        right.length = emg.length - limit_len
        right.emg = emg.emg[limit_len:]
        right.pred1 = emg.pred1[limit_len:]
        right.pred2 = emg.pred2[limit_len:]
        generate_emg(right)
        return

    # 图像尺寸
    file_width = total_len / 100
    plt.figure(1, figsize=(file_width, 11))

    # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 用来正常显示负号
    plt.rcParams['axes.unicode_minus'] = False

    # 绘制emg面板 左下角顶点(0,0.7),横向沾满1.0,纵向占0.3
    plt.axes([0, 0.7, 1.0, 0.3])
    # 坐标轴范围
    plt.axis([0, total_len, -1, 1])

    # 配置面板
    config_plate(plt, total_len)

    # 绘制emg数据
    x = list(range(total_len))
    plt.plot(x, emg.emg,
             color=config['emg']['emg']['color'],
             linestyle='-',
             linewidth=config['emg']['emg']['width'],
             label='emg')

    # 绘制pred1面板 左下角顶点(0,0.6) 横向沾满1.0,纵向高0.3
    plt.axes([0, 0.38, 1.0, 0.3])
    # 坐标轴范围
    plt.axis([0, total_len, -1, 1])
    # 配置面板
    config_plate(plt, total_len)
    # 绘制pred1数据
    x = list(range(total_len))
    plt.plot(x, emg.pred1,
             color=config['emg']['pred1']['color'],
             linestyle='-',
             linewidth=config['emg']['pred1']['width'],
             label='pred1')

    # 绘制pred2面板 左下角顶点(0,0.6) 横向沾满1.0,纵向高0.3
    plt.axes([0, 0.06, 1.0, 0.3])
    # 坐标轴范围
    plt.axis([0, total_len, -1, 1])
    # 配置面板
    config_plate(plt, total_len)
    # 绘制pred2数据
    x = list(range(total_len))
    plt.plot(x, emg.pred2,
             color=config['emg']['pred2']['color'],
             linestyle='-',
             linewidth=config['emg']['pred2']['width'],
             label='pred2')

    # x轴标签 每600个点标注一下分钟数
    plt.xticks([index * 600 for index in range(1, int(total_len / 600) + 1)],
               [str(int(index + emg.offset / 600)) + "分" for index in range(1, int(total_len / 600) + 1)], fontsize=12)

    plt.legend()

    # 绘制表头
    # title = ctg.fetal_name + "(" + str(int(ctg.offset / 240)) + "-" + str(int((ctg.offset + ctg.length) / 240)) + ")"
    # plt.title(title)

    # 保存PDF
    file_name = emg.file_name + "(" + str(int(emg.offset / 600)) + "-" + str(int((emg.offset + emg.length) / 600)) + ")"
    absolute_path = config['emg']['save-path'] + '/' + file_name + '.pdf'
    plt.savefig(absolute_path, dpi=240)
    plt.close()
    print("%s is ok" % file_name)
