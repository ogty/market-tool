constant_variable = 0

def to():
    return constant_variable
    
def update() -> int:
    global constant_variable

    constant_variable = 100

    return constant_variable