import matplotlib.pyplot as plt
import numpy as np

# 原始数据
fields = ["success", "1Reentrancy", "2UncheckedCall", "3FailedSend", "4TimestampDependence", "5UnsecuredBalance",
          "6MisuseOfOrigin", "7Suicidal", "8Securify-Reentrancy"]

# 修改后的漏洞顺序
vulnerability_names = [
    'Reentrancy', 'Unsecured Balance', 'Failed Send', 'Unchecked Call',
    'Suicidal', 'Misuse tx.orgin', 'Timestamp_Depend', 'Securify-Reent'
]
labels = vulnerability_names
success = [160794, 44284, 204662, 416]
txspector_true = [11, 8, 0, 0, 26, 1, 0, 0]
txspector_false = [205067, 205070, 205078, 205078, 205052, 205077, 205078, 205078]
framework_true = [426, 273, 59, 7649, 247, 130, 0, 24]
framework_false = [204652, 204805, 205019, 197429, 204831, 204948, 205078, 205054]

# 计算 Both, txspector_True_only, framework_True_only
both = [min(t, f) for t, f in zip(txspector_true, framework_true)]
txspector_true_only = [t - b for t, b in zip(txspector_true, both)]
framework_true_only = [f - b for f, b in zip(framework_true, both)]

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 统计八种漏洞的情况
vulnerability_counts = {
    'TxSpector': txspector_true,
    'Framework': framework_true,
    'Both': both,
    'TxSpector_Only': txspector_true_only,
    'Framework_Only': framework_true_only
}

x = np.arange(len(labels))  # x轴的位置
width = 0.10  # 柱状图的宽度

fig = plt.figure(figsize=(18, 6))
gs = fig.add_gridspec(20, 20)  # 修改为20行20列

ax1 = fig.add_subplot(gs[:, :-3])  # 主图占据前17列 (85%)
ax2 = fig.add_subplot(gs[:10, -3:])  # 第一行右侧饼状图占据最后3列的前10行 (15%)
ax3 = fig.add_subplot(gs[10:, -3:])  # 第二行右侧饼状图占据最后3列的后10行 (15%)

# 使用更素雅的颜色和明显的图案
color_tx = 'peachpuff'
color_framework = 'lightblue'
color_both = 'mediumslateblue'
color_framework_only = 'cornflowerblue'
color_txspector_only = 'orange'

# 八种漏洞的柱状图
rects1 = ax1.bar(x - 2 * width, vulnerability_counts['TxSpector'], width, label='TxSpector Detected', color=color_tx,
                 hatch='//')  # , edgecolor='black')
rects2 = ax1.bar(x - width, vulnerability_counts['Framework'], width, label='Framework Detected', color=color_framework,
                 hatch='\\\\')  # , edgecolor='black')
rects3 = ax1.bar(x, vulnerability_counts['Both'], width, label='Both Detected', color=color_both, hatch='xxx'
                 )  # ,edgecolor='black')
rects4 = ax1.bar(x + width, vulnerability_counts['TxSpector_Only'], width, label='TxSpector True & Framework False',
                 color=color_txspector_only, hatch='///')  # , edgecolor='black')
rects5 = ax1.bar(x + 2 * width, vulnerability_counts['Framework_Only'], width, label='Framework True & TxSpector False',
                 color=color_framework_only, hatch='\\\\\\')  # , edgecolor='black')


# 添加数据标签
# def add_labels(rects, ax):
#     for rect in rects:
#         height = rect.get_height()
#         if height == 0:
#             height_text = '0'
#         else:
#             height_text = '{}'.format(int(height))
#         ax.annotate(height_text,
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 0),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom',
#                     fontsize=10,fontweight='bold',
#                     rotation=-40)  # 调整字体大小
def add_labels(rects, ax, labels):
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        if height == 0:
            height_text = '0'
        else:
            height_text = '{}'.format(int(height))
        if label in ['Suicidal', 'Securify-Reent']:
            rotation = 0
        elif label in ['Timestamp_Depend']:
            rotation = 8
        else:
            rotation = 50
        ax.annotate(height_text,
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=9,
                    rotation=rotation)  # 调整字体大小和旋转角度


add_labels(rects1, ax1, labels)
add_labels(rects2, ax1, labels)
add_labels(rects3, ax1, labels)
add_labels(rects4, ax1, labels)
add_labels(rects5, ax1, labels)

# 设置对数刻度的Y轴
ax1.set_yscale('log')

# 图表美化
ax1.set_xlabel('Attack rule categories', fontsize=12, fontweight='bold')  # 调整x轴字体大小
ax1.set_ylabel('Count of Vulnerable Transactions (Log Scale)', fontsize=14, fontweight='bold')
# ax1.set_title('Database 1 - Comparison of Vulnerability Detection by TxSpector and Framework', fontsize=16,
#               fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=0, fontsize=10, fontweight='bold')  # 调整x轴标签字体大小
ax1.legend(fontsize=12)

# 绘制饼状图（success 的情况）
success_counts_tx = [success[0], success[1]]
success_counts_framework = success[2:]
success_colors = ['#a1c4fd', 'whitesmoke']  # 使用淡雅的颜色
success_hatches = ['///', '']

print(success_counts_tx)
# TxSpector Success 的饼状图
wedges, texts, autotexts = ax2.pie(success_counts_tx, autopct='%1.1f%%', startangle=140, colors=success_colors,
                                   explode=(0.1, 0), wedgeprops={'edgecolor': 'black'})
for i, patch in enumerate(wedges):
    if success_hatches[i]:
        patch.set_hatch(success_hatches[i])
ax2.set_title('TxSpector Success Rate', fontsize=14, fontweight='bold')

# Framework Success 的饼状图
wedges, texts, autotexts = ax3.pie(success_counts_framework, autopct='%1.1f%%', startangle=140, colors=success_colors,
                                   explode=(0.1, 0), wedgeprops={'edgecolor': 'black'})
for i, patch in enumerate(wedges):
    if success_hatches[i]:
        patch.set_hatch(success_hatches[i])
ax3.set_title('Framework Success Rate', fontsize=14, fontweight='bold')

# 设置饼状图字体
for autotext in autotexts:
    autotext.set_fontsize(14)
for text in texts:
    text.set_fontsize(14)


# 添加具体数值的注释
def add_pie_labels(ax, success_count, total_count):
    for i, count in enumerate(success_count):
        angle = (wedges[i].theta2 - wedges[i].theta1) / 2. + wedges[i].theta1
        y = np.sin(np.deg2rad(angle))
        x = np.cos(np.deg2rad(angle))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(angle)
        ax.annotate(f'{count}',
                    xy=(x, y),
                    xytext=(1.35 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment, fontsize=11,
                    arrowprops=dict(arrowstyle="-|>", color='black', connectionstyle=connectionstyle))

print(success_counts_tx)
add_pie_labels(ax2, success_counts_tx, 2656309)
add_pie_labels(ax3, success_counts_framework, 2655742)

# 使用内置样式
plt.style.use('seaborn-v0_8-whitegrid')  # 使用 seaborn-whitegrid 样式

# 调整图表布局
fig.tight_layout()

# 保存为PDF文件
plt.savefig('database1_result.pdf', format='pdf')

# 展示图表
plt.show()

# 显示数据表格
data_table = pd.DataFrame(vulnerability_counts, index=vulnerability_names)
print(data_table)
