import pandas as pd
import json
from path import Path
from tables.exceptions import HDF5ExtError
from VisionQuant.utils.Params import LOCAL_DIR, HDF5_COMP_LEVEL, HDF5_COMPLIB, Market


def kdata_store_market_transform(_market):
    if _market in [Market.Ashare.MarketSH, Market.Ashare.MarketSH.STOCK, Market.Ashare.MarketSH.ETF,
                   Market.Ashare.MarketSH.INDEX, Market.Ashare.MarketSH.KCB]:
        return 'Ashare', 'sh'
    elif _market in [Market.Ashare.MarketSZ, Market.Ashare.MarketSZ.STOCK, Market.Ashare.MarketSZ.ETF,
                     Market.Ashare.MarketSZ.INDEX, Market.Ashare.MarketSZ.CYB]:
        return 'Ashare', 'sz'
    else:
        raise ValueError("错误的市场类型")


def anadata_store_market_transform(_market):
    if _market is Market.Ashare:
        return 'Ashare'
    else:  # todo:增加不同市场类型
        return 'Future'


def store_kdata_to_hdf5(datastruct):
    try:
        market, market_type = kdata_store_market_transform(datastruct.code.market)
        if market_type is None:
            fname = datastruct.code.code + '.h5'
        else:
            fname = market_type + datastruct.code.code + '.h5'
        fpath = Path('/'.join([LOCAL_DIR, 'KData', market, fname]))
        store = pd.HDFStore(fpath, complib=HDF5_COMPLIB, complevel=HDF5_COMP_LEVEL)
    except HDF5ExtError as e:
        print(e)
    else:
        for freq in datastruct.get_freqs():
            kdata = datastruct.get_kdata(freq)
            if len(kdata) > 0:
                store.put(key='_' + freq, value=kdata.data_struct)
        store.close()


def store_relavity_score_data_to_hdf5(result_df, market=Market.Ashare):
    try:
        fname = 'relavity_analyze_result.h5'
        fpath = Path('/'.join([LOCAL_DIR, 'AnalyzeData', fname]))
        store = pd.HDFStore(fpath, complib=HDF5_COMPLIB, complevel=HDF5_COMP_LEVEL)
    except HDF5ExtError as e:
        print(e)
    else:
        key = anadata_store_market_transform(market)
        if len(result_df) > 0:
            store.put(key=key, value=result_df, format='table', append=True)
        store.close()


def store_blocks_score_data_to_hdf5(result_df, market=Market.Ashare):
    try:
        fname = 'blocks_score_analyze_result.h5'
        fpath = Path('/'.join([LOCAL_DIR, 'AnalyzeData', fname]))
        store = pd.HDFStore(fpath, complib=HDF5_COMPLIB, complevel=HDF5_COMP_LEVEL)
    except HDF5ExtError as e:
        print(e)
    else:
        key = anadata_store_market_transform(market)
        if len(result_df) > 0:
            store.put(key=key, value=result_df, format='table', append=True)
        store.close()


def store_code_list_stock(list_df, market):
    market_str = anadata_store_market_transform(market)
    fpath = Path('/'.join([LOCAL_DIR, 'code_list_' + market_str + '.csv']))
    list_df.to_csv(fpath, encoding='utf-8', index=False)


def store_blocks_data(data: dict, market=Market.Ashare):

    market_str = anadata_store_market_transform(market)
    fpath = Path('/'.join([LOCAL_DIR, market_str + '_blocks_data.json']))
    with open(fpath, 'w+') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
