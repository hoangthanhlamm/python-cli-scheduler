import re
from typing import Union

from cli_scheduler.constants.time_constants import TimeInterval

scheduler_format = '^<run_now>@<interval>/<delay>$<end_timestamp>#<retry>'


def parse_scheduler_kwargs(schedule: str):
    def to_bool(d_str: str) -> bool:
        if d_str.lower() == 'false' or d_str == '0':
            return False
        return True

    def to_int(d_str: str, default=None) -> Union[None, int]:
        if d_str.isnumeric():
            return int(d_str)
        elif d_str in TimeInterval.mapping:
            return TimeInterval.mapping[d_str]
        elif d_str == '' or d_str.lower() == 'none' or d_str.lower() == 'null':
            return default
        else:
            raise ValueError(f'Not support interval with {d_str}')

    run_now_str = re.search(r'\^([a-zA-Z0-9]*)', schedule)
    run_now = to_bool(run_now_str.group(1)) if run_now_str is not None else True

    interval_str = re.search(r'@([a-zA-Z0-9]*)', schedule)
    interval = to_int(interval_str.group(1), default=None) if interval_str is not None else None

    delay_str = re.search(r'/(\d*)', schedule)
    delay = to_int(delay_str.group(1), default=0) if delay_str is not None else 0

    end_timestamp_str = re.search(r'\$(\d*)', schedule)
    end_timestamp = to_int(end_timestamp_str.group(1), default=None) if end_timestamp_str is not None else None

    retry_str = re.search(r'#([a-zA-Z0-9]*)', schedule)
    retry = to_bool(retry_str.group(1)) if retry_str is not None else True

    return {'run_now': run_now, 'interval': interval, 'delay': delay, 'end_timestamp': end_timestamp, 'retry': retry}
