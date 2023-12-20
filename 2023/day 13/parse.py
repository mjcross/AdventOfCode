from dataclasses import dataclass

@dataclass
class Puzzle:
    rows: list[int]

    def __post_init__(self):
        self.nRows = len(self.rows)
        self.nCols = len(self.rows[0])

        self.cols = []
        for i in range(self.nCols):
            col = ''
            for row in self.rows:
                col += row[i]
            self.cols.append(col)

    def __str__(self):
        return '\n'.join(self.rows)


def parse(stream):
    puzzles = []

    rows = []
    for rawline in stream:
        line = rawline.strip()
        if line:
            rows.append(line)
        else:
            puzzles.append(Puzzle(rows))
            rows = []
    puzzles.append(Puzzle(rows))
    
    return puzzles
