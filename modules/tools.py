def vig_matrix():
    abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n = len(abecedario)

    vig_matrix = []
    for i in range(n):
        row = abecedario[i:] + abecedario[:i]
        vig_matrix.append(row)
    return vig_matrix
