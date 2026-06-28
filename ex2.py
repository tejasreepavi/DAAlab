import time
import random
import string
import streamlit as st

def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    return matches, comparisons

def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    matches, comparisons = [], 0
    i = j = 0
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1; j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches, comparisons

def rabin_karp(text, pattern, q=101):
    n, m = len(text), len(pattern)

    d = 256
    h = pow(d, m - 1, q)
    p_hash = t_hash = 0
    matches, comparisons = [], 0
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
    for s in range(n - m + 1):
        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)
        if s < n - m:
            t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q
            if t_hash < 0:
                t_hash += q
    return matches, comparisons


# --- Main Execution ---
st.title("String Matching Algorithms")

text = st.text_input(
    "Enter the Text",
    value="AABAACAADAABAABA"
)

pattern = st.text_input(
    "Enter the Pattern",
    value="AABA"
)

if st.button("Search"):

    st.subheader("Results")

    m1, c1 = naive_search(text, pattern)
    m2, c2 = kmp_search(text, pattern)
    m3, c3 = rabin_karp(text, pattern)

    st.write(f"Text : {text}")
    st.write(f"Pattern : {pattern}")

    st.success(f"Naive Search -> Matches: {m1}, Comparisons: {c1}")
    st.success(f"KMP Search -> Matches: {m2}, Comparisons: {c2}")
    st.success(f"Rabin-Karp -> Matches: {m3}, Comparisons: {c3}")

    st.subheader("Performance Comparison")

    text_large = ''.join(random.choices('ABCD', k=10000))
    patterns = ['AB', 'ABCD', 'ABCDAB', 'ABCDABCD']

    data = []

    for p in patterns:

        _, c1 = naive_search(text_large, p)
        _, c2 = kmp_search(text_large, p)
        _, c3 = rabin_karp(text_large, p)

        data.append({
            "Pattern": p,
            "Naive": c1,
            "KMP": c2,
            "Rabin-Karp": c3
        })

    st.table(data)