import sys
import pandas as pd


def generate_contract_merged_data(tx_mapping_df: pd.DataFrame, detection_results_df: pd.DataFrame) -> pd.DataFrame:
    # 合并两个 DataFrame，基于交易哈希（tx_hash）
    merged_df = pd.merge(tx_mapping_df, detection_results_df, left_on='tx_hash', right_on='hash')

    # 删除合并时多余的 'hash' 列
    merged_df.drop(columns=['hash'], inplace=True)

    # 定义漏洞类型
    vuln_types = [
        'success', '1Reentrancy', '2UncheckedCall', '3FailedSend',
        '4TimestampDependence', '5UnsecuredBalance', '6MisuseOfOrigin',
        '7Suicidal', '8Securify-Reentrancy'
    ]

    # 初始化一个字典用于存储汇总结果
    results = {}

    # 遍历合并后的 DataFrame，按合约地址汇总结果
    for index, row in merged_df.iterrows():
        to_address = row['to_address']
        if to_address not in results:
            results[to_address] = {f'{vuln_type}_txspector': False for vuln_type in vuln_types}
            results[to_address].update({f'{vuln_type}_framework': False for vuln_type in vuln_types})

        # 更新汇总结果，若任一方案检测结果为 True，则设为 True
        for vuln_type in vuln_types:
            results[to_address][f'{vuln_type}_txspector'] |= row[f'{vuln_type}_d1_txspector']
            results[to_address][f'{vuln_type}_framework'] |= row[f'{vuln_type}_d1_framework']

    # 将汇总结果转换为 DataFrame
    summary_df = pd.DataFrame.from_dict(results, orient='index').reset_index()
    summary_df.rename(columns={'index': 'to_address'}, inplace=True)
    return summary_df

def generate_combine_result(first_df, osiris_df, oyente_df):
    # 合并 integer_underflow 和 integer_overflow 为 integer
    osiris_df['integer'] = osiris_df['integer_underflow'] | osiris_df['integer_overflow']
    oyente_df['integer'] = oyente_df['integer_underflow'] | oyente_df['integer_overflow']

    # osiris 和 oyente 的漏洞类型
    osiris_vuln_types = ['callstack', 'reentrancy', 'time_dependency', 'integer', 'money_concurrency']

    # txspector 和 framework 的漏洞类型
    txspector_framework_vuln_types = [
        '1Reentrancy', '2UncheckedCall', '3FailedSend', '4TimestampDependence',
        '5UnsecuredBalance', '6MisuseOfOrigin', '7Suicidal', '8Securify-Reentrancy'
    ]

    # 处理每种漏洞类型
    for vuln_type in txspector_framework_vuln_types:
        txspector_contracts = first_df[first_df[f'{vuln_type}_txspector'] == True]['to_address'].tolist()
        framework_contracts = first_df[first_df[f'{vuln_type}_framework'] == True]['to_address'].tolist()

        results = {
            'type': osiris_vuln_types,  # 由于类型是独立的，所以直接拼接
            'osiris_txspector': [],
            'oyente_txspector': [],
            'osiris_framework': [],
            'oyente_framework': []
        }
        for osiris_type in osiris_vuln_types:
            results['osiris_txspector'].append(
                osiris_df[osiris_df['contract_address'].isin(txspector_contracts)][osiris_type].sum())
            results['osiris_framework'].append(
                osiris_df[osiris_df['contract_address'].isin(framework_contracts)][osiris_type].sum())

        for oyente_type in osiris_vuln_types:
            results['oyente_txspector'].append(
                oyente_df[oyente_df['contract_address'].isin(txspector_contracts)][oyente_type].sum())
            results['oyente_framework'].append(
                oyente_df[oyente_df['contract_address'].isin(framework_contracts)][oyente_type].sum())

        # 将结果转换为 DataFrame 并保存为 CSV 文件
        result_df = pd.DataFrame(results)
        result_df.to_csv(f'{vuln_type}_results.csv', index=False)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python contract_compare.py filter_lab_transaction.csv tx_detection_results.csv oriris.csv oyente.csv')
        sys.exit(1)

    tx_mapping_path = sys.argv[1]
    detection_results_path = sys.argv[2]
    osiris_path = sys.argv[3]
    oyente_path = sys.argv[4]
    # 读取交易映射 CSV 文件
    tx_mapping_df = pd.read_csv(tx_mapping_path)

    # 读取漏洞检测结果 CSV 文件
    detection_results_df = pd.read_csv(detection_results_path)
    # 生成合约汇总数据
    contract_merged_data = generate_contract_merged_data(tx_mapping_df, detection_results_df)

    contract_merged_data.to_csv('contract_merged_data.csv', index=False)

    osiris_df = pd.read_csv(osiris_path)
    oyente_df = pd.read_csv(oyente_path)

    # 联合 oriris 和 oyente 的结果，输出统计结果
    generate_combine_result(contract_merged_data, osiris_df, oyente_df)