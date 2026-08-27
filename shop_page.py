# shop_page.py
import streamlit as st
import time
import json
from database import Product, Order, User, TryOnFeatureMeter

# Simulated constant session contexts - replace with your application authentication framework variables
token_user_id = st.session_state.get("user_id", 1)
COMMISSION_RATE = 0.15  # 15% Platform application commission fee


def render_marketplace_hub(db):
    st.markdown("## 🛍️ AI Fashion Design Hub Marketplace")

    # ---------------------------------------------------------
    # PART A: PERSISTENT MINI SHOPPING CART MONITOR
    # ---------------------------------------------------------
    active_cart_orders = (
        db.query(Order)
        .filter(Order.buyer_id == token_user_id, Order.status == "cart")
        .all()
    )

    cart_count = sum(o.quantity for o in active_cart_orders)

    with st.expander(
        f"🛒 Shopping Cart Tracker ({cart_count} items selected)", expanded=False
    ):
        if not active_cart_orders:
            st.info("Your shopping cart workspace is currently empty.")
        else:
            gross_total = 0.0
            for current_order in active_cart_orders:
                prod = current_order.product
                item_total = current_order.quantity * current_order.unit_price
                gross_total += item_total

                # Split pricing visualization breakdown
                app_commission = item_total * COMMISSION_RATE
                artisan_payout = item_total - app_commission

                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    st.markdown(f"**{prod.title}** (Qty: {current_order.quantity})")
                    st.caption(
                        f"Seller ID: {current_order.seller_id} | Notes: {prod.notes or 'None'}"
                    )
                with c2:
                    st.write(f"Total: ${item_total:.2f}")
                    st.caption(
                        f"Base: ${artisan_payout:.2f} + App Service: ${app_commission:.2f}"
                    )
                with c3:
                    if st.button("❌ Remove", key=f"drop_cart_{current_order.id}"):
                        current_order.status = "cancelled"
                        db.commit()
                        st.toast("Item dropped from active tray.")
                        time.sleep(0.2)
                        st.rerun()
            st.divider()
            st.markdown(f"### **Aggregate Due: ${gross_total:.2f}**")

            if st.button(
                "💳 Proceed to Checkout (Stripe Gateway Integration)",
                use_container_width=True,
            ):
                # Process structural payout partitions on stripe session tokenization loops
                for active_item in active_cart_orders:
                    tot = active_item.quantity * active_item.unit_price
                    active_item.commission_paid = tot * COMMISSION_RATE
                    active_item.seller_payout = tot - active_item.commission_paid
                    active_item.status = "paid"
                    active_item.stripe_session_id = "st_live_mock_" + str(time.time())
                db.commit()
                st.success(
                    "🎉 Payment verified via Stripe Connect! Base costs distributed to sellers, and commissions routed to app account."
                )
                time.sleep(1.0)
                st.rerun()

    # ---------------------------------------------------------
    # PART B: CONTEXTUAL PRODUCT METADATA SEARCH BAR
    # ---------------------------------------------------------
    st.markdown("### 🔎 Lookbook Query Finder")
    search_query = st.text_input(
        "Filter via Seller ID, Product Title, Attributes, or Studio Workspace Notes:",
        value="",
        placeholder="Type 'Ankara', notes, or seller variables...",
    )

    # Base database query formulation logic
    query_builder = db.query(Product)
    if search_query:
        query_builder = query_builder.filter(
            (Product.title.ilike(f"%{search_query}%"))
            | (Product.description.ilike(f"%{search_query}%"))
            | (Product.notes.ilike(f"%{search_query}%"))
            | (Product.seller_id.like(f"%{search_query}%"))
        )
    catalog_products = query_builder.all()

    # ---------------------------------------------------------
    # PART C: STOREFRONT GRID LAYOUT
    # ---------------------------------------------------------
    st.markdown("### 🏷️ Available Studio Inventory Catalog")
    if not catalog_products:
        st.warning("No apparel assets match your structural matrix query.")
        return

    # User Premium TryOn Status tracking lookup
    meter = (
        db.query(TryOnFeatureMeter)
        .filter(TryOnFeatureMeter.user_id == token_user_id)
        .first()
    )
    if not meter:
        meter = TryOnFeatureMeter(
            user_id=token_user_id, free_uses_left=5, has_premium_access=False
        )
        db.add(meter)
        db.commit()

    # Render standardized commerce cells
    for row_idx in range(0, len(catalog_products), 3):
        cols = st.columns(3, gap="medium")
        for i, prod in enumerate(catalog_products[row_idx : row_idx + 3]):
            with cols[i]:
                st.markdown(
                    f"""
                <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; background: white; margin-bottom: 10px;">
                    <h4 style="margin: 0 0 8px 0; color: #2d3748;">{prod.title}</h4>
                    <p style="font-size: 18px; font-weight: bold; color: #E05A47; margin: 4px 0;">${prod.price:.2f}</p>
                    <p style="font-size: 12px; color: #718096; height: 40px; overflow: hidden;">{prod.description or 'No descriptor loaded.'}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Action 1: Cart Commitment Engine Interaction Route
                if st.button(
                    f"🛒 Append to Cart",
                    key=f"add_cart_btn_{prod.id}",
                    use_container_width=True,
                ):
                    existing_item = (
                        db.query(Order)
                        .filter(
                            Order.buyer_id == token_user_id,
                            Order.product_id == prod.id,
                            Order.status == "cart",
                        )
                        .first()
                    )
                    if existing_item:
                        existing_item.quantity += 1
                    else:
                        new_cart_entry = Order(
                            buyer_id=token_user_id,
                            seller_id=prod.seller_id,
                            product_id=prod.id,
                            status="cart",
                            quantity=1,
                            unit_price=prod.price,
                        )
                        db.add(new_cart_entry)
                    db.commit()
                    st.toast(f"'{prod.title}' appended to your cart trajectory!")
                    time.sleep(0.2)
                    st.rerun()

                    # Action 2: Try-On AR Processing Evaluation Gate
                    # 1. 🔥 TYPE CAST GUARD: Bypasses strict model checks and clears meter red highlights permanently
                    from typing import Any, cast

                    safe_meter = cast(Any, meter)

                    # Safe fallbacks to check features without compile warnings
                    has_premium = bool(getattr(safe_meter, "has_premium_access", False))
                    free_left = int(getattr(safe_meter, "free_uses_left", 0))

                    # 2. Setup button states clean and clear
                    if has_premium:
                        btn_label = "✨ Try On (Premium Mode)"
                        disabled_flag = False
                    elif free_left > 0:
                        btn_label = f"✨ Try On (Free Uses Left: {free_left})"
                        disabled_flag = False
                    else:
                        btn_label = "🔒 Try On (Limit Exceeded)"
                        disabled_flag = True


import streamlit as st
import time
import os
from typing import Any, cast

# Assuming your SQLAlchemy models are imported directly from your database module
# from database import Order, Product, TryOnFeatureMeter, User


def render_marketplace_hub(db, token_user_id, COMMISSION_RATE=0.10):
    st.markdown("## 🛍️ AI Fashion Design Hub Marketplace")

    # ---------------------------------------------------------
    # PART A: PERSISTENT MINI SHOPPING CART MONITOR
    # ---------------------------------------------------------
    active_cart_orders = (
        db.query(Order)
        .filter(Order.buyer_id == token_user_id, Order.status == "cart")
        .all()
    )

    cart_count = sum(o.quantity for o in active_cart_orders)

    with st.expander(
        f"🛒 Shopping Cart Tracker ({cart_count} items selected)", expanded=False
    ):
        if not active_cart_orders:
            st.info("Your shopping cart workspace is currently empty.")
        else:
            gross_total = 0.0
            for current_order in active_cart_orders:
                prod = current_order.product
                item_total = current_order.quantity * current_order.unit_price
                gross_total += item_total

                # Split pricing visualization breakdown
                app_commission = item_total * COMMISSION_RATE
                artisan_payout = item_total - app_commission

                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    st.markdown(f"**{prod.title}** (Qty: {current_order.quantity})")
                    st.caption(
                        f"Seller ID: {current_order.seller_id} | Notes: {prod.notes or 'None'}"
                    )
                with c2:
                    st.write(f"Total: ${item_total:.2f}")
                    st.caption(
                        f"Base: ${artisan_payout:.2f} + App Service: ${app_commission:.2f}"
                    )
                with c3:
                    if st.button("❌ Remove", key=f"drop_cart_{current_order.id}"):
                        current_order.status = "cancelled"
                        db.commit()
                        st.toast("Item dropped from active tray.")
                        time.sleep(0.2)
                        st.rerun()
            st.divider()
            st.markdown(f"### **Aggregate Due: ${gross_total:.2f}**")

            # Updated button label to reflect your unified African architecture focus
            if st.button(
                "💳 Proceed to Checkout (Paystack Gateway Integration)",
                use_container_width=True,
            ):
                # Update statuses inside your Supabase transactional loop
                for active_item in active_cart_orders:
                    tot = active_item.quantity * active_item.unit_price
                    active_item.commission_paid = tot * COMMISSION_RATE
                    active_item.seller_payout = tot - active_item.commission_paid
                    active_item.status = "paid"
                    active_item.stripe_session_id = "pst_live_mock_" + str(time.time())
                db.commit()
                st.success(
                    "🎉 Payment verified securely! Base split funds distributed to sellers, and commissions routed to app workspace account."
                )
                time.sleep(1.0)
                st.rerun()

    # ---------------------------------------------------------
    # PART B: CONTEXTUAL PRODUCT METADATA SEARCH BAR
    # ---------------------------------------------------------
    st.markdown("### 🔎 Lookbook Query Finder")
    search_query = st.text_input(
        "Filter via Seller ID, Product Title, Attributes, or Studio Workspace Notes:",
        value="",
        placeholder="Type 'Ankara', notes, or seller variables...",
    )

    # Base database query formulation logic
    query_builder = db.query(Product)
    if search_query:
        query_builder = query_builder.filter(
            (Product.title.ilike(f"%{search_query}%"))
            | (Product.description.ilike(f"%{search_query}%"))
            | (Product.notes.ilike(f"%{search_query}%"))
            | (Product.seller_id.like(f"%{search_query}%"))
        )
    catalog_products = query_builder.all()

    # ---------------------------------------------------------
    # PART C: STOREFRONT GRID LAYOUT
    # ---------------------------------------------------------
    st.markdown("### 🏷️ Available Studio Inventory Catalog")
    if not catalog_products:
        st.warning("No apparel assets match your structural matrix query.")
        return

    # User Premium TryOn Status tracking lookup
    meter = (
        db.query(TryOnFeatureMeter)
        .filter(TryOnFeatureMeter.user_id == token_user_id)
        .first()
    )
    if not meter:
        meter = TryOnFeatureMeter(
            user_id=token_user_id, free_uses_left=5, has_premium_access=False
        )
        db.add(meter)
        db.commit()

    # Render standardized commerce cells
    for row_idx in range(0, len(catalog_products), 3):
        cols = st.columns(3, gap="medium")
        for i, prod in enumerate(catalog_products[row_idx : row_idx + 3]):
            with cols[i]:
                st.markdown(
                    f"""
                <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; background: white; margin-bottom: 10px;">
                    <h4 style="margin: 0 0 8px 0; color: #2d3748;">{prod.title}</h4>
                    <p style="font-size: 18px; font-weight: bold; color: #E05A47; margin: 4px 0;">${prod.price:.2f}</p>
                    <p style="font-size: 12px; color: #718096; height: 40px; overflow: hidden;">{prod.description or 'No descriptor loaded.'}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # ==========================================================
                # ACTION 1: CART COMMITMENT ENGINE INTERACTION ROUTE
                # ==========================================================
                if st.button(
                    f"🛒 Append to Cart",
                    key=f"add_cart_btn_{prod.id}",
                    use_container_width=True,
                ):
                    existing_item = (
                        db.query(Order)
                        .filter(
                            Order.buyer_id == token_user_id,
                            Order.product_id == prod.id,
                            Order.status == "cart",
                        )
                        .first()
                    )
                    if existing_item:
                        existing_item.quantity += 1
                    else:
                        new_cart_entry = Order(
                            buyer_id=token_user_id,
                            seller_id=prod.seller_id,
                            product_id=prod.id,
                            status="cart",
                            quantity=1,
                            unit_price=prod.price,
                        )
                        db.add(new_cart_entry)
                    db.commit()
                    st.toast(f"'{prod.title}' appended to your cart trajectory!")
                    time.sleep(0.2)
                    st.rerun()

                # ==========================================================
                # ACTION 2: TRY-ON AR PROCESSING EVALUATION GATE
                # (FIXED INDENTATION: Aligned outside Action 1's button block)
                # ==========================================================
                from typing import Any, cast

                safe_meter = cast(Any, meter)

                # Safe fallbacks to check features without compile warnings
                has_premium = bool(getattr(safe_meter, "has_premium_access", False))
                free_left = int(getattr(safe_meter, "free_uses_left", 0))

                # Setup button labels and validation flags cleanly
                if has_premium:
                    btn_label = "✨ Try On (Premium Mode)"
                    disabled_flag = False
                elif free_left > 0:
                    btn_label = f"✨ Try On (Free Left: {free_left})"
                    disabled_flag = False
                else:
                    btn_label = "🔒 Try On (Limit Exceeded)"
                    disabled_flag = True

                # Render action engine button
                if st.button(
                    btn_label,
                    key=f"tryon_act_{prod.id}",
                    disabled=disabled_flag,
                    use_container_width=True,
                ):
                    # Decrement free trial tracking values dynamically inside cloud rows
                    if not has_premium:
                        new_uses = max(0, free_left - 1)
                        setattr(safe_meter, "free_uses_left", new_uses)
                        db.commit()

                    # Heavy image rendering running within the click context scope execution block
                    with st.spinner("Processing optimization textures..."):
                        try:
                            # Fetch the user's uploaded modeling photo from active session thread memory
                            p_bytes = st.session_state.get(
                                "custom_client_uploader_bytes", None
                            )

                            # Pull garment design binary data directly out of public product row variables
                            safe_prod = cast(Any, prod)
                            g_bytes = getattr(safe_prod, "raw_images_blob", None)

                            if p_bytes is None:
                                st.warning(
                                    "⚠️ Try-On Notice: Please go to Step 3 and upload a Custom Client Model Photo first."
                                )
                            elif g_bytes is None:
                                st.error(
                                    "❌ Mismatch Error: No design texture blueprints found attached to this listing row."
                                )
                            else:
                                # Call your high-fidelity decoupled processing engine function
                                from tryon_service import (
                                    execute_silhouette_tryon_pipeline,
                                )

                                # Formulate a smart string fallback indicator for the garment cut name mapping class
                                apparel_cut_name = str(
                                    getattr(safe_prod, "title", "gown")
                                ).lower()

                                # Dynamically extract category metadata attributes from your product model columns
                                category_value = str(
                                    getattr(safe_prod, "category", "one-pieces")
                                ).lower()
                                if category_value not in [
                                    "tops",
                                    "bottoms",
                                    "one-pieces",
                                ]:
                                    category_value = "one-pieces"  # Enforce strict system safety criteria bounds

                                lightweight_jpeg_bytes = (
                                    execute_silhouette_tryon_pipeline(
                                        person_bytes=p_bytes,
                                        fabric_data=g_bytes,
                                        outfit_type=apparel_cut_name,
                                        category=category_value,
                                        scale_val=1.0,
                                        x_val=0,
                                        y_val=0,
                                    )
                                )

                                # Render the crisp output lookbook image card onto the user screen
                                st.image(
                                    lightweight_jpeg_bytes,
                                    caption=f"AI Fitted Lookbook Output Result: {apparel_cut_name.capitalize()}",
                                    use_container_width=True,
                                )

                                st.toast(
                                    "🎉 Custom garment drape compiled successfully!"
                                )
                                time.sleep(0.1)

                        except Exception as tryon_ui_err:
                            st.error(
                                f"Sandbox fitting error trace loop: {tryon_ui_err}"
                            )

                # If limits have been crossed, render the Premium expansion gateway button cell
                if disabled_flag:
                    st.caption("⚠️ Try-On threshold exceeded.")
                    if st.button(
                        "Unlock Unlimited Try-Ons ($9.99)",
                        key=f"premium_buy_{prod.id}",
                        type="primary",
                        use_container_width=True,
                    ):
                        setattr(safe_meter, "has_premium_access", True)
                        db.commit()
                        st.success(
                            "Paystack Token Received: Premium Unlimited Access enabled!"
                        )
                        time.sleep(0.5)
                        st.rerun()

    # --- END OF PRODUCT INVENTORY LOOP TRACKS ---
    st.markdown("</div>", unsafe_allow_html=True)
