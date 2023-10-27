import numpy as np
import pandas as pd

if __name__ == '__main__':
    # serl = pd.Series(data = [1, 2, 3, 4, 5], index= ['a', 'b', 'c', 'd', 'e'])
    # print(serl)
    #
    # serl2 = pd.Series(data = {'a':[1,2,3,4], 'b':[1,2,3,4,5]})
    # print(serl2)
    # # 将字典变成数据框
    # d = {'color': ['blue', 'green', 'gold', 'red', 'grey'],
    #      'object': ['car', 'bus', 'van', 'boat', 'ship'],
    #      'price': [1.2, 2.3, 3, 4.5, 5.6]}
    # frame = pd.DataFrame(d, index=['a', 'b', 'c', 'd', 'e'])
    # print(frame)
    #
    d = [[1.0, 2.2, 3, 4], [1, 2, 3, 4], [7, 8, 9, 0], [3, 5, 7, 9]]
    df = pd.DataFrame(d, index=['a', 'b', 'c', 'd'], columns=['A', 'B', 'C', 'D'])
    # print(df)
    # print(np.mean(df))  # 每一列的均值
    # print(np.mean(df, axis=1))  # 每一行的均值
    # print(df.mean(axis=1))  # 每一行的均值
    # print(df.std())  # 标准差
    des = df.describe()  # 按列查看分布情况
    des2 = df.T.describe()  # 按行查看分布情况
    df = pd.DataFrame(data=[[2, 3, 4, 5, 6]], columns=['a', 'b', 'c', 'd', 'e'])
    df.reset_index(inplace=True)
    print(df)

    # 创建一个示例 DataFrame
    data = pd.DataFrame({'A': [1, 2, 3],
                         'B': [4, 5, 6],
                         'C': [7, 8, 9]})
    print(data)

    # 将 DataFrame 转换为形状 (3, 3)
    reshaped_data = data.values.reshape((3, 3))

    print(reshaped_data)
    print(data.loc[[~True, True, True]])
    # 输出：
