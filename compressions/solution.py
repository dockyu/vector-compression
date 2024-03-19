class Solution:
    def __init__(self, start=None, V=None, C=None):
        """
        初始化一個Solution實例。

        參數:
        c1 (int): 起點，壓縮序列的開始位置。
        V (list): 變化序列，描述從c1開始的壓縮序列的變化。
        C (list): 壓縮序列，根據c1和V生成的最終壓縮序列。
        """
        self.start = start
        self.V = V if V is not None else []
        self.C = C if C is not None else []

    @classmethod
    def from_start_v(cls, start, V):
        """
        根據start和V建立Solution實例的類方法。

        參數:
        start (int): 起點。
        V (list): 變化序列。

        返回:
        Solution實例。
        """
        return cls(start=start, V=V)

