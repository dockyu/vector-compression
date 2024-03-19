from draw import Draw
from compressions.one_d_one_vector import OneDOneVector



def verify():
    S = [0, 8, 1, 18]
    d = 4

    oneDOneVector = OneDOneVector(S, d)
    oneDOneVector.brute_force() # 保證會對

    oneDOneVector_test = OneDOneVector(S, d)
    oneDOneVector_test.DFS() # 要驗證的方法

    pass

def run():
    S = [34, 2, 5]
    d = 4

    oneDOneVector = OneDOneVector(S, d)
    oneDOneVector.brute_force_v2()
    # oneDOneVector.show()

def test():
    S = [34, 83, 0, 72, 94, 58]
    d = 7

    oneDOneVector_1 = OneDOneVector(S, d)
    oneDOneVector_1.brute_force()
    oneDOneVector_1.show()

    oneDOneVector_2 = OneDOneVector(S, d)
    oneDOneVector_2.brute_force_v2()
    oneDOneVector_2.show()



def main():
    # verify()
    # run()
    test()

if __name__ == "__main__":
    main()
