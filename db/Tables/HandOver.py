from decimal import *
import os

class HandOver:
    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\HandOver.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        city = ""
        sCellID = ""
        nCellID = ""
        hoatt = 0
        hosucc = 0
        hosuccRate = 0

        itemList = []
        cnt = 0

        def _isOK(item):
            if item[3] == '0':
                if item[5] != '3.1415926':
                    print("handover:hoatt=0,hosuccRate!=null")
                    return False
            else:
                if float(item[5]) != float(Decimal(str(int(item[4]) / int(item[3])))
                                                   .quantize(Decimal('0.0000'), rounding=ROUND_HALF_UP)):
                    print("--------------------------------------------------")
                    print(item[5])
                    print(Decimal(str(int(item[4]) / int(item[3]))).quantize(Decimal('0.0000'), rounding=ROUND_HALF_UP))
                    print(item)
                    print("handover:hosuccRate!=hosucc/hoatt")
                    return False
            return True

        def _insertAll():
            script = 'INSERT INTO handover VALUES(?,?,?,?,?,?)'
            cursor.executemany(script, itemList)
            cursor.commit()

        with open(filePath) as file_obj:
            for i, content in enumerate(file_obj):
                if i == 0:
                    continue
                if cnt == size:
                    _insertAll()
                    itemList.clear()
                    cnt = 0
                dataList = content.rstrip().split(",")
                city = dataList[0]
                sCellID = dataList[1]
                nCellID = dataList[2]
                hoatt = dataList[3]
                hosucc = dataList[4]
                hosuccRate = dataList[5]
                if hosucc == '':
                    hosucc = '0'
                if hoatt == '':
                    hoatt = '0'
                if hosuccRate == '':
                    if hoatt == '0':
                        hosuccRate = '3.1415926'
                    else:
                        hosuccRate = float(int(hosucc) / int(hoatt))
                tempSqlItem = (city, sCellID, nCellID, hoatt, hosucc, hosuccRate)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt != 0:
                _insertAll()
                itemList.clear()

        print("handover finished!")
