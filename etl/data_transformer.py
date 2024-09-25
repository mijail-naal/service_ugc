from typing import Generator

from schemas import DictData


class DataTransformer:
    """Class to convert ConsumerRecord into string."""

    def record_to_string(self, times: int, extractor: Generator) -> list:
        data = []
        for _ in range(times):
            for record in extractor:
                record_map = DictData(**record._asdict())
                data.append(record_map.key + '-' + record_map.value)
        return data

    def generate_values(self, data: list) -> str:
        values = ''
        list_values = [x.split('-') for x in data]

        for i in list_values:
            values += '(' + "'" + "', '".join(i) + "'" + '), '
        return values.rstrip(', ')
