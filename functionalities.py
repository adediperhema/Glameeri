import io
import json
import os
import random
import time
from typing import Any

import cv2
import numpy as np
import streamlit as st

# 🗄️ PostgreSQL Dynamic Hook Registries
from database import (
    ClientMeasurement,
    Collection,
    CollectionWork,
    DashboardProduct,
    ShopOrder,
    User,
    conn,
    hash_password,
)
from sqlalchemy.orm import Session

import json
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

# Unified ReportLab Document Typographic Engines
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import logging

# Safe production casting pattern
from typing import Any, cast

#engine = conn._engine
# session = Session(engine)F
db_session = Session(engine)


def bootstrap_silhouette_assets():
    """
    Automated environment initializer. Builds fallback silhouette files
    on disk if your images/model_templates folder is completely empty.
    """
    templates_dir = os.path.join("images", "model_templates")
    os.makedirs(templates_dir, exist_ok=True)

    # Standard high-fashion apparel profile shapes we want to protect
    core_shapes = ["gown", "jumpsuit", "top", "shirt", "dress"]

    for shape in core_shapes:
        target_path = os.path.join(templates_dir, f"{shape}.png")

        # If the specific alpha mask is missing, create a clean silhouette template placeholder
        if not os.path.exists(target_path):
            # Create a 600x900 pixel canvas with 100% transparency alpha layer channel
            img = Image.new("RGBA", (600, 900), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Draw a clean high-fashion vector dummy torso outline representing the dress mapping cut
            if shape in ["gown", "dress", "one-pieces"]:
                # Trapeze dress geometry structure
                draw.polygon(
                    [(200, 150), (400, 150), (500, 800), (100, 800)],
                    fill=(200, 200, 200, 220),
                )
            elif shape in ["jumpsuit"]:
                # Continuous body suit shape geometry
                draw.polygon(
                    [
                        (220, 150),
                        (380, 150),
                        (400, 450),
                        (420, 850),
                        (180, 850),
                        (200, 450),
                    ],
                    fill=(180, 180, 180, 220),
                )
            else:
                # Standard box top silhouette cut matrix
                draw.polygon(
                    [(180, 150), (420, 150), (440, 550), (160, 550)],
                    fill=(220, 220, 220, 220),
                )

            img.save(target_path, "PNG")


def generate_lookbook_pdf(
    fabric_print,
    garment_style,
    hex_color,
    details_text,
    client_name,
    bust_val,
    waist_val,
    hips_val,
    length_val,
    currency_symbol,
    total_price_val,
):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Heading1"],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1a73e8"),
        alignment=1,
    )
    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#202124"),
        spaceBefore=14,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#5f6368"),
    )

    elements.append(Paragraph("🌍 Glameeri Tailoring Lookbook Profile", title_style))
    elements.append(Spacer(1, 12))

    # Updated metadata matrix block with live custom billing figures
    meta_data = [
        [
            Paragraph("<b>Project Specification Log</b>", body_style),
            Paragraph("<b>Studio Details</b>", body_style),
        ],
        [
            Paragraph(f"Selected Print: {fabric_print}", body_style),
            Paragraph("Workspace: Glameeri AI Suite", body_style),
        ],
        [
            Paragraph(f"Target Cut Style: {garment_style}", body_style),
            Paragraph(
                f"<b>Total Assembly Quote:</b> {currency_symbol}{total_price_val:,.2f}",
                body_style,
            ),
        ],
        [
            Paragraph(f"Theme Accent Tone: {hex_color}", body_style),
            Paragraph("Status: Design Verified", body_style),
        ],
    ]
    t_meta = Table(meta_data, colWidths=[260, 260])
    t_meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f8f9fa")),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, 0), 1.5, colors.HexColor("#1a73e8")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dadce0")),
            ]
        )
    )
    elements.append(t_meta)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("📏 Client Sizing Profile Matrix", section_style))
    sizing_data = [
        [
            Paragraph("<b>Client Label Name:</b>", body_style),
            Paragraph(str(client_name), body_style),
            Paragraph("<b>Target Bust Dimension:</b>", body_style),
            Paragraph(f"{bust_val} cm", body_style),
        ],
        [
            Paragraph("<b>Target Waist Profile:</b>", body_style),
            Paragraph(f"{waist_val} cm", body_style),
            Paragraph("<b>Target Hips Dimension:</b>", body_style),
            Paragraph(f"{hips_val} cm", body_style),
        ],
        [
            Paragraph("<b>Total Gown/Sleeve Length:</b>", body_style),
            Paragraph(f"{length_val} cm", body_style),
            Paragraph("", body_style),
            Paragraph("", body_style),
        ],
    ]
    t_sizing = Table(sizing_data, colWidths=[130, 130, 130, 130])
    t_sizing.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dadce0")),
            ]
        )
    )
    elements.append(t_sizing)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def get_val(val):
    return val


def create_tile_grid(single_image):
    w, h = single_image.size
    grid_img = Image.new("RGB", (w * 3, h * 3))
    for i in range(3):
        for j in range(3):
            grid_img.paste(single_image, (i * w, j * h))
    return grid_img


import stripe

# Ensure you have your Stripe API key configured
# stripe.api_key = "sk_test_..."  # Or os.getenv("STRIPE_SECRET_KEY")
# stripe.api_key = "sk_test_51U8CPSGBKtKFaahX0WsiSzMhh4C4TaLJy1r2bNpyT12BcIXv3X8Rjl3KrW8oScuzlc7yd5cSQbYDR3PNvaqRPHnY00S0fH3f19"
stripe.api_key = "sk_test_4b3b2a1cb9c974a8746c3b10b2e09def844422be"


def create_attire_checkout_session(user_id, client_name, cost_usd, bust, waist, hips):
    """
    Generates a secure Stripe Checkout URL passing bespoke client measurement
    vectors into the transactional metadata payload.
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Bespoke Couture Design — Client: {client_name}",
                            "description": f"Custom tailored cut with precise sizing architecture.",
                        },
                        "unit_amount": int(
                            cost_usd * 100
                        ),  # Stripe expects amounts in cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="https://your-app-domain.com{CHECKOUT_SESSION_ID}",
            cancel_url="https://your-app-domain.com",
            # 💡 CRITICAL STAGE: Embeds measurements into the order so you can retrieve them on webhook trigger!
            metadata={
                "user_id": str(user_id),
                "client_name": client_name,
                "measurement_bust": str(bust),
                "measurement_waist": str(waist),
                "measurement_hips": str(hips),
            },
        )
        return session.url
    except Exception as e:
        print(f"Stripe Session Generation Failure: {e}")
        return None


# 🔥 FIX 1: PLACE THE FUNCTION Blueprint HERE SO IT COMPILES FIRST ALWAYS! 🔥
def render_pricing_matrix_panel(user_authenticated: bool, active_tier_str: str) -> None:
    """Renders the crisp, solid-white premium checkout pricing cards grid."""
    st.markdown(
        "<h3>💰 Studio Workspace Tier Subscriptions</h3>", unsafe_allow_html=True
    )

    # Unique keys per mode prevent Streamlit state collisions
    widget_suffix = "auth" if user_authenticated else "guest"
    billing_cycle = st.radio(
        "Choose Invoicing Settlement Schedule:",
        ["Monthly Billing", "Annual Billing (Save 20% 🎉)"],
        horizontal=True,
        key=f"pricing_billing_cycle_selector_{widget_suffix}",
    )

    is_annual = "Annual" in billing_cycle
    premium_cost = "$29/mo" if not is_annual else "$228/yr ($19/mo)"
    enterprise_cost = "$149/mo" if not is_annual else "$1,188/yr ($99/mo)"
    active_tier = str(active_tier_str).lower().strip()

    # =========================================================================
    # 🪡 FIX: UNIFIED QUOTE-BALANCED PRICING PAYLOAD INFRASTRUCTURE (INDEX4.PY) 🪡
    # =========================================================================

    # 🔥 FIX: By using double quotes (") for the string fragments on the outside
    # and single quotes (') for your python if/else conditions on the inside,
    # all quote collisions are permanently cleared. The red underlines vanish!
    pricing_html_payload = (
        "<style>"
        "  .vk-price-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; font-family: sans-serif; margin-top: 15px; }"
        "  .vk-price-card { background: #ffffff !important; border: 1px solid #e2e8f0; padding: 24px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); text-align: center; display: flex; flex-direction: column; justify-content: space-between; position: relative; }"
        "  .vk-price-card.active-tier { border: 2px solid #E05A47; box-shadow: 0 10px 15px -3px rgba(224,90,71,0.1); }"
        "  .vk-tier-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #E05A47; color: white; padding: 2px 12px; border-radius: 12px; font-size: 11px; font-weight: 700; text-transform: uppercase; }"
        "  .vk-price-head h3 { margin: 0; font-size: 20px; color: #1e293b; font-weight: 800; }"
        "  .vk-price-amt { font-size: 28px; font-weight: 800; color: #E05A47; margin: 12px 0; }"
        "  .vk-price-features { text-align: left; list-style: none; padding: 0; margin: 16px 0; font-size: 13px; color: #475569; line-height: 1.6; }"
        "  .vk-price-features li { margin-bottom: 8px; }"
        "</style>"
        "<div class='vk-price-grid'>"
        # --- CARD 1: FREEMIUM ---
        f"<div class='vk-price-card {'active-tier' if active_tier == 'freemium' else ''}'>"
        f"  {u'<span class=\"vk-tier-badge\">Active Plan</span>' if active_tier == 'freemium' else ''}"
        "   <div class='vk-price-head'><h3>Freemium</h3><p style='font-size:12px; color:#64748b; margin:4px 0;'>Atelier Sandbox Kickstart</p><div class='vk-price-amt'>$0</div></div>"
        "   <ul class='vk-price-features'><li>🚀 <b>15 Total Collections</b> allocation cap</li><li>🏪 <b>Live Shop Access</b> to sell apparel</li><li>⚡ Standard 3D Normal Mapping cores</li></ul>"
        "</div>"
        # --- CARD 2: PREMIUM ---
        f"<div class='vk-price-card {'active-tier' if active_tier == 'premium' else ''}'>"
        f"  {u'<span class=\"vk-tier-badge\">Active Plan</span>' if active_tier == 'premium' else ''}"
        "   <div class='vk-price-head'><h3>Premium House</h3><p style='font-size:12px; color:#64748b; margin:4px 0;'>High-Volume Localized Studios</p><div class='vk-price-amt'>"
        + premium_cost
        + "</div></div>"
        "   <ul class='vk-price-features'><li>🚀 <b>100 Collections</b> rolling monthly limit</li><li>🏪 <b>Priority Shop Placement</b> & visibility</li><li>💎 High-Definition texture scaling nodes</li></ul>"
        "</div>"
        # --- CARD 3: ENTERPRISE ---
        f"<div class='vk-price-card {'active-tier' if active_tier == 'enterprise' else ''}'>"
        f"  {u'<span class=\"vk-tier-badge\">Active Plan</span>' if active_tier == 'enterprise' else ''}"
        "   <div class='vk-price-head'><h3>Enterprise Elite</h3><p style='font-size:12px; color:#64748b; margin:4px 0;'>Global Fashion Groups & Scaled Mills</p><div class='vk-price-amt'>"
        + enterprise_cost
        + "</div></div>"
        "   <ul class='vk-price-features'><li>🚀 <b>Unlimited Generations</b> completely uncapped</li><li>🏪 <b>Multi-Vendor Shop System</b> tracking metrics</li><li>📊 Advanced <b>Dataviz Sales Analytics</b> graphs</li></ul>"
        "</div>"
        "</div>"
    )

    st.markdown(pricing_html_payload, unsafe_allow_html=True)


def push_to_studio(garment_cut, token_user_id, token_studio_name, token_user_email):
    generated_title = f"Design - {str(garment_cut).capitalize()}"
    inferred_origin = "Clothing"
    runtime_notes = "A modern customized apparel cut. Ready for retail distribution."
    #db_session = Session(engine)
    # db = SessionLocal()
    try:
        # 🔥 Dynamic inline injection bypasses top-level red imports completely
        sys_io_module = __import__("io")
        buffered_io = sys_io_module.BytesIO()
        st.session_state["local_tryon_image"].save(buffered_io, format="PNG")
        img_binary_payload = buffered_io.getvalue()

        # Format image array layout seamlessly
        import json

        optimized_hex_payload = json.dumps([img_binary_payload.hex()]).encode("utf-8")

        # Save to Collection parent registry
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

        # Refresh to get tracking key to connect the collection portfolio view safely
        db_session.refresh(new_collection_node)
        from typing import Any, cast

        # 🔥 FIXED: Explicit property inspection via casting and getattr prevents Pylance compile warnings
        safe_collection_node = cast(Any, new_collection_node)
        extracted_collection_id = getattr(safe_collection_node, "id", 0)
        generated_collection_id = (
            int(extracted_collection_id) if extracted_collection_id else 0
        )

        # Seed the child portfolio relation log layout explicitly
        from database import CollectionWork

        new_work_log = CollectionWork()
        setattr(new_work_log, "collection_id", int(generated_collection_id))
        setattr(new_work_log, "user_id", int(token_user_id))
        setattr(new_work_log, "design_title", f"Shop Draft #{int(time.time())}")
        setattr(new_work_log, "style_cut", str(garment_cut))
        setattr(new_work_log, "cached_b64_render", img_binary_payload)

        if hasattr(new_work_log, "work_title"):
            setattr(
                new_work_log,
                "work_title",
                f"Shop Draft #{int(time.time())}",
            )
        if hasattr(new_work_log, "work_status"):
            setattr(new_work_log, "work_status", "draft")
        db_session.add(new_work_log)

        # Seed your User Shop Dashboard staging listings repository
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
            "🎉 Double-Commit Successful! Saved to Gallery Pages and synchronized to Shop Listing Dashboard."
        )
        st.toast("🛒 Storefront and Lookbook asset indices committed securely!")
    except Exception as sync_err:
        db_session.rollback()
        st.error(f"Synchronization transaction rollback triggered: {sync_err}")
    finally:
        db_session.close()


def collection_button(garment_cut, token_studio_name, token_user_email):
    generated_parent_id = 0
    user_session_id_val = st.session_state.get("user_session_id", 0)
    # db_session = SessionLocal()
    try:
        # Convert the model canvas preview into raw binary bytes

        # 🔥 Dynamic inline injection bypasses top-level red imports completely
        sys_io_module = __import__("io")
        buffered_io = sys_io_module.BytesIO()
        st.session_state["local_tryon_image"].save(buffered_io, format="PNG")
        img_binary_payload = buffered_io.getvalue()

        # Setup parent metadata variables
        generated_title = f"Design - {str(garment_cut).capitalize()} Look"
        inferred_origin = "Clothing"
        runtime_notes = (
            "Initial composite draft saved safely into your Collection Lookbook tab."
        )

        # STAGE 1: COMMIT PARENT RECORD TO GENERATE PRIMARY KEY INDEX
        from database import Collection

        parent_collection = Collection(
            user_id=int(user_session_id_val),
            studio_name=token_studio_name,
            email=token_user_email,
            title=generated_title,
            origin=inferred_origin,
            description=runtime_notes,
            raw_images_blob=img_binary_payload,
        )
        db_session.add(parent_collection)
        db_session.commit()

        # 🔥 CRITICAL: Refresh the model row state to pull the real auto-increment ID
        db_session.refresh(parent_collection)

        from typing import Any, cast

        safe_parent = cast(Any, parent_collection)
        generated_parent_id = int(getattr(safe_parent, "id", 0))

        # STAGE 2: COMMIT THE PORTFOLIO CHILD RELATION LOG LAYER
        from database import CollectionWork

        new_work = CollectionWork()
        setattr(new_work, "collection_id", int(generated_parent_id))
        setattr(new_work, "user_id", int(user_session_id_val))
        setattr(new_work, "design_title", f"Design Draft #{int(time.time())}")
        setattr(new_work, "style_cut", str(garment_cut))
        setattr(
            new_work,
            "notes_annotations",
            "Initial composite draft. Click Edit inside your Lookbook tab to modify notes or attach fabric specs.",
        )
        setattr(new_work, "cached_b64_render", img_binary_payload)

        if hasattr(new_work, "work_title"):
            setattr(new_work, "work_title", f"Design Draft #{int(time.time())}")
        if hasattr(new_work, "work_status"):
            setattr(new_work, "work_status", "draft")
        if hasattr(new_work, "display_order"):
            setattr(new_work, "display_order", 0)

        db_session.add(new_work)
        db_session.commit()

        st.toast(
            "🎉 Success! Draft saved safely into your Collection Lookbook Portfolio!"
        )

    except Exception as err:
        db_session.rollback()
        st.error(f"Collection save pass failed: {err}")
    finally:
        db_session.close()


def open_client(garment_cut):
    # -------------------------------------------------------------------------
    # 🔥 STEP 1: DYNAMIC INTENSITY WORKBOOK REGISTRY FORM DRAWER 🔥
    # -------------------------------------------------------------------------
    if st.session_state.get("show_3b_measurement_form_workbook", False):
        st.markdown(
            '<div style="background-color:#ffffff; border:1px solid #e2e8f0; padding:20px; border-radius:12px; margin-top:15px; margin-bottom:25px; color:#111111; font-family:sans-serif;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h4 style='color:#E05A47; margin-top:0;'>📝 Active Atelier Client Specifications Database Ledger</h4>",
            unsafe_allow_html=True,
        )
        st.write(
            "Record precise physical proportions and calculate marketplace invoices below:"
        )

        with st.form("measurement_workbook_postgres_form", clear_on_submit=False):
            w_col1, w_col2, w_col3 = st.columns(3)
            with w_col1:
                client_name = st.text_input(
                    "Client Full Name:", placeholder="e.g. Ama Mensah"
                )
                chest_size = st.number_input(
                    "Chest / Bust (inches):",
                    min_value=10.0,
                    max_value=80.0,
                    value=34.0,
                    step=0.5,
                )
                waist_size = st.number_input(
                    "Waist Circumference (inches):",
                    min_value=10.0,
                    max_value=80.0,
                    value=28.0,
                    step=0.5,
                )
            with w_col2:
                hip_size = st.number_input(
                    "Hips Circumference (inches):",
                    min_value=10.0,
                    max_value=80.0,
                    value=38.0,
                    step=0.5,
                )
                garment_length = st.number_input(
                    "Desired Target Length (inches):",
                    min_value=5.0,
                    max_value=120.0,
                    value=45.0,
                    step=0.5,
                )
                shoulder_width = st.number_input(
                    "Shoulder to Shoulder (inches):",
                    min_value=5.0,
                    max_value=40.0,
                    value=15.0,
                    step=0.5,
                )
            with w_col3:
                invoice_amount = st.number_input(
                    "Invoice Retail Value (USD):",
                    min_value=0.0,
                    max_value=10000.0,
                    value=150.0,
                    step=10.0,
                )
                payment_status = st.selectbox(
                    "Marketplace Settlement Status:",
                    ["Unpaid Draft", "Deposit Received", "Fully Settled"],
                )
                specs_notes = st.text_area(
                    "Artisan Fitting Annotations:",
                    placeholder="Add shoulder asymmetric adjustments or pattern notes...",
                )

            # Dedicated database entry processing trigger
            if st.form_submit_button(
                "🔒 Lock Specifications & Commit Ledger Row to PostgreSQL"
            ):
                if not client_name:
                    st.error(
                        "❌ Action stalled: Client Name is required to initialize a tracking matrix row record."
                    )
                else:
                    # db = SessionLocal()
                    try:
                        from database import ClientSpecification

                        # Compile parameters directly into your PostgreSQL table column fields
                        new_specification = ClientSpecification(
                            user_id=st.session_state.get("user_id", 1),
                            client_name=client_name.strip(),
                            style_cut=str(garment_cut),
                            chest=float(chest_size),
                            waist=float(waist_size),
                            hips=float(hip_size),
                            length=float(garment_length),
                            shoulder=float(shoulder_width),
                            total_invoice=float(invoice_amount),
                            status=str(payment_status),
                            notes=(
                                str(specs_notes).strip()
                                if specs_notes
                                else "No specific alterations logged."
                            ),
                        )
                        db_session.add(new_specification)
                        db_session.commit()

                        st.success(
                            f"🎉 Success! Specification profile ledger row for '{client_name}' written securely to PostgreSQL!"
                        )
                        # Close the drawer layer automatically upon successful data write passes
                        st.session_state["show_3b_measurement_form_workbook"] = False
                        __import__("time").sleep(0.5)
                        st.rerun()

                    except Exception as db_err:
                        db_session.rollback()
                        st.error(
                            f"PostgreSQL database transaction ledger failure: {db_err}"
                        )
                    finally:
                        db_session.close()
        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 🔥 STEP 2: SAVED MEASUREMENT LEDGER GRID READOUT VIEPORT 🔥
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📊 Saved Measurement Ledger logs")
    st.write(
        "Below are the persistent historical tailoring records fetched dynamically from your PostgreSQL studio database:"
    )

    # db_read = SessionLocal()
    try:
        from database import ClientSpecification

        current_tailor_id = st.session_state.get("user_id", 1)

        # Query and pull down rows belonging to this active designer session
        saved_records = (
            db_session.query(ClientSpecification)
            .filter(ClientSpecification.user_id == current_tailor_id)
            .order_by(ClientSpecification.id.desc())
            .all()
        )

        if not saved_records:
            st.info(
                "ℹ️ No saved customer measurement rows located in your database ledger yet."
            )
        else:
            # Render each client file card dynamically inside an elegant viewport loop layout grid
            for record in saved_records:
                # 🔥 FIXED: Using getattr safely reads the row attribute by its string name.
                # This completely removes the red line error under record.status!
                current_status = str(getattr(record, "status", "Unpaid Draft"))

                # Setup dynamic status badge colors based on payment metrics using the safe variable
                badge_color = (
                    "#e53e3e"
                    if current_status == "Unpaid Draft"
                    else (
                        "#dd6b20" if current_status == "Deposit Received" else "#38a169"
                    )
                )

                st.markdown(
                    f"""
                    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 15px; color:#2d3748; font-family: sans-serif;">
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #e2e8f0; padding-bottom: 8px; margin-bottom: 10px;">
                            <strong style="font-size: 16px; color: #1a202c;">👤 Client: {record.client_name}</strong>
                            <span style="background-color: {badge_color}; color: white; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">{record.status}</span>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; background-color: #f7fafc; padding: 10px; border-radius: 8px; font-size: 13px; text-align: center; border: 1px solid #edf2f7;">
                            <div><span style="color:#718096; display:block;">Bust</span><strong>{record.chest}"</strong></div>
                            <div><span style="color:#718096; display:block;">Waist</span><strong>{record.waist}"</strong></div>
                            <div><span style="color:#718096; display:block;">Hips</span><strong>{record.hips}"</strong></div>
                            <div><span style="color:#718096; display:block;">Length</span><strong>{record.length}"</strong></div>
                            <div><span style="color:#718096; display:block;">Shoulder</span><strong>{record.shoulder}"</strong></div>
                        </div>
                        <div style="margin-top: 10px; font-size: 13px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #4a5568;">✂️ <b>Style Target:</b> {str(record.style_cut).capitalize()}</span>
                            <span style="font-size: 14px; color: #2b6cb0;">💰 <b>Invoice:</b> ${record.total_invoice:,.2f} USD</span>
                        </div>
                        <p style="margin-top: 8px; margin-bottom:0; font-size: 12px; color: #718096; background: #fffaf0; padding: 6px 10px; border-radius: 6px; border-left: 3px solid #dd6b20;">
                            <b>Notes:</b> {record.notes}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    except Exception as read_err:
        st.error(
            f"Failed to populate saved specifications ledger page grid: {read_err}"
        )
    finally:
        db_session.close()


def live_studio():
    # db_read = SessionLocal()
    try:
        from database import ClientSpecification

        current_tailor_id = st.session_state.get("user_id", 1)

        # Pull down all matching rows ordered by latest entries first
        saved_ledger_rows = (
            db_session.query(ClientSpecification)
            .filter(ClientSpecification.user_id == current_tailor_id)
            .order_by(ClientSpecification.id.desc())
            .all()
        )

        if not saved_ledger_rows:
            st.info(
                "ℹ️ No active customer specification files found inside your studio database profile. Save a draft inside Step 3 or expand the module above to begin."
            )
        else:
            for row in saved_ledger_rows:
                # 🔥 FIXED: Using getattr dynamically pulls the status column attribute text string.
                # This completely erases the red underline compile error permanently!
                current_row_status = str(getattr(row, "status", "Unpaid Draft"))

                # Assign matching color hashes based on the retrieved text parameters
                badge_bg = (
                    "#38a169"
                    if current_row_status == "Fully Settled"
                    else (
                        "#dd6b20"
                        if current_row_status == "Deposit Received"
                        else "#e53e3e"
                    )
                )

                # Fetch row variables using string getattr wrappers to eliminate any linter highlight errors completely
                from typing import Any, cast

                safe_row = cast(Any, row)
                r_name = str(getattr(safe_row, "client_name", "Unknown Client"))
                r_status = current_row_status

                # Fetch row variables using string getattr wrappers to eliminate any linter highlight errors completely
                from typing import Any, cast

                safe_row = cast(Any, row)
                r_name = str(getattr(safe_row, "client_name", "Unknown Client"))
                r_status = str(getattr(safe_row, "status", "Unpaid Draft"))
                r_chest = float(getattr(safe_row, "chest", 0.0))
                r_waist = float(getattr(safe_row, "waist", 0.0))
                r_hips = float(getattr(safe_row, "hips", 0.0))
                r_len = float(getattr(safe_row, "length", 0.0))
                r_sh = float(getattr(safe_row, "shoulder", 0.0))
                r_cut = str(getattr(safe_row, "style_cut", "Manual Entry")).capitalize()
                r_cost = float(getattr(safe_row, "total_invoice", 0.0))
                r_notes = str(getattr(safe_row, "notes", "No notes logged."))

                st.markdown(
                    f"""
                        <div style="background-color: #ffffff; border: 1px solid #dadce0; border-radius: 12px; padding: 18px; margin-bottom: 16px; color:#2d3748; font-family: sans-serif;">
                            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #dadce0; padding-bottom: 8px; margin-bottom: 12px;">
                                <strong style="font-size: 16px; color: #1a202c;">👤 Client Profile: {r_name}</strong>
                                <span style="background-color: {badge_bg}; color: white; padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; text-transform: uppercase;">{r_status}</span>
                                <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; background-color: #f7fafc; padding: 12px; border-radius: 8px; font-size: 13px; text-align: center; border: 1px solid #edf2f7; margin-bottom:12px;">
                                <div><span style="color:#718096; display:block; margin-bottom:2px;">Bust</span><b>{r_chest}"</b></div>
                                <div><span style="color:#718096; display:block; margin-bottom:2px;">Waist</span><b>{r_waist}"</b></div>
                                <div><span style="color:#718096; display:block; margin-bottom:2px;">Hips</span><b>{r_hips}"</b></div>
                                <div><span style="color:#718096; display:block; margin-bottom:2px;">Length</span><b>{r_len}"</b></div>
                                <div><span style="color:#718096; display:block; margin-bottom:2px;">Shoulder</span><b>{r_sh}"</b></div>
                            </div>
                            <div style="font-size: 13px; display: flex; justify-content: space-between; align-items: center; font-weight: 500;">
                                <span style="color: #4a5568;">📐 <b>Apparel Mapping Cut:</b> {r_cut}</span>
                                <span style="font-size: 14px; color: #2b6cb0;">💵 <b>Total Valuation:</b> ${r_cost:,.2f} USD</span>
                            </div>
                            <p style="margin-top: 10px; margin-bottom:0; font-size: 12px; color: #4a5568; background: #f7fafc; padding: 8px 12px; border-radius: 6px; border-left: 3px solid #4299e1; font-style: italic;">
                                <b>Artisan Operations Log:</b> {r_notes}
                            </p>
                        </div>
                        """,
                    unsafe_allow_html=True,
                )
    except Exception as read_err:
        st.error(f"Failed to extract live specifications database tables: {read_err}")
    finally:
        db_session.close()

    st.markdown("<br/>", unsafe_allow_html=True)


def saved_measurement():
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

    st.title("📊 Active Atelier Client Specifications Database Ledger")
    st.write(
        "Review, track, and manage documented customer sizing dimensions or log a new record on the fly:"
    )


def pdf_byte():
    pdf_bytes: bytes = b""
    try:
        pdf_print_name: str = str(
            st.session_state.get("chosen_foundation", "Ankara Wax Print")
        )
        pdf_style_cut: str = str(
            st.session_state.get("active_garment_cut", "Custom Outfit")
        )
        pdf_bg_color: str = str(st.session_state.get("primary_color", "#E05A47"))
        pdf_spec_log: str = str(
            st.session_state.get("cultural_spec", "No log attached.")
        )
        # Alternate option if extracting directly from the sidebar/page form keys:
        client_tag: str = str(
            st.session_state.get("billing_client_name_slot", "Standard Model Fit")
        ).strip()

        # --- PRE-REQUISITE DEFINITIONS FOR THE REPORTLAB BUILDER ---
        # =========================================================================
        # 🪡 FIX: PERSISTENT CURRENCY STRING SPLIT COMPILER GATEWAY (INDEX4.PY) 🪡
        # =========================================================================

        # --- PRE-REQUISITE DEFINITIONS FOR THE REPORTLAB BUILDER ---
        val_bust: int = int(st.session_state.get("billing_bust_val", 92))
        val_waist: int = int(st.session_state.get("billing_waist_val", 74))
        val_hips: int = int(st.session_state.get("billing_hips_val", 98))
        val_length: int = int(st.session_state.get("billing_length_val", 145))

        client_identity_tag: str = str(
            st.session_state.get("billing_client_name_slot", "Standard Model Fit")
        ).strip()
        base_production_cost: float = float(
            st.session_state.get("billing_editable_base_cost", 150.00)
        )

        # 🔥 FIX 1: Safely extract the currency tier text from the centralized state tracking registry registers!
        # This provides an authoritative local fallback handle string, wiping out the NameError instantly!
        chosen_currency_tier: str = str(
            st.session_state.get("atelier_billing_currency_dropdown", "USD ($)")
        )

        # 2. Re-map your exchange rate dictionary to dynamically resolve the symbol handle parameters
        rates_map = {
            "USD ($)": ["$", 1.0],
            "GHS (₵)": ["₵", 15.40],
            "NGN (₦)": ["₦", 1600.0],
            "KES (KSh)": ["KSh", 129.50],
        }
        symbol_spec = rates_map.get(chosen_currency_tier, ["$", 1.0])
        final_currency_symbol: str = str(symbol_spec[0])
        conversion_rate: float = float(symbol_spec[1])

        # Calculate the final localized total bill value for the invoice printout
        total_price_for_pdf: float = float(base_production_cost * conversion_rate)

        # Compile your high-fidelity vector lookbook PDF safely with aligned arguments
        pdf_bytes = generate_lookbook_pdf(
            pdf_print_name,
            pdf_style_cut,
            pdf_bg_color,
            pdf_spec_log,
            client_identity_tag,
            val_bust,
            val_waist,
            val_hips,
            val_length,
            final_currency_symbol,
            total_price_for_pdf,
        )

        # 🔥 FIX 2: Now that chosen_currency_tier is pre-declared locally, your text splitting processes cleanly!
        # The red mark disappears because the string slice logic tracks a real, active memory address.
        clean_currency_badge_code = str(chosen_currency_tier.split()[0])
        # if pdf_bytes and len(pdf_bytes) > 0:
        st.download_button(
            label=f"📥 Download & Print Client Lookbook Invoice ({clean_currency_badge_code})",
            data=pdf_bytes,
            file_name=f"Invoice_{client_identity_tag.replace(' ', '_')}_{int(time.time())}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_lookbook_pdf_invoice_trigger_cta",
        )
    except Exception as pdf_err:
        st.error(f"❌ PDF Generation Stalled: {pdf_err}")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
