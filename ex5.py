import streamlit as st
import random
import pandas as pd

comparison_count = 0


def min_max_dc(arr, low, high):
    global comparison_count

    if low == high:
        return arr[low], arr[low]

    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    mid = (low + high) // 2
    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin

    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def min_max_naive(arr):
    mn, mx = arr[0], arr[0]
    comps = 0

    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x

        comps += 1
        if x > mx:
            mx = x

    return mn, mx, comps


# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="Min-Max Divide & Conquer", page_icon="📊")

st.title("📊 Min-Max using Divide and Conquer")

st.write("Enter numbers separated by commas.")

user_input = st.text_input(
    "Array",
    "3,1,7,4,9,2,8,5,6,0"
)

if st.button("Find Min & Max"):

    try:
        arr = [int(x.strip()) for x in user_input.split(",")]

        comparison_count = 0
        mn, mx = min_max_dc(arr, 0, len(arr) - 1)
        dc_comps = comparison_count

        _, _, naive_comps = min_max_naive(arr)

        st.success("Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Minimum", mn)

        with col2:
            st.metric("Maximum", mx)

        st.write("### Comparisons")
        st.write(f"**Divide & Conquer:** {dc_comps}")
        st.write(f"**Naive:** {naive_comps}")

        st.write("## Performance Analysis")

        data = []

        for size in [10, 100, 1000, 10000]:
            arr = [random.randint(1, 10000) for _ in range(size)]

            comparison_count = 0
            min_max_dc(arr, 0, len(arr) - 1)
            dc = comparison_count

            _, _, naive = min_max_naive(arr)

            formula = 3 * size // 2 - 2

            data.append([size, dc, naive, formula])

        df = pd.DataFrame(
            data,
            columns=[
                "Size",
                "DC Comparisons",
                "Naive Comparisons",
                "Formula (3n/2 - 2)"
            ]
        )

        st.dataframe(df, use_container_width=True)

    except:
        st.error("Please enter valid integers separated by commas.")
