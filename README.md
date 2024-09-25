# User Manual for the t-route Output Visualization Dashboard

## Introduction

Welcome to the t-route Output Visualization Dashboard for the Lower Colorado region. This interactive dashboard allows you to explore hydrological data through an intuitive interface, visualize variables over time, and interact with geospatial data on a map. It is designed to help researchers, hydrologists, and environmental scientists analyze and compare hydrological datasets effectively.

This manual will guide you through the installation, setup, and usage of the dashboard, ensuring you can leverage all its features for your data analysis needs.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
   - [System Requirements](#system-requirements)
   - [Dependencies](#dependencies)
   - [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [Using the Dashboard](#using-the-dashboard)
   - [Dataset Selection](#dataset-selection)
   - [Feature ID Selection](#feature-id-selection)
   - [Time Range Adjustment](#time-range-adjustment)
   - [Variable Selection](#variable-selection)
   - [Displaying Data and Plots](#displaying-data-and-plots)
   - [Map Interaction](#map-interaction)
5. [Customization](#customization)
   - [Adding New Datasets](#adding-new-datasets)
   - [Modifying Default Paths](#modifying-default-paths)
6. [Troubleshooting](#troubleshooting)
   - [Common Issues and Solutions](#common-issues-and-solutions)
7. [Conclusion](#conclusion)
8. [Disclaimer](#Disclaimer)

## Installation

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: Python 3.7 or higher
- **Internet Connection**: Required for installing dependencies and running the dashboard

### Dependencies

Ensure the following Python packages are installed:

- `streamlit`
- `xarray`
- `pandas`
- `numpy`
- `matplotlib`
- `geopandas`
- `folium`
- `streamlit_folium`
- `shapely`

You can install them using the following command:

```bash
pip install streamlit xarray pandas numpy matplotlib geopandas folium streamlit_folium shapely
```

### Installation Steps

1. **Clone the Repository** (if applicable):

   ```bash
   git clone https://github.com/your_username/your_repository.git
   ```

   Replace `your_username` and `your_repository` with your GitHub username and repository name.

2. **Navigate to the Directory**:

   ```bash
   cd your_repository
   ```

3. **Save the Dashboard Script**:

   Save the dashboard code provided into a Python script file named, for example, `dashboard.py`.

## Running the Application

To start the dashboard, use the following command in your terminal:

```bash
streamlit run /path/to/dashboard.py
```

Replace `/path/to/` with the actual path to where you saved the `dashboard.py` file.

**Example**:

```bash
streamlit run dashboard.py
```

Once the command is executed, Streamlit will launch the dashboard in your default web browser.

## Using the Dashboard

### Dataset Selection

- **Default Datasets**: The dashboard comes with default dataset paths pre-configured. These datasets are located in:

  ```plaintext
  /home/amin/Amin_fork_V2/t-route/test/LowerColorado_TX_v4/output
  /home/amin/Amin_fork_V2/t-route/test/LowerColorado_TX_v4/output2
  ```

- **Adding Datasets**: In the sidebar, you can add new dataset paths by entering the path in the "Add new dataset path" text input.

- **GeoPackage Path**: Ensure the GeoPackage path is set correctly. The default path is:

  ```plaintext
  /home/amin/Amin_fork_V2/t-route/test/LowerColorado_TX_v4/domain/LowerColorado_NGEN_v201.gpkg
  ```

### Feature ID Selection

- After selecting a NetCDF file, the dashboard will load the available `feature_id`s.
- Use the multiselect box in the sidebar to select one or more `feature_id`s to visualize.
- If you know the `feature_id`s you are interested in, you can type them directly into the input box.

### Time Range Adjustment

- Use the time range slider in the sidebar to specify the start and end times for the data visualization.
- The slider automatically adjusts to the minimum and maximum times available in the dataset.

### Variable Selection

- Choose the variable you want to plot from the dropdown menu in the sidebar. Options include:

  - `flow`
  - `velocity`
  - `depth`

### Displaying Data and Plots

- **DataFrame Display**:

  - In the main area of the dashboard, the left column displays the data in a table format.
  - You can choose to display the full DataFrame or only selected columns by toggling the "Show full dataframe" checkbox in the sidebar.

- **Plot Display**:

  - The right column displays plots of the selected variable over time for the selected `feature_id`s.
  - The plots are interactive and will update automatically when you adjust the selections or time range.

### Map Interaction

- **Enable Map**:

  - To view the geospatial map, select "Yes" under the "Map" option in the sidebar.

- **Interacting with the Map**:

  - The map displays flowpaths from the GeoPackage file.
  - Click on flowpaths to select or deselect them. Selected flowpaths are highlighted on the map.
  - The dashboard updates the data and plots based on your selections on the map.

- **Tooltip Information**:

  - Hover over flowpaths on the map to view details such as `ID`, `To ID`, `Mainstem`, and `Divide ID`.

## Customization

### Adding New Datasets

- In the sidebar, use the "Add new dataset path" text input to specify the path to additional NetCDF datasets.
- After adding a new path, it will appear in the datasets list for selection.

### Modifying Default Paths

- You can modify the default dataset paths and GeoPackage path directly in the code by changing the values of `default_datasets` and `default_gpkg_path` variables.

  ```python
  default_datasets = [
      "/path/to/your/first/dataset",
      "/path/to/your/second/dataset",
  ]
  default_gpkg_path = "/path/to/your/geopackage.gpkg"
  ```

- Alternatively, use the sidebar inputs to override these paths without modifying the code.

## Troubleshooting

### Common Issues and Solutions

- **No NetCDF Files Found**:

  - **Problem**: The dashboard displays a warning that no NetCDF files were found in the directory.
  - **Solution**: Ensure that the dataset paths provided contain NetCDF files with a `.nc` extension.

- **No Data Available for Selected Feature IDs**:

  - **Problem**: After selecting feature IDs, the dashboard shows a warning that no data is available.
  - **Solution**: Verify that the selected feature IDs exist in the chosen NetCDF files. You may need to adjust your selection or check the data for correctness.

- **Map Not Displaying**:

  - **Problem**: The map does not display when "Yes" is selected under "Map".
  - **Solution**: Ensure that the GeoPackage file path is correct and that the file contains the necessary layers (`flowpaths`). Also, check that all required geospatial libraries (`geopandas`, `folium`) are installed.

- **Performance Issues**:

  - **Problem**: The dashboard is slow to respond or load data.
  - **Solution**: Large datasets can affect performance. Try reducing the number of selected feature IDs or simplifying the geometries in the GeoPackage file. Ensure that caching is enabled by not modifying the `@st.cache_data` decorators.

## Conclusion

This dashboard provides an interactive platform for visualizing and analyzing hydrological data in the Lower Colorado region. By following this user manual, you should be able to set up, run, and utilize the dashboard effectively for your research or projects. The modular design allows for easy customization and extension to accommodate different datasets or regions.

## Disclaimer
This visualizer is not official version, It's built for internal use of inland hydraulic team 


![image](https://github.com/user-attachments/assets/fb401d1b-30a9-4800-96cb-072beff48f4f)
