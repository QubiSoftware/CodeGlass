def check_value(x: int) -> None:
    """
    Basit bir IF örneği.
    CodeGlass için temiz bir akış:
        - multiplier ata
        - result hesapla
        - IF (result > 10)
            - True: "Value is high"
            - False: "Value is low or equal"
    """
    multiplier = 2
    result = x * multiplier

    if result > 10:
        print("Value is high")
    else:
        print("Value is low or equal")


if __name__ == "__main__":
    check_value(3)
    check_value(10)
