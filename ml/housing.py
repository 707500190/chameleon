import hashlib
import os
import tarfile

import numpy as np
import pandas as pd
from six.moves import urllib

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"

HOUSING_PATH = "datasets/housing"

HOUSING_URL = DOWNLOAD_ROOT + HOUSING_PATH + "/housing.tgz"


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    if not os.path.isdir(housing_path):
        os.makedirs(housing_path)

    tgz_path = os.path.join(housing_path, "housing.tgz")

    urllib.request.urlretrieve(housing_url, tgz_path)

    housing_tgz = tarfile.open(tgz_path)

    housing_tgz.extractall(path=housing_path)

    housing_tgz.close()


def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path, "housing.csv")

    return pd.read_csv(csv_path)


def split_train_test(data, test_ration):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ration)
    test_indices = shuffled_indices[: test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]


def test_set_check(identifier, test_ratio, hash):
    return hash(np.int64(identifier)).digest()[-1] < 256 * test_ratio


def split_train_test_by_id(data, test_ratio, id_column, hash=hashlib.md5):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio, hash))
    return data.loc[~in_test_set], data.loc[in_test_set]



if __name__ == '__main__':
    housing = load_housing_data()
    # 设置随机数种子为42
    np.random.seed(42)
    split_train_test(housing, 0.2)
    # 设置主键，可以使用函数自带，也可使用不变的属性组合
    housing_with_id = housing.reset_index()  # add index column
    train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "index")

    # from sklearn.model_selection import train_test_split
    #
    # train_set, test_set = train_test_split(housing_with_id, 0.2, random_state=42)
