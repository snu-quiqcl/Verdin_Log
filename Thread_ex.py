# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:06:54 2023

@author: alexi
"""
from threading import Thread, Event, Lock
import time, datetime

class A:
    def __init__(self,id_ = 0):
        self.id_ = id_
        self.event = Event()
        self.event.set()
        self.thread = Thread(target=self.foo, daemon = True)
        
    def foo(self):
        while True:
            self.event.wait()
            print(self.id_)
            time.sleep(0.1)
            
    def goo(self):
        self.event.clear()
        for i in range(10):
            print('goo')
            time.sleep(0.5)
        self.event.set()
    
    def lock(self):
        self.event.clear()
    
    def realease(self):
        self.event.set()
        
    def func(self):
        self.thread.start()
        self.goo()
        
class B:
    def __init__(self, id_ = 0):
        self.count = 0
        self.lock = Lock()
        self.thread = Thread(target=self.foo, daemon = True)
        self.id_ = id_
        
    def foo(self,val = 0):
        for i in range(30):
            with self.lock:
                print(val)
                time.sleep(0.1)
            
    def goo(self):
        with self.lock:
            for i in range(10):
                print('goo')
                time.sleep(0.5)
            self.foo(val= 20)
    
    def lock(self):
        self.event.clear()
    
    def realease(self):
        self.event.set()
        
    def func(self):
        self.thread.start()
        self.goo()
        
        
if __name__ == '__main__':
    b1 = B(1)
    b1.func()