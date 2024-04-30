import streamlit as st


def main():
    st.title('Hello World!')

    if st.button('Say hello'):
        st.write('Why hello there')


if __name__ == '__main__':
    main()
    