import timeit

# Алгоритм Рабіна-Карпа
def rabin_karp(text, pattern):
    d = 256  # Кількість символів у наборі (ASCII)
    q = 101  # Просте число для хешування
    m = len(pattern)
    n = len(text)
    h = 1
    p = 0  # Хеш значення для патерна
    t = 0  # Хеш значення для тексту
    result = []

    # Обчислення h = pow(d, m-1) % q
    for i in range(m - 1):
        h = (h * d) % q

    # Обчислюємо хеш для патерна і для першого вікна тексту
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Рухаємо патерн по тексту
    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                result.append(i)

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return result

# Алгоритм Кнута-Морріса-Пратта
def kmp_search(text, pattern):
    m = len(pattern)
    n = len(text)
    lps = [0] * m
    j = 0  # Індекс для патерна
    result = []

    # Препроцесинг LPS масиву
    compute_lps(pattern, m, lps)

    i = 0  # Індекс для тексту
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result

def compute_lps(pattern, m, lps):
    length = 0
    lps[0] = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

# Алгоритм Боєра-Мура
def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    result = []
    bad_char = bad_char_table(pattern)

    s = 0 
    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            result.append(s)
            s += (m - bad_char.get(text[s + m], -1) if s + m < n else 1)
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))

    return result


def bad_char_table(pattern):
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i
    return bad_char


# Параметри серій досліджень
series_parameters = [
    {"agents": 65536, "items": 131072, "sessions": 262144, "session_size": 192, "likes": 1536},
    {"agents": 131072, "items": 262144, "sessions": 524288, "session_size": 256, "likes": 2048},
    {"agents": 262144, "items": 524288, "sessions": 1048576, "session_size": 256, "likes": 2048},
    {"agents": 524288, "items": 1048576, "sessions": 2097152, "session_size": 256, "likes": 2048}
]

# Підрядки для тестування
existing_substring = "алгоритми"
non_existing_substring = "неіснуючий"

# Текст для тестування (як заміна для реальних статей)
test_text = "Методи та структури даних для реалізації бази даних рекомендаційної системи соціальної мережі. Алгоритми формування рекомендацій ..."

# Вимірювання часу
for params in series_parameters:
    print(f"\n Параметри серії: агенти={params['agents']}, предмети={params['items']}, сесії={params['sessions']}, розмір сесії={params['session_size']}, вподобання={params['likes']}")

    time_rabin_karp_exist = timeit.timeit(lambda: rabin_karp(test_text, existing_substring), number=100)
    time_rabin_karp_non_exist = timeit.timeit(lambda: rabin_karp(test_text, non_existing_substring), number=100)

    time_kmp_exist = timeit.timeit(lambda: kmp_search(test_text, existing_substring), number=100)
    time_kmp_non_exist = timeit.timeit(lambda: kmp_search(test_text, non_existing_substring), number=100)

    time_boyer_moore_exist = timeit.timeit(lambda: boyer_moore(test_text, existing_substring), number=100)
    time_boyer_moore_non_exist = timeit.timeit(lambda: boyer_moore(test_text, non_existing_substring), number=100)

    print(f"Існуючий підрядок:\n  Рабін-Карп: {time_rabin_karp_exist}\n  Кнут- Морріс-Пратт: {time_kmp_exist}\n  Боєр-Мур: {time_boyer_moore_exist}")
    print(f"Неіснуючий підрядок:\n  Рабін-Карп: {time_rabin_karp_non_exist}\n  Кнут- Морріс -Пратт: {time_kmp_non_exist}\n  Боєр-Мур: {time_boyer_moore_non_exist}")
