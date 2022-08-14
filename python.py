from collections import Counter
from dataclasses import dataclass

URL = 0
EMPTY_LINE_1 = 1
EMPTY_LINE_2 = 2
TIMESTAMP = 3
TIME_ZONE = 4
METHOD = 5
ADDRESS = 6
PROTOCOL = -3
RESPONSE_STATUS_CODE = -2
NUMBER_OF_BYTES = -1

FILENAMES = ["Jul95", "Aug95"]


class Utils:
    def bytes_to_gb(self, bts):
        return bts // 1e+9

    def format(self, number):
        return "{:,}".format(number)


@dataclass
class Read:
    distinct_hosts = list()
    http_code_status = list()
    total_of_bytes = list()
    top_5_url_not_found = list()
    line_read_error = list()
    filename: str

    def __from_file(self):
        with open(
                f"data/access_log_{self.filename}",
                mode="r",
                encoding="iso8859-1"
        ) as lines:
            count_line = 0
            for line in lines:
                count_line += 1
                current_line = line.rstrip().split(" ")

                try:
                    self.distinct_hosts.append(current_line[URL])

                    bts = current_line[NUMBER_OF_BYTES]

                    self.total_of_bytes.append(
                        int(bts) if bts not in [" ", "-"] else 0
                    )

                    is_a_not_found_request = (
                            current_line[RESPONSE_STATUS_CODE] == "404"
                    )

                    if is_a_not_found_request:
                        self.http_code_status.append(
                            current_line[RESPONSE_STATUS_CODE]
                        )
                        self.top_5_url_not_found.append(current_line[ADDRESS])

                except (ValueError, IndexError, UnicodeDecodeError) as err:
                    line_read_error = current_line
                    print(
                        err,
                        line_read_error,
                        f"Line size {len(current_line)}",
                        f"Line {count_line}"
                    )

            return self

    def __number_of_hosts(self):
        hosts = Utils().format(
            len(list(dict.fromkeys(self.distinct_hosts)))
        )
        print("1) número distintos de hosts:", hosts)
        return self

    def __number_of_errors(self):
        errors = Utils().format(len(self.http_code_status))
        print("2) número de consultas que retornam erro do tipo 404:", errors)
        return self

    def __top_5_address_with_errors(self):
        top_5 = Counter(self.top_5_url_not_found)
        print(
            "3) 5 primeiras URLs com mais erros 404:", top_5.most_common(5)
        )
        return self

    def __bytes_sum(self):
        total = Utils().bytes_to_gb(sum(self.total_of_bytes))
        print(
            "4) quantidade de bytes acumulados ou processados neste "
            "servidor web:",
            f"{total}Gb"
        )
        return self

    def __show(self):
        print(self.filename, "*" * 50)
        (
            self.__number_of_hosts().
            __number_of_errors().
            __top_5_address_with_errors().
            __bytes_sum()
        )

        if self.line_read_error:
            print("Errors:", self.line_read_error)

    def run(self):
        self.distinct_hosts = list()
        self.http_code_status = list()
        self.total_of_bytes = list()
        self.top_5_url_not_found = list()
        self.line_read_error = list()
        self.__from_file().__show()


if __name__ == "__main__":
    for month in FILENAMES:
        Read(month).run()
