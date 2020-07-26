import os

class ATUC2I:
    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\ATUC2I.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        itemList = []
        cnt = 0

        def _isOK(item):
            if item[4] not in ["0", "1"]:
                print("atuc2i:cosite不对:" + item.__str__())
                return False
            return True

        def _insertAll():
            script = 'INSERT INTO atuc2i VALUES(?,?,?,?,?)'
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
                sectorID = dataList[0]
                nCellID = dataList[1]
                ratioAll = dataList[2]
                rank = dataList[3]
                cosite = dataList[4]
                tempSqlItem = (sectorID, nCellID, ratioAll, rank, cosite)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt != 0:
                _insertAll()
                itemList.clear()

        print("atuc2i finished!")