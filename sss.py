import random
import cProfile

class SSS:

    '''
        The constructor takes a prime as input
        which is used to define the field that the
        Shamir Secret Sharing is to use.
    '''
    def __init__(self, FIELD_MOD = (2 ** 61) - 1):
        # Mersenne prime (Required for fast mod)
        self.FIELD_MOD = FIELD_MOD


    '''
        Returns the field inverse of x.
        This method requires python 3.8 or higher.
    '''
    @staticmethod
    def findInverse(self, x):
        return pow(x, -1, self.FIELD_MOD)


    '''
        Returns x mod FIELD_MOD.
        This only works if FIELD_MOD is a Mersenne prime.
    '''
    def fastMod(self, x):
        # Bit magic exploiting the use of Mersenne primes
        return (x & self.FIELD_MOD) + (x >> 61)


    '''
        Returns a map from each shares x-coordinate to its
        reconstruction value. I.e. for each share (x_i, y_i)
        we create a function r_i which is 1 when x=x_i and 0 otherwise.
        The reconstruction values are then r_0(0),r_1(0)...r_threshold(0)
    '''
    def getReconstructionValues(self, shares, threshold):
        result = dict()

        # Use only threshold number of shares since this is all we need
        tShares = shares[0:threshold]

        # For each shares create a reconstruction value
        for share in tShares:
            numerator = 1
            denominator = 1
            # Todo: Optimize by using sum/product identities?
            # Todo: can numerator be written as n!/share or something similiar?
            for x in tShares:
                if (x[0] != share[0]):
                    numerator *= (-x[0])
                    denominator *= (share[0] - x[0])

            # Find the inverse of the denominator to do
            # division (since we work in a field)
            inverse = self.findInverse(self, denominator)

            # Multiply the inverse with the numerator
            # to get the reconstruction value.
            result[share[0]] = (numerator * inverse) % self.FIELD_MOD

        return result


    '''
        Reconstructs the secret given enough shares.
        If no threshold value is given then lagrange interpolation
        is done using all the shares.
    '''
    def reconstructSecret(self, shares, threshold = -1):
        # If no threshold is given we just try to use all shares
        # Using more shares than the threshold value does
        # not make the result incorrect, but worsens performance.
        if (threshold == -1):
            threshold = len(shares)

        # Create the reconstruction vector
        reconstructionValuesMap = self.getReconstructionValues(shares, threshold)

        secret = 0
        # Multiply the reconstruction values with
        # the corresponding share values.
        for i in range(0, threshold):
            secret += shares[i][1] * reconstructionValuesMap[shares[i][0]]

        return secret % self.FIELD_MOD


    '''
        Horner's method for fast polynomial evaluation.
        Returns the function value at x for the polynomial
        defined by the coefs parameter.
    '''
    def horner(self, x, coefs):
        n = len(coefs)
        result = coefs[0]

        for i in range(1, n):
            result = result * x + coefs[i]

        return result % self.FIELD_MOD


    '''
        Validates that the input given to createShares.
        Raises and Exception if the input is invalid.
    '''
    def validateInput(self, secret, n, threshold):
        # If the number of shares is less than t then
        # we can not reconstruct the poly.
        if (n < threshold):
            print("Error: The number of shares, n, is smaller than the threshold.")
            raise Exception

        # The threshold must be larger than 1 for SSS to work
        if (1 >= threshold):
            print("Error: The threshold must be larger than 1.")
            raise Exception

        # The secret must be a value in the field
        if (secret < 0 or secret >= self.FIELD_MOD):
            print("Error: The secret must be a value in the field.")
            raise Exception


    '''
        Create n shamir secret shares for a given secret
        and a given threshold.
    '''
    def createShares(self, secret, n, threshold):
        self.validateInput(secret, n, threshold)

        # Get a random polynomial of degree treshold - 1
        coefs = self.getRandomPoly(threshold, secret)

        # Get n shares, i.e. n points on the polynomial
        # Notice that x = 0 is a very very bad choice
        # (this is the secret)
        shares = list()
        for x in range(1, n + 1):
            shares.append((x, self.horner(x, coefs)))

        return shares


    '''
        Returns a random polynomial over a field.
        The polynomial is represented as a list of coefficients.
        The coefficients are ordered such that the highest
        degree term's coefficient is first in the list and so on...
    '''
    def getRandomPoly(self, treshold, secret):
        coefs = random.SystemRandom().sample(range(0, self.FIELD_MOD), treshold - 1)
        coefs.append(secret)
        return coefs
