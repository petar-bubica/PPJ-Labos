class Stog:
    def __init__(self):
        self.stog = []
    def push(self,element):
        self.stog.append(element)
    def pop(self):
        return self.stog.pop()
    def prazanStog(self):
        if stog == []:
            return True
        else:
            return False
    def peek(self):
        if self.prazanStog() == False:
            return self.stog[-1]
    def velicina(self):
        return len(self.stog)


