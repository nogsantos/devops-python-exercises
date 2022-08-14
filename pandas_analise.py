import re
from dataclasses import dataclass

import pandas as pd
from pandas import DataFrame

FILENAMES = ["Jul95", "Aug95"]


class Utils:
    def bytes_to_gb(self, bts):
        return bts // 1e+9

    def format(self, number):
        return "{:,}".format(number)


@dataclass
class Analise:
    filename: str
    frame: DataFrame = DataFrame()

    def __process(self):
        list_df = []
        for chuck in pd.read_csv(
                f"data/access_log_{self.filename}",
                sep="\\n",
                engine="python",
                encoding="iso8859-1",
                header=None,
                chunksize=10 ** 5
        ):
            list_df.append(chuck[:])

        self.frame = pd.concat(list_df)

        rows = []
        for d in self.frame[0]:
            rows.append([
                re.findall(x, d)
                for x
                in [
                    r"^\S*",
                    r"\[(.*?)\/",
                    r"\"(.*?)\"",
                    r"\s(\d+)\s",
                    r"(\d+)(?!.*\d)"
                ]
            ])

        self.frame = pd.DataFrame(
            rows[:], columns=["host", "day", "request", "http", "bytes"]
        )
        return self

    def replace_to_zero(self, col, value_to_zero):
        self.frame[col] = self.frame[col].replace(value_to_zero, "0")

    def convert_str(self, columns):
        for c in columns:
            self.frame[c] = [
                str("".join(map(str, x))).strip() for x in self.frame[c]
            ]

    def __number_of_hosts(self):
        hosts = Utils().format(len(self.frame["host"].value_counts()))
        print("1) número distintos de hosts:", hosts)
        return self

    def __number_of_errors(self):
        errors = Utils().format(
            self.frame[self.frame["http"].str.contains("404")].count()["host"]
        )
        print("2) número de consultas que retornam erro do tipo 404:", errors)
        return self

    def __top_5_address_with_errors(self):
        top_5 = self.frame[
            self.frame["http"].str.contains("404")
        ].groupby(["request"]).count().sort_values(by="http")
        print(
            "3) 5 primeiras URLs com mais erros 404:", top_5["http"].tail()
        )
        return self

    def __bytes_sum(self):
        self.frame.drop(self.frame.tail(1).index, inplace=True)
        total = Utils().bytes_to_gb(
            self.frame["bytes"].astype("int64").sum()
        )
        print(
            "4) quantidade de bytes acumulados ou processados neste "
            "servidor web:",
            f"{total}Gb"
        )
        return self

    def __show(self):
        self.convert_str(self.frame.columns)
        self.replace_to_zero("bytes", "404")
        print(self.filename, "*" * 50)
        (
            self.__number_of_hosts().
            __number_of_errors().
            __top_5_address_with_errors().
            __bytes_sum()
        )

    def run(self):
        self.__process().__show()


if __name__ == "__main__":
    for month in FILENAMES:
        Analise(month).run()
