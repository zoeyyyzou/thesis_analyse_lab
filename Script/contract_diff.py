import sys
import pandas as pd


def generate_diff(contract_merged_data, osiris_df, oyente_df):
    """
    1. 首先根据合约地址，过滤出 contract_merged_data 和 osiris_df 都有的合约；
    2. 然后，过滤出 contract_merged_data 中包含 True，但是 osiris_df 和 oyente_df 中全是 False 的项，保存为csv；
    3. 然后，过滤出 contract_merged_data 中全是 False，但是 osiris_df 或 oyente_df 包含 True 的项，保存为csv；
    """

    # 首先过滤出大家都有的合约
    common_contracts = contract_merged_data[contract_merged_data['to_address'].isin(osiris_df['contract_address'])]
    common_contracts = common_contracts[common_contracts['to_address'].isin(oyente_df['contract_address'])]

    # 过滤 osiris_df 中 contract_address 为 common_contracts 的合约
    osiris_df = osiris_df[osiris_df['contract_address'].isin(common_contracts['to_address'])]
    oyente_df = oyente_df[oyente_df['contract_address'].isin(common_contracts['to_address'])]

    # 首先删除 contract_merged_data 中的 'success' 列
    common_contracts.drop(columns=['success_txspector'], inplace=True)
    common_contracts.drop(columns=['success_framework'], inplace=True)

    # 然后过滤出 contract_merged_data 中任意一列包含 True 的行，只要 Reentrancy_txspector,ncheckedCall_txspector,TimestampDependence_txspector... 任意一列包含 True，就保留
    true_txspector = common_contracts[
        common_contracts['1Reentrancy_txspector'] | common_contracts['2UncheckedCall_txspector'] |
        common_contracts['3FailedSend_txspector'] | common_contracts['4TimestampDependence_txspector'] |
        common_contracts['5UnsecuredBalance_txspector'] | common_contracts['6MisuseOfOrigin_txspector'] |
        common_contracts['7Suicidal_txspector'] | common_contracts['8Securify-Reentrancy_txspector']
        ]
    false_txspector = common_contracts[
        ~common_contracts['1Reentrancy_txspector'] & ~common_contracts['2UncheckedCall_txspector'] &
        ~common_contracts['3FailedSend_txspector'] & ~common_contracts['4TimestampDependence_txspector'] &
        ~common_contracts['5UnsecuredBalance_txspector'] & ~common_contracts['6MisuseOfOrigin_txspector'] &
        ~common_contracts['7Suicidal_txspector'] & ~common_contracts['8Securify-Reentrancy_txspector']
        ]
    true_framework = common_contracts[
        common_contracts['1Reentrancy_framework'] | common_contracts['2UncheckedCall_framework'] |
        common_contracts['3FailedSend_framework'] | common_contracts['4TimestampDependence_framework'] |
        common_contracts['5UnsecuredBalance_framework'] | common_contracts['6MisuseOfOrigin_framework'] |
        common_contracts['7Suicidal_framework'] | common_contracts['8Securify-Reentrancy_framework']
        ]
    false_framework = common_contracts[
        ~common_contracts['1Reentrancy_framework'] & ~common_contracts['2UncheckedCall_framework'] &
        ~common_contracts['3FailedSend_framework'] & ~common_contracts['4TimestampDependence_framework'] &
        ~common_contracts['5UnsecuredBalance_framework'] & ~common_contracts['6MisuseOfOrigin_framework'] &
        ~common_contracts['7Suicidal_framework'] & ~common_contracts['8Securify-Reentrancy_framework']
        ]

    true_oyente = oyente_df[
        oyente_df['reentrancy'] | oyente_df['time_dependency']
        ]
    false_oyente = oyente_df[
        ~oyente_df['reentrancy'] & ~oyente_df['time_dependency']
        ]
    true_osiris = osiris_df[
        osiris_df['reentrancy'] | osiris_df['time_dependency']
        ]
    false_osiris = osiris_df[
        ~osiris_df['reentrancy'] & ~osiris_df['time_dependency']
        ]

    true_oyente_false_txspector = true_oyente[true_oyente['contract_address'].isin(false_txspector['to_address'])]
    true_oyente_false_txspector.to_csv(f"true_oyente_false_txspector.csv", index=False)
    true_oyente_false_framework = true_oyente[true_oyente['contract_address'].isin(false_framework['to_address'])]
    true_oyente_false_framework.to_csv(f"true_oyente_false_framework.csv", index=False)
    false_oyente_true_txspector = false_oyente[false_oyente['contract_address'].isin(true_txspector['to_address'])]
    false_oyente_true_txspector.to_csv(f"false_oyente_true_txspector.csv", index=False)
    false_oyente_true_framework = false_oyente[false_oyente['contract_address'].isin(true_framework['to_address'])]
    false_oyente_true_framework.to_csv(f"false_oyente_true_framework.csv", index=False)
    true_osiris_false_txspector = true_osiris[true_osiris['contract_address'].isin(false_txspector['to_address'])]
    true_osiris_false_txspector.to_csv(f"true_osiris_false_txspector.csv", index=False)
    true_osiris_false_framework = true_osiris[true_osiris['contract_address'].isin(false_framework['to_address'])]
    true_osiris_false_framework.to_csv(f"true_osiris_false_framework.csv", index=False)
    false_osiris_true_txspector = false_osiris[false_osiris['contract_address'].isin(true_txspector['to_address'])]
    false_osiris_true_txspector.to_csv(f"false_osiris_true_txspector.csv", index=False)
    false_osiris_true_framework = false_osiris[false_osiris['contract_address'].isin(true_framework['to_address'])]
    false_osiris_true_framework.to_csv(f"false_osiris_true_framework.csv", index=False)

    true_osiris_false_txspector_false_framework = true_osiris_false_txspector[
        true_osiris_false_txspector['contract_address'].isin(false_framework['to_address'])]
    true_osiris_false_txspector_false_framework.to_csv(f"true_osiris_false_txspector_false_framework.csv", index=False)
    true_oyente_false_txspector_false_framework = true_oyente_false_txspector[
        true_oyente_false_txspector['contract_address'].isin(false_framework['to_address'])]
    true_oyente_false_txspector_false_framework.to_csv(f"true_oyente_false_txspector_false_framework.csv", index=False)

    # # 过滤出 true_txspector 中的 to_address 不在 osiris_df 和 oyente_df 中的行
    # trans_true_contract_false = true_txspector[~true_txspector['to_address'].isin(osiris_df['contract_address'])]
    # trans_true_contract_false = trans_true_contract_false[
    #     ~true_txspector['to_address'].isin(oyente_df['contract_address'])]
    # trans_true_contract_false.to_csv(f"trans_true_contract_false.csv", index=False)
    #
    # osiris_true_trans_false = osiris_df[~osiris_df['contract_address'].isin(true_txspector['to_address'])]
    # osiris_true_trans_false.to_csv(f"osiris_true_trans_false.csv", index=False)
    # oyente_true_trans_false = oyente_df[~oyente_df['contract_address'].isin(true_txspector['to_address'])]
    # oyente_true_trans_false.to_csv(f"oyente_true_trans_false.csv", index=False)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(
            'Usage: python contract_diff.py contract_merged_data.csv oriris.csv oyente.csv')
        sys.exit(1)

    contract_merged_data_path = sys.argv[1]
    osiris_path = sys.argv[2]
    oyente_path = sys.argv[3]

    contract_merged_data = pd.read_csv(contract_merged_data_path)

    osiris_df = pd.read_csv(osiris_path)
    oyente_df = pd.read_csv(oyente_path)

    generate_diff(contract_merged_data, osiris_df, oyente_df)
