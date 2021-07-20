An implementation of Shamir Secret Sharing.
https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing

The implementation uses field arithmetic, but avoids implementing polynomial arithmetic over a field. This is done by not fully reconstructing the polynomial, only the secret.

Dependencies:
Python 3.8 or higher (For using Python's pow() to find the modular multiplicative inverse)
