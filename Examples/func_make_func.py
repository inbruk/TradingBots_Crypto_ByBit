

def always(n):
    def F():
        return n
    return F

five = always(5)
print(five())