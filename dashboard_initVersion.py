# to run use this command: streamlit run /home/amin/Amin_fork_V2/t-route/test/misc/dashboard)initVersion.py

import streamlit as st
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import glob
import os
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point
from functools import reduce

warnings.filterwarnings('ignore')

# Default paths
default_datasets = [
    "/home/amin/Amin_fork_V2/t-route/test/LowerColorado_TX_v4/output",
    "/home/amin/Amin_fork_V2/t-route/test/LowerColorado_TX_v4/output2",
]
default_gpkg_path = r"/home/amin/Amin_fork_V2/t-route/test/LowerColorado_TX_v4/domain/LowerColorado_NGEN_v201.gpkg"

def initialize_app():
    st.set_page_config(page_title="LowerColorado!", page_icon=":bar_chart:", layout="wide")
    st.title(" :earth_americas: LowerColorado")
    if 'selected_feature_ids' not in st.session_state:
        st.session_state.selected_feature_ids = []

@st.cache_data
def load_netcdf_files(file_path):
    return sorted(glob.glob(os.path.join(file_path, "*.nc")))

@st.cache_data
def netcdf_to_dataframe(file):
    ds = xr.open_dataset(file)
    return ds.to_dataframe().reset_index()

@st.cache_data
def load_geopackage(gpkg_path):
    return gpd.read_file(gpkg_path, layer='flowpaths')

def geojson_style_function(feature):
    return {'color': 'blue', 'weight': 2}

def geojson_highlight_function(feature):
    return {'color': 'red', 'weight': 5}

def highlighted_style_function(feature):
    return {'color': 'red', 'weight': 5}

def prepare_geodataframe(gdf, simplify_tolerance):
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs(epsg=4326)
    gdf['geometry'] = gdf['geometry'].simplify(tolerance=simplify_tolerance)
    return gdf

@st.cache_data
def create_cached_map(_gdf, selected_feature_ids=None, simplify_tolerance=0.001):
    gdf = prepare_geodataframe(_gdf, simplify_tolerance)
    m = initialize_map(gdf)
    add_geojson_to_map(m, gdf, selected_feature_ids)
    return m

def initialize_map(gdf):
    bounds = gdf.total_bounds
    centroid = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    return folium.Map(location=centroid, zoom_start=10)

def add_geojson_to_map(m, gdf, selected_feature_ids):
    geojson = folium.GeoJson(
        data=gdf.__geo_interface__,
        style_function=geojson_style_function,
        highlight_function=geojson_highlight_function,
        tooltip=folium.GeoJsonTooltip(fields=['id', 'toid', 'mainstem', 'divide_id'], aliases=['ID', 'To ID', 'Mainstem', 'Divide ID']),
        name='geojson'
    )

    geojson.add_child(folium.features.GeoJsonPopup(fields=['id'], labels=False, sticky=False))
    geojson.add_to(m)

    if selected_feature_ids:
        highlight_selected_features(m, gdf, selected_feature_ids)

def highlight_selected_features(m, gdf, selected_feature_ids):
    for feature_id in selected_feature_ids:
        feature_id = 'wb-' + str(feature_id)
        highlight = gdf[gdf['id'] == feature_id]
        if not highlight.empty:
            folium.GeoJson(
                data=highlight,
                style_function=highlighted_style_function,
                tooltip=folium.GeoJsonTooltip(fields=['id', 'toid', 'mainstem', 'divide_id'], aliases=['ID', 'To ID', 'Mainstem', 'Divide ID']),
            ).add_to(m)
            bounds = highlight.total_bounds
            padding = 0.01
            m.fit_bounds([[bounds[1] - padding, bounds[0] - padding], [bounds[3] + padding, bounds[2] + padding]])

def process_and_merge_dataframes(netcdf_files, selected_feature_ids):
    merged_df = pd.DataFrame()
    for file in netcdf_files:
        temp_df = netcdf_to_dataframe(file)
        temp_df = temp_df[temp_df['feature_id'].isin(selected_feature_ids)]
        temp_df['time'] = pd.to_datetime(temp_df['time'])
        merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
    return merged_df

def merge_datasets(*dfs):
    merged_df = dfs[0]
    for i, df in enumerate(dfs[1:], start=2):
        merged_df = pd.merge(merged_df, df, on=["feature_id", "time", "type"], suffixes=('', f'_{i}'))
    return merged_df

def plot_data(filtered_dfs, column_to_plot, selected_feature_ids, col2):
    fig, ax = plt.subplots(figsize=(8, 6))
    for feature_id in selected_feature_ids:
        for i, df in enumerate(filtered_dfs):
            feature_df = df[df['feature_id'] == feature_id]
            ax.plot(feature_df['time'], feature_df[column_to_plot], marker='o', linestyle='-' if i == 0 else '--', label=f'Dataset {i+1} - feature_id: {feature_id}')
    ax.set_xlabel('Time')
    ax.set_ylabel(column_to_plot.capitalize())
    ax.set_title(f'{column_to_plot.capitalize()} vs Time for selected feature_ids')
    plt.xticks(rotation=20)
    ax.legend()
    plt.tight_layout()
    col2.pyplot(fig)

def plot_df(merged_df, column_to_plot, show_full_df):
    if show_full_df:
        st.dataframe(merged_df)
    else:
        selected_cols = merged_df.columns[merged_df.columns.str.startswith(column_to_plot)]
        st.dataframe(merged_df[['time', 'feature_id'] + selected_cols.tolist()])

def extract_id_from_tooltip(tooltip):
    start_str = "wb-"
    start_idx = tooltip.find(start_str) + len(start_str)
    end_idx = tooltip.find("\n", start_idx)
    if start_idx != -1 and end_idx != -1:
        return int(tooltip[start_idx:end_idx].strip())
    return None

def handle_sidebar_inputs():
    st.sidebar.header("Datasets")
    datasets = st.sidebar.multiselect("Select or add dataset paths:", default_datasets, default=default_datasets)
    new_dataset_path = st.sidebar.text_input("Add new dataset path")

    if new_dataset_path:
        datasets.append(new_dataset_path)

    gpkg_path = st.sidebar.text_input("GeoPackage Path", default_gpkg_path)

    return datasets, gpkg_path

def run_app():
    initialize_app()

    datasets, gpkg_path = handle_sidebar_inputs()

    netcdf_files_list = [load_netcdf_files(path) for path in datasets]
    file_dict = {os.path.basename(f): f for f in netcdf_files_list[0]}  # Assuming same filenames in all directories
    selected_file_name = st.sidebar.selectbox("Select a NetCDF file", list(file_dict.keys()))
    show_map = st.sidebar.selectbox("Map", ["No", "Yes"])

    selected_files = [file_dict[selected_file_name].replace(datasets[0], datasets[i]) for i in range(len(datasets))]

    if all(selected_files):
        st.write(f"Selected file: {selected_file_name}")

        dfs = [netcdf_to_dataframe(selected_file) for selected_file in selected_files]
        
        selected_feature_ids_all = dfs[0]['feature_id'].unique().tolist()
        entire_dfs = [process_and_merge_dataframes(selected_file, selected_feature_ids_all) for selected_file in netcdf_files_list]

        if dfs:
            unique_feature_ids = dfs[0]['feature_id'].unique().tolist()

            selected_feature_ids = st.sidebar.multiselect(
                label="Select or type feature IDs:",
                options=unique_feature_ids,
                default=st.session_state.selected_feature_ids,
                key='feature_id_multiselect'
            )

            st.session_state.selected_feature_ids = selected_feature_ids

            if selected_feature_ids:
                merged_dfs = [process_and_merge_dataframes(selected_file, selected_feature_ids) for selected_file in netcdf_files_list]

                merged_df = merge_datasets(*merged_dfs)

                min_time = min(df['time'].min() for df in merged_dfs).to_pydatetime()
                max_time = max(df['time'].max() for df in merged_dfs).to_pydatetime()

                time_range = st.sidebar.slider("Select time range", min_value=min_time, max_value=max_time, value=(min_time, max_time), 
                                               step=pd.Timedelta(hours=1), format="YYYY-MM-DD HH:mm")
                filtered_dfs = [df[(df['time'] >= time_range[0]) & (df['time'] <= time_range[1])] for df in merged_dfs]
                column_to_plot = st.sidebar.selectbox("Select column to plot", ['flow', 'velocity', 'depth'])
                
                st.session_state.column_to_plot = column_to_plot
                
                st.session_state.show_full_df = st.sidebar.checkbox("Show full dataframe", value=True, key="show_full_df_checkbox")
                
                display_data_and_plot(merged_df, filtered_dfs, column_to_plot, selected_feature_ids)

                if show_map == "Yes":
                    display_map(gpkg_path, entire_dfs)

            else:
                st.warning("Please select at least one feature_id to display.")
        else:
            st.warning("No data available to display.")
    else:
        st.warning("No NetCDF files found in the directory.")

def display_data_and_plot(merged_df, filtered_dfs, column_to_plot, selected_feature_ids):
    col1, col2 = st.columns(2)
    with col1:
        plot_df(merged_df, column_to_plot, st.session_state.show_full_df)

    if all(not df.empty for df in filtered_dfs):
        with col2:
            plot_data(filtered_dfs, column_to_plot, selected_feature_ids, col2)
    else:
        st.warning("No data available to display for the selected time range.")

def display_map(gpkg_path, entire_dfs):
    gdf = load_geopackage(gpkg_path)
    if not gdf.empty:
        # Use the cached map function to improve performance
        map_object = create_cached_map(gdf, st.session_state.selected_feature_ids)
        map_data = st_folium(map_object, width=1200, height=800, key="map")

        if map_data and "last_object_clicked_tooltip" in map_data and map_data["last_object_clicked_tooltip"] is not None:
            clicked_id = extract_id_from_tooltip(map_data["last_object_clicked_tooltip"])
            if clicked_id:
                update_selected_feature_ids(clicked_id, entire_dfs)

def update_selected_feature_ids(clicked_id, entire_dfs):
    if clicked_id in st.session_state.selected_feature_ids:
        st.session_state.selected_feature_ids.remove(clicked_id)
    else:
        st.session_state.selected_feature_ids.append(clicked_id)
    
    filtered_dfs = [df[df['feature_id'].isin(st.session_state.selected_feature_ids)] for df in entire_dfs]
    
    merged_df_select = reduce(lambda left, right: pd.merge(left, right, on=["feature_id", "time", "type"], how='outer'), filtered_dfs)
    display_data_and_plot(merged_df_select, filtered_dfs, st.session_state.column_to_plot, st.session_state.selected_feature_ids)

if __name__ == "__main__":
    run_app()
