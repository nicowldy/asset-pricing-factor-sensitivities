from __future__ import annotations

import os
from src.config import FF_FF3_RAW as FF_3F_RAW, FF_CAPM_RAW as FF_1F_RAW


def extract_market_factor_data() -> None:
    os.makedirs(os.path.dirname(str(FF_1F_RAW)), exist_ok=True)
    with open(str(FF_3F_RAW)) as fin, open(str(FF_1F_RAW), "w") as fout:
        fout.write(",MKT,RF\n")
        next(fin)
        for line in fin:
            cols = line.strip().split(",")
            fout.write(f"{cols[0]},{cols[1]},{cols[4]}\n")


if __name__ == "__main__":
    extract_market_factor_data()
