import os

class C2I:
    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\C2I.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        city = ""
        sCellID = ""
        nCellID = ""
        prC2I9 = 0
        c2iMean = 0
        std = 0
        sampleCount = 0
        weightedC2I = 0

        itemList = []
        cnt = 0

        def _isOK(item):
            if float(item[7]) != float(item[3]) * float(item[6]):
                print("c2i:weightedC2I与prC2I9和sampleCount关系不对:" + item.__str__())
                return False
            return True

        def _insertAll():
            script = 'INSERT INTO c2i VALUES(?,?,?,?,?,?,?,?)'
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
                city = dataList[0]
                sCellID = dataList[1]
                nCellID = dataList[2]
                prC2I9 = dataList[3]
                c2iMean = dataList[4]
                std = dataList[5]
                sampleCount = dataList[6]
                weightedC2I = dataList[7]
                if weightedC2I == '':
                    weightedC2I = float(prC2I9) * float(sampleCount)
                tempSqlItem = (city, sCellID, nCellID, prC2I9, c2iMean, std, sampleCount, weightedC2I)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt != 0:
                _insertAll()
                itemList.clear()

        print("c2i finished!")