from .solution import Solution

class OneDOneVector:
    def __init__(self, S, d = None):
        """
        初始化OneDOneVector類別的實例。

        參數:
        S (list of int): 原始序列
        d (int): 壓縮序列的間距
        
        屬性:
        solutions (list of Solution): 儲存所有最佳解，初始化為空列表
        """
        self.S = S
        self.d = d
        self.E = float('inf')  # 初始化最小誤差為無限大
        self.solutions = []  # 使用Solution實例的列表來儲存解

    def brute_force(self):
        """
        給定 S, d
        透過暴力法找出原始序列壓縮後的最佳起點，最小化總誤差。

        方法:
        從原始序列S中找到最小值和最大值，建立一個可能的起點範圍，
        從最小值-2*d到最大值+2*d。對於範圍內的每一個可能起點，
        調用DP_from_start方法計算從該起點開始壓縮時的總誤差E和壓縮後的變化序列V。
        """
        min_val = min(self.S)
        max_val = max(self.S)

        for start in range(min_val - 2 * self.d, max_val + 2 * self.d + 1):
            E, solutions = self.DP_from_start(start)
            
            if E < self.E:
                # 發現更小的E，清空solutions，更新E，添加當前解
                self.solutions.clear()
                self.E = E
                self.solutions.extend(solutions)
            elif E == self.E:
                # 當E相等時，檢查每個solution的V是否與現有解的所有V都不同
                for solution in solutions:
                    if not any(solution.V == existing_solution.V for existing_solution in self.solutions):
                        self.solutions.append(solution)  # 添加不同的solution

    def brute_force_v2(self):
        """
        給定 S, d
        迭代每一個節點 i，使 Ci = Si，用DP方法算出對齊(Ci = Si)的情況下的最佳解，
        並從中找出最好的

        方法:
        迭代每一個節點 i，從 0 到 len(S)-1
        用DP方法算出對齊(Ci = Si)的情況下的最佳解，
        調用DP_from_node方法計算從該對齊點開始壓縮時的總誤差E和壓縮後的變化序列V，
        並從中找出最好的。
        """
        for i in range(len(self.S)):
            # print(i)
            E, solutions = self.DP_from_node(i)

            if E < self.E:
                # 發現更小的E，清空solutions，更新E，添加當前解
                self.solutions.clear()
                self.E = E
                self.solutions.extend(solutions)
            elif E == self.E:
                # 當E相等時，檢查每個solution的V是否與現有解的所有V都不同
                for solution in solutions:
                    if not any(solution.V == existing_solution.V for existing_solution in self.solutions):
                        self.solutions.append(solution)  # 添加不同的solution
        pass

    def DP_from_start(self, start):
        """
        根據給定的起點計算壓縮序列，並返回總誤差和solution。

        參數:
        start (int): 起始點

        返回:
        E (float): 從該起點開始壓縮時的總誤差
        solutions (list of Solution): 從該起點開始的最佳解的list
        """

        # 初始化 table D
        n = len(self.S)  # 序列的長度
        D = [[float('inf')] * (2 * n + 1) for _ in range(n)]
        mid = n  # 中間位置的索引
        D[0][mid] = abs(start - self.S[0])  # 初始化第一行

        # DP 從第二行開始逐行填充 table D
        for i in range(1, n):  # 從第二行開始
            for j in range(0, 2 * n + 1):  # 遍歷每一列，包含所有可能的索引
                # 計算index，從-n到n
                index = j - mid
                # 計算當前位置的值與實際值的差異
                diff = abs(start + index * self.d - self.S[i])
                # 針對j的不同值進行處理，以避免越界
                left = D[i-1][j-1] if j > 0 else float('inf')  # 第i-1個比目前的值小d
                right = D[i-1][j+1] if j < 2 * n else float('inf')  # 第i-1個比目前的值大d

                # 更新D[i][j]為最小誤差
                if left == float('inf') and right == float('inf'):
                    # 如果left和right都是無窮大，直接設置當前位置的誤差為無窮大
                    D[i][j] = float('inf')
                else:
                    # 否則，更新D[i][j]為最小誤差
                    D[i][j] = min(left, right, D[i-1][j]) + diff

        # 印出 D
        # for row in D:
        #     print(" ".join(f"{val:8.2f}" for val in row))

        # 初始化stack
        stack = [{"i": n-1, "j": j, "V": []} for j, val in enumerate(D[-1]) if val == min(D[-1])]
        solutions = []  # 指定start的solution

        while stack:
            state = stack.pop()
            i, j, V = state["i"], state["j"], state["V"]
            if i == 0:
                # 回朔到底，創建一個Solution並添加到solutions
                solutions.append(Solution.from_start_v(start, V))
                continue

            # 計算左、右的成本
            left = D[i-1][j-1] if j > 0 else float('inf')
            right = D[i-1][j+1] if j < 2*n else float('inf')
            E_i = min(left, right)  # 前i個的E

            # 如果左側成本是最小成本
            if left == E_i:
                V_left = [True] + V
                stack.append({"i": i-1, "j": j-1, "V": V_left})
            
            # 如果右側成本是最小成本
            if right == E_i:
                V_right = [False] + V
                stack.append({"i": i-1, "j": j+1, "V": V_right})

        # 由 start, V, d 建構出 C
        for solution in solutions:
            C = self.create_C(solution.start, solution.V)
            solution.C = C
            
        E = min(D[-1])  # 此start最小的E
        return E, solutions 

    def DP_from_node(self, i):
        """
        對齊第i點計算壓縮序列，並返回總誤差和solution。

        參數:
        i (int): 對齊點的index，從 0 ~ len(self.S)-1

        返回:
        E (float): 從該起點開始壓縮時的總誤差
        solutions (list of Solution): 從該起點開始的最佳解的list
        """
        # 判斷i適合法範圍
        if i < 0:
            print("DP_from_node: i 小於 0")
            return []
        if i > len(self.S) - 1:
            print("DP_from_node: i 大於等於 S 的長度")
            return []

        left_S = self.S[:i+1]
        right_S = self.S[i:]
        reversed_left_S = left_S[::-1]
        # print(f"left_S: {left_S}")
        # print(f"right_S: {right_S}")
        # print(f"reversed_left_S: {reversed_left_S}")

        oneDOneVector_l = OneDOneVector(reversed_left_S, self.d)
        oneDOneVector_r = OneDOneVector(right_S, self.d)

        E_l, solutions_l = oneDOneVector_l.DP_from_start(self.S[i])
        E_r, solutions_r = oneDOneVector_r.DP_from_start(self.S[i])
        
        E = E_l + E_r
        solutions = []
        for solution_l in solutions_l:
            start = solution_l.C[-1]
            V_l = solution_l.V[::-1]
            V_l = reversed_bool_list = [not x for x in V_l]
            for solution_r in solutions_r:
                V_r = solution_r.V
                # print(f"V_l: {V_l}")
                # print(f"V_r: {V_r}")
                V = V_l + V_r
                # print(f"V: {V}")
                # print(f"left S = {reversed_left_S}")
                # print(f"left E_l = {E_l}")
                # print(f"  start = {solution_l.start}")
                # print(f"  V = {solution_l.V}")
                # print(f"  C = {solution_l.C}")
                # print(f"right S = {right_S}")
                # print(f"right E_r = {E_r}")
                # print(f"  start = {solution_r.start}")
                # print(f"  V = {solution_r.V}")
                # print(f"  C = {solution_r.C}")

                solutions.append(Solution.from_start_v(start, V))
        
        # 由 start, V, d 建構出 C
        for solution in solutions:
            C = self.create_C(solution.start, solution.V)
            solution.C = C
        
        return E, solutions







    def translate_from_V(self, V):
        """
        根據給定的變化序列，返回總誤差和solution。

        參數:
        V (list of boolean): 變化序列

        返回:
        E (float): 該變化序列的總誤差
        solutions (list of Solution): 從該起點開始的最佳解的list
        """
        start = self.S[0]  # 隨機產生起點，這裡直接對齊S[0]
        C = self.create_C(start, V)
        # 計算每一個點的誤差
        delta = [ci - si for ci, si in zip(C, self.S)]

        """
        獲取中位數
        """
        # 對 delta 進行排序
        sorted_delta = sorted(delta)

        # 計算中位數
        len_delta = len(sorted_delta)
        if len_delta % 2 == 1:
            # 如果是奇數，直接取中間的值
            delta_median = sorted_delta[len_delta // 2]
        else:
            # 如果是偶數，取中間兩個值的平均
            delta_median = (sorted_delta[len_delta // 2 - 1] + sorted_delta[len_delta // 2]) / 2.0
        
        C = [val - delta_median for val in C]  ## 對齊中位數 => 根據中位數的差修正每一個
        E = self.calculate_E(C)
        
        print("測試")
        print(print("Total Error (E): ", E))
        print(f"  C: {C}, V: {V}")
        
        return E, Solution(start=C[0], V=V, C=C)

    def create_C(self, start, V):
        """
        由 start, V, self.d 產生 C
        """
        C = [start]
        for v in V:
            # 根據V中的布爾值決定是加上self.d還是減去self.d
            variety = self.d if v else -self.d
            C.append(C[-1] + variety)
        return C

    def calculate_E(self, C):
        # 計算 self.S 和 C 每一項的差的絕對值的合
        E = sum(abs(si - ci) for si, ci in zip(self.S, C))
        return E

    def show(self):
        print("原始序列    (S): ", self.S)
        print("Vector      (d): ", self.d)
        
        if not self.solutions:
            print("沒有找到任何Solution。")
            return
        
        print("Total Error (E): ", self.E)
        print(f"總共有 {len(self.solutions)} 組Solution")

        for i, solution in enumerate(self.solutions, 1):
            C = solution.C
            # 使用列表推導將布林型列表轉換為包含'1'和'0'的新列表
            V_list = [1 if v else 0 for v in solution.V]
            print(f"  Solution #{i} C: {C}, V: {V_list}")