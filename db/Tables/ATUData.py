import os

class ATUData:

    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\ATUData.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        seq = 0
        fileName = ""
        timeStamp = ""
        longitude = 0
        latitude = 0
        cellID = ""
        tac = 0
        earfcn = 0
        pci = 0
        rsrp = 0
        rsSinr = 0
        nCellID1 = ""
        nCellEarfcn1 = 0
        nCellPCI1 = 0
        nCellRsrp1 = 0
        nCellID2 = ""
        nCellEarfcn2 = 0
        nCellPCI2 = 0
        nCellRsrp2 = 0
        nCellID3 = ""
        nCellEarfcn3 = 0
        nCellPCI3 = 0
        nCellRsrp3 = 0
        nCellID4 = ""
        nCellEarfcn4 = 0
        nCellPCI4 = 0
        nCellRsrp4 = 0
        nCellID5 = ""
        nCellEarfcn5 = 0
        nCellPCI5 = 0
        nCellRsrp5 = 0
        nCellID6 = ""
        nCellEarfcn6 = 0
        nCellPCI6 = 0
        nCellRsrp6 = 0

        itemList = []
        cnt = 0

        def _getNullData(data, type):
            if data != '':
                return data
            if type == 'num':
                return -1
            return 'null'

        def _isOK(item):
            if int(item[8]) > 503 or int(item[8]) < 0:
                print("ATUData:pci不对:" + item.__str__())
                return False
            if item[7] not in ['37900', '38098', '38400', '38496', '38544', '38950', '39148']:
                print("Cell:earfcn不对:" + item.__str__())
                return False
            return True

        def _insertAll():
            script = 'INSERT INTO atudata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
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
                seq = dataList[0]
                fileName = dataList[1]
                timeStamp = dataList[2]
                longitude = dataList[3]
                latitude = dataList[4]
                cellID = dataList[5]
                tac = dataList[6]
                earfcn = dataList[7]
                pci = dataList[8]
                rsrp = dataList[9]
                rsSinr = dataList[10]
                nCellID1 = _getNullData(dataList[11], 'str')
                nCellEarfcn1 = _getNullData(dataList[12], 'num')
                nCellPCI1 = _getNullData(dataList[13], 'num')
                nCellRsrp1 = _getNullData(dataList[14], 'num')
                nCellID2 = _getNullData(dataList[15], 'str')
                nCellEarfcn2 = _getNullData(dataList[16], 'num')
                nCellPCI2 = _getNullData(dataList[17], 'num')
                nCellRsrp2 = _getNullData(dataList[18], 'num')
                nCellID3 = _getNullData(dataList[19], 'str')
                nCellEarfcn3 = _getNullData(dataList[20], 'num')
                nCellPCI3 = _getNullData(dataList[21], 'num')
                nCellRsrp3 = _getNullData(dataList[22], 'num')
                nCellID4 = _getNullData(dataList[23], 'str')
                nCellEarfcn4 = _getNullData(dataList[24], 'num')
                nCellPCI4 = _getNullData(dataList[25], 'num')
                nCellRsrp4 = _getNullData(dataList[26], 'num')
                nCellID5 = _getNullData(dataList[27], 'str')
                nCellEarfcn5 = _getNullData(dataList[28], 'num')
                nCellPCI5 = _getNullData(dataList[29], 'num')
                nCellRsrp5 = _getNullData(dataList[30], 'num')
                nCellID6 = _getNullData(dataList[31], 'str')
                nCellEarfcn6 = _getNullData(dataList[32], 'num')
                nCellPCI6 = _getNullData(dataList[33], 'num')
                nCellRsrp6 = _getNullData(dataList[34], 'num')
                tempSqlItem = (seq, fileName, timeStamp, longitude, latitude,
                            cellID, tac, earfcn, pci, rsrp, rsSinr,
                            nCellID1, nCellEarfcn1, nCellPCI1, nCellRsrp1,
                            nCellID2, nCellEarfcn2, nCellPCI2, nCellRsrp2,
                            nCellID3, nCellEarfcn3, nCellPCI3, nCellRsrp3,
                            nCellID4, nCellEarfcn4, nCellPCI4, nCellRsrp4,
                            nCellID5, nCellEarfcn5, nCellPCI5, nCellRsrp5,
                            nCellID6, nCellEarfcn6, nCellPCI6, nCellRsrp6)
                if _isOK(tempSqlItem):
                    itemList.append(tempSqlItem)
                    cnt += 1
            if cnt != 0:
                _insertAll()
                itemList.clear()

        print("atudata finished!")
