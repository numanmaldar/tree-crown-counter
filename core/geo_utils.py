import rasterio
import pandas as pd

def get_image_resolution(image_path):
    """
    Reads GSD (ground sample distance) from a georeferenced raster.
    Returns (res_x, res_y) in meters/pixel, or (None, None) if not georeferenced.
    """
    try:
        with rasterio.open(image_path) as src:
            if src.crs is None:
                return None, None
            res_x, res_y = src.res
            return res_x, res_y
    except Exception:
        return None, None


def calculate_crown_areas(boxes_df, res_x, res_y):
    """
    Adds a crown_area_m2 column to a DeepForest predictions dataframe.
    boxes_df must have xmin, ymin, xmax, ymax columns (pixel coordinates).
    res_x, res_y: meters per pixel in x and y directions.
    """
    df = boxes_df.copy()
    width_px = df["xmax"] - df["xmin"]
    height_px = df["ymax"] - df["ymin"]
    df["crown_area_m2"] = (width_px * res_x) * (height_px * res_y)
    return df


def summarize_results(df):
    """
    Returns summary stats: tree count, total canopy area, avg crown size.
    """
    return {
        "tree_count": len(df),
        "total_canopy_area_m2": df["crown_area_m2"].sum(),
        "average_crown_area_m2": df["crown_area_m2"].mean(),
    }