# -*- coding: utf-8 -*-
"""
Max Drawdown (MDD)

@author: FL
"""
# Date: 18/06/26 = Tue

import numpy as np
import matplotlib.pyplot as plt


def mdd(p):
    m = []
    peak = 0
    mdd_so_far = 0
    for i in range(len(p)):
        if p[i] > peak:
            peak = p[i]
        if peak - p[i] > mdd_so_far:
            mdd_so_far = peak - p[i]
        m.append(mdd_so_far)
    return m


if __name__ == '__main__':
    p = np.random.randn(100).cumsum()
    plt.plot(p)
    m = mdd(p)
    plt.plot(m)
    plt.show()
