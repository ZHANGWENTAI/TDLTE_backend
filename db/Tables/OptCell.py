import os

class OptCell:

    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\OptCell.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        sectorID = ""
        earfcn = 0
        cellType = ""

        itemList = []
        cnt = 0

        def _isOK(item):
            if item[1] not in ['37900', '38098', '38400', '38496', '38544', '38950', '39148']:
                print("OptCell:earfcn不对:" + item.__str__())
                return False
            if item[2] not in ["优化区", "保护带"]:
                print("OptCell:ecellType不对:" + item.__str__())
                return False
            return True

        def _insertAll():
            script = 'INSERT INTO optcell VALUES(?,?,?)'
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
                sectorID = dataList[0]
                earfcn = dataList[1]
                cellType = dataList[2]
                tempSqlItem = (sectorID, earfcn, cellType)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt % size != 0:
                _insertAll()
                itemList.clear()

        print("optcell finished!")
