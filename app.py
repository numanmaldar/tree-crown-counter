import streamlit as st
import os
import tempfile
from deepforest import main
from core.geo_utils import get_image_resolution, calculate_crown_areas, summarize_results
from core.overlays import draw_boxes_on_image

st.set_page_config(page_title="Tree Crown Counter", layout="wide")

st.title("🌳 Tree Crown Counter & Canopy Area Estimator")
st.markdown(
    "Upload a high-resolution forest image (GeoTIFF preferred) to detect individual "
    "tree crowns and estimate canopy coverage."
)

# --- Sidebar controls ---
st.sidebar.header("Settings")
confidence_threshold = st.sidebar.slider(
    "Detection confidence threshold", 0.0, 1.0, 0.3, 0.05
)

manual_gsd = st.sidebar.number_input(
    "Manual resolution override (meters/pixel) — only used if image has no geospatial metadata",
    min_value=0.0, value=0.0, step=0.01, format="%.3f"
)

st.sidebar.markdown("---")
with st.sidebar.expander("⚠️ Limitations — please read"):
    st.markdown("""
    - Model is **pretrained on NEON forest plot data (US)** and not fine-tuned for this specific region — accuracy varies by forest type, density, and imaging conditions.
    - Canopy area is estimated using **bounding boxes**, not true crown-shaped polygons — this **overestimates area** for irregular crowns and can **double-count** in dense, overlapping canopy.
    - No field validation has been performed on this deployment — treat outputs as estimates, not ground truth.
    - Accuracy depends heavily on image resolution; very low-resolution or blurry imagery will degrade detection quality significantly.
    - If the uploaded image lacks embedded geospatial metadata, area results depend entirely on the manual resolution value you provide — an incorrect value will silently produce wrong areas.
    """)

# --- File upload ---
uploaded_file = st.file_uploader("Upload forest image (.tif, .tiff, .png, .jpg)", type=["tif", "tiff", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        image_path = tmp.name

    st.info("Running detection... this may take a moment on first load (model download).")

    with st.spinner("Detecting tree crowns..."):
        model = main.deepforest()
        boxes = model.predict_image(path=image_path)

        if boxes is None or len(boxes) == 0:
            st.warning("No trees detected. Try a different image or check that it contains visible vegetation.")
            st.stop()

        # Filter by confidence threshold
        boxes = boxes[boxes["score"] >= confidence_threshold].reset_index(drop=True)

        if len(boxes) == 0:
            st.warning(f"No detections above confidence threshold {confidence_threshold}. Try lowering it.")
            st.stop()

        # Resolve resolution: georeferenced metadata first, manual override fallback
        res_x, res_y = get_image_resolution(image_path)
        used_manual_gsd = False

        if res_x is None or res_y is None:
            if manual_gsd > 0:
                res_x, res_y = manual_gsd, manual_gsd
                used_manual_gsd = True
            else:
                st.error(
                    "This image has no embedded geospatial metadata, and no manual resolution "
                    "was provided. Please enter a resolution (meters/pixel) in the sidebar to "
                    "calculate real-world area."
                )
                st.stop()

        boxes_with_area = calculate_crown_areas(boxes, res_x, res_y)
        summary = summarize_results(boxes_with_area)

        annotated_path = os.path.join(tempfile.gettempdir(), "annotated_output.png")
        draw_boxes_on_image(image_path, boxes_with_area, output_path=annotated_path)

    # --- Results display ---
    st.success("Detection complete!")

    if used_manual_gsd:
        st.caption(f"⚠️ No geospatial metadata found — using manual resolution: {manual_gsd} m/pixel")
    else:
        st.caption(f"✅ Geospatial metadata detected — resolution: {res_x:.3f} x {res_y:.3f} m/pixel")

    col1, col2, col3 = st.columns(3)
    col1.metric("Trees Detected", summary["tree_count"])
    col2.metric("Total Canopy Area", f"{summary['total_canopy_area_m2']:.1f} m²")
    col3.metric("Average Crown Size", f"{summary['average_crown_area_m2']:.2f} m²")

    st.image(annotated_path, caption="Detected tree crowns", use_container_width=True)

    # --- Downloads ---
    st.subheader("Download Results")
    csv_data = boxes_with_area.to_csv(index=False)
    st.download_button(
        "Download detections as CSV",
        data=csv_data,
        file_name="tree_crown_detections.csv",
        mime="text/csv"
    )

    with open(annotated_path, "rb") as f:
        st.download_button(
            "Download annotated image",
            data=f,
            file_name="annotated_tree_crowns.png",
            mime="image/png"
        )

    with st.expander("View raw detection data"):
        st.dataframe(boxes_with_area)

else:
    st.info("👆 Upload an image to get started.")