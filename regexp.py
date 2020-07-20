def calculate(data, findall):
    matches = findall(r'([a-c])([+-])?=([a-c])?([+-]?\d+)?')
    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        # Если бы могло быть только =, вообще одной строкой все считалось бы, вот так:
        val =  data.get(v2, 0) + int(n or 0)
        if s:
            if s == "+":
                data[v1] += val
            elif s == "-":
                data[v1] -= val
        else:
            data[v1] = val


    return data
if __name__ =="__main__":
    pass
