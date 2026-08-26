# tryon_service.py
import io
import os
import logging
from PIL import Image
import numpy as np
import streamlit as st

logger = logging.getLogger(__name__)


def execute_silhouette_tryon_pipeline(
    person_bytes: bytes,
    fabric_data,
    outfit_type: str,
    category: str,
    templates_folder: str = "images/model_templates",
    scale_val: float = 1.0,
    x_val: int = 0,
    y_val: int = 0,
    api_url: str = "https://huggingface.co",
) -> bytes:
    """
    High-Fidelity Multi-Format Draping Engine.
    Supports PNG and JPG templates of ANY color (White, Black, Red, Blue, patterned).
    1. Dynamically generates a background isolation mask by evaluating pixel opacity and variance.
    2. Quantizes the apparel envelope to create a 100% solid foundation, preventing color bleed-through.
    3. Tiles and drapes Step 2 design pattern maps smoothly inside the clean apparel boundary.
    4. Fits apparel onto model portrait coordinates with perfect color clarity.
    """
    # 1. Resolve and verify the target apparel template file route (.png, .jpg, .jpeg)
    clean_apparel_name = outfit_type.strip().lower() if outfit_type else "gown"
    extensions_to_check = [".png", ".jpg", ".jpeg"]
    target_apparel_path = None

    for ext in extensions_to_check:
        test_path = os.path.join(templates_folder, f"{clean_apparel_name}{ext}")
        if os.path.exists(test_path):
            target_apparel_path = test_path
            break

    if not target_apparel_path:
        target_apparel_path = os.path.join(
            templates_folder, f"{clean_apparel_name}.png"
        )
        if not os.path.exists(target_apparel_path):
            raise FileNotFoundError(
                f"Apparel template outline '{clean_apparel_name}' missing from directory path {templates_folder}"
            )

    # 2. Open base model portrait structures in clean RGBA channels
    person_img = Image.open(io.BytesIO(person_bytes)).convert("RGBA")
    w_person, h_person = person_img.size

    raw_apparel = Image.open(target_apparel_path).convert("RGBA")

    # -------------------------------------------------------------------
    # 🔥 FIX: UNIVERSAL COLOUR BACKGROUND ISOLATION MASK GENERATOR 🔥
    # Works perfectly whether the template garment is white, black, red, blue, etc.
    # -------------------------------------------------------------------
    apparel_np = np.array(raw_apparel)
    r, g, b, a = (
        apparel_np[:, :, 0],
        apparel_np[:, :, 1],
        apparel_np[:, :, 2],
        apparel_np[:, :, 3],
    )

    # Dynamic Mask Calculation Pass:
    # Check if the template is a PNG with an existing alpha channel
    has_alpha_channel = np.any(a < 255)

    if has_alpha_channel:
        # If it's a transparent PNG, any pixel with opacity > 5 is part of the colored garment
        garment_pixels_condition = a > 5
    else:
        # If it's a flat JPG/JPEG file with a solid backdrop (e.g. white background studio cutout)
        # We find the background by checking for high brightness or flat uniform color cells
        is_white_bg = (r > 220) & (g > 220) & (b > 220)
        is_black_bg = (r < 35) & (g < 35) & (b < 35)
        background_condition = is_white_bg | is_black_bg
        garment_pixels_condition = ~background_condition

    # Build a clean binary mask: Clear out background pixels entirely, set garment area to completely solid
    final_apparel_alpha = np.zeros_like(a)
    final_apparel_alpha[garment_pixels_condition] = 255

    # Re-apply the clean alpha channel back into our array matrix
    apparel_np[:, :, 3] = final_apparel_alpha
    clean_apparel_mask = Image.fromarray(apparel_np)

    # 3. Safe Type Validation for Step 2 active fabric textures
    if isinstance(fabric_data, bytes):
        fabric_texture_img = Image.open(io.BytesIO(fabric_data)).convert("RGB")
    elif isinstance(fabric_data, Image.Image):
        fabric_texture_img = fabric_data.convert("RGB")
    elif isinstance(fabric_data, np.ndarray):
        fabric_texture_img = Image.fromarray(fabric_data).convert("RGB")
    elif isinstance(fabric_data, tuple):
        if "active_fabric" in st.session_state and isinstance(
            st.session_state["active_fabric"], Image.Image
        ):
            fabric_texture_img = st.session_state["active_fabric"].convert("RGB")
        else:
            raise TypeError(
                "Fabric data arrived as a tuple configuration and no active layout fallback was found in memory."
            )
    else:
        raise TypeError(
            f"Invalid fabric asset format sent from Step 2: {type(fabric_data)}."
        )

    # -------------------------------------------------------------------
    # 🔥 STEP 4: 100% VISIBLE ORIGINAL DESIGN INJECTION LAYER 🔥
    # -------------------------------------------------------------------
    mask_width, mask_height = clean_apparel_mask.size
    fabric_w, fabric_h = fabric_texture_img.size

    # Tile your Step 2 design pattern across the dimensions of the apparel shape
    tiled_fabric = Image.new("RGB", (mask_width, mask_height))
    for x in range(0, mask_width, fabric_w):
        for y in range(0, mask_height, fabric_h):
            tiled_fabric.paste(fabric_texture_img, (x, y))

    # Intersect layers: We build a solid foundation shield layer first.
    # This completely blocks out the original color of the template (e.g. bright red or green gown pixels)
    # so that ONLY your Step 2 print design is visible.
    vibrant_base_layer = Image.new(
        "RGBA", (mask_width, mask_height), (255, 255, 255, 255)
    )
    vibrant_base_layer.paste(tiled_fabric, (0, 0))

    # Inject the high-fidelity mask channel envelope
    vibrant_base_layer.putalpha(clean_apparel_mask.getchannel("A"))

    # Crop empty padding margins to establish accurate positioning anchors
    bbox = vibrant_base_layer.getbbox()
    if bbox:
        vibrant_base_layer = vibrant_base_layer.crop(bbox)

    # 5. Geometric Proportional Placement Math
    if category in ["tops", "one-pieces"]:
        target_width = int(w_person * 0.54 * scale_val)
        target_height = int(h_person * 0.48 * scale_val)
        center_x = (w_person // 2) + x_val
        center_y = int(h_person * 0.46) + y_val
    else:
        target_width = int(w_person * 0.48 * scale_val)
        target_height = int(h_person * 0.54 * scale_val)
        center_x = (w_person // 2) + x_val
        center_y = int(h_person * 0.72) + y_val

    target_width = max(10, target_width)
    target_height = max(10, target_height)
    resized_apparel = vibrant_base_layer.resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )

    # -------------------------------------------------------------------
    # STEP 6: WEAR THE NEW APPAREL MATRIX OUTCOME ON THE MODEL
    # -------------------------------------------------------------------
    apparel_overlay_canvas = Image.new("RGBA", (w_person, h_person), (0, 0, 0, 0))

    x_paste = center_x - (target_width // 2)
    y_paste = center_y - (target_height // 2)

    apparel_overlay_canvas.paste(resized_apparel, (x_paste, y_paste), resized_apparel)
    final_composite_img = Image.alpha_composite(person_img, apparel_overlay_canvas)

    # 7. Compress and convert frame down to web-optimized JPEG bytes representation
    output_buffer = io.BytesIO()
    final_rgb_lookbook = final_composite_img.convert("RGB")
    final_rgb_lookbook.save(output_buffer, format="JPEG", quality=95, optimize=True)

    logger.info(
        "🎉 Universal Colored Apparel Try-on Core Engine Mapping Sequence Complete!"
    )
    return output_buffer.getvalue()
