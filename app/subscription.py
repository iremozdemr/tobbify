import streamlit as st
from database import UserSubscription

def show_subscription_page():
    # sayfa başlığı
    st.title("manage profile")

    # kullanıcı giriş kontrolü
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("you need to log in to manage your subscription.")
        if st.button("go to login"):
            st.session_state["current_page"] = "login"
        return
    
    st.subheader("username")
    st.write(f"{st.session_state['username']}")

    # kullanıcının abonelik bilgilerini kontrol ve yükleme
    if "subscription_details" not in st.session_state:
        subscription = UserSubscription.get_subscription_details(user_id)
        if not subscription:
            st.error("no subscription found for your account.")
            if st.button("back to homepage"):
                st.session_state["current_page"] = "home"
            return
        st.session_state["subscription_details"] = subscription  # Başlat

    # mevcut abonelik bilgilerini al
    subscription = st.session_state["subscription_details"]
    st.subheader("subscription details")
    st.write(f"**subscription type:** {subscription['subscription_type']}")
    st.write(f"**start date:** {subscription['start_date']}")
    st.write(f"**end date:** {subscription['end_date']}")

    # kullanıcının seçili türünü saklama
    if "selected_subscription_type" not in st.session_state:
        st.session_state["selected_subscription_type"] = subscription["subscription_type"]

    # abonelik türü seçimi
    new_type = st.selectbox(
        "choose a new subscription type:",
        ["Free", "Family", "Premium"],
        index=["Free", "Family", "Premium"].index(st.session_state["selected_subscription_type"]),
        key="selected_subscription_type"
    )

    # güncelleme işlemi
    if st.button("update subscription"):
        if new_type == subscription["subscription_type"]:
            st.warning("you have selected the current subscription type.")
        else:
            success = UserSubscription.update_subscription_type(subscription["subscription_id"], new_type)
            if success:
                st.success("subscription type updated successfully!")
                st.session_state["subscription_details"]["subscription_type"] = new_type  # Güncelle
            else:
                st.error("an error occurred while updating your subscription.")

    # ana sayfaya geri dönme
    if st.button("back to homepage"):
        st.session_state["current_page"] = "home"