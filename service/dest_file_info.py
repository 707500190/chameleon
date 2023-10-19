class DestFileInfo:
    """
    目标文件对象内容：
        1.后缀；
        2.绝对路径；
        3.文件名称；
    """

    def __init__(self):
        # 后缀
        self._suffix = ''
        # 绝对路径
        self._final_path = ''
        # 文件名称
        self._file_name = ''

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        if not isinstance(value, str):
            raise TypeError("suffix must be a string")
        self._suffix = value

    @property
    def final_path(self):
        return self._final_path

    @final_path.setter
    def final_path(self, value):
        if not isinstance(value, str):
            raise TypeError("final_path must be a string")
        self._final_path = value

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        if not isinstance(value, str):
            raise TypeError("file_name must be a string")
        self._file_name = value
