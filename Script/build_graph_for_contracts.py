import pandas as pd
import matplotlib.pyplot as plt
import os

# 使用内置样式
plt.style.use('seaborn-v0_8-whitegrid')

# 定义漏洞及其对应的列名
vulnerabilities = [
    '5UnsecuredBalance',
    '6MisuseOfOrigin',
    '3FailedSend',
    '4TimestampDependence',
    '7Suicidal',
    '1Reentrancy',
    '2UncheckedCall',
    '8Securify-Reentrancy'
]

# 定义列名
columns = ['Transaction', 'Oyente_contract', 'Oyente_callstack', 'Oyente_reentrancy', 'Oyente_time_dependency',
           'Oyente_integer_underflow', 'Oyente_integer_overflow', 'Oyente_money_concurrency',
           'Osiris_contract', 'Osiris_callstack', 'Osiris_reentrancy', 'Osiris_time_dependency',
           'Osiris_integer_underflow', 'Osiris_integer_overflow', 'Osiris_money_concurrency']

# 定义文件路径
base_path = '../contract_transaction/8_vulnerabilities/'
os.makedirs(base_path, exist_ok=True)

# 读取所有CSV文件
data = {}
for tool in ['TxSpector', 'Framework']:
    for vul in vulnerabilities:
        file_path = os.path.join(base_path, f'{tool}_{vul}_record.csv')
        if os.path.exists(file_path):
            data[f'{tool}_{vul}'] = pd.read_csv(file_path)
        else:
            data[f'{tool}_{vul}'] = pd.DataFrame(columns=columns)


# 准备绘图数据
def prepare_data(tool, vul):
    df = data[f'{tool}_{vul}']
    total_transactions = df.shape[0]
    if df.empty:
        return total_transactions, {'callstack': (0, 0), 'reentrancy': (0, 0), 'timestamp_dependency': (0, 0),
                                    'integer_overflow_underflow': (0, 0), 'money_concurrency': (0, 0)}

    # 去重合约地址
    oyente_unique = df['Oyente_contract'].dropna().unique()
    osiris_unique = df['Osiris_contract'].dropna().unique()

    result = {
        'callstack': (df[df['Oyente_callstack'] == True]['Oyente_contract'].dropna().unique().size,
                      df[df['Osiris_callstack'] == True]['Osiris_contract'].dropna().unique().size),
        'reentrancy': (df[df['Oyente_reentrancy'] == True]['Oyente_contract'].dropna().unique().size,
                       df[df['Osiris_reentrancy'] == True]['Osiris_contract'].dropna().unique().size),
        'timestamp_dependency': (df[df['Oyente_time_dependency'] == True]['Oyente_contract'].dropna().unique().size,
                                 df[df['Osiris_time_dependency'] == True]['Osiris_contract'].dropna().unique().size),
        'integer_overflow_underflow': (
            df[(df['Oyente_integer_underflow'] == True) | (df['Oyente_integer_overflow'] == True)][
                'Oyente_contract'].dropna().unique().size,
            df[(df['Osiris_integer_underflow'] == True) | (df['Osiris_integer_overflow'] == True)][
                'Osiris_contract'].dropna().unique().size
        ),
        'money_concurrency': (df[df['Oyente_money_concurrency'] == True]['Oyente_contract'].dropna().unique().size,
                              df[df['Osiris_money_concurrency'] == True]['Osiris_contract'].dropna().unique().size),
    }
    return total_transactions, result


# 绘制柱状图
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.subplots_adjust(hspace=0.4, wspace=0.4, bottom=0.25)  # 为图例留出更多空间

plot_positions = [
    (0, 0), (0, 1), (0, 2), (0, 3),
    (1, 0), (1, 1), (1, 2), (1, 3)
]

titles = [
    'Reentrancy', 'Unsecured Balance', 'Failed Send', 'Unchecked Call',
    'Suicidal', 'Misuse of Origin', 'Timestamp Dependency', 'Securify Reentrancy'
]

patterns = ['|||||', '\\\\', '//', '--']
colors = ['#BBE9FF', '#E2BBE9', '#FFC700', '#9DDE8B']
categories = ['Cs', 'Reen', 'Time', 'Integer', 'TOD']

for i, (vul, title) in enumerate(zip(vulnerabilities, titles)):
    row, col = plot_positions[i]
    ax = axes[row, col]

    # 获取数据
    txspector_total, txspector_data = prepare_data('TxSpector', vul)
    framework_total, framework_data = prepare_data('Framework', vul)

    txspector_values = [txspector_data[cat][0] for cat in
                        ['callstack', 'reentrancy', 'timestamp_dependency', 'integer_overflow_underflow',
                         'money_concurrency']]
    framework_values = [framework_data[cat][0] for cat in
                        ['callstack', 'reentrancy', 'timestamp_dependency', 'integer_overflow_underflow',
                         'money_concurrency']]
    txspector_values_osiris = [txspector_data[cat][1] for cat in
                               ['callstack', 'reentrancy', 'timestamp_dependency', 'integer_overflow_underflow',
                                'money_concurrency']]
    framework_values_osiris = [framework_data[cat][1] for cat in
                               ['callstack', 'reentrancy', 'timestamp_dependency', 'integer_overflow_underflow',
                                'money_concurrency']]

    # 绘制柱状图
    x = range(len(categories))
    bars1 = ax.bar(x, txspector_values, width=0.2, label='TxSpector_Oyente', align='center', hatch=patterns[0],
                   color=colors[0])
    bars2 = ax.bar([p + 0.2 for p in x], txspector_values_osiris, width=0.2, label='TxSpector_Osiris', align='center',
                   hatch=patterns[1], color=colors[1])
    bars3 = ax.bar([p + 0.4 for p in x], framework_values, width=0.2, label='Framework_Oyente', align='center',
                   hatch=patterns[2], color=colors[2])
    bars4 = ax.bar([p + 0.6 for p in x], framework_values_osiris, width=0.2, label='Framework_Osiris', align='center',
                   hatch=patterns[3], color=colors[3])

    # 添加数值标签
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    # 设置标签和标题
    # ax.set_xlabel('Categories')  # 注释掉设置 x 轴标签的部分
    ax.set_ylabel('Number of Contracts')
    total_transactions = max(txspector_total, framework_total)
    ax.set_title(f'{title} ({total_transactions} transactions)')
    ax.set_xticks([p + 0.3 for p in x])
    ax.set_xticklabels(categories, rotation=0, ha='right')

# 添加图例
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.1))


plt.tight_layout()
plt.savefig('../contract_result.pdf', format='pdf')
plt.show()
