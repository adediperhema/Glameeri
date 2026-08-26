import io
import cv2
import numpy as np
import logging
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import mediapipe as mp

logger = logging.getLogger(__name__)

mp_pose = mp.solutions.pose
pose_detector = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

ALLOWED_CATEGORIES = {"tops", "bottoms", "one-pieces"}
CORS_ORIGINS = ["http://localhost:8501", "http://127.0.0.1:8501"]


def remove_background(image: np.ndarray) -> np.ndarray:
    if image.shape[2] == 3:
        b_ch, g_ch, r_ch = cv2.split(image)
        a_ch = np.ones(b_ch.shape, dtype=b_ch.dtype) * 255
        image = cv2.merge((b_ch, g_ch, r_ch, a_ch))
    gray = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2GRAY)
    _, alpha_mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    alpha_mask = cv2.morphologyEx(alpha_mask, cv2.MORPH_CLOSE, kernel)
    alpha_mask = cv2.morphologyEx(alpha_mask, cv2.MORPH_OPEN, kernel)
    image[:, :, 3] = cv2.bitwise_and(image[:, :, 3], alpha_mask)
    return image


def create_app() -> FastAPI:
    app = FastAPI(title="Free CPU Virtual Try-On API with Sliders", version="1.2.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    @app.post("/try-on")
    async def try_on(
        person_image: UploadFile = File(...),
        garment_image: UploadFile = File(...),
        category: str = Form(...),
        offset_x: int = Form(0),  # New parameter: Left/Right push
        offset_y: int = Form(0),  # New parameter: Up/Down push
        scale_multiplier: float = Form(1.0),  # New parameter: Fine-tune resize
    ) -> Response:
        if category not in ALLOWED_CATEGORIES:
            raise HTTPException(status_code=400, detail="Invalid category")

        try:
            p_bytes = await person_image.read()
            g_bytes = await garment_image.read()

            person_cv = cv2.imdecode(np.frombuffer(p_bytes, np.uint8), cv2.IMREAD_COLOR)
            garment_cv = cv2.imdecode(
                np.frombuffer(g_bytes, np.uint8), cv2.IMREAD_UNCHANGED
            )

            if person_cv is None or garment_cv is None:
                raise ValueError("Could not decode images.")

            garment_cv = remove_background(garment_cv)
            h_person, w_person, _ = person_cv.shape

            person_rgb = cv2.cvtColor(person_cv, cv2.COLOR_BGR2RGB)
            results = pose_detector.process(person_rgb)

            if not results.pose_landmarks:
                raise HTTPException(
                    status_code=400, detail="Could not detect body layout."
                )

            landmarks = results.pose_landmarks.landmark
            ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            lh = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            rh = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

            ls_x, ls_y = int(ls.x * w_person), int(ls.y * h_person)
            rs_x, rs_y = int(rs.x * w_person), int(rs.y * h_person)
            lh_x, lh_y = int(lh.x * w_person), int(lh.y * h_person)
            rh_x, rh_y = int(rh.x * w_person), int(rh.y * h_person)

            # Sizing based on body joints
            if category == "tops":
                target_width = int(abs(ls_x - rs_x) * 1.5)
                shoulder_center_y = (ls_y + rs_y) // 2
                hip_center_y = (lh_y + rh_y) // 2
                target_height = int(abs(hip_center_y - shoulder_center_y) * 1.2)

                center_x = (ls_x + rs_x) // 2
                center_y = (
                    shoulder_center_y + (target_height // 2) - int(target_height * 0.1)
                )
            else:
                target_width = int(abs(lh_x - rh_x) * 1.6)
                target_height = int(target_width * 1.2)
                center_x = (lh_x + rh_x) // 2
                center_y = (lh_y + rh_y) // 2 + (target_height // 4)

            # Apply UI Slider Modifications
            target_width = int(target_width * scale_multiplier)
            target_height = int(target_height * scale_multiplier)
            center_x += offset_x
            center_y += offset_y

            target_width = max(10, target_width)
            target_height = max(10, target_height)

            # Process composition paste
            resized_garment = cv2.resize(
                garment_cv, (target_width, target_height), interpolation=cv2.INTER_AREA
            )

            x1, y1 = center_x - (target_width // 2), center_y - (target_height // 2)
            x2, y2 = x1 + target_width, y1 + target_height

            img_x1, img_y1 = max(0, x1), max(0, y1)
            img_x2, img_y2 = min(w_person, x2), min(h_person, y2)

            g_x1, g_y1 = max(0, -x1), max(0, -y1)
            g_x2 = g_x1 + (img_x2 - img_x1)
            g_y2 = g_y1 + (img_y2 - img_y1)

            if img_x2 > img_x1 and img_y2 > img_y1:
                overlay_crop = resized_garment[g_y1:g_y2, g_x1:g_x2]
                alpha_mask = np.expand_dims(overlay_crop[:, :, 3] / 255.0, axis=2)

                bg_crop = person_cv[img_y1:img_y2, img_x1:img_x2]
                fg_crop = overlay_crop[:, :, :3]

                blended = (fg_crop * alpha_mask + bg_crop * (1.0 - alpha_mask)).astype(
                    np.uint8
                )
                person_cv[img_y1:img_y2, img_x1:img_x2] = blended

            _, encoded_img = cv2.imencode(".png", person_cv)
            return Response(content=encoded_img.tobytes(), media_type="image/png")

        except Exception as exc:
            logger.exception("Synthesis error")
            raise HTTPException(status_code=500, detail=str(exc))

    return app


app = create_app()
