def main():
    calTotals = []
    with open('input.txt', 'r') as file:
        elfCals = 0
        for line in file:
            record = line.rstrip()
            if record:
                elfCals += int(record)
            else:
                calTotals.append(elfCals)
                elfCals = 0
        nCals = 0
    if record:
        # no blank line after last elf 
        calTotals.append(elfCals)
        elfCals = 0

    calTotals.sort(reverse=True)

    print(len(calTotals), 'elves')
    print('top elf', calTotals[0])
    print('sum of top three', sum(calTotals[:3]))

if __name__ == "__main__":
    main()