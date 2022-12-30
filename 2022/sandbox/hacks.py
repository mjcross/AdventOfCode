items = list(range(5))
length = len(items)

for shift in range(-10, 11):
    if shift < 0:
        alt_shift = (shift - 1) % length
        print(f'insert left of {shift} equals insert right of {alt_shift}')

    if shift > 0:
        alt_shift = (shift + 1) % -length
        print(f'insert right of {shift} equals insert left of {alt_shift}')

    if shift == 0:
        print('shift of zero ')
