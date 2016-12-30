# coding:utf-8

class A_Class(object):
    
    def method(self):
        self.__method()
        
    def _method(self):
        print "_method called from A"
    
    def __method(self):
        print "__method called from A"
        
    getMethod = property(_method)
        
class B_Class(A_Class):
    
    def _method(self):
        print "_method called from B"
    
    def __method(self):
        print "__method called from B"
        
    



tempA = A_Class()
tempA._method()
tempA.getMethod

tempB = B_Class()
#tempB.method()
tempB._method()
tempB.getMethod



    