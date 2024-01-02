from fractions import Fraction

def lagrangeInterpolate(points, x):
    """Fits a polynomial curve to the given points and evaluates it at the
    given X ordinate, returning the Y value as an exact fraction if possible.
    See https://en.wikipedia.org/wiki/Lagrange_polynomial#Barycentric_form for
    the formulas used.
    """
    
    X = [point[0] for point in points]
    Y = [point[1] for point in points]

    # avoid division by zero
    if x in X:
        return Y[X.index(x)]

    # calculate barycentric weights from x ordinates
    W = []
    for x_j in X:
        weight = Fraction(1, 1)
        for x_m in X:
            if x_m != x_j:
                weight *= Fraction(1, x_j - x_m)
        W.append(weight)    
    
    # evaluate Lagrange interpolating polynomial
    numerator = sum([Fraction(w_j, x - x_j) * y_j for w_j, x_j, y_j in zip(W, X, Y)])
    denominator = sum([Fraction(w_j, x - x_j) for w_j, x_j, y_j in zip(W, X, Y)])

    return numerator / denominator

def main():
    # basic tests
    points = [
        (65, 3_725),
        (196, 32_896),
        (327, 91_055),
        (458, 178_202)
    ]
    print(lagrangeInterpolate(points, 26_501_365))


if __name__ == '__main__':
    main()