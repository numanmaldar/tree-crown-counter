from deepforest import main, get_data
from deepforest import visualize
import os

# Load pretrained model — leave on CPU for now
model = main.deepforest()

# Get sample image path
image_path = get_data("OSBS_029.tif")

# Run prediction
boxes = model.predict_image(path=image_path)

os.makedirs("output", exist_ok=True)

print(boxes.head())
print(f"\nTotal trees detected: {len(boxes)}")

boxes.to_csv("output/detections.csv", index=False)

visualize.plot_results(boxes, savedir="output")

import rasterio

with rasterio.open(get_data("OSBS_029.tif")) as src:
    print("CRS:", src.crs)
    print("Transform:", src.transform)
    print("Resolution (x, y):", src.res)
    
from core.geo_utils import get_image_resolution, calculate_crown_areas, summarize_results

res_x, res_y = get_image_resolution(image_path)
print(f"\nResolution: {res_x}m x {res_y}m per pixel")

boxes_with_area = calculate_crown_areas(boxes, res_x, res_y)
print(boxes_with_area[["xmin", "ymin", "xmax", "ymax", "score", "crown_area_m2"]].head())

summary = summarize_results(boxes_with_area)
print("\n--- SUMMARY ---")
print(f"Tree count: {summary['tree_count']}")
print(f"Total canopy area: {summary['total_canopy_area_m2']:.2f} m²")
print(f"Average crown area: {summary['average_crown_area_m2']:.2f} m²")

from core.overlays import draw_boxes_on_image

annotated = draw_boxes_on_image(image_path, boxes_with_area, output_path="output/annotated_result.png")
print("\nAnnotated image saved to output/annotated_result.png")