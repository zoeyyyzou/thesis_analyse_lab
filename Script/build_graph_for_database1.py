"""
This script is used to build the graph for the database 1.
RUN: python3 build_graph_for_database1.py
"""
"""
success 的数据单独展示在一个小图
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 读取 CSV 文件
failure_analysis = pd.read_csv('../database1/failure_stat.csv')

# 八种漏洞的文件路径
vulnerability_files = [
    '../database1/5UnsecuredBalance_analysis.csv', '../database1/6MisuseOfOrigin_analysis.csv',
    '../database1/3FailedSend_analysis.csv', '../database1/4TimestampDependence_analysis.csv',
    '../database1/7Suicidal_analysis.csv', '../database1/1Reentrancy_analysis.csv',
    '../database1/2UncheckedCall_analysis.csv', '../database1/8Securify-Reentrancy_analysis.csv'
]

# 修改后的漏洞顺序
vulnerability_names = [
    'Reentrancy', 'Unsecured Balance', 'Failed Send', 'Unchecked Call',
    'Suicidal', 'Misuse tx.orgin', 'Timestamp_Depend', 'Securify-Reent'
]

# 统计 success = True 的情况
success_true_tx = 2656309 - len(failure_analysis[failure_analysis['TxSpector_False'].notna()])
success_true_framework = 2655742 - len(failure_analysis[failure_analysis['Framework_False'].notna()])

# 统计八种漏洞的情况
vulnerability_counts = {
    'TxSpector': [],
    'Framework': [],
    'Both': [],
    'Framework_Only': [],
    'TxSpector_Only': []
}

# 处理每个漏洞文件
for file in vulnerability_files:
    df = pd.read_csv(file)
    df.rename(columns={'tameOri_TxSpector_TRUE': 'Ori_TxSpector_TRUE'}, inplace=True, errors='ignore')

    vulnerability_counts['Framework'].append(len(df['TxSpector_TRUE'].dropna()))
    vulnerability_counts['TxSpector'].append(len(df['Ori_TxSpector_TRUE'].dropna()))
    vulnerability_counts['Both'].append(len(df['Ori_TRUE_Tx_TRUE'].dropna()))

    framework_only = df[(df['Ori_FALSE_Tx_TRUE'].notna()) & (df['Ori_TRUE_Tx_FALSE'].isna())]
    txspector_only = df[(df['Ori_TRUE_Tx_FALSE'].notna()) & (df['Ori_FALSE_Tx_TRUE'].isna())]

    vulnerability_counts['Framework_Only'].append(len(framework_only))
    vulnerability_counts['TxSpector_Only'].append(len(txspector_only))

# 按照指定顺序重新排序漏洞计数
vulnerability_counts = {k: [vulnerability_counts[k][i] for i in [5, 0, 2, 6, 4, 1, 3, 7]] for k in vulnerability_counts}

# 绘制主图（八种漏洞）
labels = vulnerability_names
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
                 hatch='//') #, edgecolor='black')
rects2 = ax1.bar(x - width, vulnerability_counts['Framework'], width, label='Framework Detected', color=color_framework,
                 hatch='\\\\') #, edgecolor='black')
rects3 = ax1.bar(x, vulnerability_counts['Both'], width, label='Both Detected', color=color_both, hatch='xxx'
                 ) #,edgecolor='black')
rects4 = ax1.bar(x + width, vulnerability_counts['TxSpector_Only'], width, label='TxSpector True & Framework False',
                 color=color_txspector_only, hatch='///') #, edgecolor='black')
rects5 = ax1.bar(x + 2 * width, vulnerability_counts['Framework_Only'], width, label='Framework True & TxSpector False',
                 color=color_framework_only, hatch='\\\\\\') #, edgecolor='black')


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
        if label in ['Suicidal',  'Securify-Reent']:
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
success_counts_tx = [success_true_tx, 2656309 - success_true_tx]
success_counts_framework = [success_true_framework, 2655742 - success_true_framework]
success_colors = ['#a1c4fd', 'whitesmoke']  # 使用淡雅的颜色
success_hatches = ['///', '']

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


add_pie_labels(ax2, success_counts_tx, 2656309)
add_pie_labels(ax3, success_counts_framework, 2655742)

# 使用内置样式
plt.style.use('seaborn-v0_8-whitegrid')  # 使用 seaborn-whitegrid 样式

# 调整图表布局
fig.tight_layout()

# 保存为PDF文件
plt.savefig('../database1/database1_result.pdf', format='pdf')

# 展示图表
plt.show()

# 显示数据表格
data_table = pd.DataFrame(vulnerability_counts, index=vulnerability_names)
print(data_table)
