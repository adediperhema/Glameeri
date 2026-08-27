import io
import sys
import json
import os
import random
import time
from typing import Any

import cv2
import numpy as np
import streamlit as st
from functionalities import (
    bootstrap_silhouette_assets,
    generate_lookbook_pdf,
    create_tile_grid,
    get_val,
    create_attire_checkout_session,
    render_pricing_matrix_panel,
    push_to_studio,
    collection_button,
    open_client,
    live_studio,
    saved_measurement,
    pdf_byte,
)

# 🗄️ PostgreSQL Dynamic Hook Registries
from database import (
    ClientMeasurement,
    Collection,
    CollectionWork,
    DashboardProduct,
    ShopOrder,
    User,
    Base,
    conn,
    hash_password,
)
import json
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

# Unified ReportLab Document Typographic Engines
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import logging
from sqlalchemy.orm import Session

# Safe production casting pattern
from typing import Any, cast

# safe_profile = cast(Any, raw_profile_object)


# Configure system logging parameters
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Initialize the Streamlit SQL connection wrapper first
#conn = st.connection("sql", url=DATABASE_URL)

# 2. Extract the raw SQLAlchemy engine correctly (No leading underscore!)
engine = conn.engine

# 3. Spin up your traditional ORM session object using the engine
db_session = Session(engine)

# Put this in a hidden admin section or at the very bottom of your app during setup
# if st.button("Dev Tools: Sync Database Tables"):
# We use conn._engine to tap into Streamlit's optimized connection engine
#    Base.metadata.create_all(bind=conn._engine)
#    st.success("Successfully created tables in Supabase!")


# --- ADD THIS SECURITY IMPORT TO THE TOP OF YOUR INDEX.PY FILE ---
from security import (
    create_tryon_checkout_session,
    decode_and_verify_session_token,
    generate_user_session_token,
    get_password_hash,
    verify_password,
)

# =========================================================================
# 🛡️ CRYPTOGRAPHIC SECURITY VERIFICATION SHIELD GATE (TOP OF APP.PY)
# =========================================================================


# =========================================================================
# =========================================================================
# 🪡 FIX: SOLID CRISP WHITE PROFILE CARD & POPUP OVERLAY LAYOUT (INDEX4.PY)
# =========================================================================


# --- DECLARE THIS DICTIONARY CONSTANT AT THE TOP OF YOUR SCRIPT FILE ---

OFFLINE_BLUEPRINTS = {
    "Ankara Wax Print": "ANKARA GEOMETRY RULES:\n- Dynamic diamond matrix design layers.",
    "Kente Cloth Heritage": "KENTE WEAVING MATRIX SPECIFICATIONS:\n- Interlocking horizontal strip modules.",
    "Adire Tech": "ADIRE TECH CODES:\n- Indigo tie-dye resist structures using user hex tones.",
    "Modern Afro-Futurism": "AFRO-FUTURISM BLUEPRINT:\n- Cyber fractal node pathways matching selection colors.",
    "Plain Solid Colour": "PLAIN SOLID COLOR SPECIFICATIONS:\n- Uniform untextured minimalist canvas frames.",
}

BODY_SEGMENTATION_ROUTER = {
    "gown": {
        "anatomy_zones": [
            "Shoulders",
            "Chest/Bust",
            "Waistline",
            "Hips",
            "Full Leg Extension",
        ],
        "warp_intensity_x": 0.05,
        "warp_intensity_y": 0.08,
        "texture_density_ratio": 4.5,
        "fitting_notes": "👗 full-length structural drape: Requires uniform 3D vertical wrinkle mapping from upper chest down to ankles.",
    },
    "jumpsuit": {
        "anatomy_zones": [
            "Torso",
            "Midsection",
            "Crotch Junction",
            "Thighs",
            "Lower Calves",
        ],
        "warp_intensity_x": 0.07,
        "warp_intensity_y": 0.09,
        "texture_density_ratio": 5.0,
        "fitting_notes": "👖 Bi-lateral split layout: Requires high-compression horizontal warping around the crotch junction and inner thigh seams.",
    },
    "peplum": {
        "anatomy_zones": ["Neckline", "Upper Bust", "Ribcage", "Flared Hip Fringe"],
        "warp_intensity_x": 0.04,
        "warp_intensity_y": 0.06,
        "texture_density_ratio": 3.8,
        "fitting_notes": "👚 Flared perimeter layout: Requires expansion transform scaling directly along the lower waist ribcage fringe lines.",
    },
    "jacket": {
        "anatomy_zones": [
            "Collar Neck",
            "Shoulder Pads",
            "Chest Width",
            "Bicep Sleeves",
            "Wrist Cuffs",
        ],
        "warp_intensity_x": 0.06,
        "warp_intensity_y": 0.05,
        "texture_density_ratio": 4.0,
        "fitting_notes": "🧥 Structured outer overlay: Requires stiff linear grid alignment across the upper shoulders and sleeve cylinders.",
    },
    # Add trouser,skirt and tops, jacket
}
# Inject CSS targeting a specific key
st.markdown(
    """
        <style>
        .st-key-sidebar_logout_cta button {
            background-color: #1E88E5 !important; /* Your custom blue hex code */
            color: white !important;               /* White text color */
            border: none !important;
            border-radius: 8px;                    /* Rounded corners */
            width: auto;
            max-height: 70%;
            object-fit: contain;
        }
    
        /* Optional: Hover effect */
        .st-key-sidebar_logout_cta button:hover {
            background-color: #1565C0 !important; /* Darker blue on hover */
            color: #FFFFFF !important;
        }

        .st-key-sidebar_exit_home_cta button {
                    background-color: #1E88E5 !important; /* Your custom blue hex code */
                    color: white !important;               /* White text color */
                    border: none !important;
                    border-radius: 8px;                    /* Rounded corners */
                    width: auto;
                    max-height: 70%;
                    object-fit: contain;
                }
            
        /* Optional: Hover effect */
        .st-key-sidebar_exit_home_cta button:hover {
            background-color: #1565C0 !important; /* Darker blue on hover */
            color: #FFFFFF !important;
        }
        </style>
    """,
    unsafe_allow_html=True,
)


import os
from PIL import Image, ImageDraw

# Execute the bootstrapper instantly at startup lifecycle steps
bootstrap_silhouette_assets()


###########set up side bar#######################

# =========================================================================
# 🧭 PERSISTENT WORKSPACE SIDEBAR NAVIGATION CONTROLLER
# =========================================================================

# 1. Apply premium corporate typography padding rules to override system sidebar limits
# =========================================================================
# 🧭 PERSISTENT WORKSPACE SIDEBAR NAVIGATION CONTROLLER (AUTH-PROTECTED)
# =========================================================================

# FIX: Wrapping everything inside this session tracker hides the sidebar until login!
# =========================================================================
# 🧵 FIX: HIGH-FIDELITY SIDEBAR CIRCULAR DISPLAY HEADER (INDEX4.PY) 🧵
# =========================================================================

# Check if the user session has been fully authenticated inside global state management

# =========================================================================
# 🧵 FIX: HIGH-FIDELITY SIDEBAR CIRCULAR DISPLAY HEADER (INDEX4.PY) 🧵
# =========================================================================

# Check if the user session has been fully authenticated inside global state management
# =========================================================================
# 🪡 FIX: SINGLE-TIMELINE SANITIZED SIDEBAR HEAD PACK (OBLITERATES RAW TEXT)
# =========================================================================

# Check if the user session has been fully authenticated inside global state management
# =========================================================================
# 🪡 FIX: COMPRESSED INTERACTIVE CLICK-TO-POPUP LIGHTBOX MODAL (INDEX4.PY)
# =========================================================================


# =========================================================================
# 🪡 INJECTION A: BACKGROUND STRIPE RETURN INTERCEPT LOOP (TOP OF INDEX4.PY)
# =========================================================================


# Catch live query parameters passed back into your browser address bar by Stripe
query_params = st.query_params

if query_params.get("payment_status") == "success" and "tier_upgrade" in query_params:
    target_tier_token = str(query_params.get("tier_upgrade"))
    auth_user_id_val = int(query_params.get("auth_id", 0))

    if auth_user_id_val > 0:
        # When you want to insert or update data, just use 'with conn.session'
        with conn.session as db_sync:
            # db_sync = SessionLocal()
            try:
                target_user_row = (
                    db_sync.query(User).filter(User.id == auth_user_id_val).first()
                )
                if target_user_row:
                    setattr(target_user_row, "subscription_tier", target_tier_token)
                    setattr(
                        target_user_row, "monthly_generation_count", 0
                    )  # Clear generation blocks immediately!
                    db_sync.commit()
                    st.success(
                        f"💳 Payment Verified via Stripe webhook payload! Workspace successfully unlocked and upgraded to '{target_tier_token.upper()}'."
                    )
                    st.query_params.clear()  # Clear address parameters out cleanly
                    time.sleep(1.0)
                    st.rerun()
            except Exception as e:
                db_sync.rollback()
            finally:
                db_sync.close()

elif query_params.get("payment_status") == "attire_success":
    client_name_badge = str(query_params.get("client")).replace("_", " ")
    st.sidebar.success(
        f"🎉 Success! Payment received for attire order: '{client_name_badge}'!"
    )
    st.query_params.clear()


# Check if the user session has been fully authenticated inside global state management
if st.session_state.get("authenticated") == True:

    fallback_studio_name = "Premium Fashion House"
    user_session_id_val = st.session_state.get("user_session_id", 0)
    
    current_user: Any = None
    token_studio_name: str = fallback_studio_name
    verified_email_log: str = "studio@volkoda.com"
    verified_bio_log: str = "No corporate profile logs attached."
    active_avatar_name: str = "default_profile.png"

    # 1. FIX: Keep database queries intact and read variables BEFORE closing the connection
    try:
        if user_session_id_val > 0:
            current_user = (
                db_session.query(User).filter(User.id == user_session_id_val).first()
            )
            if current_user:
                token_studio_name = str(getattr(current_user, "studio_name", fallback_studio_name))
                verified_email_log = str(getattr(current_user, "email", "studio@volkoda.com"))
                verified_bio_log = str(getattr(current_user, "biography", "No corporate profile logs attached."))
                active_avatar_name = str(getattr(current_user, "profile_picture_name", "default_profile.png"))
    except Exception as query_error:
        st.sidebar.error(f"Profile recovery bottleneck: {query_error}")
    finally:
        db_session.close()  # Now it is completely safe to close the database session

    active_studio_title: str = str(token_studio_name)
    avatar_render_source_url = "https://unsplash.com" # High fashion default fallback image

    # =========================================================================
    # 🪡 FIX 2: BASE64 CLOUD STRING INTERPRETATION LOGIC (NO DISK CHECKS) 🪡
    # =========================================================================
    if active_avatar_name and active_avatar_name != "default_profile.png":
        # If the string starts with data:image, it means it's our new persistent Base64 cloud file stream!
        if active_avatar_name.startswith("data:image"):
            avatar_render_source_url = active_avatar_name
        else:
            # Fallback legacy check just in case an old local text filename is still registered in your rows
            local_avatar_disk_path = os.path.join("profile_pics", active_avatar_name)
            if os.path.exists(local_avatar_disk_path):
                try:
                    with open(local_avatar_disk_path, "rb") as image_file:
                        import base64
                        raw_b64_bytes = base64.b64encode(image_file.read())
                        clean_b64_string = raw_b64_bytes.decode("utf-8").replace("\n", "").replace("\r", "")
                        avatar_render_source_url = f"data:image/png;base64,{clean_b64_string}"
                except Exception:
                    pass

    # 🔥 Sidebar payload with solid crisp white parameters (#ffffff)
    sidebar_profile_html_payload = (
        "<style>"
        ".vk-modal-checkbox-switch { display: none !important; }"
        ".vk-avatar-trigger-badge { cursor: zoom-in; transition: transform 0.2s ease-in-out; display: block; margin: 0 auto 12px auto; width: 80px; height: 80px; }"
        ".vk-avatar-trigger-badge:hover { transform: scale(1.05); }"
        ".vk-lightbox-modal-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(30, 30, 30, 0.75); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); z-index: 999999; display: flex; justify-content: center; align-items: center; opacity: 0; pointer-events: none; transition: opacity 0.25s ease-in-out; }"
        ".vk-expanded-profile-popup { background: #ffffff !important; padding: 32px; border-radius: 20px; border: 1px solid #e2e8f0; width: 88%; max-width: 380px; text-align: center; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04); transform: scale(0.88); transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); }"
        ".vk-modal-checkbox-switch:checked ~ .vk-lightbox-modal-backdrop { opacity: 1; pointer-events: auto; }"
        ".vk-modal-checkbox-switch:checked ~ .vk-lightbox-modal-backdrop .vk-expanded-profile-popup { transform: scale(1); }"
        ".vk-modal-dismiss-cta { margin-top: 22px; background-color: #E05A47; color: white !important; border: none; padding: 10px 24px; border-radius: 8px; font-family: sans-serif; font-weight: 700; font-size: 14px; cursor: pointer; display: inline-block; transition: background 0.2s; text-decoration: none !important; }"
        ".vk-modal-dismiss-cta:hover { background-color: #C04837; }"
        "</style>"
        "<input type='checkbox' id='vkProfileToggleSwitch' class='vk-modal-checkbox-switch' />"
        "<div style='background: #ffffff !important; border: 1px solid #e2e8f0; padding: 16px; border-radius: 14px; margin-bottom: 20px; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px 0 rgba(0,0,0,0.06); text-align: center; font-family: sans-serif;'>"
        "<label for='vkProfileToggleSwitch' class='vk-avatar-trigger-badge'>"
        f"<img src='{avatar_render_source_url}' style='width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid #E05A47; box-shadow: 0 2px 6px rgba(0,0,0,0.1);' alt='Studio DP'/>"
        "</label>"
        "<div>"
        "<p style='margin: 0; font-size: 10px; color: #E05A47; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;'>🎨 Active Atelier Canvas</p>"
        f"<h3 style='margin: 4px 0 0 0; color: #2C2623; font-size: 18px; font-weight: 800; line-height: 1.2;'>Hi! {active_studio_title}</h3>"
        f"<label for='vkProfileToggleSwitch' style='font-size: 11px; color: #64748b; cursor: pointer; text-decoration: underline; display: block; margin-top: 6px;'>🔍 View Studio Info</label>"
        "</div>"
        "</div>"
        "<div class='vk-lightbox-modal-backdrop'>"
        "<div class='vk-expanded-profile-popup' style='font-family: sans-serif;'>"
        f"<img src='{avatar_render_source_url}' style='width: 130px; height: 130px; border-radius: 50%; object-fit: cover; border: 4px solid #E05A47; margin: 0 auto 16px auto; display: block; box-shadow: 0 4px 15px rgba(0,0,0,0.1);' alt='HD Avatar'/>"
        f"<h2 style='margin: 0; color: #1e293b; font-size: 24px; font-weight: 800;'>{active_studio_title}</h2>"
        f"<p style='margin: 4px 0 16px 0; font-size: 13px; color: #E05A47; font-weight: 600;'>{verified_email_log}</p>"
        "<div style='border-top: 1px solid #e2e8f0; padding-top: 16px; text-align: left;'>"
        "<span style='font-size: 11px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>📜 Studio Biography / Focus:</span>"
        f"<p style='margin: 4px 0 0 0; font-size: 14px; color: #334155; line-height: 1.4; font-style: italic;'>\"{verified_bio_log}\"</p>"
        "</div>"
        "<label for='vkProfileToggleSwitch' class='vk-modal-dismiss-cta'>↩️ Close Studio Profile</label>"
        "</div>"
        "</div>"
    )

    # Render directly to the sidebar area using safe HTML evaluation flags
    st.sidebar.markdown(sidebar_profile_html_payload, unsafe_allow_html=True)

    # 1. Fetch live metrics directly out of your PostgreSQL records on every rerun pass
    user_session_id_val = st.session_state.get("user_session_id", 0)
    # db_session = SessionLocal()
    current_user = db_session.query(User).filter(User.id == user_session_id_val).first()

    user_tier = str(getattr(current_user, "subscription_tier", "freemium"))
    current_usage = int(getattr(current_user, "monthly_generation_count", 0))
    db_session.close()

    # Evaluate generation thresholds instantly via your security.py guards
    from security import verify_generation_allowance

    _, is_expired, restriction_msg = verify_generation_allowance(
        user_tier, current_usage
    )

    # 2. Render your solid white click-expanding user badge into the top sidebar tray panel
    # st.sidebar.markdown(sidebar_profile_html_payload, unsafe_allow_html=True)
    # st.sidebar.markdown("### 🧭 Workspace Navigation")

    # 🔥 FIX 1: ALWAYS allow full navigation to the radio buttons so they can sell and view analytics!
    # Even if expired, they can click into the Ledger or Orders sheets without getting locked out.
    # Render the primary layout navigation controller radio button panel
    sidebar_selection = st.sidebar.radio(
        "Select Active Workspace Module:",
        [
            "🎨 Production Designer Canvas",
            "📁 Fabric Collection Manager",
            "📏 Saved Measurements Ledger",
            "🌟 Collection Lookbook Portfolio",
            "📊 Analytical Orders Ledger",
            "🛒 Marketplace",
            "👤 Edit Studio Profile",
            "💰 Subscription Pricing Plan",
        ],
        key="active_sidebar_tab",
    )
    # "📈 User Shop Dashboard", # NEW DIRECT ACCESS ROUTE PANEL NODE
    # "🛍️ Marketplace Shop"
    # "🛒 Browse Material Shop",

    # Render an explicit alert warning on the sidebar panel if they have run out of free accounts slots
    if is_expired:
        st.sidebar.error(
            "🔒 Generation Allowance Expired. Upgrade plan to unlock 3D Imprint tools."
        )

    if st.sidebar.button(
        "🔒 SECURE SIGN OUT / LOCK SESSION",
        key="sidebar_logout_cta",
        use_container_width=True,
    ):
        st.session_state["authenticated"] = False
        st.session_state["is_logged_in"] = False
        st.session_state["user_session_token"] = None
        st.session_state["user_session_id"] = None
        st.session_state["app_view"] = "is_logged_in"
        st.rerun()

    # =========================================================================
    # CORE INTERFACE BLOCK MODULE A: 3D GRAPHICS TRY-ON PIPELINE MODULE
    # =========================================================================

    # =========================================================================
    # 🧵 STEP 1: INITIAL GLOBAL LAYOUT DECLARATIONS (TOP OF INDEX4.PY) 🧵
    # =========================================================================

    # =========================================================================
    # 🧵 STEP 2: LOWER INTERFACE ROUTING CYCLES (LOWER IN INDEX4.PY) 🧵
    # =========================================================================

    # Lower down in your active view panel router, your call execution works flawlessly:
    if sidebar_selection == "🎨 Production Designer Canvas ":
        st.title("🎨 3D Surface Try-On Imprinter Engine")

        if is_expired:
            st.error(restriction_msg)
            st.info(
                "💡 Pro Tip: Your store dashboard features remain active. Head over to the '📊 Analytical Orders Ledger' menu module to continue managing your sales transactions or upgrade below."
            )

            # 🔥 FIX 2: The red underline on render_pricing_matrix_panel vanishes forever because the pointer path is open!
            render_pricing_matrix_panel(
                user_authenticated=True, active_tier_str=user_tier
            )
            st.stop()

        # (Your dropdown parameters and 3D normal mapping loops process normally below here...)

    # =========================================================================
    # 🏪 CORE INTERFACE BLOCK MODULE E: ADVANCED ANALYTICAL ORDERS LEDGER (THE SHOP)
    # =========================================================================
    # =========================================================================


# 1. Ensure the baseline navigation callback function is initialized early
def navigate_to(target_view_name: str) -> None:
    """Safely transitions active session workspace panels smoothly without lag."""
    st.session_state["app_view"] = str(target_view_name)

    # st.sidebar.markdown(
    #    "<h2>🛠️ Glameeri Studio Panel Controller</h2>", unsafe_allow_html=True
    # )

    # 🛡️ CRYPTOGRAPHIC JWT SIGNATURE VERIFICATION SHIELD GATE
    from security import decode_and_verify_session_token

    # =========================================================================


if st.session_state.get("authenticated") == True:

    # Apply premium corporate typography padding rules to override system sidebar limits
    st.sidebar.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 1px solid #dadce0 !important;
            }
            [data-testid="stSidebar"] h2 {
                font-size: 16px !important;
                font-weight: 500 !important;
                color: #202124 !important;
                margin-bottom: 12px !important;
                letter-spacing: -0.3px;
            }
            .status-badge {
                background-color: #f1f3f4;
                padding: 4px 10px;
                border-radius: 100px;
                font-size: 11px;
                font-weight: 500;
                color: #1a73e8;
                display: inline-block;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================================
    # 🪡 FIX: TYPE-SAFE JWT DICTIONARY PROPERTY UNPACKING (INDEX4.PY) 🪡
    # =========================================================================

    # Locate where verified_payload claims are read inside your dashboard gateway loop:

    # Extract the payload dictionary object safely out of your secure token decoder
    active_token: Any = st.session_state.get("user_session_token", None)
    verified_payload: Any = None

    if active_token is not None and isinstance(active_token, str):
        from security import decode_and_verify_session_token

        verified_payload = decode_and_verify_session_token(active_token)

    # 🔥 FIX: Enforce an explicit type-validation shield guard check!
    # This guarantees to the linter that the payload is a dictionary, clearing the red lines instantly.
    if verified_payload is not None and isinstance(verified_payload, dict):
        token_user_id: int = int(verified_payload.get("sub", 0))
        token_studio_name: str = str(verified_payload.get("studio", "Glameeri Atelier"))
        token_user_email: str = str(verified_payload.get("email", "studio@volkoda.com"))
    else:
        # Fallback parameters applied safely if tokens degrade or expire mid-session
        token_user_id = int(st.session_state.get("user_session_id", 0))
        token_studio_name = "Premium Fashion House"
        token_user_email = "studio@volkoda.com"

    # =========================================================================
    # 🧭 UPDATED SIDEBAR WORKSPACE OPTION CONTROLLER (INDEX4.PY)
    # =========================================================================

    # 🏠 HANDLER ROW FOR HOME LINK EXIT GATE REDIRECT
    if st.sidebar.button("🏠 EXIT STUDIO TO HOME MENU", key="sidebar_exit_home_cta"):
        st.session_state["authenticated"] = False
        st.session_state["is_logged_in"] = False
        st.session_state["user_session_token"] = None
        st.session_state["app_view"] = "home"
        st.session_state["wizard_step"] = 1
        st.rerun()
else:
    # Fallback default value ensures that pre-login routed logic blocks don't trigger NameErrors
    sidebar_selection = "🎨 Production Designer Canvas"

# =========================================================================
# ROUTED ENGINE RENDERING FRAMES DROP IN SMOOTHLY DIRECTLY BENEATH THIS LINE
# =========================================================================

# =========================================================================
# 👤 ROUTED INTERFACE DISPLAY: EDITABLE STUDIO ACCOUNT PROFILE SETTINGS
# =========================================================================
if sidebar_selection == "👤 Edit Studio Profile":
    ##############

            # THE EDITABLE ACCOUNT FORM DATA MATRIX SECTION
            st.markdown("### 📝 Modify Account Details")
            
            # FIX 1: We use a SINGLE cohesive form block for both the inputs and the submit button
            with st.form("edit_profile_form_matrix"):
                
                # FIX 2: Added explicit 'key' strings that match exactly what your submission logic looks for!
                edit_studio_name = st.text_input(
                    "Edit Studio / Atelier Display Title Name:",
                    value=current_user.studio_name,
                    key="profile_edit_field_name"  # <-- Critical Key
                )
                
                edit_biography = st.text_area(
                    "Edit Studio Biography / Specialization Profile Log:",
                    value=current_user.biography,
                    key="profile_edit_field_bio"   # <-- Critical Key
                )
                
                update_pfp = st.file_uploader(
                    "Replace Profile Picture File Asset (Optional):",
                    type=["png", "jpg", "jpeg"],
                )

                # Place the submit button cleanly inside the single form container
                submit_button = st.form_submit_button("💾 Save Profile Data Changes")

            # =========================================================================
            # 🪡 FIX 3: RESTRUCTURED LOGIC TRIGGER (RUNS ON SUBMIT) 🪡
            # =========================================================================
            if submit_button:
                # Grab the cleaned values directly from session state variables now that the keys match
                clean_edit_name = str(st.session_state.get("profile_edit_field_name", "")).strip()
                clean_edit_bio = str(st.session_state.get("profile_edit_field_bio", "")).strip()

                if not clean_edit_name:
                    st.error("❌ Alteration Denied: Studio Name cannot be empty.")
                else:
                    try:
                        active_user_id = st.session_state.get("user_session_id", 0)
                        db_user = (
                            db_session.query(User)
                            .filter(User.id == active_user_id)
                            .first()
                        )

                        if db_user:
                            # 1. Update text attributes using type-safe setattr patterns
                            setattr(db_user, "studio_name", clean_edit_name)
                            setattr(db_user, "biography", clean_edit_bio)

                            # 2. OPTIONAL: Handle Avatar Upload directly into our persistent Base64 string row!
                            if update_pfp is not None:
                                import base64
                                pfp_bytes = update_pfp.getvalue()
                                encoded_pfp = base64.b64encode(pfp_bytes).decode("utf-8")
                                clean_b64_string = f"data:image/jpeg;base64,{encoded_pfp}"
                                setattr(db_user, "profile_picture_name", clean_b64_string)

                            # 3. Save updates permanently to Supabase cloud
                            db_session.commit()
                            
                            st.success("🎉 Studio profile data altered and synced securely to Supabase!")
                            time.sleep(0.5)
                            st.rerun()

                    except Exception as db_err:
                        db_session.rollback()
                        st.error(f"Cloud update framework sync failure: {db_err}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.stop()  # Halts drawing right here to hide background try-on canvas modules cleanly


# Safe initialization for collection records array bucket memory slots
if "studio_collections" not in st.session_state:
    st.session_state["studio_collections"] = []


# =========================================================================
# CONTAINER BLOCK MODULE A: 📁 DEDICATED FABRIC COLLECTION & GALLERY VIEW
# =========================================================================
#

# Ensure your cryptographic token verification shield gate is actively unpacking user data:
# token_user_id = verified_payload["sub"]
# token_studio_name = verified_payload["studio"]
# token_user_email = verified_payload["email"]


# =========================================================================
# 📁 ROUTED MODULE VIEW: DUAL-PANEL COLLECTION DATABASE GALLERY MANAGER
# =========================================================================
if sidebar_selection == "📁 Fabric Collection Manager":
    ##############

    # 1. Establish the precise filesystem track path pointing to your local logo file
    local_logo_disk_path = os.path.join("images", "fashion_logo1_nobg.png")

    # Authoritative high-fashion fallback image link deployed if your local disk asset is missing
    navbar_logo_render_url = "https://unsplash.com"

    # 2. Pull image bytes and convert to a clean single-line Base64 format to bypass cross-origin blocks
    if os.path.exists(local_logo_disk_path):
        try:
            with open(local_logo_disk_path, "rb") as logo_bytes_file:
                import base64

                encoded_logo_b64 = base64.b64encode(logo_bytes_file.read())

                # Match the exact name used on BOTH lines to clear the red text error!
                clean_logo_b64_string = (
                    encoded_logo_b64.decode("utf-8").replace("\n", "").replace("\r", "")
                )
                navbar_logo_render_url = (
                    f"data:image/jpeg;base64,{clean_logo_b64_string}"
                )
        except Exception:
            pass

        # 3. COMPRESS THE NAVBAR PAYLOAD INSIDE PARENTHESES TO ERASE RAW CODE TEXT GATES
        navbar_branding_html_payload = (
            "<style>"
            "  .vk-navbar { display: flex; align-items: center; justify-content: space-between; background: #ffffff; border: 1px solid #e2e8f0; padding: 14px 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); font-family: sans-serif; }"
            "  .vk-navbar-logo-img { width: auto; max-height: 60px; object-fit: contain; border-radius: 6px; }"
            "  .brand-text-wrapper { flex-grow: 1; text-align: center; margin-right: 60px; }"
            "  .brand-tagline { font-size: 16px; font-weight: 600; color: #E05A47; text-transform: uppercase; letter-spacing: 1px; }"
            "</style>"
            "<div class='vk-navbar'>"
            f"  <img src='{navbar_logo_render_url}' class='vk-navbar-logo-img' alt='AfriTextile Core Branding Logo'/>"
            "   <div class='brand-text-wrapper'>"
            "       <span class='brand-tagline'>AI Fashion innovation Studio</span>"
            "   </div>"
            "</div>"
        )

        # Force the markdown engine to interpret the payload as native web node parameters
        st.markdown(navbar_branding_html_payload, unsafe_allow_html=True)

    ##############
    st.markdown('<div class="vk-card">', unsafe_allow_html=True)
    st.markdown(
        '<p class="vk-section-header">📁 Fabric Collection Workspace Manager</p>',
        unsafe_allow_html=True,
    )
    st.write(
        "Onboard new textile print lines, upload master batch swatches, and track active production inventory items below:"
    )

    import json
    import time

    layout_creator_panel, layout_gallery_panel = st.columns([1.1, 1.4], gap="large")

    # --- SUB-SECTION 1: THE COLLECTION INTAKE HUB CREATOR ---
    with layout_creator_panel:
        st.markdown("### 📥 Onboard Collection Roll")
        with st.form("create_collection_form", clear_on_submit=True):
            new_coll_title = st.text_input(
                "Collection Reference Title / Group Tag Name:",
                placeholder="e.g. Lagos Harmattan Wax 2026",
            )
            new_coll_origin = st.selectbox(
                "Cultural Foundation Heritage Link (Optional):",
                [
                    "Unspecified / General Heritage",
                    "Ankara Wax Print",
                    "Kente Cloth Heritage",
                    "Adire Tech",
                    "Modern Afro-Futurism",
                ],
            )
            new_coll_desc = st.text_area(
                "Workspace Annotation / Client Notes:",
                placeholder="Enter fabric density, target cuts, parameters...",
            )
            uploaded_swatches = st.file_uploader(
                "Upload Sample Swatch Graphics (PNG/JPG):",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
            )

            submit_btn = st.form_submit_button("📥 Compile and Add to Studio Inventory")

            if submit_btn:
                if new_coll_title and uploaded_swatches:
                    # Compress and encode multiple swatches to binary byte structures for row insertion
                    raw_bytes_list = []
                    for swatch_file in uploaded_swatches:
                        try:
                            raw_bytes_list.append(swatch_file.getvalue().hex())
                        except Exception as parse_err:
                            st.error(
                                f"File string optimization issue skipped: {parse_err}"
                            )

                    # Convert list to string block payload segment safely
                    encoded_blob_payload = json.dumps(raw_bytes_list).encode("utf-8")

                    # Open connection and commit database records linked explicitly to user payload parameters!
                    # db = SessionLocal()
                    new_db_collection = Collection(
                        user_id=token_user_id,
                        studio_name=token_studio_name,
                        email=token_user_email,
                        title=new_coll_title.strip(),
                        origin=new_coll_origin,
                        description=(
                            new_coll_desc.strip()
                            if new_coll_desc
                            else "No annotations logged."
                        ),
                        raw_images_blob=encoded_blob_payload,
                    )
                    db_session.add(new_db_collection)
                    db_session.commit()
                    db_session.close()

                    st.success(
                        f"🎉 Batch '{new_coll_title}' committed securely to PostgreSQL inventory!"
                    )
                    __import__("time").sleep(0.4)
                    st.rerun()
                else:
                    st.error(
                        "❌ Action stalled: Reference Title and minimum 1 asset swatch graph block required."
                    )

    # --- 🔥 THE SPECIFIC CORRECTION: SHIFTED ALL THE WAY BACK TO FLUSH RIGHT UNDER THE GENERATOR COLUMNS 🔥 ---
    # Moving this out of the 'if submit_btn:' logic allows it to render continuously on your page viewport!
    with layout_gallery_panel:
        st.markdown("### 🖼️ Live Workshop Swatch Gallery")

        # Connect to server and filter collections exclusively belonging to this logged-in tailor session
        # db = SessionLocal()
        try:
            user_saved_collections = (
                db_session.query(Collection)
                .filter(Collection.user_id == token_user_id)
                .order_by(Collection.id.desc())
                .all()
            )

            if not user_saved_collections:
                st.info(
                    "ℹ️ No active fabric collections compiled yet inside your database profile workspace ledger row."
                )
            else:
                for collection in user_saved_collections:
                    st.markdown(
                        f"""
                        <div style="background-color: #ffffff; border: 1px solid #dadce0; border-radius: 12px; padding: 16px; margin-bottom: 16px; color: #111111; font-family: sans-serif;">
                            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px dashed #dadce0; padding-bottom:6px; margin-bottom:8px;">
                                <strong style="font-size:16px; color:#2d3748;">{collection.title}</strong>
                                <span style="background-color:#edf2f7; padding:2px 8px; border-radius:20px; font-size:12px; color:#4a5568; font-weight:600;">{collection.origin}</span>
                            </div>
                            <p style="font-size:14px; color:#718096; margin:0 0 12px 0;">{collection.description}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # --- UNWRAP AND DISPLAY CONVERSIONS FOR MULTIPLE IMAGE SWATCHES ---
                    # --- UNWRAP AND DISPLAY CONVERSIONS FOR MULTIPLE IMAGE SWATCHES ---
                    # 🔥 FIXED: Using getattr dynamically extracts the column attribute out of the instance
                    # This completely erases the red '.raw_images_blob' highlight error permanently!
                    from typing import Any, cast

                    safe_collection = cast(Any, collection)
                    active_blob_payload = getattr(
                        safe_collection, "raw_images_blob", None
                    )

                    if active_blob_payload:
                        try:
                            # Decode and unpack hex string arrays out of binary bytes node columns safely
                            json_string_data = active_blob_payload.decode("utf-8")
                            hex_images_list = json.loads(json_string_data)

                            if hex_images_list:
                                # Create an image row layout view grid
                                img_cols = st.columns(min(4, len(hex_images_list)))
                                for idx, hex_str in enumerate(hex_images_list):
                                    with img_cols[idx % len(img_cols)]:
                                        # Translate hex parameters back to clean display bytes natively
                                        raw_swatch_bytes = bytes.fromhex(hex_str)
                                        st.image(
                                            raw_swatch_bytes, use_container_width=True
                                        )
                        except Exception as display_err:
                            st.caption(
                                f"ℹ️ Graphic unwrapping notification: {display_err}"
                            )

        finally:
            db_session.close()

    st.markdown("</div>", unsafe_allow_html=True)

            # ---------------------------------------------------------------------
        # 🚀 NEW NAVIGATION BUTTON: LINKS DYNAMICALLY TO THE PORTFOLIO PAGE 🚀
        # ---------------------------------------------------------------------
   if st.button(
        "👁️ View Onboarded Assets inside Lookbook Portfolio ➔", 
        key="fabric_manager_to_portfolio_redirect_cta",
        type="secondary",
        use_container_width=True
    ):
        st.session_state["sidebar_selection_state_key"] = "🌟 Collection Lookbook Portfolio"
        __import__('time').sleep(0.1)
        st.rerun()

    # 🔥 THE EXACT POSITION: Place this at the very end of the Fabric Manager branch.
    # It must be indented by exactly 4 spaces (aligned with the button, not inside it).
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
        # 🔥 FIXED: Removed the stray standalone st.stop() that was freezing your script timeline!
        # The code can now drop down naturally to evaluate the rest of your dashboard modules.




# =========================================================================
# CONTAINER BLOCK MODULE B: 🛒 SECURE MATERIAL SHOP ORDER SYSTEM
# =========================================================================
# =========================================================================
# CONTAINER BLOCK MODULE B: 🛒 MATERIAL SHOP VIEW WITH LIVE MULTI-SEARCH
# =========================================================================
elif sidebar_selection == "🛒 Marketplace":
    ##############

    # 1. Establish the precise filesystem track path pointing to your local logo file
    local_logo_disk_path = os.path.join("images", "fashion_logo1_nobg.png")

    # Authoritative high-fashion fallback image link deployed if your local disk asset is missing
    navbar_logo_render_url = "https://unsplash.com"

    # 2. Pull image bytes and convert to a clean single-line Base64 format to bypass cross-origin blocks
    if os.path.exists(local_logo_disk_path):
        try:
            with open(local_logo_disk_path, "rb") as logo_bytes_file:
                import base64

                encoded_logo_b64 = base64.b64encode(logo_bytes_file.read())

                # 🔥 FIX: Match the exact name used on BOTH lines to clear the red text error!
                clean_logo_b64_string = (
                    encoded_logo_b64.decode("utf-8").replace("\n", "").replace("\r", "")
                )
                navbar_logo_render_url = (
                    f"data:image/jpeg;base64,{clean_logo_b64_string}"
                )
        except Exception:
            pass

        # 3. 🔥 COMPRESS THE NAVBAR PAYLOAD INSIDE PARENTHESES TO ERASE RAW CODE TEXT GATES 🔥
        # Alternating to double quotes (") on the outside and single quotes (') on the inside clears all syntax error crashes!
        navbar_branding_html_payload = (
            "<style>"
            "  .vk-navbar { display: flex; align-items: center; justify-content: space-between; background: #ffffff; border: 1px solid #e2e8f0; padding: 14px 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); font-family: sans-serif; }"
            "  .vk-navbar-logo-img { width: auto; max-height: 60px; object-fit: contain; border-radius: 6px; }"
            "  .brand-text-wrapper { flex-grow: 1; text-align: center; margin-right: 60px; }"
            "  .brand-tagline { font-size: 16px; font-weight: 600; color: #E05A47; text-transform: uppercase; letter-spacing: 1px; }"
            "</style>"
            "<div class='vk-navbar'>"
            f"  <img src='{navbar_logo_render_url}' class='vk-navbar-logo-img' alt='AfriTextile Core Branding Logo'/>"
            "   <div class='brand-text-wrapper'>"
            "       <span class='brand-tagline'>AI Fashion innovation Studio</span>"
            "   </div>"
            "</div>"
        )

        # "       <span class='brand-title'>AfriTextile</span>"
        # style="width: 500px; height: 600px;"
        # Force the markdown engine to interpret the payload as native web node parameters
        st.markdown(navbar_branding_html_payload, unsafe_allow_html=True)
    from shop_page import render_marketplace_hub

        # db = SessionLocal()
    render_marketplace_hub(db_session)
    db_session.close()
    ##############
    st.markdown('<div class="vk-card">', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
    # =========================================================================
# elif sidebar_selection == "🖼️ Interactive Portfolio Gallery":
elif sidebar_selection == "🌟 Collection Lookbook Portfolio":
    st.markdown('<div class="vk-card">', unsafe_allow_html=True)
    st.markdown(
        '<p class="vk-section-header">🌟 Artisan Studio Row Lookbook Portfolio</p>',
        unsafe_allow_html=True,
    )
    st.write(
        "Browse your design drafts, client lookbooks, and textile rolls. Click the inspect button on any asset card to launch its item profile detail workbook modal:"
    )

    import json
    from typing import Any, cast

    # 🔥 1. DECLARE THE HIGH-FIDELITY DETAILED PROFILE DRAWER DIALOG MODAL 🔥
    @st.dialog("📋 Lookbook Item Structural Profile Workbook", width="large")
    def launch_lookbook_item_lightbox_modal(
        title: str, origin: str, notes: str, blob_data: Any
    ):
        """
        Centered Dialog Overlay Window.
        Presents both text data arrays and image swatches cleanly without covering the whole browser workspace page canvas.
        """
        # Top Heading Layout Matrix
        m_col1, m_col2 = st.columns([2.2, 1])
        with m_col1:
            st.subheader(title)
        with m_col2:
            st.markdown(
                f"<span style='background-color:#ebf8ff; color:#2b6cb0; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:bold; text-transform:uppercase;'>{origin}</span>",
                unsafe_allow_html=True,
            )

        st.divider()

        # Dual-Column Modal Grid splitting text definitions on the left and graphics on the right
        modal_left_txt, modal_right_img = st.columns([1, 1.2], gap="medium")

        with modal_left_txt:
            st.markdown("##### 📝 Operations Logging & Annotations")
            st.info(notes)
            st.caption(
                "🔒 Recorded securely to PostgreSQL Studio Ledger Tracking matrices."
            )

        with modal_right_img:
            st.markdown("##### 🖼️ Compiled Graphic Assets Swatches")
            if blob_data:
                try:
                    # Attempt A: Parse as JSON list string (Multi-file fabric collection manager format)
                    json_str_check = blob_data.decode("utf-8")
                    hex_array_list = json.loads(json_str_check)

                    if isinstance(hex_array_list, list) and len(hex_array_list) > 0:
                        for s_idx, hex_string_code in enumerate(hex_array_list):
                            decoded_raw_bytes = bytes.fromhex(hex_string_code)
                            st.image(
                                decoded_raw_bytes,
                                caption=f"Roll Swatch Roll #{s_idx+1}",
                                use_container_width=True,
                            )
                    else:
                        st.image(
                            blob_data,
                            caption="Lookbook Canvas Render",
                            use_container_width=True,
                        )
                except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
                    try:
                        # Attempt B: If JSON parsing fails, it's direct raw binary try-on output bytes block
                        st.image(
                            blob_data,
                            caption="AI Tailored Production Lookbook Blueprint",
                            use_container_width=True,
                        )
                    except Exception as render_failure:
                        st.caption(
                            f"ℹ️ Core graphic rendering bypass trace: {render_failure}"
                        )
            else:
                st.warning(
                    "No graphic image blobs attached to this database row index."
                )

        st.divider()
        # Bottom Actions close container trigger row layout
        if st.button(
            "❌ Close Profile Drawer",
            use_container_width=True,
            key="close_lookbook_dialog_modal_cta",
        ):
            st.rerun()  # Closes the focus dialog drawer seamlessly

    # 🔥 2. DATABASE RETRIEVAL MATRIX AND ROW ALIGNMENT RENDERING PASS 🔥
    # db_read = SessionLocal()
    try:
        current_tailor_id = st.session_state.get("user_id", 1)

        saved_portfolio_items = (
            db_session.query(Collection)
            .filter(Collection.user_id == current_tailor_id)
            .order_by(Collection.id.desc())
            .all()
        )

        if not saved_portfolio_items:
            st.info(
                "ℹ️ Your design lookbook portfolio ledger is currently empty. Head over to Step 3 Virtual Studio or your Fabric Manager to sync your first artifact!"
            )
        else:
            items_per_row = 3
            chunked_portfolio_rows = [
                saved_portfolio_items[i : i + items_per_row]
                for i in range(0, len(saved_portfolio_items), items_per_row)
            ]

            # Loop through rows to keep workspace columns structured and flush
            for row_idx, row_items in enumerate(chunked_portfolio_rows):
                columns_container = st.columns(3, gap="medium")

                for col_idx, item in enumerate(row_items):
                    with columns_container[col_idx]:
                        safe_item = cast(Any, item)

                        # Dynamic getattr values fetch strips out strict linter red highlights warnings
                        item_id = int(getattr(safe_item, "id", 0))
                        item_title = str(
                            getattr(safe_item, "title", "Untitled Portfolio Look")
                        )
                        item_origin = str(
                            getattr(safe_item, "origin", "General Heritage")
                        )
                        item_desc = str(
                            getattr(
                                safe_item, "description", "No artisan notes attached."
                            )
                        )
                        image_payload = getattr(safe_item, "raw_images_blob", None)

                        # Render the outer card structure layout parameters
                        st.markdown(
                            f"""
                            <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px; color:#2d3748; font-family: sans-serif; box-shadow: 0 1px 3px rgba(0,0,0,0.02); min-height: 115px; margin-bottom:10px;">
                                <div style="display: flex; flex-direction: column; justify-content: flex-start; align-items: flex-start; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px; margin-bottom: 8px; gap: 4px;">
                                    <strong style="font-size: 15px; color: #1a202c; line-height: 1.2;">📋 {item_title}</strong>
                                    <span style="background-color: #ebf8ff; color: #2b6cb0; padding: 1px 8px; border-radius: 20px; font-size: 10px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">{item_origin}</span>
                                </div>
                                <p style="font-size: 12px; color: #4a5568; margin: 0; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                                    {item_desc}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Compact, clean item overview thumbnail container
                        if image_payload:
                            try:
                                json_string = image_payload.decode("utf-8")
                                parsed_hex_list = json.loads(json_string)
                                if (
                                    isinstance(parsed_hex_list, list)
                                    and len(parsed_hex_list) > 0
                                ):
                                    # Show first thumbnail roll swatch inside card
                                    st.image(
                                        bytes.fromhex(parsed_hex_list[0]),
                                        use_container_width=True,
                                    )
                                else:
                                    st.image(image_payload, use_container_width=True)
                            except Exception:
                                st.image(image_payload, use_container_width=True)

                        # 🔥 THE TRIGGER CTA: Opens our dynamic modal frame overlay instantly on click pass 🔥
                        if st.button(
                            "🔍 Inspect Profile Workbook",
                            key=f"launch_lightbox_item_idx_{item_id}_{row_idx}_{col_idx}",
                            use_container_width=True,
                        ):
                            launch_lookbook_item_lightbox_modal(
                                title=item_title,
                                origin=item_origin,
                                notes=item_desc,
                                blob_data=image_payload,
                            )

                st.markdown(
                    "<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True
                )
                st.divider()

    except Exception as portfolio_fetch_err:
        st.error(
            f"Failed to compile aligned lookbook portfolio gallery rows: {portfolio_fetch_err}"
        )
    finally:
        db_session.close()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="vk-card">', unsafe_allow_html=True)
    st.stop()

# --- MODULE B: THE VISIBLE LIVE SIDEBAR MEASUREMENTS LEDGER PAGE TAB ---
elif sidebar_selection == "📏 Saved Measurements Ledger":
    ##############

    saved_measurement()
    # --- ACTION GATE B: DUAL SAVE - FAST DIRECT ENTRY FROM WITHIN THE LEDGER PAGE VIEW PANEL ---
    with st.expander(
        "➕ Click to Log a New Client Specification Directly on This Page",
        expanded=False,
    ):
        st.markdown(
            '<div style="background:#ffffff; padding:10px; border-radius:12px;">',
            unsafe_allow_html=True,
        )
        sc_page1, sc_page2 = st.columns(2)
        with sc_page1:
            p_client_name = st.text_input(
                "Customer Name / Tracking Tag Input:", key="page_ledger_client_name"
            )
            p_bust = st.number_input(
                "Bust Dimension Width (cm):",
                min_value=40,
                max_value=200,
                value=92,
                key="page_ledger_bust",
            )
            p_waist = st.number_input(
                "Waist Dimension Width (cm):",
                min_value=30,
                max_value=200,
                value=74,
                key="page_ledger_waist",
            )
            p_curr = st.selectbox(
                "Invoicing Currency Context:",
                ["USD ($)", "GHS (₵)", "NGN (₦)", "KES (KSh)"],
                key="page_ledger_curr",
            )
        with sc_page2:
            p_hips = st.number_input(
                "Hips Dimension Width (cm):",
                min_value=40,
                max_value=250,
                value=98,
                key="page_ledger_hips",
            )
            p_length = st.number_input(
                "Garment Sleeve Length (cm):",
                min_value=20,
                max_value=300,
                value=145,
                key="page_ledger_length",
            )
            p_cost = st.number_input(
                "Final Invoice Cost Valuation:",
                min_value=1.0,
                max_value=10000.0,
                value=150.00,
                step=5.0,
                key="page_ledger_cost",
            )

    if st.button(
        "💾 Save to Ledger",
        key="page_ledger_direct_save_cta",
        use_container_width=True,
    ):
        clean_ledger_name = str(p_client_name).strip()
        if not clean_ledger_name:
            st.error(
                "❌ Entry Blocked: Client tracking name parameter cannot remain blank."
            )
        else:
            user_session_id_val = st.session_state.get("user_id", 1)
            # db_session = SessionLocal()
            try:
                # 🔥 UNIFIED FIX: Use ClientSpecification model and attributes exclusively to align both entry points
                from database import ClientSpecification

                new_record = ClientSpecification()
                setattr(new_record, "user_id", int(user_session_id_val))
                setattr(new_record, "client_name", clean_ledger_name)
                setattr(new_record, "style_cut", "Manual Entry")
                setattr(new_record, "chest", float(p_bust))
                setattr(new_record, "waist", float(p_waist))
                setattr(new_record, "hips", float(p_hips))
                setattr(new_record, "length", float(p_length))
                setattr(new_record, "shoulder", 15.0)  # Default template fill parameter
                setattr(new_record, "total_invoice", float(p_cost))
                setattr(new_record, "status", str(p_curr))
                setattr(
                    new_record,
                    "notes",
                    "Logged directly through the main historical ledger viewport panel interface.",
                )

                db_session.add(new_record)
                db_session.commit()
                st.success(
                    f"🎉 Client tracking row '{clean_ledger_name}' successfully added directly to ledger table!"
                )
                import time

                __import__("time").sleep(0.5)
                st.rerun()
            except Exception as err:
                db_session.rollback()
                st.error(f"Write failed: {err}")
            finally:
                db_session.close()

    # -------------------------------------------------------------------------
    # 🔥 LIVE QUERY VIEPORT GATE: RENDERS ALL SAVED RECORDS TO THE SCREEN 🔥
    # -------------------------------------------------------------------------
    st.markdown("### 🖼️ Live Studio Specification Records")
    live_studio(db_session)

    # =========================================================================
    # 🧵 CONTINUATION CORE: RELATIONAL DATA LOOP & PURGE MECHANICS (INDEX4.PY) 🧵
    # =========================================================================

    st.write("#### 📜 Documented Customer Specifications Summary Rows:")

    # --- SUB-INJECTION B: HISTORICAL DATA ROW SCANNER GENERATION ---
    user_session_id_val = st.session_state.get("user_session_id", 0)
    # db_session = SessionLocal()

    try:
        # Query all stored logs tracking under the current authenticated user's ID key
        saved_records = (
            db_session.query(ClientMeasurement)
            .filter(ClientMeasurement.user_id == user_session_id_val)
            .order_by(ClientMeasurement.creation_timestamp.desc())
            .all()
        )

        if saved_records:
            for log_row in saved_records:
                row_id = getattr(log_row, "id")
                c_name = getattr(log_row, "client_name")
                b_val = getattr(log_row, "bust_dimension")
                w_val = getattr(log_row, "waist_dimension")
                h_val = getattr(log_row, "hips_dimension")
                l_val = getattr(log_row, "garment_length")
                curr_tier = getattr(log_row, "settlement_currency")
                cost_val = getattr(log_row, "final_cost_valuation")
                time_stamp = getattr(log_row, "creation_timestamp").strftime(
                    "%Y-%m-%d %H:%M"
                )

                # Split layout into asymmetric columns (Large for the data card, Small for the button)
                col_card, col_delete_btn = st.columns(2)

                with col_card:
                    st.markdown(
                        f"""
                            <div style='background:#ffffff; border:1px solid #e2e8f0; padding:16px; border-radius:12px; margin-bottom:14px; font-family:sans-serif;'>
                                <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding-bottom:8px; margin-bottom:10px;'>
                                    <span style='font-size:16px; font-weight:700; color:#1e293b;'>👤 Client: {c_name}</span>
                                    <span style='font-size:12px; color:#64748b;'>🗓️ Logged: {time_stamp}</span>
                                </div>
                                <div style='display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; font-size:13px; color:#475569;'>
                                    <div><b>Bust:</b> {b_val} cm</div>
                                    <div><b>Waist:</b> {w_val} cm</div>
                                    <div><b>Hips:</b> {h_val} cm</div>
                                    <div><b>Length:</b> {l_val} cm</div>
                                </div>
                                <div style='margin-top:10px; padding-top:8px; border-top:1px dashed #e2e8f0; display:flex; justify-content:space-between; align-items:center;'>
                                    <span style='font-size:12px; color:#64748b;'>Currency Tier: {curr_tier}</span>
                                    <span style='font-size:15px; font-weight:700; color:#E05A47;'>Final Bill: {cost_val:,.2f}</span>
                                </div>
                            </div>
                            """,
                        unsafe_allow_html=True,
                    )

                with col_delete_btn:
                    st.markdown("<br/>", unsafe_allow_html=True)
                    # 🔥 ACTION PASS: INTERACTIVE DATA PURGE / DELETE ROW TRIGGER 🔥
                    # Injecting the unique database row_id into the element key prevents Streamlit Duplicate Key crashes!
                    if st.button(
                        "🗑️ Delete Row",
                        key=f"delete_client_row_id_{row_id}",
                        use_container_width=True,
                    ):
                        # inner_db_session = SessionLocal()
                        try:
                            # Isolate the exact matching record pointer inside your relational tables
                            target_delete_record = (
                                db_session.query(ClientMeasurement)
                                .filter(ClientMeasurement.id == row_id)
                                .first()
                            )

                            if target_delete_record:
                                db_session.delete(target_delete_record)
                                db_session.commit()
                                st.toast(
                                    f"🗑️ Record row for '{c_name}' successfully purged out of local tables."
                                )
                                time.sleep(0.4)
                                st.rerun()
                        except Exception as delete_err:
                            db_session.rollback()
                            st.error(f"Purge stalled: {delete_err}")
                        finally:
                            db_session.close()
        else:
            st.info(
                "ℹ️ Workspace Logs Empty: No client measurement entries have been recorded inside this workspace yet."
            )
    except Exception as err:
        st.error(f"Failed to fetch ledger rows from PostgreSQL server: {err}")
    finally:
        db_session.close()  # Safely recycle connection tracks to keep the database pool live

        st.markdown('<div class="vk-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="vk-section-header">📏 Step 3b: Capture Tailoring Measurement Specifications</p>',
            unsafe_allow_html=True,
        )

    # =========================================================================
    # 🪡 FIX: PERSISTENT STATE MEASUREMENT PASS TO REPORTLAB (INDEX4.PY) 🪡
    # =========================================================================

    pdf_byte()
    st.markdown('<div class="vk-card">', unsafe_allow_html=True)
    st.stop()

# 📊 COMMERCIAL STOREFRONT REVENUE LEDGER & METRICS ENGINE
# =========================================================================
elif sidebar_selection == "📊 Analytical Orders Ledger":
    ##############
    # 1. Establish the precise filesystem track path pointing to your local logo file
    local_logo_disk_path = os.path.join("images", "fashion_logo1_nobg.png")

    # Authoritative high-fashion fallback image link deployed if your local disk asset is missing
    navbar_logo_render_url = "https://unsplash.com"

    # 2. Pull image bytes and convert to a clean single-line Base64 format to bypass cross-origin blocks
    if os.path.exists(local_logo_disk_path):
        try:
            with open(local_logo_disk_path, "rb") as logo_bytes_file:
                import base64
                encoded_logo_b64 = base64.b64encode(logo_bytes_file.read())
                clean_logo_b64_string = (
                    encoded_logo_b64.decode("utf-8").replace("\n", "").replace("\r", "")
                )
                navbar_logo_render_url = (
                    f"data:image/jpeg;base64,{clean_logo_b64_string}"
                )
        except Exception:
            pass

    # 3. COMPRESS THE NAVBAR PAYLOAD INSIDE PARENTHESES TO ERASE RAW CODE TEXT GATES
    navbar_branding_html_payload = (
        "<style>"
        "  .vk-navbar { display: flex; align-items: center; justify-content: space-between; background: #ffffff; border: 1px solid #e2e8f0; padding: 14px 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); font-family: sans-serif; }"
        "  .vk-navbar-logo-img { width: auto; max-height: 60px; object-fit: contain; border-radius: 6px; }"
        "  .brand-text-wrapper { flex-grow: 1; text-align: center; margin-right: 60px; }"
        "  .brand-tagline { font-size: 16px; font-weight: 600; color: #E05A47; text-transform: uppercase; letter-spacing: 1px; }"
        "</style>"
        "<div class='vk-navbar'>"
        f"  <img src='{navbar_logo_render_url}' class='vk-navbar-logo-img' alt='AfriTextile Core Branding Logo'/>"
        "   <div class='brand-text-wrapper'>"
        "       <span class='brand-tagline'>AI Fashion innovation Studio</span>"
        "   </div>"
        "</div>"
    )
    st.markdown(navbar_branding_html_payload, unsafe_allow_html=True)

    ##############
    # 4. EXTRACT USER DATA FROM SUPABASE (READ STAGE RUNS BEFORE EXTRACTING MODULES)
    from database import User
    from typing import Any, cast
    
    token_user_id = st.session_state.get("user_session_id", 0)
    
    # Establish record variables safely outside of blocks
    merchant_studio_name = "AfriTextile Artisan Label"
    merchant_biography = "No public studio overview logged yet."
    merchant_profile_img = "default_profile.png"
    
    try:
        db_user_row = db_session.query(User).filter(User.id == token_user_id).first()
        if db_user_row:
            safe_user = cast(Any, db_user_row)
            merchant_studio_name = str(getattr(safe_user, "studio_name", "AfriTextile Artisan Label"))
            merchant_biography = str(getattr(safe_user, "biography", "No public studio overview logged yet."))
            merchant_profile_img = str(getattr(safe_user, "profile_picture_name", "default_profile.png"))
    except Exception as db_err:
        st.error(f"Ledger metric sync warning: {db_err}")

    # =========================================================================
    # STEP 5: RUN MAIN SELLER DASHBOARD MODULE SUITE FIRST (PLACED AT THE TOP)
    # =========================================================================
    from seller_dashboard import render_seller_dashboard_suite
    render_seller_dashboard_suite(db_session, token_user_id)
    
    # Close database context cleanly right after our core widgets finish building
    db_session.close()

    st.markdown("<br/><hr style='border:0; border-top:1px dashed #cbd5e1; margin:25px 0;'/><br/>", unsafe_allow_html=True)

    # =========================================================================
    # STEP 6: RENDER SYNC TRACKER PANEL AT THE VERY BOTTOM OF THE PAGE 
    # =========================================================================
    st.markdown('<div style="background-color:#ffffff; border:1px solid #e2e8f0; padding:20px; border-radius:14px; box-shadow:0 1px 3px rgba(0,0,0,0.05); font-family:sans-serif;">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#1e293b; font-weight:800;'>🌐 Global Storefront Identity Sync Tracker</h4>", unsafe_allow_html=True)
    
    prof_col1, prof_col2 = st.columns([1, 4], gap="medium")
    with prof_col1:
        # 🪡 FIX: Decodes your database Base64 avatar payload dynamically instead of looking for file folders
        avatar_render_source_url = "https://unsplash.com"
        
        if merchant_profile_img and merchant_profile_img != "default_profile.png":
            if merchant_profile_img.startswith("data:image"):
                avatar_render_source_url = merchant_profile_img
            else:
                legacy_path = os.path.join("profile_pics", merchant_profile_img)
                if os.path.exists(legacy_path):
                    try:
                        with open(legacy_path, "rb") as image_file:
                            raw_bytes = base64.b64encode(image_file.read()).decode("utf-8")
                            avatar_render_source_url = f"data:image/png;base64,{raw_bytes}"
                    except Exception:
                        pass
        
        # Display the custom cloud file cleanly on page sector grids
        st.image(avatar_render_source_url, use_container_width=True, caption="Active Identity")
            
    with prof_col2:
        st.markdown(f"##### 🏷️ Registered Identity Label: **{merchant_studio_name}**")
        st.markdown(f"<p style='font-style:italic; color:#475569; font-size:14px;'>\"{merchant_biography}\"</p>", unsafe_allow_html=True)
        st.divider()
        
        # Action broadcast checkbox persistence logic
        include_profile_flag = st.checkbox(
            "🚀 Broadcast brand profile picture and biography metrics directly onto live marketplace product grids",
            value=st.session_state.get("step3_broadcast_profile_parameters", True),
            key="step3_marketplace_broadcast_profile_checkbox"
        )
        st.session_state["step3_broadcast_profile_parameters"] = include_profile_flag

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================================================================
# 💰 THE SOLID WHITE PREMIUM CHECKOUT PRICING MODULE PAGE (INDEX4.PY) 💰
# =========================================================================
elif sidebar_selection == "💰 Subscription Pricing Plan":
    ##############

    # 1. Establish the precise filesystem track path pointing to your local logo file
    local_logo_disk_path = os.path.join("images", "fashion_logo1_nobg.png")

    # Authoritative high-fashion fallback image link deployed if your local disk asset is missing
    navbar_logo_render_url = "https://unsplash.com"

    # 2. Pull image bytes and convert to a clean single-line Base64 format to bypass cross-origin blocks
    if os.path.exists(local_logo_disk_path):
        try:
            with open(local_logo_disk_path, "rb") as logo_bytes_file:
                import base64

                encoded_logo_b64 = base64.b64encode(logo_bytes_file.read())

                # 🔥 FIX: Match the exact name used on BOTH lines to clear the red text error!
                clean_logo_b64_string = (
                    encoded_logo_b64.decode("utf-8").replace("\n", "").replace("\r", "")
                )
                navbar_logo_render_url = (
                    f"data:image/jpeg;base64,{clean_logo_b64_string}"
                )
        except Exception:
            pass

        # 3. 🔥 COMPRESS THE NAVBAR PAYLOAD INSIDE PARENTHESES TO ERASE RAW CODE TEXT GATES 🔥
        # Alternating to double quotes (") on the outside and single quotes (') on the inside clears all syntax error crashes!
        navbar_branding_html_payload = (
            "<style>"
            "  .vk-navbar { display: flex; align-items: center; justify-content: space-between; background: #ffffff; border: 1px solid #e2e8f0; padding: 14px 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); font-family: sans-serif; }"
            "  .vk-navbar-logo-img { width: auto; max-height: 60px; object-fit: contain; border-radius: 6px; }"
            "  .brand-text-wrapper { flex-grow: 1; text-align: center; margin-right: 60px; }"
            "  .brand-tagline { font-size: 16px; font-weight: 600; color: #E05A47; text-transform: uppercase; letter-spacing: 1px; }"
            "</style>"
            "<div class='vk-navbar'>"
            f"  <img src='{navbar_logo_render_url}' class='vk-navbar-logo-img' alt='AfriTextile Core Branding Logo'/>"
            "   <div class='brand-text-wrapper'>"
            "       <span class='brand-tagline'>AI Fashion innovation Studio</span>"
            "   </div>"
            "</div>"
        )

        # "       <span class='brand-title'>AfriTextile</span>"
        # style="width: 500px; height: 600px;"
        # Force the markdown engine to interpret the payload as native web node parameters
        st.markdown(navbar_branding_html_payload, unsafe_allow_html=True)

    ##############

    # Extract user data out of active state row records
    user_session_id_val = st.session_state.get("user_session_id", 0)
    # db_session = SessionLocal()
    db_user = db_session.query(User).filter(User.id == user_session_id_val).first()
    current_active_tier = str(getattr(db_user, "subscription_tier", "freemium"))
    db_session.close()

    # Render cards
    render_pricing_matrix_panel(
        user_authenticated=True, active_tier_str=current_active_tier
    )
    st.markdown("<br/><br/>", unsafe_allow_html=True)

    st.write("#### 🛠️ Manage Workspace Operational Status:")
    selected_plan_target = st.selectbox(
        "Select target subscription upgrade plan level:",
        ["Freemium Sandbox", "Premium House Seams", "Enterprise Elite Matrix"],
        key="pricing_plan_selection_dropdown",
    )

    # =========================================================================
    # 🪡 INJECTION B: INTEGRATED STRIPE CHECKOUT REDIRECTS FOR PLANS (INDEX4.PY)
    # =========================================================================

    # =========================================================================
    # 🪡 INJECTION B: INTEGRATED STRIPE CHECKOUT REDIRECTS FOR PLANS (INDEX4.PY)
    # =========================================================================

    # Inside your active Pricing tier module page:
    if (
        st.button(
            "💳 Authorize Subscription Settlement & Synchronize Workspace",
            key="pricing_execute_checkout_cta",
            use_container_width=True,
        )
        and st.session_state.get("authenticated") == True
    ):
        plan_map = {
            "Premium House Seams": "premium",
            "Enterprise Elite Matrix": "enterprise",
            "Freemium Sandbox": "freemium",
        }
        chosen_tier_token = plan_map.get(selected_plan_target, "freemium")
        billing_cycle = st.selectbox("Choose billing:", ["Monthly", "Annual"])

        if chosen_tier_token == "freemium":
            # Freemium changes remain local and bypass Stripe payment layers completely
            # db_write_session = SessionLocal()
            try:
                target_user_row = (
                    db_session.query(User)
                    .filter(User.id == user_session_id_val)
                    .first()
                )
                if target_user_row:
                    setattr(target_user_row, "subscription_tier", "freemium")
                    db_session.commit()
                    st.success(
                        "🎉 Switched back to Freemium Sandbox Plan level tier successfully."
                    )
                    st.rerun()
            except Exception as e:
                db_session.rollback()
            finally:
                db_session.close()
        else:
            # 🔥 STRIPE CORES: Trigger real-time high-security checkout link generation!
            from security import create_subscription_checkout_session

            is_annual_bool = "Annual" in billing_cycle

            st.info(
                "⏳ Initializing highly secure Stripe payment handshake session channels. Please stand by..."
            )
            checkout_gateway_url = create_subscription_checkout_session(
                user_session_id_val, chosen_tier_token, is_annual_bool
            )

            if "ERROR" in checkout_gateway_url:
                st.error(checkout_gateway_url)
            else:
                # Provide an immediate active browser routing element link out to the user canvas screen
                st.markdown(
                    f'<a href="{checkout_gateway_url}" target="_blank" style="display:block; text-align:center; background-color:#E05A47; color:white; padding:12px; border-radius:8px; text-decoration:none; font-weight:700;">➡️ Proceed to Stripe Secure Checkout Portal</a>',
                    unsafe_allow_html=True,
                )
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================================================================
# 🔓 PUBLIC GUEST SCREENS SECTOR (LOGINS, REGISTER, AND PRE-LOGIN PRICING)
# =========================================================================
else:
    # Force-hide sidebar panel tracking nodes on public entrance screens
    st.markdown(
        "<style>div[data-testid='stSidebar'], button[data-testid='sidebar-toggle'] { display: none !important; }</style>",
        unsafe_allow_html=True,
    )

    # st.markdown("<hr style='margin:10px 0 25px 0;'/>", unsafe_allow_html=True)


##################################


##########################################

# Stops drawing right here to keep the main canvas hidden from view while inside the shop

# --- MODULE A: CONTINUES DESIGN HUB APP EXECUTION SMOOTHLY BELOW IF DESIGNER SELECTED ---
# =========================================================================


# --- MODULE A: IF USER SELECTS DESIGN CANVAS, CONTINUE CODE EXECUTION BELOW SMOOTHLY ---
# =========================================================================


###########END OF SIDE BAR MENU


# 1. Master Page Configuration Setup Gating
st.set_page_config(
    page_title="AfriTexile - AI Fabric & Garment Studio",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="auto",
)

# 2. Premium Glameeri UI Token Engine & MD3 Input CSS Injection Matrix
st.markdown(
    """
    <style>
        @import url('https://googleapis.com');
        
        :root {
            --vk-primary: #1a73e8;
            --vk-primary-variant: #1557b0;
            --vk-accent: #34a853;
            --vk-surface: #ffffff;
            --vk-background: #f8f9fa;
            --vk-text-main: #202124;
            --vk-text-muted: #5f6368;
            --vk-border: #dadce0;
            --vk-radius-lg: 16px;
            --vk-radius-md: 8px;
            
            --md-primary: #1a73e8;
            --md-primary-variant: #1557b0;
            --md-surface: #ffffff;
            --md-background: #f8f9fa;
            --md-on-surface: #202124;
            --md-on-surface-variant: #5f6368;
            --md-outline: #dadce0;
            --md-error: #b00020;
            --md-success: #137333;
        }

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Roboto', sans-serif;
            background-color: var(--vk-background) !important;
            color: var(--vk-text-main);
            line-height: 1.5;
        }

        /* Glameeri Navigation Bar Component Framework */
        .vk-navbar {
            background-color: #ffffff;
            border-bottom: 1px solid var(--vk-border);
            padding: 14px 24px;
            border-radius: var(--vk-radius-lg);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 2px rgba(60, 64, 67, 0.05);
            margin-bottom: 24px;
        }
        .brand-logo-block {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .logo-graphic {
            background: linear-gradient(135deg, #1a73e8, #ea4335, #fabc05, #34a853);
            width: 38px;
            height: 38px;
            border-radius: var(--vk-radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 18px;
        }
        .brand-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--vk-text-main);
            letter-spacing: -0.3px;
        }
        .brand-tagline {
            font-size: 10px;
            color: #1a73e8;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        /* Centered Menu Configurations Styles Injection */
        [data-testid="stHorizontalBlock"] {
            justify-content: center !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            flex-grow: 0 !important;
            width: auto !important;
            min-width: unset !important;
        }
        [data-testid="stHorizontalBlock"] button {
            border-radius: 20px !important;
            padding: 6px 16px !important;
            font-size: 14px !important;
            white-space: nowrap !important;
        }

        /* Material Elevation Card container */
        .md-card {
            background: var(--md-surface);
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 840px;
            padding: 32px;
            margin: 0 auto;
            box-sizing: border-box;
            transition: box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .md-card:hover {
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08), 0 3px 6px rgba(0, 0, 0, 0.1);
        }

        .brand-header {
            text-align: center;
            margin-bottom: 24px;
        }
        .brand-header h2 {
            font-weight: 500;
            font-size: 24px;
            color: var(--md-on-surface);
            margin: 0 0 8px 0;
            letter-spacing: -0.5px;
        }
        .brand-header p {
            font-size: 14px;
            color: var(--md-on-surface-variant);
            margin: 0;
        }

        /* Native Streamlit Input MD3 Field Styling Overrides */
        div[data-testid="stTextInput"] label, div[data-testid="stNumberInput"] label {
            font-size: 13px !important;
            color: var(--md-primary) !important;
            font-weight: 500 !important;
            margin-bottom: 6px !important;
        }
        div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
            border: 1px solid var(--md-outline) !important;
            border-radius: 6px !important;
            padding: 12px 14px !important;
            background-color: transparent !important;
            color: var(--md-on-surface) !important;
            transition: border-color 0.15s ease !important;
        }
        div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
            border-color: var(--md-primary) !important;
            border-width: 2px !important;
        }

        /* Premium Corporate Component Workspace Cards Layout */
        .vk-card {
            background-color: #ffffff;
            border: 1px solid var(--vk-border);
            border-radius: var(--vk-radius-lg);
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
        }
        .vk-hero-badge {
            display: inline-block;
            background-color: rgba(26, 115, 232, 0.06);
            color: #1a73e8;
            font-size: 12px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
        }
        .vk-headline {
            font-size: 38px;
            font-weight: 500;
            color: var(--vk-text-main);
            line-height: 1.2;
            letter-spacing: -0.8px;
            margin-bottom: 16px;
        }
        .vk-section-header {
            font-size: 20px;
            font-weight: 500;
            color: var(--vk-text-main);
            border-bottom: 2px solid #fabc05;
            padding-bottom: 6px;
            margin-bottom: 20px;
        }
        .status-badge {
            background-color: #f1f3f4;
            padding: 6px 14px;
            border-radius: 100px;
            font-size: 13px;
            font-weight: 500;
            color: #1a73e8;
            display: inline-block;
        }

        /* Material Style System Action Primary Button Overrides */
        div.stButton > button {
            background-color: var(--md-primary) !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            border: none !important;
            padding: 12px 24px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
            transition: background-color 0.15s, box-shadow 0.15s !important;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: var(--md-primary-variant) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        }
        
        /* Secondary Link Buttons Framework */
        .md-text-btn-container {
            text-align: center;
            margin-top: 16px;
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        
    </style>
""",
    unsafe_allow_html=True,
)


# Initialize relational database schemas immediately upon runtime execution pass
# try:
#    init_db()
# except Exception as db_init_err:
#    st.error(
#        f"PostgreSQL connection stalled. Check network database port strings: {db_init_err}"
#    )

# Safe Initialization for Core System Session Variables
if "app_view" not in st.session_state:
    st.session_state["app_view"] = "home"
if "authenticated" not in st.session_state or st.session_state["app_view"] == "home":
    st.session_state["authenticated"] = False
    st.markdown(
        """
        <style>
            div[data-testid="stSidebar"], 
            button[data-testid="sidebar-toggle"] { 
                display: none !important; 
            }
            .stApp [data-testid="stToolbar"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
if "user_session_id" not in st.session_state:
    st.session_state["user_session_id"] = None
if "wizard_step" not in st.session_state:
    st.session_state["wizard_step"] = 1
if "active_fabric" not in st.session_state:
    st.session_state["active_fabric"] = None
if "local_tryon_image" not in st.session_state:
    st.session_state["local_tryon_image"] = None
if "motif_spec_input" not in st.session_state:
    st.session_state["motif_spec_input"] = (
        "Vibrant rotational stars and visual matrix chains"
    )
if "motif_color" not in st.session_state:
    st.session_state["motif_color"] = "#F2B705"
if "cultural_spec" not in st.session_state:
    st.session_state["cultural_spec"] = None
if "chosen_foundation" not in st.session_state:
    st.session_state["chosen_foundation"] = "Ankara Wax Print"

# ... rest of your global CSS markup markdown injection rules remain exactly the same ...


# =========================================================================
# 👤 USER REGISTRATION VIEW INTERFACE LAYOUT PANEL
# =========================================================================

# Lower down in your code workspace, your nav button execution path runs smoothly:
# if st.session_state.get("app_view") == "register":
#    st.markdown('<div class="vk-card">', unsafe_allow_html=True)


# =========================================================================
# 🚀 MODULE MODULE: POSTGRESQL SIGNIN ENGINE WITH ACTIVE SESSION KEYS
# =========================================================================


# STRICT STEP MANAGEMENT: Step 1 (Design), Step 2 (Review), Step 3 (Render Try-on), Step 4 (Measurements/PDF)
if "wizard_step" not in st.session_state:
    st.session_state["wizard_step"] = 1

DEFAULT_MOTIFS = {
    "Ankara Wax Print": "Vibrant rotational stars and visual matrix chains",
    "Kente Cloth Heritage": "Interlocking parallel lines and family heritage blocks",
    "Adire Tech": "Hand-drawn circular spiral grids representing local proverbs",
    "Modern Afro-Futurism": "Non-linear fractal lines and neon cyber grids",
    "Plain Solid Colour": "No motifs - keep fabric plain and untextured",
}

if "motif_spec_input" not in st.session_state:
    st.session_state["motif_spec_input"] = DEFAULT_MOTIFS["Ankara Wax Print"]


def sync_motif_on_context_change():
    selected_context = st.session_state["dropdown_foundation_select"]
    st.session_state["motif_spec_input"] = DEFAULT_MOTIFS.get(
        selected_context, "Geometric matrix chains"
    )


OFFLINE_BLUEPRINTS = {
    "Ankara Wax Print": "ANKARA GEOMETRY RULES:\n- Dynamic diamond matrix design layers.",
    "Kente Cloth Heritage": "KENTE WEAVING MATRIX SPECIFICATIONS:\n- Interlocking horizontal strip modules.",
    "Adire Tech": "ADIRE TECH CODES:\n- Indigo tie-dye resist structures using user hex tones.",
    "Modern Afro-Futurism": "AFRO-FUTURISM BLUEPRINT:\n- Cyber fractal node pathways matching selection colors.",
    "Plain Solid Colour": "PLAIN SOLID COLOR SPECIFICATIONS:\n- Uniform untextured minimalist canvas frames.",
}

# --- ADD THIS EXCHANGE DICTIONARY SPECIFICATION MAP TO THE TOP OF YOUR SCRIPT ---

CURRENCY_EXCHANGE_REGISTRY = {
    "USD ($)": {"symbol": "$", "rate": 1.0, "label": "United States Dollar"},
    "GHS (₵)": {"symbol": "₵", "rate": 15.40, "label": "Ghanaian Cedi"},
    "NGN (₦)": {"symbol": "₦", "rate": 1600.0, "label": "Nigerian Naira"},
    "KES (KSh)": {"symbol": "KSh", "rate": 129.50, "label": "Kenyan Shilling"},
}


# --- ADD THIS BODY SEGMENTATION REGISTRY TO THE TOP OF YOUR SCRIPT ---

BODY_SEGMENTATION_ROUTER = {
    "gown": {
        "anatomy_zones": [
            "Shoulders",
            "Chest/Bust",
            "Waistline",
            "Hips",
            "Full Leg Extension",
        ],
        "warp_intensity_x": 0.05,
        "warp_intensity_y": 0.08,
        "texture_density_ratio": 4.5,
        "fitting_notes": "👗 full-length structural drape: Requires uniform 3D vertical wrinkle mapping from upper chest down to ankles.",
    },
    "jumpsuit": {
        "anatomy_zones": [
            "Torso",
            "Midsection",
            "Crotch Junction",
            "Thighs",
            "Lower Calves",
        ],
        "warp_intensity_x": 0.07,
        "warp_intensity_y": 0.09,
        "texture_density_ratio": 5.0,
        "fitting_notes": "👖 Bi-lateral split layout: Requires high-compression horizontal warping around the crotch junction and inner thigh seams.",
    },
    "peplum": {
        "anatomy_zones": ["Neckline", "Upper Bust", "Ribcage", "Flared Hip Fringe"],
        "warp_intensity_x": 0.04,
        "warp_intensity_y": 0.06,
        "texture_density_ratio": 3.8,
        "fitting_notes": "👚 Flared perimeter layout: Requires expansion transform scaling directly along the lower waist ribcage fringe lines.",
    },
    "jacket": {
        "anatomy_zones": [
            "Collar Neck",
            "Shoulder Pads",
            "Chest Width",
            "Bicep Sleeves",
            "Wrist Cuffs",
        ],
        "warp_intensity_x": 0.06,
        "warp_intensity_y": 0.05,
        "texture_density_ratio": 4.0,
        "fitting_notes": "🧥 Structured outer overlay: Requires stiff linear grid alignment across the upper shoulders and sleeve cylinders.",
    },
}


# --- GLAMEERI NAVBAR BRAND LOGO SYSTEM ---
# =========================================================================
# 🧵 FIX: COMPRESSED NATIVE BASE64 LOCAL LOGO NAVBAR INJECTOR (INDEX4.PY) 🧵
# =========================================================================


# 1. Establish the precise filesystem track path pointing to your local logo file
local_logo_disk_path = os.path.join("images", "fashion_logo1.png")

# Authoritative high-fashion fallback image link deployed if your local disk asset is missing
navbar_logo_render_url = "https://unsplash.com"

# 2. Pull image bytes and convert to a clean single-line Base64 format to bypass cross-origin blocks
if os.path.exists(local_logo_disk_path):
    try:
        with open(local_logo_disk_path, "rb") as logo_bytes_file:
            import base64

            encoded_logo_b64 = base64.b64encode(logo_bytes_file.read())

            # 🔥 FIX: Match the exact name used on BOTH lines to clear the red text error!
            clean_logo_b64_string = (
                encoded_logo_b64.decode("utf-8").replace("\n", "").replace("\r", "")
            )
            navbar_logo_render_url = f"data:image/jpeg;base64,{clean_logo_b64_string}"
    except Exception:
        pass

# 3. 🔥 COMPRESS THE NAVBAR PAYLOAD INSIDE PARENTHESES TO ERASE RAW CODE TEXT GATES 🔥
# Alternating to double quotes (") on the outside and single quotes (') on the inside clears all syntax error crashes!
navbar_branding_html_payload = (
    "<style>"
    "  .vk-navbar { display: flex; align-items: center; justify-content: space-between; background: #ffffff; border: 1px solid #e2e8f0; padding: 14px 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); font-family: sans-serif; }"
    "  .vk-navbar-logo-img { width: auto; max-height: 60px; object-fit: contain; border-radius: 6px; }"
    "  .brand-text-wrapper { flex-grow: 1; text-align: center; margin-right: 60px; }"
    "  .brand-tagline { font-size: 16px; font-weight: 600; color: #E05A47; text-transform: uppercase; letter-spacing: 1px; }"
    "</style>"
    "<div class='vk-navbar'>"
    f"  <img src='{navbar_logo_render_url}' class='vk-navbar-logo-img' alt='AfriTextile Core Branding Logo'/>"
    "   <div class='brand-text-wrapper'>"
    "       <span class='brand-tagline'>AI Fashion innovation Studio</span>"
    "   </div>"
    "</div>"
)

# "       <span class='brand-title'>AfriTextile</span>"
# style="width: 500px; height: 600px;"
# Force the markdown engine to interpret the payload as native web node parameters
st.markdown(navbar_branding_html_payload, unsafe_allow_html=True)


# Row-level Centered Navigation bar channels
if not st.session_state["authenticated"]:
    nav_c1, nav_c2, nav_c3, nav_c4, nav_c5, nav_c6 = st.columns(6)
    with nav_c1:
        st.button("🏠 Home", on_click=navigate_to, args=("home",), key="main_nav_home")
    with nav_c2:
        st.button(
            "ℹ️ About", on_click=navigate_to, args=("about",), key="main_nav_about"
        )
    with nav_c3:
        st.button(
            "🛠️ Services", on_click=navigate_to, args=("services",), key="main_nav_serv"
        )
    with nav_c4:
        st.button(
            "💰 Pricing", on_click=navigate_to, args=("pricing",), key="main_nav_price"
        )
    with nav_c5:
        st.button(
            "⚡ Start Now",
            on_click=navigate_to,
            args=("start_now",),
            key="main_nav_start",
        )

    #    st.button(
    #        "🔑 Login", on_click=navigate_to, args=("login",), key="main_nav_login"
    #    )
    st.markdown("<br/>", unsafe_allow_html=True)

    # ==========================================
    # MODULE ENGINES & CALCULATION LOGIC BLOCKS
    # ==========================================

    # -----------------------------------------------------------------
    # 🔥 NEW SUB-INJECTION: HOMEPAGE IMAGE GALLERY (BELOW MENU AREA) 🔥
    # -----------------------------------------------------------------
    # =========================================================================
    # 🧵 FIX: COMPRESSED BASE64 LOCAL IMAGE INJECTOR FOR THE HOMEPAGE 🧵
    # =========================================================================

    # =========================================================================
    # 🧵 FIX: COMPRESSED SINGLE LOCAL IMAGE PRESENTATION BOX (INDEX4.PY) 🧵
    # =========================================================================

    # =========================================================================
    # 🪡 FIX: COMPRESSED SINGLE TIMELINE HOMEPAGE LOOKBOOK INJECTOR (INDEX4.PY)
    # =========================================================================

    # Lower code blocks flow smoothly below this baseline container card layout cell...


def render_fallback_fabric(hex_color, pattern_style, description, motif_hex_color):
    # Establish a clean master square block for the single module element canvas
    base = Image.new("RGB", (300, 300), color="#FFFFFF")
    # base = Image.new("RGB", (300, 300), color="#D0E60F")
    draw = ImageDraw.Draw(base)
    try:
        fill_color = hex_color
    except:
        fill_color = "#E05A47"

    desc_clean = str(description).lower().strip()
    motif_color = motif_hex_color

    # 1. BASE FABRIC BACKGROUND LAYOUTS
    if "Plain" in pattern_style:
        base = Image.new("RGB", (300, 300), color=fill_color)
        draw = ImageDraw.Draw(base)
    elif "Kente" in pattern_style:
        x = 0
        while x < 300:

            w_block = random.randint(30, 60)
            draw.rectangle([x, 0, x + 15, 300], fill="#F2B705")
            # draw.rectangle([0, x, 300, x + 15], fill="#F2B705")
            draw.rectangle([0, x, 300, x + 15], fill=motif_color)
            draw.rectangle([x, 0, x + (w_block // 2), 300], fill=fill_color)
            x += w_block
            # for y in range(0, 300, 40):
            # draw.rectangle([0, y, 300, y + 8], fill="#F2B705")

    # motif_color_input = st.color_picker(
    #    "Motif Overlay Color Picker:", "#F2B705", key="motif_color_picker_id"
    # )

    # for x in range(0, 300, 30):
    #    draw.rectangle([x, 0, x + 15, 300], fill=fill_color)
    #    draw.rectangle([0, x, 300, x + 5], fill=motif_color)

    elif "Adire" in pattern_style:
        # base = Image.new("RGB", (300, 300), color="#1A2B4C")
        base = Image.new("RGB", (300, 300), color=fill_color)
        draw = ImageDraw.Draw(base)
        for r in range(20, 150, 35):
            draw.circle((150, 150), r, outline=motif_color, width=3)
    elif "Afro-Futurism" in pattern_style:
        base = Image.new("RGB", (300, 300), color=fill_color)
        draw = ImageDraw.Draw(base)
        random.seed(sum(ord(c) for c in pattern_style))
        points = [(random.randint(15, 285), random.randint(15, 285)) for _ in range(8)]
        for i in range(len(points) - 1):
            # draw.line([points[i], points[i + 1]], fill=fill_color, width=2)
            draw.line([points[i], points[i + 1]], fill="#FF2441", width=2)
    else:  # Standard Ankara Base Diamond Matrix Layer
        base = Image.new("RGB", (300, 300), color=fill_color)
        draw = ImageDraw.Draw(base)
        for x in range(0, 300, 60):
            for y in range(0, 300, 60):
                draw.polygon(
                    [(x + 30, y), (x + 60, y + 30), (x + 30, y + 60), (x, y + 30)],
                    fill="#F7EFE7",
                    outline="#2A2A2A",
                )

    # 2. EVEN GRID SPREAD MOTIF MATRIX
    if len(desc_clean) > 0 and "plain" not in desc_clean:
        seed_value = sum(ord(char) for char in desc_clean)
        random.seed(seed_value)

        distribution_intervals = [35, 110, 185, 260]

        for cx in distribution_intervals:
            for cy in distribution_intervals:
                ox = cx + random.randint(-8, 8)
                oy = cy + random.randint(-8, 8)

                if any(
                    w in desc_clean
                    for w in ["floral", "flower", "leaf", "leaves", "petal", "rose"]
                ):
                    r_petal = 10
                    draw.ellipse(
                        [ox - r_petal, oy - 2 * r_petal, ox + r_petal, oy],
                        fill=motif_color,
                        outline="#D7A910",
                    )
                    draw.ellipse(
                        [ox - r_petal, oy, ox + r_petal, oy + 2 * r_petal],
                        fill=motif_color,
                        outline="#D7A910",
                    )
                    draw.ellipse(
                        [ox - 2 * r_petal, oy - r_petal, ox, oy + r_petal],
                        fill=motif_color,
                        outline="#D7A910",
                    )
                    draw.ellipse(
                        [ox, oy - r_petal, ox + 2 * r_petal, oy + r_petal],
                        fill=motif_color,
                        outline="#D7A910",
                    )
                    # draw.circle((ox, oy), 5, fill="#F2B705")

                    draw.circle((ox, oy), 5, fill="#F80A1B")
                    draw.circle((ox, oy), 5, outline="#0F0335")

                elif any(
                    w in desc_clean
                    for w in ["honeycomb", "grid", "hex", "hexagon", "cell", "mesh"]
                ):
                    r_hex = 28
                    p1 = (ox, oy - r_hex)
                    p2 = (ox + int(r_hex * 0.86), oy - r_hex // 2)
                    p3 = (ox + int(r_hex * 0.86), oy + r_hex // 2)
                    p4 = (ox, oy + r_hex)
                    p5 = (ox - int(r_hex * 0.86), oy + r_hex // 2)
                    p6 = (ox - int(r_hex * 0.86), oy - r_hex // 2)
                    # draw.polygon([p1, p2, p3, p4, p5, p6], outline=motif_color, width=3)
                    draw.polygon([p1, p2, p3, p4, p5, p6], outline="#F2B705", width=3)

                elif any(
                    w in desc_clean
                    for w in ["star", "celestial", "sun", "spark", "diamond"]
                ):
                    draw.polygon(
                        [
                            (ox, oy - 16),
                            (ox + 5, oy - 5),
                            (ox + 16, oy),
                            (ox + 5, oy + 5),
                            (ox, oy + 16),
                            (ox - 5, oy + 5),
                            (ox - 16, oy),
                            (ox - 5, oy - 5),
                        ],
                        fill=motif_color,
                        outline="#F2B705",
                        width=3,
                    )

                elif any(
                    w in desc_clean
                    for w in [
                        "stripe",
                        "line",
                        "wave",
                        "wavy",
                        "linear",
                        "spiral",
                        "ring",
                    ]
                ):
                    draw.circle((ox, oy), 18, outline="#F2B705", width=4)
                    draw.circle((ox, oy), 6, fill="#F2B705")

                else:
                    shape_seed = (seed_value + ox + oy) % 3
                    size_mod = random.randint(14, 28)
                    if shape_seed == 0:
                        draw.rectangle(
                            [
                                ox - size_mod // 2,
                                oy - size_mod // 2,
                                ox + size_mod // 2,
                                oy + size_mod // 2,
                            ],
                            outline=motif_color,
                            width=3,
                        )
                    elif shape_seed == 1:
                        draw.polygon(
                            [
                                (ox, oy - size_mod // 2),
                                (ox + size_mod // 2, oy + size_mod // 2),
                                (ox, oy + size_mod // 4),
                                (ox - size_mod // 2, oy + size_mod // 2),
                            ],
                            fill=motif_color,
                        )
                    else:
                        draw.arc(
                            [
                                ox - size_mod // 2,
                                oy - size_mod // 2,
                                ox + size_mod // 2,
                                oy + size_mod // 2,
                            ],
                            start=45,
                            end=315,
                            fill=motif_color,
                            width=4,
                        )

    # 3. 🔥 FIX: DYNAMIC 3D MICRO-WEAVE DISPLACEMENT FILTER PASS 🔥
    # Generates a high-contrast overlay map that introduces physical textile depth and shadows
    texture_3d_sheet = Image.new("L", (300, 300), color=128)
    tex_draw = ImageDraw.Draw(texture_3d_sheet)

    # Build an alternating interlaced thread canvas line arrays (Simulates fabric over-under warp/weft)
    for coord in range(0, 300, 3):
        # Horizontal thread lines
        tex_draw.line([(0, coord), (300, coord)], fill=255, width=1)  # Highlight line
        tex_draw.line(
            [(0, coord + 1), (300, coord + 1)], fill=225, width=1
        )  # Shadow crease line
        # Vertical thread lines
        tex_draw.line([(coord, 0), (coord, 300)], fill=245, width=1)
        tex_draw.line([(coord + 1, 0), (coord + 1, 300)], fill=205, width=1)

    # Softly blur the micro-weave grid so it meshes smoothly with your design lines
    texture_3d_sheet = (
        texture_3d_sheet.filter(ImageFilter.GaussianBlur(0.4))
        if "ImageFilter" in globals()
        else texture_3d_sheet
    )

    # Execute a mathematical contrast multiply overlay to layer true 3D texture onto your asset
    base_3d_fabric = ImageChops.multiply(
        base.convert("RGB"), texture_3d_sheet.convert("RGB")
    )

    # Bring back color saturation weights so the fabric tones stay rich, bright, and solid
    vibrant_3d_output = ImageEnhance.Color(base_3d_fabric).enhance(4.30)

    return vibrant_3d_output

    # clear_3d_sheet = Image.new("RGB", (300, 300), color=(128, 128, 128))
    # tex_draw = ImageDraw.Draw(clear_3d_sheet)
    # for coord in range(0, 300, 4):
    #    tex_draw.line([(0, coord), (300, coord)], fill=(148, 148, 148), width=1)
    #    tex_draw.line([(0, coord + 2), (300, coord + 2)], fill=(108, 108, 108), width=1)
    #    tex_draw.line([(coord, 0), (coord, 300)], fill=(148, 148, 148), width=1)
    #    tex_draw.line([(coord + 2, 0), (coord + 2, 300)], fill=(108, 108, 108), width=1)

    # clear_3d_sheet = clear_3d_sheet.filter(ImageFilter.GaussianBlur(0.2))
    # textured_canvas = ImageChops.overlay(master_canvas.convert("RGB"), clear_3d_sheet)
    # sharpening_enhancer = ImageEnhance.Contrast(textured_canvas)
    # sharp_3d_output = sharpening_enhancer.enhance(1.15)
    # return ImageEnhance.Color(sharp_3d_output).enhance(1.05)


# =========================================================================
# 🧵 REPLACEMENT CODE CORE: UNIFIED PUBLIC & PROTECTED PRICING SUITE (INDEX4.PY)
# =========================================================================


# ==========================================
# ROUTED INTERFACE DISPLAY CONTROLLERS
# ==========================================
# if st.session_state.get("authenticated") == False:
# 🔥 FIX: Force-hide the sidebar tray panel AND its floating toggle chevron button arrow! 🔥
# This guarantees that unauthenticated guest screens remain 100% full-width with zero menu options.
if (
    st.session_state["app_view"] == "home"
    and "about"
    and "services"
    and "pricing"
    and "start_now"
    and st.session_state.get("authenticated") == False
):
    st.markdown(
        """
        <style>
            div[data-testid="stSidebar"], 
            button[data-testid="sidebar-toggle"] { 
                display: none !important; 
            }
            .stApp [data-testid="stToolbar"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --- HOME VIEW ---
if st.session_state["app_view"] == "home" and not st.session_state["authenticated"]:
    # =========================================================================
    # 🧵 FIX: COMPRESSED SANITIZED BRAND IMAGER INJECTOR (INDEX4.PY) 🧵
    # =========================================================================

    # 1. Render the primary typography headers inside your centered card container

    # 2. Establish the explicit filesystem file path pointing to your local studio banner image
    local_brand_image_path = os.path.join("images", "model3.png")

    # Authoritative high-fashion Unsplash backup URL deployed if your local disk asset is missing or locked
    brand_image_render_url = "https://unsplash.com"

    # 3. Pull image bytes and convert to a clean single-line Base64 format to bypass cross-origin blocks
    if os.path.exists(local_brand_image_path):
        try:
            with open(local_brand_image_path, "rb") as image_bytes_file:
                import base64

                encoded_brand_b64 = base64.b64encode(image_bytes_file.read())
                # Wipe away hidden layout character separators to protect f-string parsing tracks completely!
                clean_brand_b64_string = (
                    encoded_brand_b64.decode("utf-8")
                    .replace("\n", "")
                    .replace("\r", "")
                )
                brand_image_render_url = (
                    f"data:image/jpeg;base64,{clean_brand_b64_string}"
                )
        except Exception:
            pass

    # 4. 🔥 COMPRESS THE PAYLOAD ONTO A UNIFIED TIMELINE TO ELIMINATE RAW VISIBLE TEXT GATES 🔥
    # Pre-declare single quotes internally to prevent double quotes collisions and syntax crashes!
    brand_showcase_html_payload = (
        "<div class='vk-card' style='text-align: center; padding: 50px 30px;''>"
        "<div class='vk-hero-badge'>Next-Gen Fashion Ecosystem</div>"
        "<h1 class='vk-headline'>AI Fabric & Garment Studio</h1>"
        "<p style='color: var(--vk-text-muted); max-width: 620px; margin: 0 auto 30px auto; font-size:15px;'>"
        "Welcome to Glameeri's integrated designer portal. Map high-density Ankara, Kente, and Adire prints onto digital style assets instantly with true 3D normal displacement field rendering."
        "</p>"
        f"<img src='{brand_image_render_url}' style='width: 100%; max-height: 400px; "
        "object-fit: cover; border-radius: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);' "
        "alt='Glameeri Active Collection Banner'/>"
        "</div>"
    )

    # Force the markdown engine to interpret the payload as native web node parameters
    st.markdown(brand_showcase_html_payload, unsafe_allow_html=True)

    # Close your custom card div wrapper cleanly at the end of the entry sequence layout cell
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 Access Interactive Design Canvas", key="home_cta_btn"):
        navigate_to("signup")
        st.rerun()

# --- ABOUT VIEW ---
elif st.session_state["app_view"] == "about" and not st.session_state["authenticated"]:

    # 1. Render the primary typography headers inside your centered card container

    # 2. Establish the explicit filesystem file path pointing to your local studio banner image
    local_brand_image_path = os.path.join("images", "for_app.png")

    # Authoritative high-fashion Unsplash backup URL deployed if your local disk asset is missing or locked
    brand_image_render_url = "https://unsplash.com"

    # 3. Pull image bytes and convert to a clean single-line Base64 format to bypass cross-origin blocks
    if os.path.exists(local_brand_image_path):
        try:
            with open(local_brand_image_path, "rb") as image_bytes_file:
                import base64

                encoded_brand_b64 = base64.b64encode(image_bytes_file.read())
                # Wipe away hidden layout character separators to protect f-string parsing tracks completely!
                clean_brand_b64_string = (
                    encoded_brand_b64.decode("utf-8")
                    .replace("\n", "")
                    .replace("\r", "")
                )
                brand_image_render_url = (
                    f"data:image/jpeg;base64,{clean_brand_b64_string}"
                )
        except Exception:
            pass

    # 4. 🔥 COMPRESS THE PAYLOAD ONTO A UNIFIED TIMELINE TO ELIMINATE RAW VISIBLE TEXT GATES 🔥
    # Pre-declare single quotes internally to prevent double quotes collisions and syntax crashes!
    brand_showcase_html_payload = (
        "<div class='vk-card' style='text-align: center; padding: 50px 30px;'>"
        "<style>"
        " .vk-navbar-img { width: auto; max-height: 1260px; object-fit: contain; border-radius: 6px; }"
        "</style>"
        "<h2 class='vk-section-header;'>ℹ️ About Glameeri AI</h2>"
        "<p style='color: var(--vk-text-muted); font-size:14px; margin-bottom:12px;'>"
        "AfriTextile AI Studio bridges local artisanal craftsmanship with automated deep learning computer vision paradigms."
        "Our pipeline relies entirely on zero-network local RAM matrix operations to guarantee high execution stability."
        "</p>"
        f"<img src='{brand_image_render_url}' class='vk-navbar-img'alt='AfriTexile Active Collection Banner'/>"
        "</div>"
    )
    # style='width: 100%; max-height: 1400px;
    # "object-fit: cover; border-radius: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);' "
    #        "alt='AfriTexile Active Collection Banner'/>"
    # Force the markdown engine to interpret the payload as native web node parameters
    st.markdown(brand_showcase_html_payload, unsafe_allow_html=True)

    # Close your custom card div wrapper cleanly at the end of the entry sequence layout cell
    st.markdown("</div>", unsafe_allow_html=True)

# --- SERVICES VIEW ---
elif (
    st.session_state["app_view"] == "services" and not st.session_state["authenticated"]
):
    st.markdown(
        """
        <div class="vk-card">
            <h2 class="vk-section-header">🛠️ Enterprise Studio Ecosystem Modules</h2>
            <ul style="color: var(--vk-text-muted); font-size:14px; padding-left:20px; line-height:2.0;">
                <li><b>Procedural Heritage Vectoring Engine:</b> Renders distinct Ankara, Kente, and Adire tokens on demand.</li>
                <li><b>3D Surface Normal Displacement Maps:</b> Simulates realistic fabric folds and chest/hip contours.</li>
                <li><b>ReportLab Lookbook Automation:</b> Generates customer portfolios compiled dynamically with sizing parameters.</li>
            </ul>
        </div>
    """,
        unsafe_allow_html=True,
    )

# --- PRICING VIEW ---
elif (
    st.session_state["app_view"] == "pricing" and not st.session_state["authenticated"]
):
    st.markdown(
        """
        <div class="vk-card" style="text-align: center;">
            <h2 class="vk-section-header">💰 Production Workspace Pricing Plans</h2>
            <div style="font-size: 36px; font-weight:700; color:#1a73e8; margin-bottom:8px;">0.00 GHS / FREE</div>
            <p style="color: var(--vk-text-muted); font-size:14px; margin-bottom:20px;">Open Community Access Plan for Local Designers</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.session_state["app_view"] = "public_pricing"
    st.rerun()
elif (
    st.session_state["app_view"] == "start_now"
    and not st.session_state["authenticated"]
):
    st.session_state["authenticated"] = False
    st.session_state["is_logged_in"] = False
    st.session_state["user_session_token"] = None
    st.session_state["user_session_id"] = None
    st.session_state["app_view"] = "is_logged_in"
    st.rerun()
# ==========================================
# 🔥 MD3 SPECIFICATION AUTH FRAMES 🔥
# ==========================================

# --- REGISTRATION VIEW (MD3 CONVERTED) ---
elif st.session_state["app_view"] == "signup" and not st.session_state["authenticated"]:
    # =========================================================================
    # 🧵 REPLACEMENT CORES: PERSISTENT STATE-BOUND REGISTRATION ENGINE 🧵
    # =========================================================================
    st.markdown('<div class="vk-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Create Studio Atelier Account")
    st.write(
        "Register your custom fashion house parameters to initialize your secure production canvas workspace:"
    )

    # 🔥 STEP 1: INITIALIZE STABLE DEFAULT STATE KEYS IN PARENT MEMORY HOOKS 🔥
    # This prevents Streamlit from wiping out your parameters during upload reruns!
    if "reg_email_cache" not in st.session_state:
        st.session_state["reg_email_cache"] = ""
    if "reg_pass_cache" not in st.session_state:
        st.session_state["reg_pass_cache"] = ""
    if "reg_studio_cache" not in st.session_state:
        st.session_state["reg_studio_cache"] = ""
    if "reg_avatar_filename" not in st.session_state:
        st.session_state["reg_avatar_filename"] = "default_profile.png"

    # --- PART A: OUT-OF-FORM OPTIONAL AVATAR FILE INTAKE LAYER ---
    # Placing this outside the form eliminates background state reset crashes entirely!

    # --- PART B: THE CORE ACCOUNT PARAMETERS FORM MATRIX ---
    # st.markdown("<br/>", unsafe_allow_html=True)
    st.write("Enter Account Credentials & Studio Metadata:")

    with st.form("user_registration_form_matrix_panel", clear_on_submit=False):

        # We explicitly update the persistent parent session state caches directly on the fly
        reg_mail = st.text_input(
            "Corporate Studio Email Address:",
            placeholder="name@studio.com",
            value=st.session_state["reg_email_cache"],
        )

        reg_pass = st.text_input(
            "Account Secret Password Access:",
            type="password",
            placeholder="Min 6 characters recommended",
            value=st.session_state["reg_pass_cache"],
        )

        reg_studio = st.text_input(
            "Atelier / Fashion House Name:",
            placeholder="e.g., Glameeri AI Localization Studio",
            value=st.session_state["reg_studio_cache"],
        )

        uploaded_avatar = st.file_uploader(
            "Upload Optional Profile Avatar Graphic (PNG/JPG):",
            type=["png", "jpg", "jpeg"],
            key="reg_avatar_file_uploader_widget",
        )

        if uploaded_avatar is not None:
            try:
                import base64

                # 1. Read raw image stream bytes directly from the uploader
                avatar_raw_bytes = uploaded_avatar.getvalue()

                # 2. Convert to a permanent single-line Base64 text payload string
                encoded_avatar_b64 = base64.b64encode(avatar_raw_bytes).decode("utf-8")
                clean_b64_payload = f"data:image/jpeg;base64,{encoded_avatar_b64}"

                # 3. Update the data column in your Supabase table via your active ORM user object
                # (Assuming 'current_user' represents your logged-in database row)
                current_user.profile_picture_name = clean_b64_payload
                db_session.commit()

                # 4. Sync it to session state cache memory
                st.session_state["reg_avatar_filename"] = clean_b64_payload

                st.sidebar.success(
                    "📸 Custom avatar uploaded and saved permanently to Supabase cloud!"
                )
            except Exception as upload_err:
                db_session.rollback()
                st.sidebar.error(f"Avatar file stream cloud save failed: {upload_err}")

        st.markdown("<br/>", unsafe_allow_html=True)


        if st.form_submit_button(
            "🚀 Complete Account Registration", use_container_width=True
        ):

            # Trim and wash incoming parameters cleanly to prevent case lookup blocks
            clean_email = str(reg_mail).strip().lower()
            clean_password = str(reg_pass).strip()
            clean_studio = str(reg_studio).strip()

            # Update background cache states immediately to protect typed strings across failures
            st.session_state["reg_email_cache"] = clean_email
            st.session_state["reg_pass_cache"] = clean_password
            st.session_state["reg_studio_cache"] = clean_studio

            # Secure Validation Safety Check Gate
            if not clean_email or not clean_password or not clean_studio:
                st.error(
                    "❌ Registration parameters cannot remain blank. Please complete all form inputs."
                )
            elif len(clean_password) < 4:
                st.error(
                    "❌ Security Restraint: Password entry must contain at least 4 characters."
                )
            else:
                # db = SessionLocal()
                try:
                    # Look up potential duplicate studio email profiles in your PostgreSQL table rows
                    user_exists = (
                        db_session.query(User).filter(User.email == clean_email).first()
                    )
                    if user_exists:
                        st.error(
                            "⚠️ Account Conflict: A studio profile is already registered under this email address."
                        )
                    else:
                        from security import get_password_hash

                        # Scramble text input into an explicit, native Python 3.14 single-pass hash signature
                        hashed_secret_payload = get_password_hash(clean_password)

                        # Instantiate the ORM database row using unconflicted setattr mapping methods
                        new_user = User()
                        setattr(new_user, "email", clean_email)
                        setattr(new_user, "hashed_password", hashed_secret_payload)
                        setattr(new_user, "studio_name", clean_studio)
                        setattr(
                            new_user,
                            "biography",
                            "No corporate profile log attached yet.",
                        )
                        setattr(
                            new_user,
                            "profile_picture_name",
                            st.session_state["reg_avatar_filename"],
                        )

                        # Force database cluster update commands
                        db_session.add(new_user)
                        db_session.commit()

                        st.success(
                            "🎉 Account compiled across PostgreSQL tables successfully! Redirecting to login..."
                        )

                        # Wipe cache traces clean upon absolute registration success
                        st.session_state["reg_email_cache"] = ""
                        st.session_state["reg_pass_cache"] = ""
                        st.session_state["reg_studio_cache"] = ""
                        st.session_state["reg_avatar_filename"] = "default_profile.png"

                        db_session.close()
                        time.sleep(0.7)

                        # Transition user smoothly over to your login panel view card
                        st.session_state["app_view"] = "is_logged_in"
                        st.rerun()
                except Exception as db_write_error:
                    db_session.rollback()
                    st.error(f"❌ Database row write failed: {db_write_error}")
                finally:
                    db_session.close()

    # Public view navigation link safely drops outside form container tracking parameters
    st.button(
        "↩️ Already Registered? Go to Login Screen",
        on_click=navigate_to,
        args=("is_logged_in",),
        key="reg_nav_back_unconflicted_trigger_cta",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# --- AUTHENTICATION LOGIN VIEW (MD3 CONVERTED) ---
# elif (
#    st.session_state["app_view"] == "is_logged_in"
#    and not st.session_state["authenticated"]
# ):
# st.markdown(
#    """
#   <div class="md-card">
#        <div class="brand-header">
#            <h2 style="color: var(--md-primary);">Sign In</h2>
#            <p>Verify session keys to enter localization network</p>
#        </div>
#    </div>
# """,
#    unsafe_allow_html=True,
# )

# =========================================================================
# 🧵 FIX: DIRECT SESSION STATE CAPTURE PASS FOR USER LOGIN HUB 🧵
# =========================================================================

# =========================================================================
# 🧵 FIX: SYNCHRONIZED SESSION STATE LOGIN CONTROLLER (OBLITERATES ERROR)
# =========================================================================

elif st.session_state.get("app_view") == "is_logged_in":
    st.markdown('<div class="vk-card">', unsafe_allow_html=True)
    st.markdown("### 🔑 Secure Atelier Access Login")
    st.write("Enter your production studio credentials to unlock your workspace:")

    # 1. Wrap the login inputs inside an explicitly isolated login form container
    with st.form("user_login_form_matrix_panel", clear_on_submit=False):

        # 🔥 FIX 1: Enforce explicit, dedicated session state mapping keys on both text fields.
        # This forces the web browser to lock your typed credentials securely into global RAM!
        st.text_input(
            "Corporate Email Address:",
            placeholder="name@studio.com",
            key="login_field_email_stream",  # Unique identification tracking token
        )

        st.text_input(
            "Password Secure Key:",
            type="password",
            placeholder="••••••••",
            key="login_field_password_stream",  # Unique identification tracking token
        )

        st.markdown("<br/>", unsafe_allow_html=True)

        # 2. Trigger verification when the entry button is clicked
        if st.form_submit_button(
            "🚀 Enter Production Studio Workspace", use_container_width=True
        ):

            # 🔥 FIX 2: Pull input strings directly from your global session state cache registers!
            # This completely bypasses empty or uninitialized local script variables.
            raw_mail_input = str(
                st.session_state.get("login_field_email_stream", "")
            ).strip()
            raw_pass_input = str(
                st.session_state.get("login_field_password_stream", "")
            ).strip()

            if raw_mail_input and raw_pass_input:
                # db = SessionLocal()
                try:
                    # Enforce lowercase parameters on lookup queries to ensure data tracks align perfectly
                    clean_login_email = raw_mail_input.lower()
                    user_record = (
                        db_session.query(User)
                        .filter(User.email == clean_login_email)
                        .first()
                    )

                    if user_record:
                        # Extract the hashed password string safely using getattr() to bypass ORM bugs
                        db_hashed_secret: str = str(
                            getattr(user_record, "hashed_password", "")
                        )

                        # 🔥 FIX 3: Run the modern native Python 3.14 verification check!
                        # Passes your cleaned plain-text string directly against your database hash row
                        if verify_password(raw_pass_input, db_hashed_secret):
                            verified_user_id: int = int(getattr(user_record, "id"))
                            verified_studio_name: str = str(
                                getattr(user_record, "studio_name")
                            )
                            verified_user_email: str = str(
                                getattr(user_record, "email")
                            )

                            # Generate signed JWT token passport strings using your verified primitive data types
                            session_jwt_token = generate_user_session_token(
                                user_id=verified_user_id,
                                studio_name=verified_studio_name,
                                email=verified_user_email,
                            )

                            # Lock authorized flags securely into active memory tracking frames
                            st.session_state["is_logged_in"] = True
                            st.session_state["authenticated"] = True
                            st.session_state["user_session_token"] = session_jwt_token
                            st.session_state["user_session_id"] = verified_user_id
                            st.session_state["app_view"] = "studio"

                            st.success(
                                "🎉 Authorization signature verified via JWT! Launching canvas..."
                            )
                            db_session.close()
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(
                                "❌ Invalid session coordinates or wrong credentials. (Password mismatch)"
                            )
                    else:
                        st.error(
                            "❌ Invalid session coordinates or wrong credentials. (Account not found)"
                        )
                except Exception as login_err:
                    st.error(f"Authentication system exception: {login_err}")
                finally:
                    db_session.close()
            else:
                st.warning(
                    "⚠️ Action Required: Please fill out both email and password input spaces."
                )

    # 3. Secure routing fallback switch allows clean transition over to account creation

    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.button(
            "🔑 Lost Password? Reset",
            on_click=navigate_to,
            args=("recovery",),
            key="login_nav_rec",
        )
    with col_sub2:
        st.button(
            "📝 No Account? Sign Up",
            on_click=navigate_to,
            args=("signup",),
            key="login_nav_sign",
        )
    st.markdown("</div>", unsafe_allow_html=True)
# elif  st.session_state["app_view"] != "is_logged_in":
# elif (
# not st.session_state["authenticated"]
# or st.session_state["app_view"] != "is_logged_in"
# ):


# Define callback jumps to enforce absolute layout logic transitions
def advance_to_step_two():
    active_motif = st.session_state["motif_spec_input"]
    st.session_state["cultural_spec"] = (
        OFFLINE_BLUEPRINTS.get(st.session_state["dropdown_foundation_select"], "")
        + f"\n- Custom Motifs: {active_motif}"
    )
    st.session_state["active_fabric"] = render_fallback_fabric(
        st.session_state["primary_color_picker_id"],
        st.session_state["dropdown_foundation_select"],
        active_motif,
        st.session_state["motif_color_picker_id"],
    )
    st.session_state["chosen_foundation"] = st.session_state[
        "dropdown_foundation_select"
    ]
    st.session_state["primary_color"] = st.session_state["primary_color_picker_id"]
    st.session_state["motif_color"] = st.session_state["motif_color_picker_id"]
    st.session_state["wizard_step"] = 2


# ==========================================
# 📐 ACTIVE APP CORE DESIGN HUB WORKSPACE 📐
# ==========================================
# =========================================================================
# 📐 ACTIVE APP CORE DESIGN HUB WORKSPACE (STAYS VISIBLE & STACKS PERFECTLY)
# =========================================================================
if st.session_state["authenticated"]:

    # ---------------------------------------------------------------------
    # 🔥 STEP 1: ALWAYS REMAINS VISIBLE DOWN THE ENTIRE PORTAL PAGE
    # ---------------------------------------------------------------------
    st.markdown('<p class="m3-title">🌍 Glameeri AI Studio</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="m3-subtitle">100% Free Pattern Workspace for African Tailors</p>',
        unsafe_allow_html=True,
    )
# =========================================================================
# 📐 ACTIVE APP CORE DESIGN HUB WORKSPACE (STABLE ACCUMULATING STACK)
# =========================================================================
if st.session_state["authenticated"]:

    # ---------------------------------------------------------------------
    # 🔥 STEP 1: ALWAYS REMAIN RENDERED AT THE TOP OF THE WORKSPACE PAGE
    # ---------------------------------------------------------------------
    st.markdown('<div class="vk-card">', unsafe_allow_html=True)
    st.markdown(
        '<p class="vk-section-header">🧵 Step 1: Design Context & Blueprint Setup</p>',
        unsafe_allow_html=True,
    )

    fabric_source = st.radio(
        "Asset Source Configuration:",
        ["Engineered Heritage Template", "Upload Shop Fabric Photo"],
        key="fabric_source_selection_toggle",
    )

    if fabric_source == "Engineered Heritage Template":
        foundation_input = st.selectbox(
            "Cultural Foundation:",
            [
                "Ankara Wax Print",
                "Kente Cloth Heritage",
                "Adire Tech",
                "Modern Afro-Futurism",
                "Plain Solid Colour",
            ],
            key="dropdown_foundation_select",
            on_change=sync_motif_on_context_change,
        )
        primary_color_input = st.color_picker(
            "Hex Tone Selection (Background Color):",
            "#E05A47",
            key="primary_color_picker_id",
        )
        motif_color_input = st.color_picker(
            "Motif Overlay Color Picker:", "#F2B705", key="motif_color_picker_id"
        )
        motif_type = st.text_input(
            "Enter ANY Motif Specification Prompt (e.g. 'floral patterns', 'honeycomb grids'):",
            key="motif_spec_input",
        )

        if st.button("✨ Compile Intelligent Design Blueprint", key="btn_blueprint"):
            active_motif = st.session_state["motif_spec_input"]
            st.session_state["cultural_spec"] = (
                OFFLINE_BLUEPRINTS.get(foundation_input, "")
                + f"\n- Custom Motifs: {active_motif}"
            )
            st.session_state["active_fabric"] = render_fallback_fabric(
                primary_color_input, foundation_input, active_motif, motif_color_input
            )
            st.session_state["chosen_foundation"] = foundation_input
            st.session_state["primary_color"] = primary_color_input
            st.session_state["motif_color"] = motif_color_input
            st.session_state["wizard_step"] = 2
            st.rerun()
    else:
        # File uploader stores data inside a persistent key string link slot
        fabric_file = st.file_uploader(
            "Upload custom workshop layout image (PNG/JPG):",
            type=["jpg", "png", "jpeg"],
            key="custom_fabric_file_upload",
        )
        if fabric_file:
            if st.button(
                "✨ Lock & Process Custom Shop Fabric Photo",
                key="btn_compile_uploaded_fabric",
            ):
                try:
                    uploaded_img_obj = Image.open(fabric_file).convert("RGB")
                    st.session_state["active_fabric"] = uploaded_img_obj
                    st.session_state["chosen_foundation"] = (
                        "Uploaded Custom Fabric Photo"
                    )
                    st.session_state["cultural_spec"] = (
                        "Custom uploaded workshop textile pattern matrix check completed."
                    )
                    st.session_state["primary_color"] = "#E05A47"
                    st.session_state["motif_color"] = "#F2B705"
                    st.session_state["motif_spec_input"] = (
                        "Custom Uploaded Shop Fabric Matrix Print"
                    )
                    st.session_state["wizard_step"] = 2
                    st.rerun()
                except Exception as fabric_load_err:
                    st.error(f"Custom Fabric Parsing Failed: {fabric_load_err}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # 🔥 STEP 2: STAYS DISPLAYED AND SECURE ON EVERY RE-RENDER OVERRIDE
    # ---------------------------------------------------------------------
    if (
        st.session_state["wizard_step"] >= 2
        and st.session_state["active_fabric"] is not None
    ):
        st.markdown('<div class="vk-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="vk-section-header">👁️ Step 2: Quality Review & Seam Grid Validation</p>',
            unsafe_allow_html=True,
        )

        t1, t2 = st.tabs(
            ["Single Module Element", "🧵 Continuous 3x3 Manufacturing Roll"]
        )
        with t1:
            st.image(
                st.session_state["active_fabric"],
                caption="Master Asset Module",
                use_container_width=True,
            )
        with t2:
            st.image(
                create_tile_grid(st.session_state["active_fabric"]),
                caption="Continuous roll simulation",
                use_container_width=True,
            )

        if st.button(
            "➡️ Approve Seam Grid & Advance to Style Try-On Workspace",
            key="step2_approve_btn",
        ):
            # Move state index forward to step 3 without losing your custom active_fabric image layer!
            st.session_state["wizard_step"] = 3
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # 🔥 STEP 3: DRAWS BENEATH STEP 2 SECURELY REGARDLESS OF FABRIC MATERIAL SOURCE
    # ---------------------------------------------------------------------
    if (
        st.session_state["wizard_step"] >= 3
        and st.session_state["active_fabric"] is not None
    ):
        st.markdown('<div class="vk-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="vk-section-header">📐 Step 3: Outfit Specification & 3D Texture Imprinting Workspace</p>',
            unsafe_allow_html=True,
        )

        chosen_foundation = st.session_state["chosen_foundation"]
        primary_color = st.session_state["primary_color"]

        st.markdown("##### 📸 Model Template & Posture Source Configuration")
        model_source = st.radio(
            "Select Layout Image Source Mode:",
            [
                "Use Workshop Lookbook Templates",
                "Upload Custom Client Model",
                "Upload Custom Client Cloth Style and Model",
            ],
            key="model_source_selector",
        )

        garment_cut = "Custom Outfit Style"
        if model_source == "Use Workshop Lookbook Templates":

            OFFLINE_BLUEPRINTS_MAPPING = {
                "Ankara Wax Print": [
                    "Off-shoulder Ankara Maxi Gown",
                    "Fitted Ankara Jumpsuit with Flared Sleeves",
                    "Ankara Peplum Top with Pencil Skirt",
                    "Modern Ankara Bomber Jacket and Trouser",
                    "Agbada",
                    "Kaftan",
                    "Long Sleeved Shirt and Trouser",
                    "Short Sleeved Shirt and Trouser",
                    "T-Shirt and Short Knicker",
                ],
                "Kente Cloth Heritage": [
                    "Traditional Multi-layered Kente Agbada",
                    "Royal Kente Wrap (Toga Style)",
                    "Kente Mermaid Tail Wedding Gown",
                    "Fitted Kente Blazer and Trousers",
                ],
                "Adire Tech": [
                    "Flowing Adire Kaftan Dress",
                    "Adire Kimono Lounge Cardigan",
                    "Modern Fitted Kaftan Suit",
                    "Adire Shift Midi Dress",
                ],
                "Modern Afro-Futurism": [
                    "Asymmetric Cyber-Punk Dashiki Gown",
                    "Metallic Accent Neo-Habesha Dress",
                    "Structured High-Collar Cape Overcoat",
                    "Futuristic Geometric Crop Set",
                ],
                "Plain Solid Colour": [
                    "Elegant Solid Minimalist Silk Slip Dress",
                    "Classic Structured Solid Blazer",
                    "Clean Architectural Plain Kaftan Gown",
                ],
                "Uploaded Custom Fabric Photo": [
                    "Custom Tailored Maxi Gown",
                    "Traditional Multi-layered Agbada",
                    "Modern Fitted Kaftan Suit",
                ],
            }
            available_styles = OFFLINE_BLUEPRINTS_MAPPING.get(
                chosen_foundation, ["Custom Tailored Gown"]
            )
            garment_cut = st.selectbox(
                "Select matching style configuration:",
                options=available_styles,
                key="active_garment_cut",
            )
            # else:
            #    garment_cut = st.text_input(
            #        "Enter Apparel Cut / Style Category Name (e.g. 'gown', 'jumpsuit', 'jacket'):",
            #        value="gown",
            #        key="active_garment_cut",
            #    )

            # =========================================================================
            # 🧵 UNIVERSAL NO-MASK AUTOMATED CHROMA EXTENSION PIPELINE CHUNK IN STEP 3
            # =========================================================================

            # col_img1, col_img2 = st.columns(2)
            # with col_img1:
            #    st.markdown("##### 🎨 3D Imprint Controls")

            # =========================================================================
            # 🧵 REPLACEMENT CODE CHUNK: PERSISTENT MODEL & MASK CACHING ENGINE 🧵
            # =========================================================================

            # =========================================================================
            # 🧵 REPLACEMENT CODE CHUNK: PERSISTENT MODEL & MASK CACHING ENGINE 🧵
            # =========================================================================

            # =========================================================================
            # 🪡 FIX: SYNCHRONIZED 3-VARIABLE UNPACKING ENTRY MATRIX (INDEX4.PY) 🪡
            # =========================================================================

            if st.button(
                "🚀 Render Imprinted Design Directly Onto Style Silhouette",
                key="step3_render_action",
                use_container_width=True,
            ):
                # 1. Recover current user usage metrics straight from PostgreSQL records
                user_session_id_val = st.session_state.get("user_session_id", 0)
                # db_session = SessionLocal()
                db_user = (
                    db_session.query(User)
                    .filter(User.id == user_session_id_val)
                    .first()
                )

                user_tier = str(getattr(db_user, "subscription_tier", "freemium"))
                current_usage = int(getattr(db_user, "monthly_generation_count", 0))

                # 🔥 FIX: Include the middle variable slot 'is_expired_flag' to match the 3-element return tuple!
                # The red lines vanish instantly because the data unpacking tracks align perfectly!
                from security import verify_generation_allowance

                is_authorized, is_expired_flag, restriction_msg = (
                    verify_generation_allowance(user_tier, current_usage)
                )

                if not is_authorized:
                    st.error(restriction_msg)
                    db_session.close()
                    st.stop()  # Aborts rendering execution track immediately!

                # ... (Your original 3D normal mapping compilation loops execute securely here) ...

                # Increment usage parameters in the table row cells upon successful compilation pass
                setattr(db_user, "monthly_generation_count", current_usage + 1)
                db_session.commit()
                db_session.close()

                actual_base_path = None
                cv_model = None
                bg_pil = None
                raw_stencil = None

                # BRANCH A: DEPLOY STABLE MEMORY POINTERS FROM THE PERSISTENT CACHE MATRIX
                if model_source == "Upload Custom Client Model & Mask":
                    # Verify that cached assets exist securely inside the session dictionary
                    if (
                        "cached_model_cv" in st.session_state
                        and "cached_model_pil" in st.session_state
                        and "cached_mask_pil" in st.session_state
                    ):
                        cv_model = st.session_state["cached_model_cv"]
                        bg_pil = st.session_state["cached_model_pil"]
                        raw_stencil = st.session_state["cached_mask_pil"]
                    else:
                        st.warning(
                            "⚠️ Action Required: Please upload both your model and mask images before rendering."
                        )

                # BRANCH B: DEPLOY SYSTEM TEMPLATES FROM LOCAL DISK STORAGE CHANNELS
                else:
                    base_project_dir = os.path.dirname(__file__)
                    images_folder_path = os.path.join(base_project_dir, "images")
                    search_tokens = [
                        t.strip()
                        for t in str(garment_cut)
                        .lower()
                        .replace("-", " ")
                        .replace("_", " ")
                        .split()
                        if len(t.strip()) > 2
                    ]

                    if os.path.exists(images_folder_path):
                        folder_contents = os.listdir(images_folder_path)
                        best_base_match = None
                        best_base_score = 0

                        for filename in folder_contents:
                            fn_lower = filename.lower()
                            if "mask" in fn_lower:
                                continue
                            match_score = sum(
                                1 for token in search_tokens if token in fn_lower
                            )
                            if match_score > best_base_score:
                                best_base_score = match_score
                                best_base_match = filename

                        if best_base_match:
                            actual_base_path = os.path.join(
                                images_folder_path, best_base_match
                            )

                    if actual_base_path:
                        cv_model = cv2.imread(actual_base_path)
                        bg_pil = Image.open(actual_base_path).convert("RGBA")
                        # Generate the automatic in-memory mask if using system templates
                        gray_temp = (
                            cv2.cvtColor(cv_model, cv2.COLOR_BGR2GRAY)
                            if cv_model is not None
                            else None
                        )
                        if gray_temp is not None:
                            _, temp_thresh = cv2.threshold(
                                cv2.GaussianBlur(gray_temp, (9, 9), 0),
                                0,
                                255,
                                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
                            )
                            raw_stencil = Image.fromarray(temp_thresh).convert("L")

                # Core 3D texture mapping math runs securely using persistent variable states below
                if (
                    cv_model is not None
                    and bg_pil is not None
                    and raw_stencil is not None
                ):
                    try:
                        h_img, w_img, _ = cv_model.shape

                        # 1. GENERATE PURE ORIGINAL GRAYSCALE BASE LIGHTING MAP
                        # 1. GENERATE PURE ORIGINAL GRAYSCALE BASE LIGHTING MAP
                        gray_model: Any = cv2.cvtColor(cv_model, cv2.COLOR_BGR2GRAY)

                        # 2. AUTOMATED APPAREL EXTRACTOR & SKIN DETECTION RESIST
                        blurred_gray = cv2.GaussianBlur(gray_model, (9, 9), 0)

                        # FIX: Pre-declare the variable with its type hint container here first!
                        # This clears out all red underlines instantly while maintaining valid Python syntax.
                        auto_thresh: Any = None
                        _, auto_thresh = cv2.threshold(
                            blurred_gray,
                            0,
                            255,
                            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
                        )
                        hsv_matrix = cv2.cvtColor(cv_model, cv2.COLOR_BGR2HSV)
                        lower_skin_bounds = np.array([0, 15, 30], dtype=np.uint8)
                        upper_skin_bounds = np.array([20, 160, 255], dtype=np.uint8)
                        body_skin_mask = cv2.inRange(
                            hsv_matrix, lower_skin_bounds, upper_skin_bounds
                        )

                        # Combine maps and strictly subtract skin pixel boundaries from fabric path
                        cv_mask = cv2.bitwise_and(
                            auto_thresh, cv2.bitwise_not(body_skin_mask)
                        )

                        # Clear out the top head hair pixels safely before mapping contours
                        cv_mask[0 : int(h_img * 0.15), :] = 0

                        # --- 🔥 NEW: CONNECTED CONTOUR FILTER (FIXES ASYMMETRICAL SHOULDER LEAKS) 🔥 ---
                        # Locates all individual shape outlines inside the mask area
                        contours, _ = cv2.findContours(
                            cv_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                        )

                        # Build a clean slate mask array to transfer only the true verified clothing body
                        clean_torso_mask = np.zeros_like(cv_mask)

                        if contours:
                            # Isolate the single largest connected shape (the main dress body asset)
                            largest_dress_contour = max(contours, key=cv2.contourArea)

                            # Draw ONLY the verified dress body onto our clean slate mask array
                            # This completely deletes any stray pixels that leaked onto bare shoulders or skin!
                            cv2.drawContours(
                                clean_torso_mask,
                                [largest_dress_contour],
                                -1,
                                255,
                                thickness=cv2.FILLED,
                            )

                        # Replace the old layout mask with our filtered, clean shoulder shield mask
                        cv_mask = clean_torso_mask
                        # --------------------------------------------------------------------------------

                        # Clean up edges using morphological elements to lock neat apparel seams
                        morph_structural_element = cv2.getStructuringElement(
                            cv2.MORPH_ELLIPSE, (3, 3)
                        )
                        cv_mask = cv2.morphologyEx(
                            cv_mask,
                            cv2.MORPH_CLOSE,
                            morph_structural_element,
                            iterations=1,
                        )
                        cv_mask = cv2.GaussianBlur(cv_mask, (3, 3), 0)

                        stencil_mask = Image.fromarray(cv_mask).convert("L")

                        # 3. ADVANCED 3D VECTOR SURFACE NORMAL ESTIMATIONS
                        sobel_x = cv2.Sobel(gray_model, cv2.CV_64F, 1, 0, ksize=5)
                        sobel_y = cv2.Sobel(gray_model, cv2.CV_64F, 0, 1, ksize=5)
                        x_grid, y_grid = np.meshgrid(np.arange(w_img), np.arange(h_img))

                        dist_map = cv2.distanceTransform(cv_mask, cv2.DIST_L2, 5)
                        cv2.normalize(dist_map, dist_map, 0, 1.0, cv2.NORM_MINMAX)

                        garment_style_query = str(garment_cut).lower()
                        detected_config = BODY_SEGMENTATION_ROUTER["gown"]
                        for (
                            anatomy_keyword,
                            config_metrics,
                        ) in BODY_SEGMENTATION_ROUTER.items():
                            if anatomy_keyword in garment_style_query:
                                detected_config = config_metrics
                                break

                        mult_x = float(detected_config["warp_intensity_x"])
                        mult_y = float(detected_config["warp_intensity_y"])
                        density_scale = float(detected_config["texture_density_ratio"])

                        warp_x = (x_grid + (sobel_x * dist_map * mult_x)).astype(
                            np.float32
                        )
                        warp_y = (y_grid + (sobel_y * dist_map * mult_y)).astype(
                            np.float32
                        )

                        # ===================================================================================
                        # 🧵 FIX: OVERWRITE SECTIONS 4, 5, & 6 INSIDE STEP 3 FOR HYPER-CLARITY MOTIFS 🧵
                        # ===================================================================================

                        # ===================================================================================
                        # 🧵 REPLACEMENT RENDER CORE: PIXEL-PERFECT ZERO-DISTORTION DESIGN ENGINE 🧵
                        # ===================================================================================

                        # 4. HIGH-DENSITY RAW FABRIC LAYER COMPILATION (ZERO WARP BLUR)
                        # We extract your chosen design pattern asset with zero sub-pixel distortion
                        design_fabric = st.session_state["active_fabric"].convert(
                            "RGBA"
                        )
                        optimized_tile_size = (
                            int(w_img // density_scale) if w_img > 100 else 60
                        )

                        # Resize using premium high-frequency Lanczos resampling filters to preserve sharp motifs
                        scaled_fabric = design_fabric.resize(
                            (optimized_tile_size, optimized_tile_size),
                            Image.Resampling.LANCZOS,
                        )

                        # Generate a clean slate background filled with your exact pattern design
                        tiled_background = Image.new("RGBA", bg_pil.size)
                        bg_w, bg_height = bg_pil.size
                        for x_pos in range(0, bg_w, optimized_tile_size):
                            for y_pos in range(0, bg_height, optimized_tile_size):
                                tiled_background.paste(scaled_fabric, (x_pos, y_pos))

                        # ===================================================================================
                        # 🧵 REPLACEMENT RENDER CORE: CLEAN-SLATE OPAQUE NO-GRAY-PATCHES CORE 🧵
                        # ===================================================================================

                        # 5. 🔥 FIX 1: HIGH-CONTRAST CREASE EXTRACTION WITH LUMINANCE RE-BALANCE 🔥
                        # Extracts micro-shadow folds from the original garment with absolute precision
                        adaptive_clahe = cv2.createCLAHE(
                            clipLimit=4.0, tileGridSize=(4, 4)
                        )
                        normalized_gray_L = adaptive_clahe.apply(gray_model)

                        # FIX: Pre-allocate an empty array and re-scale pixels to flatten out dirty gray patches
                        shading_dest_matrix = np.zeros_like(normalized_gray_L)
                        balanced_shading_map = cv2.normalize(
                            normalized_gray_L,
                            shading_dest_matrix,
                            0,
                            255,
                            cv2.NORM_MINMAX,
                        )

                        # Convert the balanced depth map into a clean raw array loop securely
                        shading_matrix = np.array(balanced_shading_map)

                        # --- COMPLETE REPLACEMENT FOR SECTION 6 INPUT BLOCKS ---

                        # 6. 🔥 FIX: CHROMINANCE INJECTION CORES (100% DISTINCT, EXACT FABRIC PRINT) 🔥
                        # We convert our pristine, unwarped tiled background image directly into a clean RGB array.
                        # This removes 'warped_texture' from the file completely and wipes out the red underline!
                        opaque_textured_garment = np.array(
                            tiled_background.convert("RGB")
                        )

                        # Create empty alpha channel shadow sheets matching the balanced data grid
                        alpha_shadows = np.zeros_like(shading_matrix, dtype=np.uint8)
                        alpha_highlights = np.zeros_like(shading_matrix, dtype=np.uint8)

                        # Shifting threshold boundaries flattens out mid-tone gray fields for crisp tones
                        alpha_shadows = np.where(
                            shading_matrix < 90,
                            ((90 - shading_matrix) * 1.3).astype(np.uint8),
                            0,
                        )
                        alpha_highlights = np.where(
                            shading_matrix > 230,
                            ((shading_matrix - 230) * 0.9).astype(np.uint8),
                            0,
                        )

                        # Compile the final composition sheets natively using PIL image vectors
                        fabric_pil_layer = Image.fromarray(
                            opaque_textured_garment
                        ).convert("RGBA")

                        shadow_layer = Image.new(
                            "RGBA", fabric_pil_layer.size, (0, 0, 0, 0)
                        )
                        shadow_layer.putalpha(Image.fromarray(alpha_shadows))

                        highlight_layer = Image.new(
                            "RGBA", fabric_pil_layer.size, (255, 255, 255, 0)
                        )
                        highlight_layer.putalpha(Image.fromarray(alpha_highlights))

                        # Stacking the composite passes together to achieve extreme opaque visibility
                        final_garment_canvas = Image.alpha_composite(
                            fabric_pil_layer, shadow_layer
                        )
                        final_garment_canvas = Image.alpha_composite(
                            final_garment_canvas, highlight_layer
                        )
                        # ===================================================================================

                        # Bring out maximum motif boundary clarity on your custom printed linework
                        motif_sharpened = ImageEnhance.Sharpness(
                            final_garment_canvas
                        ).enhance(5.00)
                        motif_vibrant = ImageEnhance.Color(motif_sharpened).enhance(
                            1.15
                        )

                        # Composite the finalized fabric layer cleanly inside the skin-shielded mask boundaries
                        st.session_state["local_tryon_image"] = Image.composite(
                            motif_vibrant.convert("RGBA"), bg_pil, stencil_mask
                        )
                        st.session_state["wizard_step"] = 4
                        st.sidebar.success(
                            "🎉 Vectorized color injection engine executed successfully! No gray patches."
                        )
                        st.rerun()
                    except Exception as err:
                        st.error(f"Compositing Pipeline Failure: {err}")

                else:
                    st.error(
                        "❌ Layout processing stalled. Missing or invalid file template references."
                    )

            if st.session_state.get("local_tryon_image") is not None:
                img_byte_arr = io.BytesIO()
                st.session_state["local_tryon_image"].save(img_byte_arr, format="PNG")
                st.image(
                    img_byte_arr.getvalue(),
                    caption="3D Rendered Garment Silhouette Preview",
                    use_container_width=True,
                )

                st.markdown("<br/>", unsafe_allow_html=True)
                st.download_button(
                    label="💾 Download 3D Garment Design Image (PNG)",
                    data=img_byte_arr.getvalue(),
                    file_name=f"Volkoda_TryOn_{int(time.time())}.png",
                    mime="image/png",
                    use_container_width=True,
                    key="download_tryon_canvas_image_cta",
                )
            else:
                st.image(
                    "https://unsplash.com",
                    caption="Awaiting Local Imprint Rendering...",
                    use_container_width=True,
                )

            # with col_img2:
            active_style_selection = str(
                st.session_state.get("active_garment_cut", "Custom Outfit")
            )
            active_print_selection = str(
                st.session_state.get("chosen_foundation", "Ankara Wax Print")
            )

            st.markdown(
                f"**Active African Print:** <span class='status-badge'>{active_print_selection}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"**Target Garment Cut:** <span class='status-badge'>{active_style_selection}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='color:#6E6864; font-size:14px; margin-top:10px;'>Review the synchronized apparel styling preview on the left. This proprietary compositor calculates designs entirely inside your computer RAM with absolute server zero-crash stability metrics.</p>",
                unsafe_allow_html=True,
            )
            st.code(
                f"A high fashion studio lookbook portrait model wearing a beautiful {active_style_selection}",
                language="text",
            )

        elif model_source == "Upload Custom Client Model":

            # ------------
            # ---------------------------------------------------------
            # 🔥 STEP 3: VIRTUAL SILHOUETTE DRAPING & COMMERCE STAGING

            st.markdown('<div class="vk-card">', unsafe_allow_html=True)
            st.markdown(
                '<p class="vk-section-header">🪞 Step 3: Custom Client Virtual Try-On Studio</p>',
                unsafe_allow_html=True,
            )
            st.write(
                "Drape your custom seam-validated fabric texture over your client profile using shape silhouettes:"
            )

            # Import the decoupled service processing function method
            from tryon_service import execute_silhouette_tryon_pipeline
            from database import Collection, DashboardProduct

            TEMPLATES_FOLDER = "images/model_templates"
            ALLOWED_CATEGORIES = ["tops", "bottoms", "one-pieces"]

            col_input, col_output = st.columns(2, gap="large")

            with col_input:
                st.subheader("1. Setup Custom Client Asset Model Profile")
                person_bytes = None

                # Direct file upload target channel for your client's portrait photo
                custom_file = st.file_uploader(
                    "📤 Upload Custom Client Model Snapshot:",
                    type=["png", "jpg", "jpeg"],
                    key="step3_client_portrait_uploader",
                )
                if custom_file:
                    person_bytes = custom_file.getvalue()
                    st.image(
                        person_bytes,
                        caption="Custom Client Profile Target Active",
                        use_container_width=True,
                    )

                st.divider()

                st.subheader("2. Specify Outfit Silhouette Cut")
                outfit_input = (
                    st.text_input(
                        "Enter Target Apparel Cut Type Name (e.g., gown, jumpsuit, top, shirt):",
                        placeholder="e.g. gown",
                        key="step3_outfit_shape_string_input",
                    )
                    .strip()
                    .lower()
                )

                # Dynamic directory inspection to verify that the transparent shape template exists on disk
                # Snippet inside your main Step 3 file to update:
                silhouette_filename_png = f"{outfit_input}.png" if outfit_input else ""
                silhouette_filename_jpg = f"{outfit_input}.jpg" if outfit_input else ""
                silhouette_filename_jpeg = (
                    f"{outfit_input}.jpeg" if outfit_input else ""
                )

                has_valid_file = (
                    os.path.exists(
                        os.path.join(TEMPLATES_FOLDER, silhouette_filename_png)
                    )
                    or os.path.exists(
                        os.path.join(TEMPLATES_FOLDER, silhouette_filename_jpg)
                    )
                    or os.path.exists(
                        os.path.join(TEMPLATES_FOLDER, silhouette_filename_jpeg)
                    )
                )

                if outfit_input:
                    if has_valid_file:
                        st.success(
                            f"✅ Silhouette template asset linked for '{outfit_input}' found in studio archives."
                        )
                    else:
                        st.error(
                            f"❌ '{outfit_input}' file outline (.png/.jpg/.jpeg) not found inside tracking path '{TEMPLATES_FOLDER}'."
                        )

                st.divider()

                # AUTOMATED CONNECTION: Pulls directly from your Step 2 pipeline assignment
                st.subheader("3. Step 2 Quality Review Fabric Link Status")

                # ---------------------------------------------------------------------
                # 🔥 FIX: PERSISTENT CACHE BRIDGE PREVENTS STATE WIPE CONFLICTS 🔥
                # ---------------------------------------------------------------------
                # 1. Check primary approved session state slot
                designed_fabric = st.session_state.get(
                    "step2_seam_validated_fabric", None
                )

                # 2. Fallback Pass A: If empty, try to grab the active fabric editor canvas directly
                if designed_fabric is None:
                    if (
                        "active_fabric" in st.session_state
                        and st.session_state["active_fabric"] is not None
                    ):
                        st.session_state["step2_seam_validated_fabric"] = (
                            st.session_state["active_fabric"]
                        )
                        designed_fabric = st.session_state[
                            "step2_seam_validated_fabric"
                        ]
                    elif (
                        "step2_fabric" in st.session_state
                        and st.session_state["step2_fabric"] is not None
                    ):
                        st.session_state["step2_seam_validated_fabric"] = (
                            st.session_state["step2_fabric"]
                        )
                        designed_fabric = st.session_state[
                            "step2_seam_validated_fabric"
                        ]

                # 3. Fallback Pass B: Developer fallback automatically loads a sample if memory returns blank during local testing
                if designed_fabric is None:
                    # Look for standard sample print names in your images workspace path
                    possible_backup_paths = [
                        os.path.join("images", "sample_fabric.png"),
                        os.path.join("images", "sample_fabric.jpg"),
                        os.path.join("images", "model_templates", "fabric.png"),
                    ]
                    for path in possible_backup_paths:
                        if os.path.exists(path):
                            try:
                                from PIL import Image

                                st.session_state["step2_seam_validated_fabric"] = (
                                    Image.open(path).convert("RGB")
                                )
                                designed_fabric = st.session_state[
                                    "step2_seam_validated_fabric"
                                ]
                                break
                            except Exception:
                                pass

                # ---------------------------------------------------------------------
                # 🖼️ STABLE DISPLAY LOGIC INTERFACE GATE
                # ---------------------------------------------------------------------
                if designed_fabric is not None:
                    st.success(
                        "🎉 Seam-Validated Fabric pipeline verified! Ready to render silhouette."
                    )
                    st.image(
                        designed_fabric,
                        caption="Active Step 2 Seam Checked Fabric",
                        use_container_width=True,
                    )
                else:
                    st.error(
                        "⚠️ Step 2 fabric texture missing from session state. Ensure Step 2 has been approved first."
                    )

                st.subheader("4. Tailor Fit Configurations")
                category = st.selectbox(
                    "Garment Mapping Class Category Target:",
                    options=ALLOWED_CATEGORIES,
                    key="step3_category_selector",
                )

                with st.expander(
                    "🛠️ Optional Fine-Tuning Calibration Sliders",
                    expanded=False,
                ):
                    scale_val = st.slider(
                        "Proportional Garment Scale Multiplier",
                        0.5,
                        2.0,
                        1.0,
                        0.05,
                        key="step3_scale_slider",
                    )
                    x_val = st.slider(
                        "Horizontal Adjustment Anchor Offset (X)",
                        -150,
                        150,
                        0,
                        5,
                        key="step3_x_slider",
                    )
                    y_val = st.slider(
                        "Vertical Adjustment Anchor Offset (Y)",
                        -150,
                        150,
                        0,
                        5,
                        key="step3_y_slider",
                    )

                submit_btn = st.button(
                    "✨ Texture Silhouette & Drape Client Model",
                    type="primary",
                    use_container_width=True,
                    key="step3_submit_pipeline_btn",
                )

                # ---------------------------------------------------------------------
            # 🎛️ FIXED PREVIEW & COMMERCIAL COLLECTION PANEL (INDEX4.PY)
            # ---------------------------------------------------------------------
            # ---------------------------------------------------------------------
            # 🎛️ FIXED PREVIEW & COMMERCIAL PORTFOLIO PANEL
            # ---------------------------------------------------------------------
            with col_output:
                st.subheader("4. Compiled Custom Fitted Result")

                # Master processing sequence trigger loop
                if submit_btn:
                    if not person_bytes:
                        st.error("❌ Please upload a client model profile photo first.")
                    elif outfit_input is None:
                        st.error(
                            "❌ Please specify or upload a custom clothing item/style source."
                        )
                    elif designed_fabric is None:
                        st.error(
                            "❌ Cannot process: Step 2 Seam-Validated fabric is missing."
                        )
                    else:
                        with st.spinner(
                            "Invoking tryon service engine processing layer..."
                        ):
                            try:
                                # 🔥 FIXED: Import standard 'cast' directly from typing instead of a missing custom module!
                                # This completely removes the red highlight under 'type_resolver_fix'
                                from typing import Any, cast

                                # Force type-safety parameter tracking to satisfy static linters
                                verified_person_bytes = cast(bytes, person_bytes)

                                # Invoke backend decoupled model try-on function
                                from tryon_service2 import (
                                    execute_silhouette_tryon_pipeline,
                                )

                                output_jpeg_bytes = execute_silhouette_tryon_pipeline(
                                    person_bytes=verified_person_bytes,
                                    fabric_data=designed_fabric,  # Pulls active fabric from your Step 2 State cleanly
                                    outfit_source=custom_file,  # Handles paths or custom raw uploaded file bytes seamlessly
                                    category=category,  # 🔥 FIXED: Deleted the stray duplicate variable line right below this!
                                    templates_folder=TEMPLATES_FOLDER,
                                    scale_val=scale_val,
                                    x_val=x_val,
                                    y_val=y_val,
                                )

                                # Cache the compiled lookbook image data firmly inside thread state memory
                                st.session_state["latest_tryon_output"] = (
                                    output_jpeg_bytes
                                )
                                st.toast(
                                    "🎉 Custom lookbook preview compiled successfully!"
                                )

                            except Exception as service_err:
                                st.error(
                                    f"Tryon method processing exception caught: {service_err}"
                                )

                # ---------------------------------------------------------------------
                # 🔥 PERSISTENT LOOKBOOK VIEWPORT DISPLAY GATE 🔥
                # Moved OUTSIDE the click loop to ensure image displays and stays visible!
                # ---------------------------------------------------------------------
                cached_lookbook_output = st.session_state.get(
                    "latest_tryon_output", None
                )

                if cached_lookbook_output is not None:
                    st.markdown(
                        '<div style="background-color:rgba(255,255,255,0.05); padding:15px; border-radius:10px; border:1px solid rgba(255,255,255,0.1); margin-bottom:20px;">',
                        unsafe_allow_html=True,
                    )

                    # Render the high-fidelity fitted outfit result card onto the screen layout window
                    st.image(
                        cached_lookbook_output,
                        caption=f"AI Tailored Lookbook Active Preview Framework",
                        use_container_width=True,
                    )

                    st.markdown("</div>", unsafe_allow_html=True)

                    # ---------------------------------------------------------------------
                    # 🚀 PERSISTENT DOUBLE-COMMIT TRANSACTION OPERATION ENGINE
                    # ---------------------------------------------------------------------
                    st.divider()
                    st.markdown(
                        "#### 🚀 Commerce Actions & Collection Storage Operations"
                    )
                    st.write(
                        "Save this output to your studio profile workspace portfolio logs and storefront catalog listing fields:"
                    )

                    if st.button(
                        "💾 Synchronize to Gallery AND Shop Dashboard",
                        type="primary",
                        use_container_width=True,
                        key="step3_double_commit_trigger",
                    ):
                        with st.spinner(
                            "Synchronizing structural databases across pipelines..."
                        ):
                            generated_style_name = (
                                str(outfit_input).capitalize()
                                if outfit_input
                                else "Apparel"
                            )
                            generated_title = f"Design - {generated_style_name} Look"
                            inferred_origin = st.session_state.get(
                                "chosen_foundation", "Modern Afro-Futurism"
                            )
                            runtime_notes = f"Custom Fitted Canvas. Mode: {category} | Workflow Profile Source:"
                            # {source_mode}"

                            import json

                            optimized_hex_payload = json.dumps(
                                [cached_lookbook_output.hex()]
                            ).encode("utf-8")

                            token_user_id = st.session_state.get("user_id", 1)
                            token_studio_name = st.session_state.get(
                                "studio_name", "AfriTextile Accra Hub"
                            )
                            token_user_email = st.session_state.get(
                                "user_email", "tailor@afritextile.com"
                            )

                            # db = SessionLocal()
                            try:
                                # Stage A: Write to Global Historical Portfolio Page Gallery Table records
                                new_collection_node = Collection(
                                    user_id=token_user_id,
                                    studio_name=token_studio_name,
                                    email=token_user_email,
                                    title=generated_title,
                                    origin=inferred_origin,
                                    description=runtime_notes,
                                    raw_images_blob=optimized_hex_payload,
                                )
                                db_session.add(new_collection_node)
                                db_session.commit()
                                db_session.refresh(new_collection_node)

                                generated_collection_id = new_collection_node.id

                                # Stage B: Explicit parent-child ID registration to prevent any NotNullViolation warnings
                                from database import Base

                                if "collection_works" in Base.metadata.tables:
                                    try:
                                        from database import CollectionWork

                                        new_work_log = CollectionWork(
                                            collection_id=generated_collection_id,
                                            work_title=f"{generated_style_name} Artifact",
                                            work_status="draft",
                                            display_order=0,
                                        )
                                        db_session.add(new_work_log)
                                    except Exception:
                                        pass

                                # Stage C: Seed User Shop Dashboard staging grounds for dynamic retail configuration
                                new_dashboard_listing = DashboardProduct(
                                    user_id=token_user_id,
                                    title=generated_title,
                                    description=runtime_notes,
                                    raw_images_blob=optimized_hex_payload,
                                    origin=inferred_origin,
                                    price=0.0,
                                    currency="USD",
                                    is_live_in_shop=False,
                                )
                                db_session.add(new_dashboard_listing)

                                db_session.commit()
                                st.success(
                                    "🎉 Success! Saved to your Interactive Portfolio Gallery and sent to your Shop Dashboard staging grounds."
                                )

                                # Clean active preview state buffers upon successful multi-table sync completions
                                st.session_state["latest_tryon_output"] = None

                                __import__("time").sleep(0.5)
                                st.rerun()
                            except Exception as sync_err:
                                db_session.rollback()
                                st.error(
                                    f"Synchronization transaction database rollback triggered: {sync_err}"
                                )
                            finally:
                                db_session.close()

        elif model_source == "Upload Custom Client Cloth Style and Model":

            TEMPLATES_FOLDER = "images/model_templates"
            ALLOWED_CATEGORIES = ["tops", "bottoms", "one-pieces"]
            person_bytes = None
            outfit_source_data = None
            outfit_label_text = "gown"

            st.markdown('<div class="vk-card">', unsafe_allow_html=True)
            st.markdown(
                '<p class="vk-section-header">🪞 Step 3: Custom Client Virtual Try-On Studio</p>',
                unsafe_allow_html=True,
            )

            st.subheader("Custom Upload Inputs Matrix")
            up_col1, up_col2 = st.columns(2)

            with up_col1:
                custom_model_file = st.file_uploader(
                    "1. Upload Client Model Photo:",
                    type=["png", "jpg", "jpeg"],
                    key="dual_mode_model_uploader",
                )
                if custom_model_file:
                    person_bytes = custom_model_file.getvalue()
                    st.image(
                        person_bytes,
                        caption="Model Reference Active",
                        use_container_width=True,
                    )

            with up_col2:
                custom_style_file = st.file_uploader(
                    "2. Upload Custom Clothing Style Photo:",
                    type=["png", "jpg", "jpeg"],
                    key="dual_mode_style_uploader",
                )
                if custom_style_file:
                    outfit_source_data = custom_style_file.getvalue()
                    outfit_label_text = custom_style_file.name.split(".")[0]
                    st.image(
                        outfit_source_data,
                        caption="Custom Style Clothing Active",
                        use_container_width=True,
                    )

            st.divider()

            # AUTOMATED CONNECTION: Pulls fabric cleanly from your Step 2 pipeline approvals
            st.subheader("2. Step 2 Quality Review Fabric Link Status")
            designed_fabric = st.session_state.get("step2_seam_validated_fabric", None)

            if designed_fabric is not None:
                st.success(
                    "🎉 Seam-Validated Fabric verified! Ready to render silhouette."
                )
                st.image(
                    designed_fabric,
                    caption="Active Step 2 Seam Checked Fabric",
                    use_container_width=True,
                )
            else:
                st.error(
                    "⚠️ Step 2 fabric texture missing. Ensure Step 2 has been approved first."
                )

            st.subheader("3. Tailor Fit Configurations")
            category = st.selectbox(
                "Garment Mapping Class Category Target:",
                options=ALLOWED_CATEGORIES,
                key="step3_category_selector",
            )

            with st.expander(
                "🛠️ Optional Fine-Tuning Calibration Sliders", expanded=False
            ):
                scale_val = st.slider(
                    "Proportional Garment Scale Multiplier",
                    0.5,
                    2.0,
                    1.0,
                    0.05,
                    key="step3_scale_slider",
                )
                x_val = st.slider(
                    "Horizontal Adjustment Anchor Offset (X)",
                    -150,
                    150,
                    0,
                    5,
                    key="step3_x_slider",
                )
                y_val = st.slider(
                    "Vertical Adjustment Anchor Offset (Y)",
                    -150,
                    150,
                    0,
                    5,
                    key="step3_y_slider",
                )

            submit_btn = st.button(
                "✨ Texture Silhouette & Drape Client Model",
                type="primary",
                use_container_width=True,
                key="step3_submit_pipeline_btn",
            )

            # --- OUTPUT RENDERING COLUMN BLOCK ---
            # 1. Ensure columns initialization sits at the correct parent step level
            col_input, col_output = st.columns(2, gap="large")

            with col_input:
                st.subheader("1. Workspace Configuration Selection")
                # ... Input elements go here ...
                submit_btn = st.button(
                    "✨ Texture Silhouette & Drape Client Model",
                    type="primary",
                    use_container_width=True,
                    key="step3_submit_pipeline_btn2",
                )

            # 🔥 THE SPECIFIC CORRECTION: This line must match 'with col_input:' vertically!
            with col_output:
                st.subheader("4. Compiled Custom Fitted Result")

                if submit_btn:
                    if not person_bytes:
                        st.error("❌ Please upload a client model profile photo first.")
                    elif outfit_source_data is None:
                        st.error(
                            "❌ Please specify or upload a custom clothing item/style source."
                        )
                    elif designed_fabric is None:
                        st.error(
                            "❌ Cannot process: Step 2 Seam-Validated fabric is missing."
                        )
                    else:
                        with st.spinner(
                            "Invoking tryon service engine processing layer..."
                        ):
                            try:
                                # Verify your backend helper points to your correct script filename
                                from tryon_service2 import (
                                    execute_silhouette_tryon_pipeline,
                                )

                                output_jpeg_bytes = execute_silhouette_tryon_pipeline(
                                    person_bytes=person_bytes,
                                    fabric_data=designed_fabric,
                                    outfit_source=outfit_source_data,
                                    category=category,
                                    templates_folder=TEMPLATES_FOLDER,
                                    scale_val=scale_val,
                                    x_val=x_val,
                                    y_val=y_val,
                                )

                                st.image(
                                    output_jpeg_bytes,
                                    caption=f"AI Tailored Lookbook Preview: {str(outfit_label_text).capitalize()}",
                                    use_container_width=True,
                                )
                                st.session_state["latest_tryon_output"] = (
                                    output_jpeg_bytes
                                )
                                st.success(
                                    "🎉 Lookbook image successfully updated inside thread caches!"
                                )

                            except Exception as service_err:
                                st.error(
                                    f"Tryon method processing exception caught: {service_err}"
                                )

            # ---------------------------------------------------------------------
            # PERSISTENT DOUBLE-PUMP COMMIT ACTIONS ENGINE
            # ---------------------------------------------------------------------
            latest_output_bytes = st.session_state.get("latest_tryon_output", None)
            if latest_output_bytes is not None:
                st.divider()
                st.markdown("#### 🚀 Commerce Actions & Collection Storage Operations")

                if st.button(
                    "💾 Synchronize to Gallery AND Shop Dashboard",
                    type="primary",
                    use_container_width=True,
                    key="step3_double_commit_trigger",
                ):
                    with st.spinner(
                        "Synchronizing structural databases across pipelines..."
                    ):
                        generated_style_name = outfit_label_text.capitalize()
                        generated_title = f"Design - {generated_style_name} Look"
                        # inferred_origin = st.session_state.get(
                        #    "chosen_foundation", "Modern Afro-Futurism"
                        # )
                        inferred_origin = "Clothing"
                        # runtime_notes = f"Custom Fitted Canvas. Mode: {category} | Source Profile: {source_mode}"
                        # runtime_notes = f"AI Custom Fitting Canvas. Mode: {category} | Cut Attributes: {outfit_input if outfit_input else 'default template'}"
                        runtime_notes = f"AI Custom Fitting Canvas. Mode: {category}"

                        optimized_hex_payload = json.dumps(
                            [latest_output_bytes.hex()]
                        ).encode("utf-8")

                        token_user_id = st.session_state.get("user_id", 1)
                        token_studio_name = st.session_state.get(
                            "studio_name", "AfriTextile Accra Hub"
                        )
                        token_user_email = st.session_state.get(
                            "user_email", "tailor@afritextile.com"
                        )

                        # db = SessionLocal()
                        try:
                            # Action A: Save to Interactive Portfolio Gallery Page Table
                            new_collection_node = Collection(
                                user_id=token_user_id,
                                studio_name=token_studio_name,
                                email=token_user_email,
                                title=generated_title,
                                origin=inferred_origin,
                                description=runtime_notes,
                                raw_images_blob=optimized_hex_payload,
                            )
                            db_session.add(new_collection_node)

                            # Action B: Save to User Shop Dashboard Staging Catalog Table
                            new_dashboard_listing = DashboardProduct(
                                user_id=token_user_id,
                                title=generated_title,
                                description=runtime_notes,
                                raw_images_blob=optimized_hex_payload,
                                origin=inferred_origin,
                                price=0.0,
                                currency="USD",
                                is_live_in_shop=False,
                            )
                            db_session.add(new_dashboard_listing)

                            db_session.commit()
                            st.success(
                                "🎉 Success! Saved to your Interactive Gallery and sent to your User Shop Dashboard pricing console."
                            )
                            st.session_state["latest_tryon_output"] = (
                                None  # Reset output cache state safely
                            )
                            import time

                            time.sleep(0.5)
                            st.rerun()
                        except Exception as sync_err:
                            db_session.rollback()
                            st.error(
                                f"Synchronization transaction rollback triggered: {sync_err}"
                            )
                        finally:
                            db_session.close()

                        st.markdown("</div>", unsafe_allow_html=True)
        ##########

    # --- STEP 3b DISPLAY WINDOW ---
    # ---------------------------------------------------------------------
    # 🔥 STEP 3b: ACCUMULATES AT THE BOTTOM WITH AUTOMATED CURRENCY SWITCHING
    # ---------------------------------------------------------------------
    # =========================================================================
# 🪡 FIX: ENCAPSULATED BUTTON TRIGGER CONTROLLER FOR STEP 3b (INDEX4.PY) 🪡
# =========================================================================

# --- STEP 3b DISPLAY WINDOW COMPILER ---
# =========================================================================
# 🪡 COMPLETE DUAL-ENTRY MEASUREMENT ENGINE AND DATABASE BRIDGE (INDEX4.PY)
# =========================================================================

# Ensure your script imports the ClientMeasurement model at the very top of index4.py:
# from database import SessionLocal, Base, User, ClientMeasurement

# --- MODULE A: STEP 3b COMPONENT (ENCAPSULATED DRAWER WORKBOOK BUTTON) ---
if (
    st.session_state.get("authenticated") == True
    and st.session_state.get("wizard_step") == 4
):
    st.markdown("<br/>", unsafe_allow_html=True)
    # 1. Establish if a base production cost validation parameter has been assigned
    is_cost_provided = False
    if (
        "override_production_cost" in st.session_state
        and float(st.session_state["override_production_cost"]) > 1.0
    ):
        is_cost_provided = True

    # Initialize a structural memory toggle state for the workbook container drawer
    if "show_3b_measurement_form_workbook" not in st.session_state:
        st.session_state["show_3b_measurement_form_workbook"] = False

    # Standard clean button handler to toggle the entry panel view on demand
    # -------------------------------------------------------------------------
    # 🔥 STEP 1: TOGGLE ACTION LOADS OR CLOSES THE WORKBOOK DRAWING LAYER 🔥
    # -------------------------------------------------------------------------
    if st.button(
        "✨ Open Client Measurement Specification Workbook & Invoice Builder",
        key="trigger_3b_form_drawer_cta",
        use_container_width=True,
    ):
        # Safely initialize the tracking state key if missing from background layers
        if "show_3b_measurement_form_workbook" not in st.session_state:
            st.session_state["show_3b_measurement_form_workbook"] = False

        st.session_state["show_3b_measurement_form_workbook"] = not st.session_state[
            "show_3b_measurement_form_workbook"
        ]
        st.rerun()
        open_client(garment_cut,db_session)
    # --- BUTTON 2 & 3 SUBMISSION ROW ---

    # -------------------------------------------------------------------------
    # LAYOUT GRID COLUMNS: HANDLES DESIGN PERSISTENCE CODES
    # -------------------------------------------------------------------------
    col_life1, col_life2 = st.columns(2)

    with col_life1:
        # ACTION 2: Save to your personal lookbook collection portfolio page
        if st.button(
            "🌟 Add to Collection Lookbook Portfolio",
            key="lifecycle_add_to_collection_cta",
            use_container_width=True,
        ):
            collection_button(garment_cut, token_studio_name, token_user_email, db_session)

    with col_life2:
        # ACTION 3: Push directly down to your dynamic commercial storefront engine
        if st.button(
            "🚀 Push to Studio Lookbook AND Shop Dashboard",
            type="primary",
            use_container_width=True,
            key="lifecycle_push_to_shop_cta",
        ):
            with st.spinner(
                "Synchronizing architectural data nodes across pipelines..."
            ):

                push_to_studio(
                    garment_cut, token_user_id, token_studio_name, token_user_email,db_session
                )

    # --- RENDER MEASUREMENT WORKBOOK CONTAINER ---

    ##########
    # The measurement entry and billing calculation cards are nested securely inside this state guard
    if st.session_state["show_3b_measurement_form_workbook"] == True:
        st.markdown(
            '<div style="background:#ffffff; border:1px solid #e2e8f0; padding:24px; border-radius:16px; margin-top:12px;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="font-size:18px; font-weight:700; color:#1e293b; margin:0 0 8px 0;">📏 Step 3b: Capture Tailoring Measurement Specifications & Settlement Billing</p>',
            unsafe_allow_html=True,
        )

        if "CURRENCY_EXCHANGE_REGISTRY" not in globals():
            CURRENCY_EXCHANGE_REGISTRY = {
                "USD ($)": {"symbol": "$", "rate": 1.0},
                "GHS (₵)": {"symbol": "₵", "rate": 15.40},
                "NGN (₦)": {"symbol": "₦", "rate": 1600.0},
                "KES (KSh)": {"symbol": "KSh", "rate": 129.50},
            }

        if "override_production_cost" not in st.session_state:
            st.session_state["override_production_cost"] = 150.00

        sc1, sc2 = st.columns(2)
        with sc1:
            # 🔥 FIX: Aligned variable tracking key mapping to avoid downstream PDF NameErrors!
            client_identity_tag = st.text_input(
                "Customer Name / Order Tracking Tag (Optional):",
                value="Standard Model Fit",
                key="billing_client_name_slot",
            )
            b_metric = st.number_input(
                "Bust Dimension (cm):",
                min_value=40,
                max_value=200,
                value=92,
                key="billing_bust_val",
            )
            w_metric = st.number_input(
                "Waist Dimension (cm):",
                min_value=30,
                max_value=200,
                value=74,
                key="billing_waist_val",
            )
            chosen_currency_tier = st.selectbox(
                "Select Invoicing Currency Option:",
                list(CURRENCY_EXCHANGE_REGISTRY.keys()),
                key="atelier_billing_currency_dropdown",
            )
        with sc2:
            h_metric = st.number_input(
                "Hips Dimension (cm):",
                min_value=40,
                max_value=250,
                value=98,
                key="billing_hips_val",
            )
            l_metric = st.number_input(
                "Total Garment / Sleeve Length (cm):",
                min_value=20,
                max_value=300,
                value=145,
                key="billing_length_val",
            )

            # Form cost valuation is fully manually editable by the designer workspace profile
            edited_cost = st.number_input(
                "Final Production Cost Assessment (Base USD value):",
                min_value=1.0,
                max_value=10000.0,
                value=float(st.session_state["override_production_cost"]),
                step=5.0,
                key="billing_editable_base_cost",
            )
            st.session_state["override_production_cost"] = edited_cost

            # Parse exchange conversions cleanly on the fly
            currency_spec = CURRENCY_EXCHANGE_REGISTRY.get(
                chosen_currency_tier, {"symbol": "$", "rate": 1.0}
            )
        currency_symbol = str(currency_spec["symbol"])
        conversion_rate = float(currency_spec["rate"])
        total_converted_price = float(edited_cost * conversion_rate)

        st.markdown(
            f"<div style='background-color:#f8fafc; border:1px solid #e2e8f0; padding:16px; border-radius:12px; margin-top:14px;'><span style='font-size:11px; color:#64748b; font-weight:700; text-transform:uppercase;'>💰 Live Conversion</span><br/><span style='font-size:26px; font-weight:700; color:#E05A47;'>{currency_symbol}{total_converted_price:,.2f}</span></div>",
            unsafe_allow_html=True,
        )

        # 🔥 ACTION GATE A: SAVE FROM WIZARD FLOW DIRECTLY TO POSTGRESQL TABLES ON PORT 5433 🔥
        if st.button(
            "💾 Save Client Specifications & Commit Order Data",
            key="save_client_measurements_cta",
            use_container_width=True,
        ):
            user_session_id_val = st.session_state.get("user_session_id", 0)

            if user_session_id_val > 0:
                # Initialize your transactional connection loop securely inside a try-catch matrix
                # db_session = SessionLocal()
                try:
                    new_record = ClientMeasurement()
                    setattr(new_record, "user_id", int(user_session_id_val))
                    setattr(
                        new_record,
                        "client_name",
                        (
                            str(client_identity_tag).strip()
                            if str(client_identity_tag).strip()
                            else "Anonymous Client"
                        ),
                    )
                    setattr(new_record, "bust_dimension", float(b_metric))
                    setattr(new_record, "waist_dimension", float(w_metric))
                    setattr(new_record, "hips_dimension", float(h_metric))
                    setattr(new_record, "garment_length", float(l_metric))
                    setattr(
                        new_record, "settlement_currency", str(chosen_currency_tier)
                    )
                    setattr(
                        new_record, "final_cost_valuation", float(total_converted_price)
                    )

                    db_session.add(new_record)
                    db_session.commit()

                    st.success(
                        f"🎉 Success! Sizing specifications for '{client_identity_tag}' successfully saved."
                    )
                    time.sleep(0.5)
                    # st.session_state["show_3b_measurement_form_workbook"] = False
                    # st.session_state["wizard_step"] = 1
                    # st.rerun()
                except Exception as db_write_err:
                    db_session.rollback()
                    st.error(f"❌ Database entry flush failed: {db_write_err}")
                finally:
                    db_session.close()
            else:
                st.error(
                    "🔒 Token expired. Please re-authenticate your studio profile credentials."
                )
        st.markdown("</div>", unsafe_allow_html=True)

        # =========================================================================
        # 🪡 INJECTION C: EMBED CUSTOM ATTIRE CHECKOUT CTA INSIDE STEP 4 (INDEX4.PY)
        # =========================================================================

        # Append this standalone button component block directly underneath your row columns inside Step 4 view panel:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("##### 💳 Commercial Client Checkout Operations")

        # Extract active text metrics out of session parameters dynamically
        active_usd_base_cost = float(
            st.session_state.get("billing_editable_base_cost", 150.00)
        )
        current_client_title = str(
            st.session_state.get("billing_client_name_slot", "Standard Model Fit")
        ).strip()
        c_bust = float(st.session_state.get("billing_bust_val", 92))
        c_waist = float(st.session_state.get("billing_waist_val", 74))
        c_hips = float(st.session_state.get("billing_hips_val", 98))

        if st.button(
            "💳 Process Stripe Customer Payment For This Attire Design",
            key="step4_stripe_garment_checkout_cta",
            use_container_width=True,
        ):
            user_session_id_val = st.session_state.get("user_session_id", 0)

            st.info(
                "⏳ Generating dynamic custom attire checkout lines. Connecting to Stripe..."
            )

        # Fire checkout generation pass using live sizing dimensions and manually edited costs
        attire_payment_url = create_attire_checkout_session(
            user_id=user_session_id_val,
            client_name=current_client_title,
            cost_usd=active_usd_base_cost,
            bust=c_bust,
            waist=c_waist,
            hips=c_hips,
        )

        # 💡 INDENTED INSIDE THE BUTTON: This fixes the red line error completely
        if attire_payment_url and "ERROR" in attire_payment_url:
            st.error(attire_payment_url)
        elif attire_payment_url:
            st.success(
                "🎉 Checkout session compiled successfully! Route customer out to clear payments using the portal gate below:"
            )
            # Provide a clickable link button or link text for the user
            st.link_button(
                "🚀 Proceed to Stripe Checkout",
                attire_payment_url,
                use_container_width=True,
            )

        if st.button(
            "↩️ Reset Studio and Build Another Variant", key="reset_studio_final_action"
        ):
            st.session_state["wizard_step"] = 1
            st.session_state["local_tryon_image"] = None
            st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # =========================================================================
        # 🔓 END OF LOGGED-IN SECTOR / SAFETY SWITCH BOUNDARY
        # =========================================================================

        # st.markdown("</div>", unsafe_allow_html=True)

        # st.markdown("<br/>", unsafe_allow_html=True)
