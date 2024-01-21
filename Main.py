
from secret_sharing import ShamirSecretSharing


if __name__ == '__main__':
    s = ShamirSecretSharing()
    shares = s.create_shares(secret=1337, n=20, threshold=8)
    print("Shares: " + str(shares))
    print("Reconstructed secret: " + str(s.reconstruct_secret(shares, threshold=8)))

