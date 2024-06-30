"""
第一个脚本是为了生成6个csv文件，用来统计Reentrancy和Timestamp Dependence的在合约和交易中分别有多少个
"""
# import pandas as pd
# from tqdm import tqdm
#
# # 加载数据
# oyente_df = pd.read_excel('/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/contract_transaction/comparasion result.xlsx', sheet_name='Oyente result')
# osiris_df = pd.read_excel('/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/contract_transaction/comparasion result.xlsx', sheet_name='Osiris result')
# filter_lab_df = pd.read_csv('/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/contract_transaction/filter_lab_transaction.csv')
# txspector_df = pd.read_csv('/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/database1/Database1_TxSpector_result.csv')
# framework_df = pd.read_csv('/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/database1/Database1_Framework_result.csv')
#
# # 定义攻击类型及其对应的列名
# attacks = [
#     ('TxSpector_Reentrancy_record.csv', '1Reentrancy', 'reentrancy', txspector_df),
#     ('TxSpector_Securify_Reentrancy_record.csv', '8Securify-Reentrancy', 'reentrancy', txspector_df),
#     ('TxSpector_Timestamp_Dependence_record.csv', '4TimestampDependence', 'time_dependency', txspector_df),
#     ('Framework_Reentrancy_record.csv', '1Reentrancy', 'reentrancy', framework_df),
#     ('Framework_Securify_Reentrancy_record.csv', '8Securify-Reentrancy', 'reentrancy', framework_df),
#     ('Framework_Timestamp_Dependence_record.csv', '4TimestampDependence', 'time_dependency', framework_df)
# ]
#
# # 定义批次大小
# batch_size = 10000
#
# # 定义处理函数
# def process_attack(output_file, tx_col, contract_col, df):
#     filtered_df = df[df[tx_col] == True]
#     num_batches = (len(filtered_df) // batch_size) + 1
#
#     for batch_num in range(num_batches):
#         start_idx = batch_num * batch_size
#         end_idx = min((batch_num + 1) * batch_size, len(filtered_df))
#         batch_records = []
#
#         for idx, tx in tqdm(filtered_df.iloc[start_idx:end_idx].iterrows(), total=end_idx - start_idx):
#             transaction = tx['hash']
#             to_address = filter_lab_df[filter_lab_df['tx_hash'] == transaction]['to_address'].values
#
#             oyente_contract = None
#             osiris_contract = None
#
#             if len(to_address) > 0:
#                 to_address = to_address[0]
#
#                 # 检查Oyente结果
#                 oyente_result = oyente_df[(oyente_df['contract_address'] == to_address) & (oyente_df[contract_col] == True)]
#                 if not oyente_result.empty:
#                     oyente_contract = to_address
#
#                 # 检查Osiris结果
#                 osiris_result = osiris_df[(osiris_df['contract_address'] == to_address) & (osiris_df[contract_col] == True)]
#                 if not osiris_result.empty:
#                     osiris_contract = to_address
#
#             batch_records.append([transaction, oyente_contract, osiris_contract])
#
#         batch_records_df = pd.DataFrame(batch_records, columns=['Transaction', 'Oyente', 'Osiris'])
#
#         # 追加模式写入CSV
#         batch_records_df.to_csv(f'/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/contract_transaction/{output_file}', mode='a', header=(batch_num == 0), index=False)
#
#
# # 处理所有攻击类型
# for output_file, tx_col, contract_col, df in attacks:
#     process_attack(output_file, tx_col, contract_col, df)

"""
第二个脚本是为了生成16个csv文件，分别用来记住交易中的8种攻击，究竟哪些被合约工具检测出来了
"""
import pandas as pd
from tqdm import tqdm
import concurrent.futures
import os

# 加载数据
oyente_df = pd.read_excel('../contract_transaction/comparasion result.xlsx', sheet_name='Oyente result')
osiris_df = pd.read_excel('../contract_transaction/comparasion result.xlsx', sheet_name='Osiris result')
filter_lab_df = pd.read_csv('../contract_transaction/filter_lab_transaction.csv')
txspector_df = pd.read_csv('../database1/Database1_TxSpector_result.csv')
framework_df = pd.read_csv('../database1/Database1_Framework_result.csv')

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

# 定义输出路径
output_path = '../contract_transaction/8_vulnerabilities/'
os.makedirs(output_path, exist_ok=True)

# 定义处理函数
def process_vulnerability(vul_info):
    tool_name, df, vul = vul_info
    records = []
    filtered_df = df[df[vul] == True]

    for idx, tx in tqdm(filtered_df.iterrows(), total=filtered_df.shape[0], desc=f'Processing {tool_name} {vul}'):
        transaction = tx['hash']
        to_address = filter_lab_df[filter_lab_df['tx_hash'] == transaction]['to_address'].values

        oyente_contract = None
        osiris_contract = None
        oyente_results = [None]*6
        osiris_results = [None]*6

        if len(to_address) > 0:
            to_address = to_address[0]

            # 检查Oyente结果
            oyente_result = oyente_df[oyente_df['contract_address'] == to_address]
            if not oyente_result.empty:
                oyente_contract = to_address
                oyente_results = oyente_result.iloc[0, 1:].tolist()

            # 检查Osiris结果
            osiris_result = osiris_df[osiris_df['contract_address'] == to_address]
            if not osiris_result.empty:
                osiris_contract = to_address
                osiris_results = osiris_result.iloc[0, 1:].tolist()

        records.append([transaction, oyente_contract] + oyente_results + [osiris_contract] + osiris_results)

    # 转换为DataFrame并保存为CSV
    columns = ['Transaction', 'Oyente_contract', 'Oyente_callstack', 'Oyente_reentrancy', 'Oyente_time_dependency', 'Oyente_integer_underflow', 'Oyente_integer_overflow', 'Oyente_money_concurrency',
               'Osiris_contract', 'Osiris_callstack', 'Osiris_reentrancy', 'Osiris_time_dependency', 'Osiris_integer_underflow', 'Osiris_integer_overflow', 'Osiris_money_concurrency']
    records_df = pd.DataFrame(records, columns=columns)
    records_df.to_csv(os.path.join(output_path, f'{tool_name}_{vul}_record.csv'), index=False)


# 准备所有任务
tasks = [('TxSpector', txspector_df, vul) for vul in vulnerabilities] + [('Framework', framework_df, vul) for vul in vulnerabilities]

# 使用多线程处理
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_vulnerability, task) for task in tasks]
    for future in concurrent.futures.as_completed(futures):
        future.result()  # 确保任务完成并处理异常

