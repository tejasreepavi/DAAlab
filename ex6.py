import streamlit as st
import pandas as pd


def matrix_chain_order(dims):
    n = len(dims) - 1

    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')

            for k in range(i, j):
                cost = (
                    m[i][k]
                    + m[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]
                )

                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


def print_optimal_parens(s, i, j):
    if i == j:
        return f"A{i}"

    k = s[i][j]
    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)

    return f"({left} × {right})"


# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="Matrix Chain Multiplication", page_icon="📊")

st.title("📊 Matrix Chain Multiplication using Dynamic Programming")

st.write("Enter matrix dimensions separated by commas.")

user_input = st.text_input(
    "Dimensions",
    "10,30,5,60,10"
)

if st.button("Calculate"):

    try:
        dims = [int(x.strip()) for x in user_input.split(",")]

        if len(dims) < 2:
            st.error("Please enter at least two dimensions.")
        else:
            n = len(dims) - 1

            st.subheader("Matrix Dimensions")

            for i in range(n):
                st.write(f"A{i+1}: {dims[i]} × {dims[i+1]}")

            m, s = matrix_chain_order(dims)

            st.success("Computation Completed")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Minimum Scalar Multiplications", m[1][n])

            with col2:
                st.metric(
                    "Optimal Parenthesization",
                    print_optimal_parens(s, 1, n)
                )

            st.subheader("DP Cost Table")

            table = []

            for i in range(1, n + 1):
                row = []
                for j in range(1, n + 1):
                    if j < i:
                        row.append("----")
                    else:
                        row.append(m[i][j])
                table.append(row)

            df = pd.DataFrame(
                table,
                index=[f"A{i}" for i in range(1, n + 1)],
                columns=[f"A{i}" for i in range(1, n + 1)]
            )

            st.dataframe(df, use_container_width=True)

    except ValueError:
        st.error("Please enter valid integers separated by commas.")
