import os

class ATUHandOver:
    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\ATUHandOver.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        sSectorID = ""
        nSectorID = ""
        hoatt = 0

        itemList = []
        cnt = 0

        def _insertAll():
            script = 'INSERT INTO atuhandover VALUES(?,?,?)'
            cursor.executemany(script, itemList)
            cursor.commit()

        with open(filePath) as file_obj:
            for i, content in enumerate(file_obj):
                if cnt == size:
                    _insertAll()
                    itemList.clear()
                    cnt = 0
                if i == 0:
                    continue
                dataList = content.rstrip().split(",")
                sSectorID = dataList[0]
                nSectorID = dataList[1]
                hoatt = dataList[2]
                tempSqlItem = (sSectorID, nSectorID, hoatt)
                itemList.append(tempSqlItem)
                cnt += 1
            if cnt != 0:
                _insertAll()
                itemList.clear()

        print("atuhandover finished!")
