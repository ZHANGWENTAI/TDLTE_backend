from db.Tables.ENodeB import ENodeB
from db.Tables.KPI import KPI
from db.Tables.PRB import PRB
from db.Tables.MROData import MROData

def handle_register(account, authentication, cursor):
    cursor.execute('SELECT account FROM users WHERE account=?', account)

    if cursor.fetchone() is not None:
        return False
    else:
        cursor.execute('INSERT INTO users VALUES(?, ?)', account, authentication)
        cursor.commit()
        return True

def handle_login(account, authentication, cursor):
    cursor.execute('SELECT authentication FROM users WHERE account=?', account)
    result = cursor.fetchone()

    if result is None:
        return 1, 'account no exist'
    elif result[0] != authentication:
        return 1, 'password wrong'
    else:
        return 0, 'login successfully'

def handle_config(path, cursor):
    enodeb = ENodeB()
    code, msg = enodeb.loadData(cursor, 1000, path)

    return code, msg

def handle_kpi(path, cursor):
    kpi = KPI()
    code, msg = kpi.loadFromExcel(cursor, 50, path)

    return code, msg

def handle_prb(path, cursor):
    prb = PRB()
    code, msg = prb.loadFromExcel(cursor, 5000, path)

    return code, msg

def handle_mro(path, cursor):
    mro = MROData()
    code, msg = mro.loadData(cursor, 5000, path)

    return code, msg

def handle_export(tb_name, format, path):
    import pandas as pd
    from sqlalchemy import create_engine
    con = create_engine("mssql+pyodbc://zwt:240017@TDLTE")
    df = pd.read_sql(tb_name, con)
    if format == 'excel':
        df.to_excel(path + '/' + tb_name + '.xlsx')
    elif format == 'txt':
        fd = open(path + '\\tb_name' + '.txt', 'w')
        fd.write(df.to_string())
        fd.close()

    return 0, ""

def handle_c2i_analysis():
    import pandas as pd
    from sqlalchemy import create_engine
    from scipy.stats import norm

    con = create_engine("mssql+pyodbc://zwt:240017@TDLTE")
    df = pd.read_sql("""
    SELECT serving_sector, interfering_sector, AVG(lte_sc_rsrp-lte_nc_rsrp)mean, STDEV(lte_sc_rsrp-lte_nc_rsrp)std
    FROM mrodata 
    GROUP BY serving_sector, interfering_sector
    HAVING COUNT(lte_sc_rsrp-lte_nc_rsrp) > 1""", con)

    df['p_under9'] = norm.cdf((9 - df['mean']) / df['std'])
    df['p_between6'] = norm.cdf((6 - df['mean']) / df['std']) - norm.cdf((-6 - df['mean']) / df['std'])

    df.to_sql('c2inew', con, if_exists='replace')
    return 0, ""

def drop_duplication(data):
    drop_set = set()
    for i in range(data.shape[0] - 1):
        if i in drop_set:
            continue

        sector1 = data.at[i, 'ss']
        sector2 = data.at[i, 'ins']
        for j in range(i, data.shape[0]):
            if data.at[j, 'ss'] == sector2 and data.at[j, 'ins'] == sector1:
                drop_set.add(j)

    data.drop(index=list(drop_set))
    return data

def handle_overlay_analysis(x):
    import pandas as pd
    from sqlalchemy import create_engine

    con = create_engine("mssql+pyodbc://zwt:240017@TDLTE")
    script = "SELECT serving_sector as ss, interfering_sector as ins FROM c2inew WHERE p_between6 > " + str(x / 100)
    df = pd.read_sql(script, con)
    df = drop_duplication(df)

    result = pd.DataFrame(columns=['sector1', 'sector2', 'sector3'])

    for i in range(df.shape[0] - 1):
        sector1 = df.at[i, 'ss']
        sector2 = df.at[i, 'ins']

        ss_set = set()
        ins_set = set()
        for j in range(i, df.shape[0]):
            if df.at[j, 'ss'] == sector1 and df.at[j, 'ins'] != sector2:
                ss_set.add(df.at[j, 'ins'])
            elif df.at[j, 'ss'] != sector1 and df.at[j, 'ins'] == sector2:
                ins_set.add(df.at[j, 'ss'])

        third = ss_set.intersection(ins_set)
        for sector3 in third:
            result = result.append({'sector1': sector1, 'sector2': sector2, 'sector3': sector3}, ignore_index=True)

    result.to_sql('c2i3', con, if_exists='replace', index=False)
    print(result.to_dict())
    return 0, "", result.to_dict()


def handle_cell(cell_id=None, cell_name=None):
    """
    :param cell_id:
    :param cell_name:
    :return: code: if success 0, else 1
             msg: error message, if success, ""
             info: tuple or dict of query result
    """
    pass

def handle_enodeb(enodeb_id=None, enodeb_name=None):
    pass

def handle_kpi_query(cell_name, start_time, end_time, props):
    pass

def handle_prb_stat(src_path, dst_path):
    pass

def handle_prb_query(cell_name, start_time, end_time, props):
    pass
