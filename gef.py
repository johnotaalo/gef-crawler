f = open("./demofile.txt", "r")
lines = f.read().split('\r\n')
print(list(lines))