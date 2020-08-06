import os

class Cell:
    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\Cell.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def createIndex(self, cursor):
        with open(os.getcwd() + r'\db\sql\CellIndex.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        city = ""
        sectorID = ""
        sectorName = ""
        eNodeBID = 0
        eNodeBName = ""
        earfcn = 0
        pci = 0
        pss = 0
        sss = 0
        tac = 0
        azimuth = 0
        height = 0
        electtilt = 0
        mechtilt = 0
        totletilt = 0

        itemList = []
        cnt = 0

        def _isOK(item):
            if item[5] not in ['37900', '38098', '38400', '38496', '38544', '38950', '39148']:
                print("Cell:earfcn不对:" + item.__str__())
                return False
            if int(item[6]) > 503 or int(item[6]) < 0:
                print("Cell:pci不对:" + item.__str__())
                return False
            if item[7] not in ['0', '1', '2']:
                print("Cell:ecellType不对:" + item.__str__())
                return False
            if int(item[8]) > 167 or int(item[8]) < 0:
                print("Cell:ecellType不对:" + item.__str__())
                return False
            if not str(item[11]).isnumeric():
                return False
            if int(item[14]) != int(item[12]) + int(item[13]):
                return False
            if int(item[6]) != int(item[7]) + int(item[8]) * 3:
                print("Cell: pci, pss, sss关系不对:" + item.__str__())
                return False
            return True

        def _insertAll():
            script = 'INSERT INTO cell VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            cursor.executemany(script, itemList)
            cursor.commit()

        with open(filePath) as file_obj:
            for i, content in enumerate(file_obj):
                if i == 0:
                    continue
                if cnt == size - 1:
                    _insertAll()
                    itemList.clear()
                    cnt = 0
                dataList = content.rstrip().split(",")
                city = dataList[0]
                sectorID = dataList[1]
                sectorName = dataList[2]
                eNodeBID = dataList[3]
                eNodeBName = dataList[4]
                earfcn = dataList[5]
                pci = dataList[6]
                pss = dataList[7]
                sss = dataList[8]
                tac = dataList[9]
                azimuth = dataList[14]
                height = dataList[15]
                electtilt = dataList[16]
                mechtilt = dataList[17]
                totletilt = dataList[18]
                if pss == '':
                    sss = int(pci) % 3
                if sss == '':
                    sss = int(int(pci) / 3)
                if height == '':
                    height = 7
                if electtilt == '':
                    electtilt = 3
                if mechtilt == '':
                    mechtilt = 4
                if totletilt == '':
                    totletilt = 7
                tempSqlItem = (city, sectorID, sectorName, eNodeBID, eNodeBName,
                    earfcn, pci, pss, sss, tac, azimuth, height,
                    electtilt, mechtilt, totletilt)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt != 0:
                _insertAll()
                itemList.clear()

        print("cell finished!")

