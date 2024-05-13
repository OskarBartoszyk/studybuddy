import time 

timer_time = 0

def addfive():
    global timer_time
    timer_time += 5

def subfive():
    global timer_time
    timer_time -= 5

def countdown():
    global timer_time
    calc = timer_time * 60
    while calc > 0:
        print(calc)
        time.sleep(1)
        calc -= 1
    print("Time's up!")

