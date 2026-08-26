# gallery_page.py
import streamlit as st
import time
import json
from database import Collection


def render_interactive_gallery_suite(db, token_user_id):
    st.markdown(
        '<p class="vk-section-header">🖼️ Studio Collection Lookbook Portfolio</p>',
        unsafe_allow_html=True,
    )

    if st.button("⬅️ Return to Collection Manager"):
        st.session_state.sidebar_selection = "📁 Fabric Collection Manager"
        st.rerun()

    st.write(
        "Browse, audit, modify metadata variables, or download production assets live:"
    )
    st.divider()

    gallery_items = (
        db.query(Collection)
        .filter(Collection.user_id == token_user_id)
        .order_by(Collection.id.desc())
        .all()
    )

    if not gallery_items:
        st.info(
            "🎭 No portfolio items found. Save items from Step 3 or onboard new batches to view them here."
        )
        return

    for idx, item in enumerate(gallery_items):
        with st.container():
            col_view, col_edit = st.columns([1.5, 1.0], gap="medium")

            with col_view:
                st.markdown(f"### 📁 {item.title}")
                st.caption(f"**Heritage Foundation Label:** {item.origin}")
                st.write(f"**Notes:** {item.description}")

                try:
                    decoded_img_payload = json.loads(
                        item.raw_images_blob.decode("utf-8")
                    )
                    if decoded_img_payload:
                        st.markdown("#### 🎨 Asset Swatches")
                        img_cols = st.columns(min(len(decoded_img_payload), 4))

                        for img_idx, hex_str in enumerate(decoded_img_payload):
                            with img_cols[img_idx % 4]:
                                # Convert hex string representation back to original binary bytes format
                                raw_image_bytes = bytes.fromhex(hex_str)
                                st.image(raw_image_bytes, use_container_width=True)

                                clean_title_slug = "".join(
                                    c
                                    for c in item.title
                                    if c.isalnum() or c in (" ", "_", "-")
                                ).rstrip()
                                file_download_name = f"{clean_title_slug.replace(' ', '_')}_swatch_{img_idx + 1}.png"

                                # Native dynamic stream attachment generator mapping
                                st.download_button(
                                    label=f"💾 Download #{img_idx + 1}",
                                    data=raw_image_bytes,
                                    file_name=file_download_name,
                                    mime="image/png",
                                    key=f"dl_{item.id}_{img_idx}_{idx}",
                                    use_container_width=True,
                                )
                    else:
                        st.caption(
                            "No swatch visuals associated with this database record row entry."
                        )
                except Exception as err:
                    st.caption(
                        f"⚠️ Visual block rendering exception encountered: {err}"
                    )

            with col_edit:
                st.markdown("#### ⚙️ Edit Metadata")
                with st.form(key=f"edit_form_{item.id}_{idx}"):
                    edit_title = st.text_input(
                        "Modify Reference Title:", value=item.title
                    )
                    edit_origin = st.selectbox(
                        "Update Heritage Origin:",
                        [
                            "Unspecified / General Heritage",
                            "Ankara Wax Print",
                            "Kente Cloth Heritage",
                            "Adire Tech",
                            "Modern Afro-Futurism",
                        ],
                        index=(
                            [
                                "Unspecified / General Heritage",
                                "Ankara Wax Print",
                                "Kente Cloth Heritage",
                                "Adire Tech",
                                "Modern Afro-Futurism",
                            ].index(item.origin)
                            if item.origin
                            in [
                                "Unspecified / General Heritage",
                                "Ankara Wax Print",
                                "Kente Cloth Heritage",
                                "Adire Tech",
                                "Modern Afro-Futurism",
                            ]
                            else 0
                        ),
                    )
                    edit_desc = st.text_area(
                        "Edit Studio Annotations:", value=item.description
                    )

                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        submit_edit = st.form_submit_button("💾 Save changes")
                    with btn_col2:
                        delete_item = st.form_submit_button("🗑️ Delete item")

                    if submit_edit:
                        # item.title = edit_title.strip()
                        # item.origin = edit_origin
                        # item.description = edit_desc.strip()

                        item.title = edit_title
                        item.origin = edit_origin
                        item.description = edit_desc

                        db.commit()
                        st.success("Metadata track updated!")
                        time.sleep(0.3)
                        st.rerun()

                    if delete_item:
                        db.delete(item)
                        db.commit()
                        st.warning("Collection record entry successfully deleted.")
                        time.sleep(0.3)
                        st.rerun()

        st.markdown(
            "<hr style='border:1px dashed #dadce0; margin:25px 0px;'>",
            unsafe_allow_html=True,
        )
