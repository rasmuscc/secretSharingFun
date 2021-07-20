import random
import cProfile

# Mersenne prime
FIELD_MOD = (2 ** 61) - 1

def findInverse(x):
    return pow(x, -1, FIELD_MOD)

def fastMod(x):
    return (x & FIELD_MOD) + (x >> 61)

def getReconstructionValues(shares, threshold):
    result = dict()

    # Use only threshold number of shares since this is all we need
    tShares = shares[0:threshold]

    # For each shares create a reconstruction value
    for share in tShares:
        numerator = 1
        denominator = 1
        # Todo: Optimize by using sum/product identities
        # Todo: can numerator be written as n!/share?
        for x in tShares:
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


def reconstructSecret(shares, threshold = -1):
    # If no threshold is given we just try to use all shares
    # Using more shares than the threshold value does
    # not make the result incorrect, but worsens performance.
    if (threshold == -1):
        threshold = len(shares)

    # Create the reconstruction vector
    reconstructionValuesMap = getReconstructionValues(shares, threshold)

    secret = 0
    # Multiply the reconstruction values with
    # the corresponding share values.
    for i in range(0, threshold):
        secret += shares[i][1] * reconstructionValuesMap[shares[i][0]]

    return secret % FIELD_MOD

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

    # The threshold must be larger than 1 for SSH to work
    if (1 >= threshold):
        print("Error: The threshold must be larger than 1.")
        raise Exception

    # The secret must be a value in the field
    if (secret < 0 or secret >= FIELD_MOD):
        print("Error: The secret must be a value in the field.")
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
    return coefs

if __name__ == '__main__':
    shares = createShares(secret=1337, n=20, threshold=8)
    print("Reconstructed secret: " + str(reconstructSecret(shares, threshold=8)))

