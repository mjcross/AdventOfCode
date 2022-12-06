def over200(x):
    return x > 200

seq = (199, 200, 208, 210, 200, 207, 240, 269, 260, 263)

print(len(filter(over200, seq)))