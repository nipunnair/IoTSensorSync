import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json
from datetime import datetime, timedelta
import threading
import queue

from sensor_simulator import SensorSimulator
from data_processor import DataProcessor
from data_storage import DataStorage
from analytics import Analytics
from utils import format_timestamp, validate_sensor_data

# Initialize session state
if 'data_storage' not in st.session_state:
    st.session_state.data_storage = DataStorage()
if 'sensor_simulator' not in st.session_state:
    st.session_state.sensor_simulator = SensorSimulator()
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
if 'analytics' not in st.session_state:
    st.session_state.analytics = Analytics()
if 'simulation_active' not in st.session_state:
    st.session_state.simulation_active = False
if 'data_queue' not in st.session_state:
    st.session_state.data_queue = queue.Queue()

def main():
    st.set_page_config(
        page_title="IoT Sensor Data Pipeline",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🌡️ IoT Sensor Data Collection & Processing Pipeline")
    st.markdown("Real-time monitoring and data processing for Temperature, Weight, Moisture, and Pressure sensors")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # Simulation controls
        st.subheader("Sensor Simulation")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start", use_container_width=True):
                st.session_state.simulation_active = True
                st.success("Simulation started!")
                
        with col2:
            if st.button("⏹️ Stop", use_container_width=True):
                st.session_state.simulation_active = False
                st.info("Simulation stopped!")
        
        # Simulation settings
        st.subheader("Settings")
        simulation_speed = st.slider("Data Collection Interval (seconds)", 1, 10, 2)
        
        # Data management
        st.subheader("Data Management")
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.data_storage.clear_data()
            st.success("All data cleared!")
            st.rerun()
        
        # Export functionality
        st.subheader("📤 Export Data")
        export_format = st.selectbox("Export Format", ["CSV", "JSON"])
        
        if st.button("Download Cleaned Data", use_container_width=True):
            if st.session_state.data_storage.has_data():
                cleaned_data = st.session_state.data_processor.get_cleaned_data(
                    st.session_state.data_storage.get_all_data()
                )
                
                if export_format == "CSV":
                    csv_data = cleaned_data.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv_data,
                        file_name=f"cleaned_sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    json_data = cleaned_data.to_json(orient='records', date_format='iso')
                    st.download_button(
                        label="💾 Download JSON",
                        data=json_data,
                        file_name=f"cleaned_sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            else:
                st.warning("No data available for export")
    
    # Main content area
    if st.session_state.simulation_active:
        # Generate and process new sensor data
        sensor_data = st.session_state.sensor_simulator.generate_reading()
        validation_result = validate_sensor_data(sensor_data)
        
        if validation_result['valid']:
            st.session_state.data_storage.add_reading(sensor_data)
        else:
            st.error(f"❌ Invalid sensor data: {validation_result['errors']}")
    
    # Display current status
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        status = "🟢 Active" if st.session_state.simulation_active else "🔴 Inactive"
        st.metric("Simulation Status", status)
    
    with status_col2:
        total_readings = st.session_state.data_storage.get_total_readings()
        st.metric("Total Readings", total_readings)
    
    with status_col3:
        if st.session_state.data_storage.has_data():
            latest_time = st.session_state.data_storage.get_latest_timestamp()
            st.metric("Last Reading", format_timestamp(latest_time))
        else:
            st.metric("Last Reading", "No data")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Real-time Dashboard", "🔧 Data Processing", "📊 Analytics", "🔍 Data Explorer"])
    
    with tab1:
        display_realtime_dashboard()
    
    with tab2:
        display_data_processing()
    
    with tab3:
        display_analytics()
    
    with tab4:
        display_data_explorer()
    
    # Auto-refresh for real-time updates
    if st.session_state.simulation_active:
        time.sleep(simulation_speed)
        st.rerun()

def display_realtime_dashboard():
    st.header("📈 Real-time Sensor Dashboard")
    
    if not st.session_state.data_storage.has_data():
        st.info("🔄 Start the simulation to see real-time sensor data")
        return
    
    # Get recent data for visualization
    recent_data = st.session_state.data_storage.get_recent_data(hours=1)
    
    if recent_data.empty:
        st.warning("No recent data available")
        return
    
    # Current sensor values
    st.subheader("🎯 Current Readings")
    latest_reading = recent_data.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🌡️ Temperature", 
            f"{latest_reading['temperature']:.1f}°C",
            delta=f"{latest_reading['temperature'] - recent_data.iloc[-2]['temperature']:.1f}" if len(recent_data) > 1 else None
        )
    
    with col2:
        st.metric(
            "⚖️ Weight", 
            f"{latest_reading['weight']:.1f}kg",
            delta=f"{latest_reading['weight'] - recent_data.iloc[-2]['weight']:.1f}" if len(recent_data) > 1 else None
        )
    
    with col3:
        st.metric(
            "💧 Moisture", 
            f"{latest_reading['moisture']:.1f}%",
            delta=f"{latest_reading['moisture'] - recent_data.iloc[-2]['moisture']:.1f}" if len(recent_data) > 1 else None
        )
    
    with col4:
        st.metric(
            "📊 Pressure", 
            f"{latest_reading['pressure']:.1f}Pa",
            delta=f"{latest_reading['pressure'] - recent_data.iloc[-2]['pressure']:.1f}" if len(recent_data) > 1 else None
        )
    
    # Time series plots
    st.subheader("📊 Time Series Visualization")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Temperature (°C)', 'Weight (kg)', 'Moisture (%)', 'Pressure (Pa)'),
        vertical_spacing=0.1
    )
    
    # Temperature
    fig.add_trace(
        go.Scatter(x=recent_data['timestamp'], y=recent_data['temperature'], 
                  name='Temperature', line=dict(color='red')),
        row=1, col=1
    )
    
    # Weight
    fig.add_trace(
        go.Scatter(x=recent_data['timestamp'], y=recent_data['weight'], 
                  name='Weight', line=dict(color='blue')),
        row=1, col=2
    )
    
    # Moisture
    fig.add_trace(
        go.Scatter(x=recent_data['timestamp'], y=recent_data['moisture'], 
                  name='Moisture', line=dict(color='green')),
        row=2, col=1
    )
    
    # Pressure
    fig.add_trace(
        go.Scatter(x=recent_data['timestamp'], y=recent_data['pressure'], 
                  name='Pressure', line=dict(color='orange')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def display_data_processing():
    st.header("🔧 Data Processing Pipeline")
    
    if not st.session_state.data_storage.has_data():
        st.info("No data available for processing")
        return
    
    raw_data = st.session_state.data_storage.get_all_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Data Quality Metrics")
        
        quality_metrics = st.session_state.data_processor.analyze_data_quality(raw_data)
        
        for metric, value in quality_metrics.items():
            if isinstance(value, float):
                st.metric(metric.replace('_', ' ').title(), f"{value:.2f}")
            else:
                st.metric(metric.replace('_', ' ').title(), str(value))
    
    with col2:
        st.subheader("🔍 Outlier Detection")
        
        outliers = st.session_state.data_processor.detect_outliers(raw_data)
        
        if outliers.empty:
            st.success("✅ No outliers detected")
        else:
            st.warning(f"⚠️ {len(outliers)} outliers detected")
            st.dataframe(outliers)
    
    # Data cleaning options
    st.subheader("🧹 Data Cleaning Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        remove_outliers = st.checkbox("Remove Outliers", value=True)
    
    with col2:
        fill_missing = st.checkbox("Fill Missing Values", value=True)
    
    with col3:
        smooth_data = st.checkbox("Apply Smoothing", value=False)
    
    if st.button("🔄 Process Data"):
        cleaned_data = st.session_state.data_processor.clean_data(
            raw_data, 
            remove_outliers=remove_outliers,
            fill_missing=fill_missing,
            smooth_data=smooth_data
        )
        
        st.success("✅ Data processing completed!")
        
        # Show before/after comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Before Cleaning")
            st.dataframe(raw_data.tail(10))
        
        with col2:
            st.subheader("✨ After Cleaning")
            st.dataframe(cleaned_data.tail(10))

def display_analytics():
    st.header("📊 Analytics Dashboard")
    
    if not st.session_state.data_storage.has_data():
        st.info("No data available for analytics")
        return
    
    data = st.session_state.data_storage.get_all_data()
    
    # Statistical summary
    st.subheader("📈 Statistical Summary")
    
    stats = st.session_state.analytics.calculate_statistics(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Descriptive Statistics**")
        st.dataframe(stats['descriptive'])
    
    with col2:
        st.write("**Correlation Matrix**")
        correlation_fig = px.imshow(
            stats['correlation'], 
            text_auto=True, 
            aspect="auto",
            title="Sensor Data Correlation"
        )
        st.plotly_chart(correlation_fig, use_container_width=True)
    
    # Trend analysis
    st.subheader("📈 Trend Analysis")
    
    trends = st.session_state.analytics.analyze_trends(data)
    
    for sensor, trend_data in trends.items():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"{sensor.title()} Trend", trend_data['direction'])
        
        with col2:
            st.metric("Slope", f"{trend_data['slope']:.4f}")
        
        with col3:
            st.metric("R²", f"{trend_data['r_squared']:.4f}")
    
    # Distribution plots
    st.subheader("📊 Distribution Analysis")
    
    sensor_cols = ['temperature', 'weight', 'moisture', 'pressure']
    
    for sensor in sensor_cols:
        fig = px.histogram(
            data, 
            x=sensor, 
            title=f"{sensor.title()} Distribution",
            marginal="box"
        )
        st.plotly_chart(fig, use_container_width=True)

def display_data_explorer():
    st.header("🔍 Data Explorer")
    
    if not st.session_state.data_storage.has_data():
        st.info("No data available to explore")
        return
    
    data = st.session_state.data_storage.get_all_data()
    
    # Data filtering options
    st.subheader("🔧 Filter Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        date_range = st.date_input(
            "Select Date Range",
            value=(data['timestamp'].min().date(), data['timestamp'].max().date()),
            min_value=data['timestamp'].min().date(),
            max_value=data['timestamp'].max().date()
        )
    
    with col2:
        sensors_to_show = st.multiselect(
            "Select Sensors",
            ['temperature', 'weight', 'moisture', 'pressure'],
            default=['temperature', 'weight', 'moisture', 'pressure']
        )
    
    # Apply filters
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = data[
            (data['timestamp'].dt.date >= start_date) & 
            (data['timestamp'].dt.date <= end_date)
        ]
    else:
        filtered_data = data
    
    # Display filtered data
    st.subheader("📋 Filtered Data")
    
    display_columns = ['timestamp'] + sensors_to_show
    st.dataframe(filtered_data[display_columns], use_container_width=True)
    
    # Data summary
    st.subheader("📊 Summary Statistics")
    
    if sensors_to_show:
        summary_stats = filtered_data[sensors_to_show].describe()
        st.dataframe(summary_stats)
    
    # Custom visualization
    st.subheader("📈 Custom Visualization")
    
    if len(sensors_to_show) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("X-axis", sensors_to_show, index=0)
        
        with col2:
            y_axis = st.selectbox("Y-axis", sensors_to_show, index=1)
        
        if x_axis != y_axis:
            scatter_fig = px.scatter(
                filtered_data,
                x=x_axis,
                y=y_axis,
                color='timestamp',
                title=f"{x_axis.title()} vs {y_axis.title()}"
            )
            st.plotly_chart(scatter_fig, use_container_width=True)

if __name__ == "__main__":
    main()
