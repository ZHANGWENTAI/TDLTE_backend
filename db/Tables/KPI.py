import pandas as pd
import os

class KPI:
    def createTrig(self, cursor):
        with open(os.getcwd() + r'\db\sql\KPI.sql', encoding='utf-8') as script:
            cursor.execute(script.read())
            cursor.commit()

    def loadFromExcel(self, cursor, size, filePath):
        cnt = 1
        while True:
            df = pd.read_excel(filePath,
               header=None,
               names=['timestamp', 'enb_name', 'sector_name',
                'rrc_conn_succ_rate',
                'erab_succ_rate',
                'erab_drop_rate',
                'wireless_conn',
                'wireless_drop',
                'enb_inter',
                'enb_outer',
                'same_freq_handover',
                'diff_freq_handover',
                'handover_rate',
                'pdcp_upper',
                'pdcp_down',
                'rrc_rebuild',
                'enb_handout_succ',
                'enb_handout_req'],
               skiprows=cnt,
               usecols=[0,2,4,7,10,13,14,18,27,28,29,30,31,32,33,35,40,41],
               nrows=size)
            if df.shape[0] == 0:
                break
            else:
                # fill in the nil by default value 0
                df = df.replace("NIL", 0.0)
                df['timestamp'] = df['timestamp'].str.replace(' 00:00:00', '')

                # insert
                script = 'INSERT INTO kpi VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                cursor.executemany(script, df.values.tolist())
                cursor.commit()
                if df.shape[0] < size:
                    break
                else:
                    cnt += size

        print("kpi finished!")
        return 0, ""
