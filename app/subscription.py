import streamlit as st
from database import get_subscription_details, update_subscription_type


def show_subscription_page():
    # Sayfa başlığı
    st.title("Manage Subscription")

    # Kullanıcı giriş kontrolü
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("You need to log in to manage your subscription.")
        if st.button("Go to Login"):
            st.session_state["current_page"] = "login"
        return

    # Kullanıcının abonelik bilgilerini kontrol ve yükleme
    if "subscription_details" not in st.session_state:
        subscription = get_subscription_details(user_id)
        if not subscription:
            st.error("No subscription found for your account.")
            if st.button("Back to Homepage"):
                st.session_state["current_page"] = "home"
            return
        st.session_state["subscription_details"] = subscription

    # Mevcut abonelik bilgilerini göster
    subscription = st.session_state["subscription_details"]
    st.subheader("Your Subscription Details")
    st.write(f"**Subscription Type:** {subscription['subscription_type']}")
    st.write(f"**Start Date:** {subscription['start_date']}")
    st.write(f"**End Date:** {subscription['end_date']}")

    # Kullanıcının seçili türünü saklama
    if "selected_subscription_type" not in st.session_state:
        st.session_state["selected_subscription_type"] = subscription["subscription_type"]

    # Abonelik türü seçimi
    new_type = st.selectbox(
        "Choose a new subscription type:",
        ["Free", "Family", "Premium"],
        index=["Free", "Family", "Premium"].index(st.session_state["selected_subscription_type"]),
        key="selected_subscription_type"
    )

    # Güncelleme işlemi
    if st.button("Update Subscription"):
        if new_type == subscription["subscription_type"]:
            st.warning("You have selected the current subscription type.")
        else:
            success = update_subscription_type(subscription["subscription_id"], new_type)
            if success:
                st.success("Subscription type updated successfully!")
                st.session_state["subscription_details"]["subscription_type"] = new_type
            else:
                st.error("An error occurred while updating your subscription.")

    # Ana sayfaya geri dönme
    if st.button("Back to Homepage"):
        st.session_state["current_page"] = "home"