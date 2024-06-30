"""
脚本一是用来生成不同框架之间的对比结果的（database2）
⚠️：已经有新代码替代lab_build_graph_for_database2.py，不再使用脚本一。
不删除主要为了避免特殊情况下的使用。
"""

# import matplotlib.pyplot as plt
# import numpy as np
#
# # Updated data order and color (professional academic style)
# ordered_labels = [
#     'Reentrancy', 'UnsecuredBalance', 'FailedSend', 'UncheckedCall', 'Suicidal',
#     'MisuseOfOrigin', 'TimestampDependence', 'Securify-Reentrancy'
# ]
#
# data = {
#     'UnsecuredBalance':        (247, 26),
#     'MisuseOfOrigin':          (130, 1),
#     'FailedSend':              (59, 0),
#     'TimestampDependence':     (7649, 0),
#     'Suicidal':                (0, 0),
#     'Reentrancy':              (426, 11),
#     'UncheckedCall':           (273, 8),
#     'Securify-Reentrancy':     (24, 0)
# }
#
# framework_counts = [data[label][0] for label in ordered_labels]
# txspector_counts = [data[label][1] for label in ordered_labels]
#
# # Professional color scheme for IEEE or ACM
# colors_framework = 'navy'  # Deep blue for professional look
# colors_txspector = 'grey'  # Grey for contrast
#
# # Figure setup for academic publication
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.set_yscale('log')
# ind = np.arange(len(ordered_labels))
# width = 0.35
#
# # Creating bars
# txspector_bars = ax.bar(ind - width/2, txspector_counts, width, label='TxSpector', color=colors_txspector)
# framework_bars = ax.bar(ind + width/2, framework_counts, width, label='Framework', color=colors_framework)
#
# # Enhancing labels and ticks for readability and professionalism
# ax.set_xlabel('Attack Rule Types', fontsize=12, fontweight='bold')
# ax.set_ylabel('Count of Detected Transactions (Log Scale)', fontsize=12, fontweight='bold')
# ax.set_title('Comparison of Vulnerability Detection by Rule Type', fontsize=14, fontweight='bold')
# ax.set_xticks(ind)
# ax.set_xticklabels(ordered_labels, rotation=45, ha="right", fontsize=10)
# ax.legend()
#
# # Adding data labels
# def add_labels(bars):
#     for bar in bars:
#         height = bar.get_height()
#         ax.annotate(f'{height if height != 0 else 0}',
#                     xy=(bar.get_x() + bar.get_width() / 2, max(height, 1)),
#                     xytext=(0, 3),
#                     textcoords="offset points",
#                     ha='center', va='bottom', fontsize=9)
#
# add_labels(txspector_bars)
# add_labels(framework_bars)
#
# # Save and show
# plt.tight_layout()
# plt.savefig('vulnerability_detection_comparison_academic.pdf')
# plt.show()


"""
脚本2:是用来生成合约和交易之间的对比关系的（database1）
后续需要添加合约和交易检测漏洞之间的关系

run: python generate_graph_for_contract_mapping.py
"""
import matplotlib.pyplot as plt
import numpy as np

def build_contract_mapping_figure():
    # Provided data
    categories = ['1-10', '11-50', '51-100', '101-300', '301-700', '701-1000', '1001-5000', '5001-10000', '10001+']
    contracts = [17250, 3777, 968, 1115, 651, 266, 842, 264, 624]

    # Normalize contract values for color mapping with increased color difference
    norm = plt.Normalize(min(contracts), max(contracts))
    colors = plt.cm.Blues(norm(contracts) * 0.6)  # Increase color difference

    # Plotting the bar chart (normal scale) 常数型图表，为了横图更好展示
    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, contracts, color=colors, edgecolor='black', width=0.6)

    plt.xlabel('Number of Transactions per Contract', fontsize=11)
    plt.ylabel('Number of Contracts', fontsize=11)
    plt.title('Mapping of Contracts to Number of Transactions', fontsize=12, fontweight='bold')
    plt.xticks(rotation=15)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adding a line plot to represent the trend of the data with a lighter, dashed line
    plt.plot(categories, contracts, color='skyblue', marker='o', linestyle='--', linewidth=1.2, markersize=4,
             label='Trend Line')
    plt.legend()

    # Adding data labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 50, int(yval), ha='center', va='bottom', fontsize=10)

    # Saving the figure as a PDF (normal scale)
    plt.tight_layout()
    plt.savefig('../contract_transaction/contracts_transactions_mapping.pdf')

    # Plotting the bar chart with logarithmic scale for Y-axis 指数型图表，为了竖图展示
    plt.figure(figsize=(6, 12))
    bars = plt.bar(categories, contracts, color=colors, edgecolor='black', width=0.6)
    plt.yscale('log')

    plt.xlabel('Number of Transactions per Contract', fontsize=14)
    plt.ylabel('Number of Contracts (Log Scale)', fontsize=14)
    # plt.title('Contracts Mapping to Transactions Number', fontsize=16, fontweight='bold')
    plt.xticks(rotation=20, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adding data labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 50, int(yval), ha='center', va='bottom', fontsize=13)

    # Adding a line plot to represent the trend of the data with a lighter, dashed line
    plt.plot(categories, contracts, color='skyblue', marker='o', linestyle='--', linewidth=1.2, markersize=4,
             label='Trend Line')
    plt.legend()

    # Saving the figure as a PDF (log scale)
    plt.tight_layout()
    plt.savefig('../contract_transaction/contracts_transactions_mapping_log.pdf')

    plt.show()


if __name__ == '__main__':
    build_contract_mapping_figure()
