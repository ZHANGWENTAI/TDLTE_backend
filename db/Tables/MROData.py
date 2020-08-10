import os
import processbar

class MROData:

    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\MROData.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        timeStamp = ""
        servingSector = ""
        interferingSector = ""
        lteSCRsrp = 0
        lteNCRsrp = 0
        lteNCEarfcn = 0
        lteNCPCI = 0

        itemList = []
        cnt = 0
        processbar.row = 0

        def _isOK(item):
            if item[5] not in ['37900', '38098', '38400', '38496', '38544', '38950', '39148']:
                print("MROData:earfcn不对:" + item.__str__())
                return False
            if int(item[6]) > 503 or int(item[6]) < 0:
                print("MROData:pci不对:" + item.__str__())
                return False
            return True

        def _insertAll():
            script = 'INSERT INTO mrodata VALUES(?,?,?,?,?,?,?)'
            cursor.executemany(script, itemList)
            cursor.commit()

        with open(filePath) as file_obj:
            for i, content in enumerate(file_obj):
                if i == 0:
                    continue
                if cnt == size:
                    _insertAll()
                    itemList.clear()
                    processbar.row += size
                    cnt = 0
                dataList = content.rstrip().split(",")
                timeStamp = dataList[0]
                servingSector = dataList[1]
                interferingSector = dataList[2]
                lteSCRsrp = dataList[3]
                lteNCRsrp = dataList[4]
                lteNCEarfcn = dataList[5]
                lteNCPCI = dataList[6]
                tempSqlItem = (timeStamp, servingSector, interferingSector, lteSCRsrp, lteNCRsrp, lteNCEarfcn, lteNCPCI)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt != 0:
                _insertAll()
                itemList.clear()


        print("mrodata finished!")
        return 0, ""

