

def is_valid(number):
    return True if (x := len(number)) > 7 and x < 10 and number[:2].isnumeric() else False
