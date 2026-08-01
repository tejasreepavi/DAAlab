import streamlit as st


def is_safe(board, row, col):
    for prev_row in range(row):
        placed = board[prev_row]

        if placed == col:
            return False

        if abs(prev_row - row) == abs(placed - col):
            return False

    return True


def solve_n_queens(n):
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1
                backtrack_count[0] += 1

    backtrack(0)
    return solutions, backtrack_count[0]


def board_string(solution, n):
    text = ""
    text += "+" + "---+" * n + "\n"

    for row in range(n):
        text += "|"
        for col in range(n):
            if solution[row] == col:
                text += " Q |"
            else:
                text += " . |"
        text += "\n"
        text += "+" + "---+" * n + "\n"

    return text


# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="N-Queens", page_icon="♛")

st.title("♛ N-Queens Problem using Backtracking")

n = st.selectbox("Select Number of Queens", [4, 6, 8])

if st.button("Solve"):

    solutions, backtracks = solve_n_queens(n)

    st.success("Completed Successfully")

    st.metric("Number of Solutions", len(solutions))
    st.metric("Backtracks", backtracks)

    if n == 4:
        st.subheader("All Solutions")

        for i, sol in enumerate(solutions, 1):
            st.write(f"### Solution {i}")
            st.code(board_string(sol, n), language="text")