import numpy as np
import pandas as pd
from typing import Callable

# Split dataframe into several blocks then apply function on them
def run_blocks(data: pd.Series, size: int, func: Callable) -> list:
    return np.array([func(data.iloc[i:size+i]) for i in range(0, len(data), size)])

