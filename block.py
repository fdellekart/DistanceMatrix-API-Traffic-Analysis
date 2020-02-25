import pandas as pd


class Block:
    def __init__(self, conjunctions_path=r'CSV\conjunctions.csv'):
        self.conjunctions_path = conjunctions_path
        self.conjunctions = None
        self.load_conjunctions()

    def load_conjunctions(self):
        conj_csv = pd.read_csv(self.conjunctions_path)
        conj_csv['connected_right'] = self._con_to_list(conj_csv['connected_right'])
        conj_csv['connected_wrong'] = self._con_to_list(conj_csv['connected_wrong'])
        conj_csv.set_index('id', inplace=True)
        self.conjunctions = conj_csv

    def _con_to_list(self, series):
        con_series = series
        for idx, con in enumerate(con_series):
            con_series[idx] = str(con).split('-')
        return con_series
