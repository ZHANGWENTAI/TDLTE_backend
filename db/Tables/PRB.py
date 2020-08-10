import pandas as pd
import os
import processbar

class PRB:
    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\PRB.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadFromExcel(self, cursor, size, filePath):
        cnt = 1
        processbar.row = 0
        while True:
            df = pd.read_excel(filePath,
                               header=None,
                               skiprows=cnt,
                               usecols=[0, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                        21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                                        31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                                        41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                                        51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                                        61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                                        71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
                                        81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
                                        91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                                        101, 102, 103, 104,],
                               nrows=size)
            if df.shape[0] == 0:
                break
            else:
                # insert
                script = """INSERT INTO prb VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                         ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                         ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                         ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                         ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                         ?,?,?)"""

                cursor.executemany(script, df.values.tolist())
                cursor.commit()

                cnt += size
                processbar.row = cnt

        print("prb finished!")
        return 0, ""




