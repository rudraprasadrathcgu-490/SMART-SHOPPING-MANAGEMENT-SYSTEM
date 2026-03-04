import streamlit as st
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SmartCart - Shopping System", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.title {
    font-size:40px;
    font-weight:700;
    color:white;
    text-align:center;
    padding:20px;
    border-radius:15px;
    background: linear-gradient(90deg,#4e73df,#1cc88a);
}
.card {
    padding:18px;
    border-radius:12px;
    background:white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom:20px;
    text-align:center;
}
.metric-card {
    background: linear-gradient(90deg,#36b9cc,#4e73df);
    padding:18px;
    border-radius:12px;
    color:white;
    text-align:center;
    font-size:20px;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD IMAGES ----------------
laptop_img = Image.open("images/laptop.jpg")
phone_img = Image.open("images/phone.jpg")
mouse_img = Image.open("images/mouse.jpg")
keyboard_img = Image.open("images/keyboard.jpg")

# ---------------- SESSION STATE ----------------
if "products" not in st.session_state:
    st.session_state.products = [
        {"id": 1, "name": "Laptop", "price": 50000, "stock": 5, "image": laptop_img},
        {"id": 2, "name": "Phone", "price": 20000, "stock": 10, "image": phone_img},
        {"id": 3, "name": "Mouse", "price": 1500, "stock": 15, "image": mouse_img},
        {"id": 4, "name": "Keyboard", "price": 2500, "stock": 8, "image": keyboard_img},
    ]

if "cart" not in st.session_state:
    st.session_state.cart = []

if "revenue" not in st.session_state:
    st.session_state.revenue = 0

if "role" not in st.session_state:
    st.session_state.role = None

# ---------------- HEADER ----------------
st.markdown('<div class="title">🛒 SmartCart - College Shopping Management System</div>', unsafe_allow_html=True)
st.write("")

# ---------------- ROLE SELECTION ----------------
if st.session_state.role is None:

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state.role = "Admin"
            st.rerun()

    with col2:
        if st.button("🛍 Customer Login", use_container_width=True):
            st.session_state.role = "Customer"
            st.rerun()

# ---------------- ADMIN PANEL ----------------
elif st.session_state.role == "Admin":

    st.sidebar.title("Admin Panel")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if username == "admin" and password == "admin":

        menu = st.sidebar.radio("Menu", ["Dashboard", "Logout"])

        if menu == "Dashboard":

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f'<div class="metric-card">Total Revenue<br>₹ {st.session_state.revenue}</div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f'<div class="metric-card">Total Products<br>{len(st.session_state.products)}</div>', unsafe_allow_html=True)

            st.subheader("Product Inventory")
            st.table(st.session_state.products)

        elif menu == "Logout":
            st.session_state.role = None
            st.rerun()

    else:
        st.sidebar.warning("Use Username: admin | Password: admin")

# ---------------- CUSTOMER PANEL ----------------
elif st.session_state.role == "Customer":

    st.sidebar.title("Customer Panel")
    name = st.sidebar.text_input("Enter Your Name")

    menu = st.sidebar.radio("Menu", ["Shop", "View Cart", "Checkout", "Logout"])

    if menu == "Shop":

        cols = st.columns(2)

        for index, p in enumerate(st.session_state.products):
            with cols[index % 2]:

                st.image(p["image"], width="stretch")

                st.markdown(f"""
                <div class="card">
                    <h3>{p['name']}</h3>
                    <p><b>Price:</b> ₹ {p['price']}</p>
                    <p><b>Stock:</b> {p['stock']}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Add to Cart - {p['name']}", key=p["id"]):
                    if p["stock"] > 0:
                        st.session_state.cart.append(p)
                        p["stock"] -= 1
                        st.success("Added to Cart")
                    else:
                        st.error("Out of Stock")

    elif menu == "View Cart":

        if st.session_state.cart:
            st.table(st.session_state.cart)
            total = sum(item["price"] for item in st.session_state.cart)
            st.markdown(f'<div class="metric-card">Cart Total: ₹ {total}</div>', unsafe_allow_html=True)
        else:
            st.info("Cart is Empty")

    elif menu == "Checkout":

        if st.session_state.cart:
            total = sum(item["price"] for item in st.session_state.cart)

            if st.checkbox("Apply 10% Discount"):
                total *= 0.9
                st.success("Discount Applied")

            st.markdown(f'<div class="metric-card">Final Amount: ₹ {total}</div>', unsafe_allow_html=True)

            if st.button("Confirm Order"):
                st.session_state.revenue += total
                st.session_state.cart = []
                st.success("Order Placed Successfully")
        else:
            st.warning("Cart is Empty")

    elif menu == "Logout":
        st.session_state.role = None
        st.session_state.cart = []
        st.rerun()