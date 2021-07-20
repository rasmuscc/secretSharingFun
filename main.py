import random
import numpy as np

# Mersenne prime
FIELD_MOD = (2 ** 61) - 1

def getSecret(coefs):
    return polyEval(0, coefs)

def findInverse(x):
    return pow(x, -1, FIELD_MOD)

def reconstructSecret(shares):
    numberOfShares = len(shares)
    # Create the reconstruction vector
    recVector = []
    for i in range(1, numberOfShares + 1):
        inverse = -1
        numerator = 1
        for j in range(1, numberOfShares + 1):
            if (j != i):
                inverse *= ((-i) * (-j))
                numerator *= (-j)
        inverse = findInverse(inverse)
        recVector.append((numerator * inverse) % FIELD_MOD)
    print("rec" + str(recVector))
    print("shares" + str(shares))

    dotp = (np.array(recVector) @ np.array([x[1] for x in shares]))
    print(str(dotp))
    print(dotp % FIELD_MOD)
    return (np.array(recVector) @ np.array(shares)) % FIELD_MOD

def polyEval(x, coefs):
    coefs.reverse()
    y = 0
    for c in range(0, len(coefs)):
        y += coefs[c] * x ** c
    return y % FIELD_MOD

def createShares(secret, n, treshold):
    # If the number of shares is less than t then we can not
    # reconstruct the poly.
    # If the secret is larger than the size of the field
    # we report error.
    if (n < treshold or secret >= FIELD_MOD):
        raise Exception

    # Get a random polynomial of degree treshold - 1
    coefs = getRandomPoly(treshold, secret)
    print("Poly coefficients: " + str(coefs))

    # Get n shares, i.e. n points on the polynomial
    # Notice that x = 0 is a very very bad choice
    # (this is the secret)
    shares = list()
    for x in range(1, n + 1):
        shares.append((x, polyEval(x, coefs)))

    return shares

def getRandomPoly(treshold, secret):
    coefs = random.SystemRandom().sample(range(0, FIELD_MOD), treshold - 1)
    coefs.append(secret)
    return coefs

if __name__ == '__main__':
    #print("Shares: " + str(createShares(42, 3, 3)))

    shares = createShares(1337, 2, 2)
    print("Shares: " + str(shares))
    print("Reconstructed poly " + str(reconstructSecret(shares)))