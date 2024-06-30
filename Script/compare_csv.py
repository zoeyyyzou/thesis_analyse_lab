import os
import sys
import pandas as pd
from tqdm import tqdm


def compare(table1_path: str, table2_path: str, table1_suffix: str, table2_suffix: str) -> pd.DataFrame:
    # 读取两个CSV表格
    table1 = pd.read_csv(table1_path)
    table2 = pd.read_csv(table2_path)

    # 基于 'hash' 列合并两个表格
    merged = pd.merge(table1, table2, on='hash', suffixes=(table1_suffix, table2_suffix))

    # 定义输出DataFrame的列
    columns = [
        'hash',
        f'success{table1_suffix}',
        f'success{table2_suffix}',
    ]

    # 添加每种漏洞类型的结果列
    vuln_types = [
        '1Reentrancy', '2UncheckedCall', '3FailedSend', '4TimestampDependence',
        '5UnsecuredBalance', '6MisuseOfOrigin', '7Suicidal', '8Securify-Reentrancy'
    ]
    for vuln_type in vuln_types:
        columns.extend([f'{vuln_type}{table1_suffix}', f'{vuln_type}{table2_suffix}'])

    # 创建包含所需列的新DataFrame
    result_df = pd.DataFrame(merged, columns=columns)

    # 修改逻辑：如果 table1 中的某个字段为 True，则 table2 中的同名字段改为 True
    for vuln_type in ['success'] + vuln_types:
        field_table1 = f"{vuln_type}{table1_suffix}"
        field_table2 = f"{vuln_type}{table2_suffix}"
        result_df.loc[result_df[field_table1] == True, field_table2] = True

    return result_df


def generate_difference_tables(merged_df: pd.DataFrame, table1_suffix: str, table2_suffix: str):
    # 定义需要比较的字段
    fields = [
        'success', '1Reentrancy', '2UncheckedCall', '3FailedSend',
        '4TimestampDependence', '5UnsecuredBalance', '6MisuseOfOrigin',
        '7Suicidal', '8Securify-Reentrancy'
    ]

    # 创建字典存储每个字段的差异表格
    difference_tables = {}

    for field in fields:
        field_table1 = f"{field}{table1_suffix}"
        field_table2 = f"{field}{table2_suffix}"

        # 过滤出不同的行
        diff_df = merged_df[merged_df[field_table1] != merged_df[field_table2]][['hash', field_table1, field_table2]]

        # 存储到字典中
        difference_tables[field] = diff_df

    return difference_tables


def generate_statistics_table(merged_df: pd.DataFrame, table1_suffix: str, table2_suffix: str) -> pd.DataFrame:
    # 定义需要统计的字段
    fields = [
        'success', '1Reentrancy', '2UncheckedCall', '3FailedSend',
        '4TimestampDependence', '5UnsecuredBalance', '6MisuseOfOrigin',
        '7Suicidal', '8Securify-Reentrancy'
    ]

    # 统计信息列表
    stats = []

    # 统计table1的字段
    stats_row1 = {'table': table1_suffix.strip('_'), 'hash': merged_df['hash'].nunique()}
    for field in fields:
        field_table1 = f"{field}{table1_suffix}"
        stats_row1[f'{field}_True'] = merged_df[field_table1].sum()
        stats_row1[f'{field}_False'] = merged_df[field_table1].count() - merged_df[field_table1].sum()
    stats.append(stats_row1)

    # 统计table2的字段
    stats_row2 = {'table': table2_suffix.strip('_'), 'hash': merged_df['hash'].nunique()}
    for field in fields:
        field_table2 = f"{field}{table2_suffix}"
        stats_row2[f'{field}_True'] = merged_df[field_table2].sum()
        stats_row2[f'{field}_False'] = merged_df[field_table2].count() - merged_df[field_table2].sum()
    stats.append(stats_row2)

    # 创建 DataFrame
    stats_df = pd.DataFrame(stats)

    return stats_df


def generate_statistics_table2(merged_df: pd.DataFrame, table1_suffix: str, table2_suffix: str) -> pd.DataFrame:
    # 定义需要统计的字段
    fields = [
        'success', '1Reentrancy', '2UncheckedCall', '3FailedSend',
        '4TimestampDependence', '5UnsecuredBalance', '6MisuseOfOrigin',
        '7Suicidal', '8Securify-Reentrancy'
    ]

    # 统计信息列表
    stats = []

    # 遍历每个字段，对两个表分别统计True和False的数量
    for field in fields:
        field_table1 = f"{field}{table1_suffix}"
        field_table2 = f"{field}{table2_suffix}"

        true_table1 = merged_df[field_table1].sum()
        false_table1 = merged_df[field_table1].count() - true_table1

        true_table2 = merged_df[field_table2].sum()
        false_table2 = merged_df[field_table2].count() - true_table2

        stats.append({
            'field': field,
            f'{table1_suffix.strip("_")}_True': true_table1,
            f'{table1_suffix.strip("_")}_False': false_table1,
            f'{table2_suffix.strip("_")}_True': true_table2,
            f'{table2_suffix.strip("_")}_False': false_table2
        })

    # 创建 DataFrame
    stats_df = pd.DataFrame(stats)

    return stats_df


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python result_compare.py table1.csv table2.csv')
        sys.exit(1)

    table1_path = sys.argv[1]
    table2_path = sys.argv[2]

    table1_name = os.path.splitext(os.path.basename(table1_path))[0]
    table2_name = os.path.splitext(os.path.basename(table2_path))[0]

    table1_suffix = f"_{table1_name}"
    table2_suffix = f"_{table2_name}"

    result_name = sys.argv[3] if len(sys.argv) > 3 else 'result'

    # 调用compare函数并进行合并
    merged_df = compare(table1_path, table2_path, table1_suffix, table2_suffix)
    merged_df.drop_duplicates(subset='hash', keep='first', inplace=True)
    merged_df.fillna(False, inplace=True)

    merged_df.to_csv(f'{result_name}.csv', index=False)

    difference_tables = generate_difference_tables(merged_df, table1_suffix, table2_suffix)

    # 保存每个差异表格到单独的CSV文件
    for field, diff_df in difference_tables.items():
        diff_df.to_csv(f'{result_name}_difference_{field}.csv', index=False)
        print(f"Difference table for {field} saved to difference_{field}.csv")

    # 调用 generate_statistics_table 函数生成统计信息表格
    # stats_df = generate_statistics_table(merged_df, table1_suffix, table2_suffix)
    stats_df = generate_statistics_table2(merged_df, table1_suffix, table2_suffix)

    # 保存统计信息表格到 CSV 文件
    stats_df.to_csv('statistics.csv', index=False)
