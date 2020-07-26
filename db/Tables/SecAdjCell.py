import os

class SecAdjCell:

    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\SecAdjCell.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        itemList = []
        cnt = 0

        def _isOK(item):
            if item[0] == '':
                return False
            return True

        def _insertAll():
            script = 'INSERT INTO secadjcell VALUES(?,?)'
            cursor.executemany(script, itemList)
            cursor.commit()

        with open(filePath) as file_obj:
            for i, content in enumerate(file_obj):
                if i == 0:
                    continue
                if cnt % size == 0 and cnt != 0:
                    _insertAll()
                    itemList.clear()
                dataList = content.rstrip().split(",")
                sSectorID = dataList[0]
                nSectorID = dataList[1]
                tempSqlItem = (sSectorID, nSectorID)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt % size != 0:
                _insertAll()
                itemList.clear()

        print("secadjcell finished!")