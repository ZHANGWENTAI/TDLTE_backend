import pyodbc as odbc
import os

from db.Tables.OptCell import OptCell
from db.Tables.ENodeB import ENodeB
from db.Tables.Cell import Cell
from db.Tables.AdjCell import AdjCell
from db.Tables.SecAdjCell import SecAdjCell
from db.Tables.PCIAssignment import PCIAssignment
from db.Tables.ATUData import ATUData
from db.Tables.ATUC2I import ATUC2I
from db.Tables.ATUHandOver import ATUHandOver
from db.Tables.MROData import MROData
from db.Tables.C2I import C2I
from db.Tables.HandOver import HandOver
from db.Tables.KPI import KPI
from db.Tables.PRB import PRB

def _CreateTable(cursor):
    with open(os.getcwd() + r'\db\sql\create_tables.sql', encoding='utf-8') as creation:
        cursor.execute(creation.read())


def loadData(cursor):
    enodeb = ENodeB()
    enodeb.createTrig(cursor)
    enodeb.loadData(cursor, 50, os.getcwd() + r'\tb\1.tbCell.csv')

    cell = Cell()
    cell.createTrig(cursor)
    cell.loadData(cursor, 50,  os.getcwd() + r'\tb\1.tbCell.csv')

    adjcell = AdjCell()
    adjcell.createTrig(cursor)
    adjcell.loadData(cursor, 1000,  os.getcwd() + r'\tb\2.tbAdjCell.csv')

    secadjcell = SecAdjCell()
    secadjcell.createTrig(cursor)
    secadjcell.loadData(cursor, 2000,  os.getcwd() + r'\tb\3.tbSecAdjcell.csv')

    optcell = OptCell()
    optcell.createTrig(cursor)
    optcell.loadData(cursor, 50,  os.getcwd() + r'\tb\4.tbOptCell.csv')

    pciassignment = PCIAssignment()
    pciassignment.createTrig(cursor)
    pciassignment.loadData(cursor, 1,  os.getcwd() + r'\tb\5.tbPCIAssignment.csv')

    atudata = ATUData()
    atudata.createTrig(cursor)
    atudata.loadData(cursor, 1,  os.getcwd() + r'\tb\6.tbATUData.csv')

    atuc2i = ATUC2I()
    atuc2i.createTrig(cursor)
    atuc2i.loadData(cursor, 50,  os.getcwd() + r'\tb\7.tbATUC2I.csv')

    atuhandover = ATUHandOver()
    atuhandover.createTrig(cursor)
    atuhandover.loadData(cursor, 50,  os.getcwd() + r'\tb\8.tbATUHandOver.csv')

    mrodata = MROData()
    mrodata.createTrig(cursor)
    mrodata.loadData(cursor, 2000,  os.getcwd() + r'\tb\9.tbMROData.csv')

    c2i = C2I()
    c2i.createTrig(cursor)
    c2i.loadData(cursor, 50,  os.getcwd() + r'\tb\10.tbC2I.csv')

    handover = HandOver()
    handover.createTrig(cursor)
    handover.loadData(cursor, 50,  os.getcwd() + r'\tb\11.tbHandOver.csv')

    kpi = KPI()
    kpi.createTrig(cursor)

    prb = PRB()
    prb.createTrig(cursor)

# 初始化数据库，返回连接句柄
def initDB():
    cnxn = odbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=TDLTE')

    mycursor = cnxn.cursor()  # 建立游标
    mycursor.fast_executemany = True
    _CreateTable(mycursor)
    loadData(mycursor)  # 加载数据

    mycursor.close()
    cnxn.close()

# 打印查询结果
def printTable(c, tableName):
    print("-----------------------")
    script = """SELECT * FROM {0}""".format(tableName)
    try:
        c.execute(script)
    except odbc.DatabaseError as err:
        print(err)
    row = c.fetchone()
    while row:
        print(row)
        row = c.fetchone()
    print("-----------------------")