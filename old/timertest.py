import threading

def hello(str):
    print "hello " + str

t = threading.Timer(6.0, hello, ["dude"])
t.start()

msg = raw_input("sup: ")
print "cancell'd!"
t.cancel()

# note: having thread return AFTER shell prompt has returned (>>>) causes crash
