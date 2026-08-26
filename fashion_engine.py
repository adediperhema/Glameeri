import numpy as np
import cv2
from PIL import Image


def apply_3d_displacement_field(
    user_model_pil: Image.Image, fabric_pattern_input
) -> Image.Image:
    """
    Processes an in-memory user portrait and dynamically drapes a fabric pattern
    using geometric coordinate mapping and matrix transformation operations.

    :param user_model_pil: A standard PIL Image object from the streamlit web container.
    :param fabric_pattern_input: Either a PIL Image or a file path string pointing to a fabric texture.
    :return: A cleanly transformed PIL Image object ready for downstream rendering.
    """
    try:
        # 1. 🌐 WEB-SAFE IMAGE TRANSFORMATION: Convert input PIL to OpenCV format (NumPy Array)
        # We must explicitly convert RGB to BGR as OpenCV uses BGR arrangement internally
        model_array = np.array(user_model_pil.convert("RGB"))
        opencv_model = cv2.cvtColor(model_array, cv2.COLOR_RGB2BGR)

        # 2. FABRIC INPUT NORMALIZATION: Ensure fabric is ready for processing in-memory
        if isinstance(fabric_pattern_input, str):
            # If a path string is provided, read it directly
            opencv_fabric = cv2.imread(fabric_pattern_input)
            if opencv_fabric is None:
                raise FileNotFoundError(
                    f"Fabric texture file could not be read at path: {fabric_pattern_input}"
                )
        else:
            # If a PIL image object is provided, convert it to an array
            fabric_array = np.array(fabric_pattern_input.convert("RGB"))
            opencv_fabric = cv2.cvtColor(fabric_array, cv2.COLOR_RGB2BGR)

        # 3. 📐 MATRIX RESIZING: Ensure the fabric map spans across the destination image matrix dimensions
        h_model, w_model, _ = opencv_model.shape
        opencv_fabric = cv2.resize(
            opencv_fabric, (w_model, h_model), interpolation=cv2.INTER_LINEAR
        )

        # 4. 🧠 CORE ALGORITHMIC ENGINE PLACEHOLDER
        # =========================================================================
        # Replace this basic masking loop with your advanced custom 3D displacement matrix arrays.
        # This standard example generates a synthetic sinusoidal warp grid and blends it onto the target image coordinates.
        # =========================================================================

        # Build coordinate layout maps
        map_x, map_y = np.meshgrid(np.arange(w_model), np.arange(h_model))

        # Apply displacement mapping rules (Simulates a wavy fabric drape look)
        displacement_amplitude = 8.0  # Tweak to change pattern distortion strength
        displacement_frequency = 0.05  # Tweak to change wave frequencies

        map_x_warped = (
            map_x + displacement_amplitude * np.sin(map_y * displacement_frequency)
        ).astype(np.float32)
        map_y_warped = map_y.astype(np.float32)

        # Re-map texture arrays onto the destination matrix using remap constraints
        warped_fabric = cv2.remap(
            opencv_fabric,
            map_x_warped,
            map_y_warped,
            cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT,
        )

        # Isolate contours or segment areas using an alpha channel mix mask setup
        # (This standard placeholder blends the images evenly at 50% opacity)
        blended_output_cv = cv2.addWeighted(opencv_model, 0.5, warped_fabric, 0.5, 0)

        # =========================================================================

        # 5. 🔄 RETURN TRANSFORMATION PIPELINE: Convert BGR OpenCV back into a clean RGB PIL object
        final_rgb_array = cv2.cvtColor(blended_output_cv, cv2.COLOR_BGR2RGB)
        return Image.fromarray(final_rgb_array)

    except Exception as e:
        # Wrap underlying OpenCV internal execution faults into clean Python exceptions
        raise RuntimeError(f"Fashion Engine Algorithmic Failure: {str(e)}")
