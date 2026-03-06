def validate_length(value, min_length, max_length):
    try:
        number = int(value)
        return min_length <= number <= max_length
    except ValueError:
        return False
