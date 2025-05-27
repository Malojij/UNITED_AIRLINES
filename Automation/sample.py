import random
import string

from self import self

# Ensure at least 1 digit and the rest randomly sampled
digit = random.choice(string.digits)  # Guarantees at least one digit
others = random.choices(string.ascii_uppercase, k=5)

# Combine and shuffle to make digit position random
combined = list(digit + ''.join(others))
random.shuffle(combined)

self.RandomNumberForPNR = ''.join(combined)


print(f"{self.RandomNumberForPNR}")