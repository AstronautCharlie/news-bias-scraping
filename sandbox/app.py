import argparse

class App:
    def run(self):
        class foo: 
            def __init__(self): 
                self._bar = 'bar'
            
            @property
            def bar(self): 
                return self._bar

        f = foo()
        print(f.bar) 