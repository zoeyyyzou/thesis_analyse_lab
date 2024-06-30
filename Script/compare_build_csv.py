"""
为database1 & database2 的result 文件夹生成对应的csv结果文件

INPUT需要手动的更改路径：
A.  database1 INPUT
    ori_df = pd.read_csv("/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/database1/Database1_TxSpector_result.csv")
    tx_df = pd.read_csv("/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/database1/Database1_Framework_result.csv")
B.  database2 INPUT
    ori_df = pd.read_csv("/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/database2/Ori_TxSpector_result.csv")
    tx_df = pd.read_csv("/Users/yangyizou/Library/Application Support/JetBrains/PyCharm2023.3/thesis-paper/database2/Ori_Framework_result.csv")

OUTPUT需要手动修改路径：
A. df.to_csv(f'../database1/{vuln}_analysis.csv', index=False)
B. df.to_csv(f'../database2/{vuln}_analysis.csv', index=False)

run: python3 lab_compare_build_csv.py
"""
import pandas as pd

# 读取CSV文件
ori_df = pd.read_csv("../database1/Database1_TxSpector_result.csv")
tx_df = pd.read_csv("../database1/Database1_Framework_result.csv")

# 将文本形式的布尔值转换为实际的布尔值
bool_columns = ['success', '5UnsecuredBalance', '6MisuseOfOrigin', '3FailedSend', '4TimestampDependence',
                '7Suicidal', '1Reentrancy', '2UncheckedCall', '8Securify-Reentrancy']

for column in bool_columns:
    ori_df[column] = ori_df[column].astype(str).str.lower() == 'true'
    tx_df[column] = tx_df[column].astype(str).str.lower() == 'true'

# 使用外连接合并两个数据框，确保所有数据都被包含
merged_df = pd.merge(ori_df, tx_df, on='hash', suffixes=('_ori', '_tx'), how='outer')

# 填充缺失值，假设缺失的布尔值为False
merged_df.fillna({'success_ori': False, 'success_tx': False}, inplace=True)
for column in bool_columns[1:]:  # 跳过'success'列，因为我们已经处理了
    merged_df.fillna({f'{column}_ori': False, f'{column}_tx': False}, inplace=True)

# 准备 success = False 的统计
failure_analysis = pd.DataFrame()

# 提取 hash 值基于条件
failure_analysis['TxSpector_False'] = merged_df.loc[merged_df['success_ori'] == False, 'hash']
failure_analysis['Framework_False'] = merged_df.loc[merged_df['success_tx'] == False, 'hash']
failure_analysis['TxS_False_Frame_True'] = merged_df.loc[(merged_df['success_ori'] == False) & (merged_df['success_tx'] == True), 'hash']
failure_analysis['TxS_True_Frame_False'] = merged_df.loc[(merged_df['success_ori'] == True) & (merged_df['success_tx'] == False), 'hash']

# 保存 failure analysis 结果到CSV文件
failure_analysis.to_csv('../database1/failure_stat.csv', index=False)

# 漏洞列列表
vulnerability_columns = [
    '5UnsecuredBalance', '6MisuseOfOrigin', '3FailedSend', '4TimestampDependence',
    '7Suicidal', '1Reentrancy', '2UncheckedCall', '8Securify-Reentrancy'
]

# 处理每个漏洞
for vuln in vulnerability_columns:
    df = pd.DataFrame()
    df['Ori_TxSpector_TRUE'] = merged_df.loc[
        (merged_df['success_ori'] == True) & (merged_df[f'{vuln}_ori'] == True), 'hash']
    df['TxSpector_TRUE'] = merged_df.loc[(merged_df['success_tx'] == True) & (merged_df[f'{vuln}_tx'] == True), 'hash']
    df['Ori_TRUE_Tx_TRUE'] = merged_df.loc[
        (merged_df['success_ori'] == True) & (merged_df['success_tx'] == True) & (merged_df[f'{vuln}_ori'] == True) & (
                    merged_df[f'{vuln}_tx'] == True), 'hash']
    df['Ori_TRUE_Tx_FALSE'] = merged_df.loc[
        (merged_df['success_ori'] == True) & (merged_df['success_tx'] == True) & (merged_df[f'{vuln}_ori'] == True) & (
                    merged_df[f'{vuln}_tx'] == False), 'hash']
    df['Ori_FALSE_Tx_TRUE'] = merged_df.loc[
        (merged_df['success_ori'] == True) & (merged_df['success_tx'] == True) & (merged_df[f'{vuln}_ori'] == False) & (
                    merged_df[f'{vuln}_tx'] == True), 'hash']

    # 保存漏洞分析结果到CSV文件
    df.to_csv(f'../database1/{vuln}_analysis.csv', index=False)

# 确认所有任务完成
print("Analysis completed and files saved.")


