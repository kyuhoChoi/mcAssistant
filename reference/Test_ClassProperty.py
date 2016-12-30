class TestClass(object):
    A = []
    def __init__(self):
        self.B = 2
        




temp = TestClass()
temp.A.append(1)

TestClass.A.append(2)

print TestClass().A


temp2 = TestClass()
temp2.A.append(3)
print TestClass().A