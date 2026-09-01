import streamlit as st
import time
import os
import base64
import json
import urllib.request
from io import BytesIO
from PIL import Image
import numpy as np
from typing import Any, cast
from database import (
    Order,
    Product,
    TryOnFeatureMeter,
    User,
)  # Adjust imports based on your database tables

# 🔑 REPLACE THIS WITH YOUR DYNAMIC OR TEST KEY FROM YOUR PAYSTACK DASHBOARD
PAYSTACK_SECRET_KEY = os.getenv(
    "PAYSTACK_SECRET_KEY", "sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
ALLOWED_CATEGORIES = ["tops", "bottoms", "one-pieces"]


def render_marketplace_hub(db, token_user_id, COMMISSION_RATE=0.10):

    # -------------------------------------------------------------------
    # PART A: CORE INTERACTIVE CSS LIGHTBOX INFRASTRUCTURE
    # -------------------------------------------------------------------
    st.markdown(
        """
        <style>
        /* Hidden layout checkbox state toggles */
        .vk-shop-modal-switch, .vk-img-modal-switch { display: none !important; }
        
        /* Lightbox Overlay Backdrops for Merchant Profiles and Product Image Zoom Overviews */
        .vk-shop-lightbox-backdrop, .vk-img-lightbox-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(6px); z-index: 1000000; display: flex; justify-content: center; align-items: center; opacity: 0; pointer-events: none; transition: opacity 0.2s ease-in-out; }
        .vk-shop-popup-card { background: #ffffff; padding: 24px; border-radius: 16px; width: 90%; max-width: 360px; text-align: center; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); transform: scale(0.9); transition: transform 0.2s ease-in-out; font-family: sans-serif; }
        .vk-img-popup-card { background: #ffffff; padding: 12px; border-radius: 12px; max-width: 500px; width: 85%; text-align: center; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.15); transform: scale(0.9); transition: transform 0.2s ease-in-out; }
        .vk-shop-modal-switch:checked ~ .vk-shop-lightbox-backdrop, .vk-img-modal-switch:checked ~ .vk-img-lightbox-backdrop { opacity: 1; pointer-events: auto; }
        .vk-shop-modal-switch:checked ~ .vk-shop-lightbox-backdrop .vk-shop-popup-card, .vk-img-modal-switch:checked ~ .vk-img-lightbox-backdrop .vk-img-popup-card { transform: scale(1); }
        .vk-shop-modal-close-btn { margin-top: 18px; background-color: #E05A47; color: white !important; padding: 8px 20px; border-radius: 6px; font-weight: 700; font-size: 13px; cursor: pointer; display: inline-block; text-decoration: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------
    # PART B: SECURE DATA AND USAGE QUERY INITIALIZATION
    # -------------------------------------------------------------------
    active_cart_orders = (
        db.query(Order)
        .filter(Order.status == "cart", Order.buyer_id == token_user_id)
        .all()
    )
    total_cart_units = sum(int(item.quantity) for item in active_cart_orders)

    buyer_record = db.query(User).filter(User.id == token_user_id).first()
    buyer_email = (
        getattr(buyer_record, "email", "customer@glameeri.com")
        if buyer_record
        else "customer@glameeri.com"
    )

    raw_meter_query = (
        db.query(TryOnFeatureMeter)
        .filter(TryOnFeatureMeter.user_id == token_user_id)
        .first()
    )
    if not raw_meter_query:
        new_meter_row = TryOnFeatureMeter(
            user_id=token_user_id, free_uses_left=5, has_premium_access=False
        )
        db.add(new_meter_row)
        db.commit()
        raw_meter_query = (
            db.query(TryOnFeatureMeter)
            .filter(TryOnFeatureMeter.user_id == token_user_id)
            .first()
        )

    meter: Any = raw_meter_query
    safe_meter = cast(Any, meter)
    has_premium = bool(getattr(safe_meter, "has_premium_access", False))
    free_left = int(getattr(safe_meter, "free_uses_left", 0))

    # -------------------------------------------------------------------
    # PART C: GLOBAL MULTI-COLUMN INTERFACE DIVISION (NO SIDEBARS)
    # -------------------------------------------------------------------
    col_main_content, col_right_widgets = st.columns([2.1, 0.9], gap="large")

    # =========================================================================
    # 🏢 LEFT MAIN CONTENT COLUMN: SEARCH BAR & 3-COLUMN PRODUCT CATALOG 🏢
    # =========================================================================
    with col_main_content:
        st.markdown(
            "<h1 style='font-size: 19px; font-weight: bold;'>🔎 Lookbook Query Finder</h1>",
            unsafe_allow_html=True,
        )

        search_query = st.text_input(
            "Search catalog entries via Artisan Username, Product Title, Description, or Style Notes (Tags):",
            placeholder="Type username, title, descriptive words, style attributes...",
            key="global_storefront_search_field"
        ).strip()

        # =========================================================================
        # 🗑️ ABSOLUTE DELETION GATEWAY: ERASES THE UPPER MERCHANT PRESENCE BLOCK 🗑️
        # =========================================================================
        # ✅ FIXED: Any separate code blocks rendering "🌟 Deployed Shop Merchant Presence", 
        # duplicate profiles, or "No corporate profile log attached yet." right here 
        # have been completely removed from the page header!

        st.markdown("### 🏷️ Available Studio Inventory Catalog")
        if not catalog_products:
            st.warning("No apparel assets match your criteria matrices.")
        else:
            # =========================================================================
            # 🔒 TUPLE DECOUPLING: STRIP INVENTORY ENTRIES INTO INDEPENDENT DATA NODES 🔒
            # =========================================================================
            decoupled_catalog = []
            for item in catalog_products:
                decoupled_catalog.append({
                    "id": int(item.id),
                    "seller_id": int(item.seller_id),
                    "title": str(item.title),
                    "price": float(item.price),
                    "description": str(item.description or "No descriptor loaded."),
                    "image_url_raw": str(item.image_url or ""),  
                    "is_fabric": bool(getattr(item, "is_fabric", False))
                })

            # Render catalog items cleanly distributed into 3 columns per row
            for row_idx in range(0, len(decoupled_catalog), 3):
                grid_cols = st.columns(3, gap="medium")
                for i, prod_data in enumerate(decoupled_catalog[row_idx : row_idx + 3]):
                    
                    p_id = prod_data["id"]
                    p_seller_id = prod_data["seller_id"]
                    
                    with grid_cols[i]:
                        # Query the seller completely independent from the product loop scope
                        seller_profile = db.query(User).filter(User.id == p_seller_id).first()
                        s_name = "Glameeri Artisan Label"
                        s_bio = "No public studio overview logged yet."
                        s_img = "https://unsplash.com"
                        s_email = "studio@glameeri.com"
                        
                        if seller_profile:
                            s_name = str(getattr(seller_profile, "studio_name", s_name))
                            s_bio = str(getattr(seller_profile, "biography", s_bio))
                            s_email = str(getattr(seller_profile, "email", s_email))
                            pfp_field = str(getattr(seller_profile, "profile_picture_name", ""))
                            if pfp_field.startswith("data:image") or pfp_field.startswith("http"):
                                s_img = pfp_field

                        # Resolve product display images cleanly
                        store_product_display_source = "https://unsplash.com"
                        db_img_str = prod_data["image_url_raw"].strip()
                        
                        if db_img_str:
                            if "base64," in db_img_str or db_img_str.startswith("http"):
                                store_product_display_source = db_img_str
                            else:
                                STOCK_CLOTHING_GALLERY = [
                                    "https://unsplash.com",
                                    "https://unsplash.com",
                                    "https://unsplash.com"
                                ]
                                store_product_display_source = STOCK_CLOTHING_GALLERY[p_id % len(STOCK_CLOTHING_GALLERY)]

                        show_profile_card = st.session_state.get("step3_broadcast_profile_parameters", True)

                        if show_profile_card:
                            # Renders the compact verified badge at the top of each item card cleanly!
                            profile_html_section = f"<input type='checkbox' id='vkStorefrontProfileToggle_{p_id}' class='vk-shop-modal-switch' /><label for='vkStorefrontProfileToggle_{p_id}' style='display: flex; align-items: center; gap: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-bottom: none; padding: 10px; margin-bottom: 0; border-top-left-radius: 8px; border-top-right-radius: 8px; cursor: pointer;' title='Click to view profile'><img src='{s_img}' style='width: 34px; height: 34px; border-radius: 50%; object-fit: cover; border: 1.5px solid #E05A47;'/><div style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap;'><p style='margin: 0; font-size: 8px; color: #E05A47; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>🌟 Verified Creator (View Profile)</p><h5 style='margin: 0; color: #1e293b; font-size: 12px; font-weight: 800; text-decoration: underline;'>{s_name}</h5></div></label><div class='vk-shop-lightbox-backdrop'><div class='vk-shop-popup-card'><img src='{s_img}' style='width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #E05A47; margin: 0 auto 12px auto; display: block;/><h3 style='margin: 0; color: #1e293b; font-size: 20px; font-weight: 800;'>{s_name}</h3><p style='margin: 4px 0 14px 0; font-size: 12px; color: #E05A47; font-weight: 600;'>{s_email}</p><div style='border-top: 1px solid #e2e8f0; padding-top: 12px; text-align: left;'><span style='font-size: 10px; color: #94a3b8; font-weight: 700; text-transform: uppercase;'>📜 Studio Biography:</span><p style='margin: 4px 0 0 0; font-size: 13px; color: #334155; line-height: 1.4; font-style: italic;'>\"{s_bio}\"</p></div><label for='vkStorefrontProfileToggle_{p_id}' class='vk-shop-modal-close-btn'>↩️ Close Studio Profile</label></div></div>"
                            st.markdown(profile_html_section, unsafe_allow_html=True)

                        # Render the clean design clothing product graphic securely
                        st.image(store_product_display_source, use_container_width=True)

                        # Description metadata box module
                        clean_prod_desc = str(prod_data["description"])
                        st.markdown(
                            f"""
                            <div style="border: 1px solid #e2e8f0; border-top: none; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; padding: 12px; background: white; margin-top: -6px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); font-family: sans-serif;">
                                <h4 style="margin: 0 0 4px 0; color: #2d3748; font-size: 15px; font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{prod_data['title']}</h4>
                                <p style="font-size: 16px; font-weight: bold; color: #E05A47; margin: 4px 0;">${prod_data['price']:.2f}</p>
                                <p style="font-size: 11px; color: #718096; height: 34px; overflow: hidden; line-height: 1.3; margin: 0;">{clean_prod_desc}</p>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )

                        # Standard transactional shopping button interface
                        if st.button("🛒 Append to Cart", key=f"add_cart_btn_{p_id}", use_container_width=True):
                            new_cart_entry = Order(buyer_id=token_user_id, seller_id=p_seller_id, product_id=p_id, status="cart", quantity=1, unit_price=prod_data['price'])
                            db.add(new_cart_entry)
                            db.commit()
                            st.toast(f"'{prod_data['title']}' appended to cart tray successfully!")
                            time.sleep(0.1)
                            st.rerun()

                        # Unlocked global try-on accessibility for all active sessions
                        if not prod_data["is_fabric"]:
                            btn_label = "✨ Try On (Premium Active)" if has_premium else ("✨ Try On" if free_left > 0 else "🔒 Try On (Limit Exceeded)")
                            disabled_flag = False if (has_premium or free_left > 0) else True

                            if st.button(btn_label, key=f"tryon_act_{p_id}", disabled=disabled_flag, use_container_width=True):
                                st.session_state["active_tryon_target_product_id"] = p_id
                                st.rerun()

                        else:
                            # Render a locked/read-only indicator card for external general storefront browsers
                            st.button("🔒 Try On (Isolated to Designer Session)", key=f"disabled_tryon_mask_{p_id}", disabled=True, use_container_width=True)

        # --- DYNAMIC ATTACHMENT: SLIDER CONTROLS RENDERING IN AN ISOLATED FRAGMENT CANVAS ---
        target_selection_id = st.session_state.get("active_tryon_target_product_id", None)
        if target_selection_id:
            active_fitter_product = db.query(Product).filter(Product.id == target_selection_id).first()
            if active_fitter_product:
                
                # ✅ FIXED: Enforce a fallback disabled check calculation in the parent block before running the canvas
                btn_disabled_state = False if (has_premium or free_left > 0) else True

                @st.fragment
                def render_isolated_tryon_canvas(active_product, meter_row, is_disabled_flag):
                    st.markdown(f"#### 👗 High-Speed Local Tuning Canvas: **{active_product.title}**")
                    
                    with st.form(key=f"isolated_local_fitter_form_{active_product.id}"):
                        slider_c1, slider_c2 = st.columns(2)
                        with slider_c1:
                            person_file = st.file_uploader("Upload Your Photo (Person):", type=["png", "jpg", "jpeg"], key="p_upload_core")
                            if person_file:
                                st.image(person_file, caption="Target Person Mannequin", width=140)
                        with slider_c2:
                            category_selection = st.selectbox("Garment Mapping Category Structure Type:", options=ALLOWED_CATEGORIES, index=2)
                            scale_val = st.slider("Garment Scale Multiplier Factor:", min_value=0.5, max_value=2.0, value=1.0, step=0.02)
                            x_val = st.slider("Horizontal Adjust Offset (Left ⇄ Right):", min_value=-300, max_value=300, value=0, step=2)
                            y_val = st.slider("Vertical Adjust Offset (Up ⇄ Down):", min_value=-300, max_value=300, value=0, step=2)

                        action_row1, action_row2 = st.columns(2)
                        with action_row1:
                            execute_render = st.form_submit_button("✨ Apply & Replace Clothing", type="primary", use_container_width=True)
                        with action_row2:
                            clear_canvas = st.form_submit_button("↩️ Clear Selection Canvas", use_container_width=True)

                    if clear_canvas:
                        st.session_state["active_tryon_target_product_id"] = None
                        st.session_state[f"active_tryon_render_{active_product.id}"] = None
                        st.rerun()

                    if execute_render:
                        if not person_file:
                            st.error("Missing asset constraints! Please upload your portrait photo template first.")
                        else:
                            with st.spinner("Processing image components locally on your CPU via rembg engine..."):
                                try:
                                    import io
                                    person_img = Image.open(io.BytesIO(person_file.getvalue())).convert("RGBA")
                                    
                                    safe_prod_obj = cast(Any, active_product)
                                    raw_db_image_source: str = str(getattr(safe_prod_obj, "image_url", ""))
                                    raw_garment_bytes = None

                                    if raw_db_image_source.startswith("data:image"):
                                        raw_b64_text_string: str = raw_db_image_source.split(",")
                                        raw_garment_bytes = base64.b64decode(raw_b64_text_string)
                                    elif raw_db_image_source.startswith("http"):
                                        req = urllib.request.Request(raw_db_image_source, headers={"User-Agent": "Mozilla"})
                                        with urllib.request.urlopen(req) as web_res:
                                            raw_garment_bytes = web_res.read()

                                    if not raw_garment_bytes:
                                        st.error("❌ Failed to resolve active catalog image data fields into byte streams.")
                                        st.stop()

                                    import rembg
                                    ai_remove_func = getattr(rembg, "remove")
                                    clean_garment_bytes = ai_remove_func(raw_garment_bytes)
                                    garment_img = Image.open(io.BytesIO(clean_garment_bytes)).convert("RGBA")

                                    bbox = garment_img.getbbox()
                                    if bbox:
                                        garment_img = garment_img.crop(bbox)

                                    w_person, h_person = person_img.size

                                    if category_selection == "tops" or category_selection == "one-pieces":
                                        target_width = int(w_person * 0.54 * scale_val)
                                        target_height = int(h_person * 0.46 * scale_val)
                                        center_x = (w_person // 2) + x_val
                                        center_y = int(h_person * 0.46) + y_val
                                    else:
                                        target_width = int(w_person * 0.48 * scale_val)
                                        target_height = int(h_person * 0.52 * scale_val)
                                        center_x = (w_person // 2) + x_val
                                        center_y = int(h_person * 0.72) + y_val

                                    target_width = max(10, target_width)
                                    target_height = max(10, target_height)

                                    resized_garment = garment_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

                                    person_arr = np.array(person_img)
                                    garment_arr = np.array(resized_garment)

                                    x_paste = center_x - (target_width // 2)
                                    y_paste = center_y - (target_height // 2)

                                    p_y1, p_y2 = max(0, y_paste), min(h_person, y_paste + target_height)
                                    p_x1, p_x2 = max(0, x_paste), min(w_person, x_paste + target_width)

                                    g_y1, g_y2 = max(0, -y_paste), max(0, -y_paste) + (p_y2 - p_y1)
                                    g_x1, g_x2 = max(0, -x_paste), max(0, -x_paste) + (p_x2 - p_x1)

                                    if p_y2 > p_y1 and p_x2 > p_x1:
                                        bg_crop = person_arr[p_y1:p_y2, p_x1:p_x2]
                                        fg_crop = garment_arr[g_y1:g_y2, g_x1:g_x2]

                                        alpha_mask = fg_crop[:, :, 3] / 255.0
                                        alpha_mask = np.expand_dims(alpha_mask, axis=2)

                                        blended = (fg_crop[:, :, :3] * alpha_mask + bg_crop[:, :, :3] * (1.0 - alpha_mask)).astype(np.uint8)

                                        person_arr[p_y1:p_y2, p_x1:p_x2, :3] = blended
                                        person_arr[p_y1:p_y2, p_x1:p_x2, 3] = 255

                                    final_img = Image.fromarray(person_arr)
                                    output_buffer = BytesIO()
                                    final_img.convert("RGB").save(output_buffer, format="PNG")
                                    final_bytes = output_buffer.getvalue()

                                    if not has_premium:
                                        meter_row.free_uses_left = max(0, int(meter_row.free_uses_left) - 1)
                                        db.commit()

                                    st.session_state[f"active_tryon_render_{active_product.id}"] = final_bytes
                                    st.success("High-speed local rendering complete!")
                                except Exception as e:
                                    st.error(f"Local image processing pipeline encountered a failure: {e}")

                    active_render_key = f"active_tryon_render_{active_product.id}"
                    if st.session_state.get(active_render_key) is not None:
                        st.markdown("<div style='border: 2px dashed #15c39a; padding: 15px; border-radius: 8px; background-color: #f0fdf4; margin-top: 15px;'>", unsafe_allow_html=True)
                        st.image(st.session_state[active_render_key], caption="Tailored Output Local Fit", use_container_width=True)
                        
                        close_col1, close_col2 = st.columns(2)
                        with close_col1:
                            st.download_button(
                                label="📥 Save Final Look Image",
                                data=st.session_state[active_render_key],
                                file_name=f"fitted_{str(active_product.title).lower()}.png",
                                mime="image/png",
                                use_container_width=True,
                                key=f"dl_button_catalog_{active_product.id}"
                            )
                        with close_col2:
                            if st.button("❌ Close Canvas Preview", key=f"close_canvas_fitter_{active_product.id}", use_container_width=True, type="secondary"):
                                st.session_state[active_render_key] = None
                                st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)

                    # ✅ FIXED: Now uses the parameter variable 'is_disabled_flag' passed safely into the function scope!
                    if is_disabled_flag:
                        st.caption("⚠️ Try-On threshold exceeded.")
                        if st.button("Unlock Unlimited ($9.99)", key=f"premium_buy_{active_product.id}", type="primary", use_container_width=True):
                            try:
                                req_payload = {
                                    "email": buyer_email,
                                    "amount": 999,
                                    "callback_url": "http://localhost:8501",
                                    "metadata": {"custom_fields": [{"display_name": "Context", "variable_name": "checkout_type", "value": "upgrade"}]}
                                }
                                # Ensure the full API link parameter structure is used
                                req = urllib.request.Request(
                                    "https://paystack.co",
                                    data=json.dumps(req_payload).encode("utf-8"),
                                    headers={"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}", "Content-Type": "application/json"}
                                )
                                with urllib.request.urlopen(req) as res_upgrade:
                                    res_data = json.loads(res_upgrade.read().decode("utf-8"))
                                    if res_data.get("status"):
                                        upgrade_gateway_url = res_data["data"]["authorization_url"]
                                        setattr(safe_meter, "has_premium_access", True)
                                        db.commit()
                                        st.markdown(f'<a href="{upgrade_gateway_url}" target="_blank" style="display: block; text-align: center; background-color: #15c39a; color: white; padding: 12px; border-radius: 6px; font-weight: bold; text-decoration: none;">➡️ Authorize Paystack Upgrade</a>', unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Paystack Initialize Error: {e}")

                # ✅ FIXED: Explicitly pass the calculated state integer variable into the call!
                render_isolated_tryon_canvas(active_fitter_product, safe_meter, btn_disabled_state)


    # =========================================================================
    # 📊 RIGHT CONTAINER: FIXED BASKET MONITOR HEADER & ACTIVE SHOPPING CART 📊
    # =========================================================================
    with col_right_widgets:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; background: #ffffff; border: 1px solid #e2e8f0; padding: 14px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); font-family: sans-serif;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="position: relative; background-color: #E05A47; width: 46px; height: 46px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        🛒
                        <div style="position: absolute; top: -5px; right: -5px; background-color: #1e293b; color: white; border-radius: 50%; width: 20px; height: 22px; font-size: 10px; font-weight: bold; display: flex; justify-content: center; align-items: center; border: 2px solid #ffffff;">
                            {total_cart_units}
                        </div>
                    </div>
                    <div>
                        <h4 style="margin: 0; color: #1e293b; font-weight: 800; font-size: 15px;">Basket Status</h4>
                        <p style="margin: 0; color: #64748b; font-size: 11px;">{total_cart_units} item(s) staged for checkout</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 style='font-size: 19px; font-weight: bold;'>📊 AI Try-On License Status</h1>",
            unsafe_allow_html=True,
        )

        # st.markdown(
        #    "<h4 style='color:#1e293b; font-weight:800; margin-top:0;'>📊 AI Try-On License Status</h4>",
        #    unsafe_allow_html=True,
        # )
        if has_premium:
            st.success("👑 Account Status: Premium Unlimited Access Verified")
        else:
            st.metric(
                label="Free Fitting Submissions Left",
                value=f"{free_left} try-on(s)",
                help="Upgrade to premium license terms to unlock unlimited texture mapping pipelines instantly.",
            )
        st.markdown(
            "<h1 style='font-size: 17px; font-weight: bold;'>🛒 Active Cart Workspace</h1>",
            unsafe_allow_html=True,
        )

        # st.markdown(
        #    "<br/><h4 style='color:#1e293b; font-weight:800;'>🛒 Active Cart Workspace</h4>",
        #    unsafe_allow_html=True,
        # )
        if not active_cart_orders:
            # st.info("Your shopping cart drawer is empty. Select items on the left.")
            st.info("Your shopping cart drawer is empty.")
        else:
            cart_gross_total = 0.0
            for current_order in active_cart_orders:
                associated_product = current_order.product
                if not associated_product:
                    continue

                item_retail_price = float(associated_product.price)
                item_gross_calculated_price = current_order.quantity * item_retail_price
                cart_gross_total += item_gross_calculated_price

                st.markdown(f"**👗 {associated_product.title}**")

                r_col1, r_col2 = st.columns([1.2, 1.0])
                with r_col1:
                    st.caption(f"Price: `${item_gross_calculated_price:.2f}`")
                with r_col2:
                    new_qty = st.number_input(
                        "Qty:",
                        min_value=1,
                        max_value=99,
                        value=int(current_order.quantity),
                        key=f"right_panel_qty_{current_order.id}",
                    )
                    if new_qty != current_order.quantity:
                        current_order.quantity = new_qty
                        db.commit()
                        st.rerun()

                if st.button(
                    "🗑️ Drop Item",
                    key=f"right_panel_drop_{current_order.id}",
                    use_container_width=True,
                    type="secondary",
                ):
                    db.delete(current_order)
                    db.commit()
                    st.toast("Item discarded.")
                    time.sleep(0.1)
                    st.rerun()
                st.divider()

            st.markdown(f"##### 💳 Summary Total: `${cart_gross_total:.2f}`")

            if st.button(
                "🚀 Pay with Paystack Gateway",
                key="right_panel_paystack_cta",
                type="primary",
                use_container_width=True,
            ):
                try:
                    req_payload = {
                        "email": buyer_email,
                        "amount": int(cart_gross_total * 100),
                        "callback_url": "http://localhost:8501",
                        "metadata": {
                            "custom_fields": [
                                {
                                    "display_name": "Context",
                                    "variable_name": "checkout_type",
                                    "value": "cart",
                                }
                            ]
                        },
                    }
                    req = urllib.request.Request(
                        "https://paystack.co",
                        data=json.dumps(req_payload).encode("utf-8"),
                        headers={
                            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
                            "Content-Type": "application/json",
                        },
                    )
                    with urllib.request.urlopen(req) as res_cart:
                        res_data = json.loads(res_cart.read().decode("utf-8"))
                        if res_data.get("status"):
                            checkout_gateway_url = res_data["data"]["authorization_url"]
                            for active_item in active_cart_orders:
                                item_payout = (
                                    active_item.quantity * active_item.unit_price
                                )
                                active_item.commission_paid = (
                                    item_payout * COMMISSION_RATE
                                )
                                active_item.seller_payout = (
                                    item_payout - active_item.commission_paid
                                )
                                active_item.status = "paid"
                            db.commit()
                            st.markdown(
                                f'<a href="{checkout_gateway_url}" target="_blank" style="display: block; text-align: center; background-color: #09a5db; color: white; padding: 12px; border-radius: 6px; font-weight: bold; text-decoration: none;">➡️ Open Paystack Secure Tab</a>',
                                unsafe_allow_html=True,
                            )
                except Exception as e:
                    st.error(f"Paystack Initializer Configuration Error: {e}")

    # --- TERMINATE THE GRID CONTAINERS MESH ---
    st.markdown("</div>", unsafe_allow_html=True)
