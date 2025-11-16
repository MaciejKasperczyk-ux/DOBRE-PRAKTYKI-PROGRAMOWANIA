import re  

def is_palindrome(text: str) -> bool:
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n nie ujemne")

    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def count_vowels(text: str) -> int:
    vowels = "aeiouAEIOUYąęóĄĘÓ"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count


def calculate_discount(price: float, discount: float) -> float:
    if not 0 <= discount <= 1:
        raise ValueError("Invalid discount")
    return price * (1 - discount)


def flatten_list(nested_list: list) -> list:
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def word_frequencies(text: str) -> dict:
    cleaned = re.sub(r"[^a-zA-ZąęćłńóśźżĄĘĆŁŃÓŚŹŻ ]", "", text.lower())
    words = cleaned.split()
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
