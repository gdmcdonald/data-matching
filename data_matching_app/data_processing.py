import pandas as pd
from fuzzywuzzy import fuzz

class DataProcessor:
    def __init__(self, df1: pd.DataFrame, df2: pd.DataFrame, selected_columns: list):
        self.df1 = df1
        self.df2 = df2
        self.selected_columns = selected_columns

    def exact_match(self):
        return pd.merge(self.df1, self.df2, how='inner', on=self.selected_columns)

    def substring_match(self):
        matched_rows = []
        for index, row in self.df1.iterrows():
            for _, row2 in self.df2.iterrows():
                if all(row[col].lower() in row2[col].lower() for col in self.selected_columns):
                    matched_rows.append(row)
        return pd.DataFrame(matched_rows)

    def fuzzy_match(self):
        matched_rows = []
        for index, row in self.df1.iterrows():
            for _, row2 in self.df2.iterrows():
                if all(fuzz.ratio(row[col].lower(), row2[col].lower()) > 80 for col in self.selected_columns):
                    matched_rows.append(row)
        return pd.DataFrame(matched_rows)
