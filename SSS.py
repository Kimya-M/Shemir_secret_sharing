import random

def calculate_F(coefficients: list, x: int, prime: int) -> int:
    result = 0
    for coefficient in coefficients:
        result = (result * x + coefficient) % prime
    return result

def generate_random_shares(secret: int, number_of_shares: int, threshold: int, prime: int) -> list:
    if number_of_shares < threshold:
        print("Number of shares MUST be greater than the threshold!")
        return None
    if prime <= number_of_shares:
        print("Number of shares MUST be smaller than the prime number!")
        return None

    coefficients = [random.randrange(1, prime) for _ in range(threshold - 1)]
    coefficients.append(secret)

    print_polynomial(coefficients, threshold)

    shares = [(x, calculate_F(coefficients, x, prime)) for x in range(1, number_of_shares + 1)]
    return shares

def print_polynomial(coefficients: list, threshold: int) -> None:
    print("The Polynomial is:")
    polynomial = " + ".join(f"({coefficients[i]} * x ^ {threshold - i - 1})" for i in range(len(coefficients)))
    print(polynomial)

def print_shares(shares: list) -> None:
    print("Shares:")
    for x, y in shares:
        print(f"({x}, {y})")


def recover(shares: list[tuple[int, int]], prime: int, threshold: int) -> int:
    if len(shares) < threshold:
        print(f"We need at least {threshold} shares to recover the secret.")
        return None

    sum = 0
    for x, y in shares:
        result = y % prime
        for j in range(len(shares)):
            if x != shares[j][0]:
                result *= (shares[j][0] * pow(shares[j][0] - x, -1, prime)) % prime
        sum += result % prime

    return sum % prime

if __name__ == "__main__":
    secret = int(input("Secret: "))
    number_of_shares = int(input("Number of shares: "))
    threshold = int(input("Threshold: "))
    prime = int(input("Prime: "))

    shares = generate_random_shares(secret, number_of_shares, threshold, prime)

    if shares:
        print_shares(shares)
        recovered_secret = recover(shares, prime, threshold)
        print(f"Recovered secret: {recovered_secret}")
