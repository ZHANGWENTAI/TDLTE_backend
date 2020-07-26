import os

class AdjCell:
    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\AdjCell.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        itemList = []
        cnt = 0

        def _isOK(item):
            if item[2] not in ['37900', '38098', '38400', '38496', '38544', '38950', '39148']:
                print("AdjCell:s_earfcn不对:" + item.__str__())
                return False
            if item[3] not in ['37900', '38098', '38400', '38496', '38544', '38950', '39148']:
                print("AdjCell:n_earfcn不对:" + item.__str__())
                return False
            return True

        def _insertAll():
            script = 'INSERT INTO adjcell VALUES(?,?,?,?)'
            cursor.executemany(script, itemList)
            cursor.commit()

        with open(filePath) as file_obj:
            for i, content in enumerate(file_obj):
                if cnt % size == 0 and cnt != 0:
                    _insertAll()
                    itemList.clear()
                if i == 0:
                    continue
                dataList = content.rstrip().split(",")
                sSectorID = dataList[0]
                nSectorID = dataList[1]
                sEarfcn = dataList[2]
                nEarfcn = dataList[3]
                tempSqlItem = (sSectorID, nSectorID, sEarfcn, nEarfcn)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt % size != 0:
                _insertAll()
                itemList.clear()

        print("adjcell finished!")
