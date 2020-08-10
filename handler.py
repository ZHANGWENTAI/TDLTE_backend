from db.Tables.ENodeB import ENodeB
from db.Tables.KPI import KPI
from db.Tables.PRB import PRB
from db.Tables.MROData import MROData
import pyodbc as odbc
import pandas as pd
import os
from sqlalchemy import create_engine
from scipy.stats import norm
import processbar

con = create_engine("mssql+pyodbc://zwt:240017@TDLTE")

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
    # print(processbar.row)
    return code, msg

def handle_kpi(path, cursor):
    kpi = KPI()
    code, msg = kpi.loadFromExcel(cursor, 50, path)

    return code, msg

def handle_prb(path, cursor):
    prb = PRB()
    code, msg = prb.loadFromExcel(cursor, 500, path)

    script = """
                    SELECT enb_name,sector_name
                    ,dateadd(HOUR, datediff(HOUR, 0, time_stamp ), 0) as [time_stamp]"""
    script2 = """
                    from prb
                    group by enb_name,sector_name,dateadd(HOUR, datediff(HOUR, 0, time_stamp ), 0)
                    order by dateadd(HOUR, datediff(HOUR, 0, time_stamp ), 0)
                    """
    for i in range(100):
        script += """
                    ,AVG( convert(int,prb{0})) as prb{1}""".format(i, i)
    script += script2

    df = pd.read_sql(script, con)
    df.to_sql('prbnew', con, if_exists='replace', index=False)
    df.to_excel(path.replace('\表13 优化区17日-19日每PRB干扰 查询-15分钟.xlsx', '') + '/' + 'PRBnew.xlsx', index=False)

    return code, msg

def handle_mro(path, cursor):
    mro = MROData()
    code, msg = mro.loadData(cursor, 5000, path)

    return code, msg

def handle_export(tb_name, format, path):
    df = pd.read_sql(tb_name, con)
    if not os.path.exists(path):
        return 1, "path wrong"
    if format == 'excel':
        df.to_excel(path + '/' + tb_name + '.xlsx')
    elif format == 'txt':
        fd = open(path + '\\' + tb_name + '.txt', 'w')
        fd.write(df.to_string())
        fd.close()

    return 0, ""

def handle_c2i_analysis():
    df = pd.read_sql("""
    SELECT serving_sector, interfering_sector, AVG(lte_sc_rsrp-lte_nc_rsrp)mean, STDEV(lte_sc_rsrp-lte_nc_rsrp)std
    FROM mrodata 
    GROUP BY serving_sector, interfering_sector
    HAVING COUNT(lte_sc_rsrp) > 20""", con)

    df['p_under9'] = norm.cdf((9 - df['mean']) / df['std'])
    df['p_between6'] = norm.cdf((6 - df['mean']) / df['std']) - norm.cdf((-6 - df['mean']) / df['std'])

    df.to_sql('c2inew', con, if_exists='replace', index=False)
    return 0, "", df.to_dict(orient='index')

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
    print(x)
    script = "SELECT serving_sector as ss, interfering_sector as ins FROM c2inew WHERE p_between6 > " + str(x)
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
    print(result.to_dict(orient='index'))
    return 0, "", result.to_dict(orient='index')


def handle_cell(sector_id=None, sector_name=None):
    """
    :return: code: if success 0, else 1
             msg: error message, if success, ""
             res: tuple or dict of query result
    """
    res = {}
    print(sector_id, sector_name)
    if sector_id is not None:
        script = """SELECT * FROM cell WHERE sector_id = '{0}'""".format(sector_id)
    elif sector_name is not None:
        script = """SELECT * FROM cell WHERE sector_name = '{0}'""".format(sector_name)
    else:
        return 1, "Both cell_id and cell_name are None", res

    print(script)
    res = pd.read_sql(script, con).to_dict(orient='index')
    if res == {} :
        return 1, "No result! Check whether the cell_id or cell_name is right.", res
    return 0, "", res


def handle_enodeb(enodeb_id=None, enodeb_name=None):
    res = {}
    if enodeb_id is not None:
        script = "SELECT * FROM enodeb WHERE enodeb_id = '" + enodeb_id + "'"
    elif enodeb_name is not None:
        script = "SELECT * FROM enodeb WHERE enodeb_name = '" + enodeb_name + "'"
    else:
        return 1, "Both enodeb_id and enodeb_name are None", res

    res = pd.read_sql(script, con).to_dict(orient='index')
    print(script)
    if res == {}:
        return 1, "No result! Check whether enodeb_id or enodeb_name is right.", res
    return 0, "", res


def handle_kpi_query(sector_name, start_time, end_time, prop):
    msg = "No result! Check whether the data is imported."
    script = """
        SELECT time_stamp, {0} 
        FROM kpi 
        WHERE sector_name = '{1}' 
        AND time_stamp BETWEEN '{2}' AND '{3}'
        """.format(prop, sector_name, start_time, end_time)

    print(script)
    df = pd.read_sql(script, con)
    return 0, msg, df.to_dict(orient='list')


def handle_prb_query(sector_name, start_time, end_time, granularity, prb_no):
    """
    granularity: if by minutes '0', else 1
    """
    msg = "No result! Check whether the data is imported."
    if granularity == '0':
        table_name = 'prb'
    else:
        table_name = 'prbnew'
    script = """
        SELECT time_stamp, {0} 
        FROM {1} 
        WHERE sector_name = '{2}' 
        AND time_stamp BETWEEN '{3}' AND '{4}'
        """.format(prb_no, table_name, sector_name, start_time, end_time)
    print(script)
    df = pd.read_sql(script, con)
    return 0, msg, df.to_dict(orient='list')