import random
import numpy as np

# Mersenne prime
FIELD_MOD = (2 ** 61) - 1

def getSecret(coefs):
    return polyEval(0, coefs)

def findInverse(x):
    return pow(x, -1, FIELD_MOD)

def getReconstructionVector(shares):
    result = dict()

    # For each share's x-value create a reconstruction value
    for share in shares:
        # Create the product of all except the share
        numerator = 1
        denominator = 1
        for x in shares:
            if (x[0] != share[0]):
                numerator *= (-x[0])
                denominator *= (share[0] - x[0])

        # Find the inverse of the denominator to do
        # division (since we work in a field)
        inverse = findInverse(denominator)

        # Multiply the inverse with the numerator
        # to get the reconstruction value.
        result[share[0]] = (numerator * inverse) % FIELD_MOD

    return result


def reconstructSecret(shares):
    # Create the reconstruction vector
    reconstructionValuesMap = getReconstructionVector(shares)

    secret = 0
    # Multiply the reconstruction values with
    # the corresponding share values.
    # Using more shares than the threshold value does
    # not corrupt the result, but worsens performance.
    for share in shares:
        secret += share[1] * reconstructionValuesMap[share[0]]

    return secret % FIELD_MOD

# IS WAAAAY TOO SLOW
def polyEval(x, coefs):

    y = coefs[0] # Add the constant term
    coefs.reverse()
    for c in range(1, len(coefs)):
        y += coefs[c] * (x ** c)
    # This is crap, use horner's.
    coefs.reverse()
    return y % FIELD_MOD

''' Hornser's method for poly eval '''
def horner(x, coefs):
    n = len(coefs)
    result = coefs[0]

    for i in range(1, n):
        result = result * x + coefs[i]

    return result % FIELD_MOD

def createShares(secret, n, threshold):
    # If the number of shares is less than t then
    # we can not reconstruct the poly.
    if (n < threshold):
        print("Error: The number of shares, n, is smaller than the threshold.")
        raise Exception

    # The secret can not be larger than the size of the field.
    if (secret >= FIELD_MOD):
        print("Error: The secret can not be larger than the size of the field.")
        raise Exception

    # Get a random polynomial of degree treshold - 1
    coefs = getRandomPoly(threshold, secret)

    # Get n shares, i.e. n points on the polynomial
    # Notice that x = 0 is a very very bad choice
    # (this is the secret)
    shares = list()
    for x in range(1, n + 1):
        shares.append((x, horner(x, coefs)))

    return shares

def getRandomPoly(treshold, secret):
    coefs = random.SystemRandom().sample(range(0, FIELD_MOD), treshold - 1)
    coefs.append(secret)
    print("Polynomial coefficients: " + str(coefs))
    return coefs

if __name__ == '__main__':
    print("Creating 2 shares for secret '1337' with threshold value 2...")
    shares = createShares(1337, 2000, 2000)
    print("Shares: " + str(shares))
    print("Reconstructing secret from shares...")
    print("Reconstructed secret: " + str(reconstructSecret(shares)))