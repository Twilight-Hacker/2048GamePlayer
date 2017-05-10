import GameManager
import winsound


def main(numb):
    marks = 0
    mark = 0
    for i in xrange(numb):
        marks = marks + GameManager.main()
        mark = mark +1
    
    result = marks / mark
    return result



totals = []
b = main(25) 
totals.append(b)

print totals
winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

# [245, 336, 322, 132, 59, 18, 15]