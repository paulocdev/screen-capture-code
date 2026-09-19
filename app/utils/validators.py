def validate_danfe_key(key: str) -> bool:
    """
    Valida se uma chave de 44 dígitos da NF-e/NFC-e é matematicamente válida
    usando o cálculo do Dígito Verificador (Módulo 11).
    """
    if len(key) != 44 or not key.isdigit():
        return False

    # Os 43 primeiros dígitos
    base_digits = [int(d) for d in key[:43]]
    dv_original = int(key[43])

    # Pesos de 2 a 9 da direita para a esquerda
    weights = [2, 3, 4, 5, 6, 7, 8, 9]
    total_sum = 0

    for i, digit in enumerate(reversed(base_digits)):
        weight = weights[i % len(weights)]
        total_sum += digit * weight

    remainder = total_sum % 11
    expected_dv = 0 if remainder in (0, 1) else (11 - remainder)

    return expected_dv == dv_original