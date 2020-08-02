from db.Tables.ENodeB import ENodeB
from db.Tables.KPI import KPI
from db.Tables.PRB import PRB
from db.Tables.MROData import MROData
import pyodbc as odbc
import pandas as pd
from sqlalchemy import create_engine
from scipy.stats import norm


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


def handle_cell(c, cell_id=None, cell_name=None):
    """
    :param cell_id:
    :param cell_name:
    :return: code: if success 0, else 1
             msg: error message, if success, ""
             info: tuple or dict of query result
    """
    res = []
    if cell_id is not None:
        script = """SELECT * FROM cell WHERE sector_id = '{0}'""".format(cell_id)
    else:
        if cell_name is not None:
            script = """SELECT * FROM cell WHERE sector_name = '{0}'""".format(cell_name)
        else:
            return 1, "Both cell_id and cell_name are None", res
    try:
        c.execute(script)
    except odbc.DatabaseError as err:
        print(err)
    row = c.fetchone()
    while row:
        res.append(row)
        row = c.fetchone()
    return 0, "", res


def handle_enodeb(c, enodeb_id=None, enodeb_name=None):
    res = []
    if enodeb_id is not None:
        script = """SELECT * FROM cell WHERE enodebid = '{0}'""".format(enodeb_id)
    else:
        if enodeb_name is not None:
            script = """SELECT * FROM cell WHERE enodeb_name = '{0}'""".format(enodeb_name)
        else:
            return 1, "Both enodeb_id and enodeb_name are None", res
    try:
        c.execute(script)
    except odbc.DatabaseError as err:
        print(err)
    row = c.fetchone()
    while row:
        res.append(row)
        row = c.fetchone()
    return 0, "", res


def handle_kpi_query(c, cell_name, start_time, end_time, props):
    res = []
    msg = "No result! Check whether the data is imported."
    script = """
    SELECT time_stamp, {0} 
    FROM kpi 
    WHERE sector_name = '{1}' 
    AND time_stamp BETWEEN '{2}' AND '{3}'
    """.format(props, cell_name, start_time, end_time)
    print(script)
    try:
        c.execute(script)
    except odbc.DatabaseError as err:
        print(err)
    row = c.fetchone()
    while row:
        msg = ""
        res.append(row)
        row = c.fetchone()
    return 0, msg, res


def handle_prb_stat(dst_path):
    con = create_engine("mssql+pyodbc://sa:67258012@sbq")
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
    print(script)
    df = pd.read_sql(script, con)
    df.to_sql('prbnew', con)
    df.to_excel(dst_path + '/' + 'PRBnew.xlsx')
    return 0, ""


def handle_prb_query(c, cell_name, start_time, end_time, granularity, prb_no):
    """
    :param granularity: if by minutes 0, else 1
    :param prb_no:
    :return: code: if success 0, else 1
             msg: error message, if success, ""
             info: tuple or dict of query result
    """
    res = []
    msg = "No result! Check whether the data is imported."
    if granularity == 0:
        table_name = 'prb'
    else:
        table_name = 'prbnew'
    script = """
        SELECT time_stamp, {0} 
        FROM {1} 
        WHERE sector_name = '{2}' 
        AND time_stamp BETWEEN '{3}' AND '{4}'
        """.format(prb_no, table_name, cell_name, start_time, end_time)
    try:
        c.execute(script)
    except odbc.DatabaseError as err:
        print(err)
    row = c.fetchone()
    while row:
        msg = ""
        res.append(row)
        row = c.fetchone()
    return 0, msg, res

