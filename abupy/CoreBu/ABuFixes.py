# -*- encoding:utf-8 -*-
"""
    对各个依赖库不同版本，不同系统的规范进行统一以及问题修正模块
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import numbers
import sys

import matplotlib
import numpy as np
import pandas as pd
import scipy
import sklearn as skl

__author__ = '阿布'
__weixin__ = 'abu_quant'


def _parse_version(version_string):
    """
    根据库中的__version__字段，转换为tuple，eg. '1.11.3'->(1, 11, 3)
    :param version_string: __version__字符串对象
    :return: tuple 对象
    """
    version = []
    for x in version_string.split('.'):
        try:
            version.append(int(x))
        except ValueError:
            version.append(x)
    return tuple(version)


"""numpy 版本号tuple"""
np_version = _parse_version(np.__version__)
"""sklearn 版本号tuple"""
skl_version = _parse_version(skl.__version__)
"""pandas 版本号tuple"""
pd_version = _parse_version(pd.__version__)
"""scipy 版本号tuple"""
sp_version = _parse_version(scipy.__version__)
"""matplotlib 版本号tuple"""
mpl_version = _parse_version(matplotlib.__version__)

from inspect import signature, Parameter

from concurrent.futures import ThreadPoolExecutor


# six compatibility shim removed


import pickle
from functools import reduce

# Builtins for compatibility
zip = zip
range = range
map = map
filter = filter

# Fix for xrange in Python 3
try:
    xrange = range
except NameError:
    pass

# Python 3 only
Unpickler = pickle.Unpickler
Pickler = pickle.Pickler

def as_bytes(s):
    if isinstance(s, bytes):
        return s
    return s.encode('latin1')

from functools import lru_cache

from itertools import combinations_with_replacement

# noinspection PyUnresolvedReferences
from functools import partial
from scipy.stats import rankdata
from sklearn.model_selection import KFold, learning_curve, GridSearchCV, train_test_split, cross_val_score
from sklearn.mixture import GaussianMixture as GMM
from sklearn.metrics import mean_squared_error, make_scorer

mean_squared_error_scorer = make_scorer(mean_squared_error)

"""
    matplotlib fixes
"""
# 先别加了，用的地方内部try吧，不然waring太多
# try:
#     # noinspection PyUnresolvedReferences, PyDeprecation
#     import matplotlib.finance as mpf
# except ImportError:
#     # 2.2 才会有
#     # noinspection PyUnresolvedReferences, PyDeprecation
#     import matplotlib.mpl_finance as mpf

"""
    urlencode
"""
# noinspection PyUnresolvedReferences, PyCompatibility
from urllib.parse import urlencode

"""
    sklearn fixes
"""


# noinspection PyProtectedMember,PyUnresolvedReferences
def check_random_state(seed):
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)
