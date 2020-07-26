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

def handle_export(tb_name, format, path, cursor):
    pass