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

def handle_overlay_analysis():
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

    df.to_sql('c2inew3', con)

    return 0, ""

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
