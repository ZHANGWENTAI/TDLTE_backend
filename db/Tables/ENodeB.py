import pandas as pd
import os

class ENodeB:
    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\ENodeB.sql', encoding='utf-8') as script:
            # print(script.read())
            cursor.execute(script.read())
            cursor.commit()

    def loadData(self, cursor, size, filePath):
        if os.path.splitext(filePath)[-1] in ['.xlsx', '.xls', '.xlsx/', '.xls/']:
            cnt = 1
            while True:
                df = pd.read_excel(filePath,
                                   header=None,
                                   names=['city', 'eNodeBID', 'eNodeBName', 'vendor', 'longitude', 'latitude', 'style'],
                                   skiprows=cnt,
                                   usecols=[0, 3, 4, 10, 11, 12, 13],
                                   nrows=size)
                if df.shape[0] == 0:
                    print("enodeb finished!")
                    break
                else:
                    # wash data
                    df = df.loc[df['vendor'].isin(["华为", "中兴", "诺西", "爱立信", "贝尔", "大唐"])
                              & df['style'].isin(["宏站", "室分", "室外"])]
                    # insert
                    script = 'INSERT INTO enodeb VALUES(?,?,?,?,?,?,?)'
                    cursor.executemany(script, df.values.tolist())
                    cursor.commit()
                    if df.shape[0] < size:
                        print("enodeb finished!")
                        break
                    else:
                        cnt += size

            return 0, ""
        elif os.path.splitext(filePath)[-1] in ['.csv', '.csv/']:
            for df in pd.read_csv(filePath,
                                  encoding='gb2312',
                                  chunksize=size,
                                  names=['city', 'eNodeBID', 'eNodeBName', 'vendor', 'longitude', 'latitude', 'style'],
                                  usecols=[0, 3, 4, 10, 11, 12, 13]):
                if df.shape[0] == 0:
                    break
                # wash data
                df = df.loc[df['vendor'].isin(["华为", "中兴", "诺西", "爱立信", "贝尔", "大唐"])
                            & df['style'].isin(["宏站", "室分", "室外"])]
                # insert
                script = 'INSERT INTO enodeb VALUES(?,?,?,?,?,?,?)'
                cursor.executemany(script, df.values.tolist())
                cursor.commit()
            print("enodeb finished!")
            return 0, ""
        else:
            return 1, str(filePath) + ': 文件格式有误\n'