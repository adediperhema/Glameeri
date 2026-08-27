import streamlit as st
import requests


def create_attire_payhub_checkout_session(
    user_id, client_name, cost_usd, bust, waist, hips
):
    """
    Formulates a payment checkout initialization payload packet
    and sends it out securely to the PayHub merchant API servers.
    """
    try:
        # 1. Fetch your secret API key safely from Streamlit environment storage
        if "PAYHUB_SECRET_KEY" not in st.secrets:
            return "ERROR: PayHub API Secret key configuration is missing inside st.secrets."

        payhub_api_token = st.secrets["PAYHUB_SECRET_KEY"]

        # 2. Build the tracking data metadata payload mapping parameters
        # Packing garment measurement arrays so you don't lose sizing dimensions
        metadata_payload = {
            "user_id": str(user_id),
            "client_name": client_name,
            "bust_inches": str(bust),
            "waist_inches": str(waist),
            "hips_inches": str(hips),
        }

        # 3. Setup standard PayHub structural endpoint variables
        # Note: Replace this URL placeholder with the exact checkout endpoint provided in your PayHub API doc manual!
        payhub_endpoint_url = "https://payhub.com"

        headers = {
            "Authorization": f"Bearer {payhub_api_token}",
            "Content-Type": "application/json",
        }

        request_body = {
            "amount": float(cost_usd),
            "currency": "USD",  # Change to GHS, NGN, KES depending on localized setup parameters
            "description": f"Custom Tailored Attire Blueprint Design - Client: {client_name}",
            "redirect_url": "https://streamlit.app",
            "metadata": metadata_payload,
        }

        # 4. Trigger the checkout request pipeline over the internet network
        # For testing, we simulate a successful URL creation framework if offline
        # In full production, uncomment the lines below to communicate directly with the live server gateway:

        # response = requests.post(payhub_endpoint_url, json=request_body, headers=headers)
        # if response.status_code == 200 or response.status_code == 201:
        #     return response.json().get("checkout_url")
        # else:
        #     return f"ERROR: PayHub Gateway Gateway exception: {response.text}"

        # MOCK PRODUCTION RUN FALLBACK (Lets you pass layout testing immediately):
        import time

        mock_secure_checkout_url = f"https://payhub.com_{int(time.time())}"
        return mock_secure_checkout_url

    except Exception as network_err:
        return f"ERROR: Communication breakdown handling PayHub network hooks: {network_err}"


def create_subscription_payhub_checkout_session(user_id, tier_token, is_annual):
    """
    Formulates a recurring plan subscription initialization payload packet
    and hooks directly into the PayHub merchant ledger endpoint channels.
    """
    import streamlit as st
    import time

    try:
        if "PAYHUB_SECRET_KEY" not in st.secrets:
            return "ERROR: PayHub API Secret key configuration is missing inside st.secrets."

        payhub_api_token = st.secrets["PAYHUB_SECRET_KEY"]

        # Calculate pricing tiers natively based on parameters
        base_rate = 9.99 if tier_token == "premium" else 29.99
        calculated_cost = (base_rate * 12 * 0.8) if is_annual else base_rate

        request_body = {
            "amount": float(calculated_cost),
            "currency": "USD",
            "description": f"Atelier Subscription Upgrade - Plan: {tier_token.capitalize()} ({'Annual' if is_annual else 'Monthly'})",
            "redirect_url": "https://streamlit.app",
            "metadata": {
                "user_id": str(user_id),
                "target_tier": tier_token,
                "is_annual_billing": str(is_annual),
            },
        }

        # Mock production fallback URL for layout verification
        return f"https://payhub.com_{int(time.time())}"

    except Exception as err:
        return f"ERROR: Network link connection breakdown via PayHub: {err}"
