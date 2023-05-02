
class Cat:
    def __init__(self) -> None:
        self.x = 10
def Func(cat):
    cat.x += 1
    return cat

if __name__ == "__main__":
    cat = Cat()
    
    Func(cat)
    
    print(cat.x)