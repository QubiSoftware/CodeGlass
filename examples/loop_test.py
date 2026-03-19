def sum_positive_numbers(limit: int) -> int:
    """
    Basit bir döngü örneği.
    CodeGlass için temiz bir akış:
        - total başlat
        - for i in range(limit)
            - IF (i > 1)
                - total += 2
        - sonucu döndür
    """
    total = 0

    for i in range(limit):
        if i > 0:
            total += i

    return total


if __name__ == "__main__":
    print(sum_positive_numbers(5))
    print(sum_positive_numbers(10))
