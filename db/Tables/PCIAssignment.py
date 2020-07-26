import os

class PCIAssignment:

    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\PCIAssignment.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        assignID = 0
        earfcn = 0
        sectorID = ""
        sectorName = ""
        eNodeBID = 0
        pci = 0
        pss = 0
        sss = 0
        longitude = 0
        latitude = 0
        style = ""
        optDatetime = ""

        itemList = []
        cnt = 0

        def _isOK(item):
            if item[1] not in ['37900', '38098', '38400', '38496', '38544', '38950', '39148']:
                print("pciassignment:earfcn不对:" + item.__str__())
                return False
            if int(item[5]) > 503 or int(item[5]) < 0:
                print("Cell:pci不对:" + item.__str__())
                return False
            if item[6] not in ['0', '1', '2']:
                print("Cell:ecellType不对:" + item.__str__())
                return False
            if int(item[7]) > 167 or int(item[7]) < 0:
                print("Cell:ecellType不对:" + item.__str__())
                return False
            if item[10] not in ["宏站", "室分", "室外"]:
                print("pciassignment:ecellType不对:" + item.__str__())
                return False
            if int(item[5]) != int(item[6]) + int(item[7]) * 3:
                print("PCIAssignment:pci,pss,sss关系不对:" + item.__str__())
                return False
            return True

        def _insertAll():
            script = 'INSERT INTO pciassignment VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'
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
                assignID = dataList[0]
                earfcn = dataList[1]
                sectorID = dataList[2]
                sectorName = dataList[3]
                eNodeBID = dataList[4]
                pci = dataList[5]
                pss = dataList[6]
                sss = dataList[7]
                longitude = dataList[8]
                latitude = dataList[9]
                style = dataList[10]
                optDatetime = dataList[11]
                if pss == '':
                    pss = int(pci) % 3
                if sss == '':
                    sss = int(int(pci) / 3)
                tempSqlItem = (assignID, earfcn, sectorID, sectorName,
                               eNodeBID, pci, pss, sss, longitude, latitude, style, optDatetime)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt != 0:
                _insertAll()
                itemList.clear()

        print("pciassignment finished!")

