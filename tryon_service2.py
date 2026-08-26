# tryon_service.py
import io
import os
import logging
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import streamlit as st

logger = logging.getLogger(__name__)


def execute_silhouette_tryon_pipeline(
    person_bytes: bytes,
    fabric_data,
    outfit_source,  # Can be a string path (e.g. 'gown') OR raw uploaded file bytes!
    category: str,
    templates_folder: str = "images/model_templates",
    scale_val: float = 1.0,
    x_val: int = 0,
    y_val: int = 0,
) -> bytes:
    """
    Advanced Grayscale Texture Mapping Fitting Engine.
    Dynamically handles BOTH local template lookups and raw user-uploaded clothing styles.
    """
    # 1. Open base model portrait structures in clean RGBA channels
    person_img = Image.open(io.BytesIO(person_bytes)).convert("RGBA")
    w_person, h_person = person_img.size

    # 2. 🔥 DYNAMIC APPAREL SOURCE HANDLER 🔥
    # Checks if outfit_source is raw uploaded file bytes or a folder text string lookup
    if isinstance(outfit_source, bytes):
        raw_apparel = Image.open(io.BytesIO(outfit_source)).convert("RGBA")
    else:
        clean_apparel_name = outfit_source.strip().lower() if outfit_source else "gown"
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
                    f"Template path asset '{clean_apparel_name}' missing from {templates_folder}"
                )
        raw_apparel = Image.open(target_apparel_path).convert("RGBA")

    # 3. BACKGROUND ISOLATION MASK GENERATOR (Wipes out style background colors)
    # Using python libraries directly to avoid compilation/Pylance alerts
    import rembg

    try:
        bg_eraser_method = getattr(rembg, "remove")
        rembg_output_array = bg_eraser_method(raw_apparel)
        clean_apparel_base = Image.fromarray(rembg_output_array).convert("RGBA")
    except Exception as rembg_err:
        logger.warning(f"Rembg dynamic execution anomaly caught: {rembg_err}")
        clean_apparel_base = raw_apparel.convert("RGBA")

    # 4. Safe Type Validation for Step 2 active fabric textures
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
                "Fabric data arrived as a tuple configuration and no active layout fallback was found."
            )
    else:
        raise TypeError(
            f"Invalid fabric asset format sent from Step 2: {type(fabric_data)}."
        )

    # 5. GRAYSCALE DE-SATURATION & WRINKLE MAPPING ENGINES
    mask_width, mask_height = clean_apparel_base.size
    fabric_w, fabric_h = fabric_texture_img.size

    # Tile your vibrant Step 2 design pattern across the dimensions of the apparel shape
    tiled_fabric = Image.new("RGB", (mask_width, mask_height))
    for x in range(0, mask_width, fabric_w):
        for y in range(0, mask_height, fabric_h):
            tiled_fabric.paste(fabric_texture_img, (x, y))

    # Convert original colored apparel to 8-bit grayscale ("L") to completely erase colors
    apparel_grayscale = clean_apparel_base.convert("L")

    # Optimize shadow map contrast to extract wrinkles, shading, and texture lines sharply
    shadow_enhancer = ImageEnhance.Contrast(apparel_grayscale)
    grayscale_wrinkle_map = shadow_enhancer.enhance(1.35).convert("RGB")

    # Blend: Multiply design colors with the grayscale lighting depth layer
    textured_fabric_with_folds = ImageChops.multiply(
        tiled_fabric, grayscale_wrinkle_map
    )
    final_vibrant_attire = Image.blend(tiled_fabric, textured_fabric_with_folds, 0.40)

    # Intersect layers: Lock final design outcome inside the transparent silhouette vectors
    textured_apparel = Image.new("RGBA", (mask_width, mask_height), (0, 0, 0, 0))
    textured_apparel.paste(final_vibrant_attire, (0, 0))
    textured_apparel.putalpha(clean_apparel_base.getchannel("A"))

    # Crop empty padding margins to establish accurate positioning anchors
    bbox = textured_apparel.getbbox()
    if bbox:
        textured_apparel = textured_apparel.crop(bbox)

    # 6. Geometric Proportional Placement Math
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
    resized_apparel = textured_apparel.resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )

    # 7. WEAR THE FINISHED TEXTURED APPAREL ON THE MODEL
    apparel_overlay_canvas = Image.new("RGBA", (w_person, h_person), (0, 0, 0, 0))
    x_paste = center_x - (target_width // 2)
    y_paste = center_y - (target_height // 2)

    apparel_overlay_canvas.paste(resized_apparel, (x_paste, y_paste), resized_apparel)
    final_composite_img = Image.alpha_composite(person_img, apparel_overlay_canvas)

    # 8. Compress and convert frame down to web-optimized JPEG bytes representation
    output_buffer = io.BytesIO()
    final_rgb_lookbook = final_composite_img.convert("RGB")
    final_rgb_lookbook.save(output_buffer, format="JPEG", quality=95, optimize=True)

    return output_buffer.getvalue()
