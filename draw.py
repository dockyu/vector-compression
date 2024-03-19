import matplotlib.pyplot as plt

class Draw:
    def __init__(self):
        """初始化一個畫布"""
        self.figure, self.ax = plt.subplots()

    def plot_data(self, data, title='Data Visualization'):
        """繪製數據"""
        self.ax.plot(data)
        self.ax.set_title(title)
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Value')

    def clear(self):
        """清除畫布，準備下一次繪製"""
        self.ax.clear()

    def show(self):
        """顯示圖表"""
        plt.show()
