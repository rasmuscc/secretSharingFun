from sss import SSS

if __name__ == '__main__':
    s = SSS()
    shares = s.createShares(secret=1337, n=20, threshold=8)
    print("Shares: " + str(shares))
    print("Reconstructed secret: " + str(s.reconstructSecret(shares, threshold=8)))

