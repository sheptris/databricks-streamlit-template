"""
Databricks Streamlit Template Application

This is a template Streamlit application designed to run as a Databricks App.
It demonstrates common patterns for data visualization and interaction with Databricks resources.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Optional: Uncomment these imports when connecting to Databricks resources
# from databricks import sql
# from databricks.sdk import WorkspaceClient

# Page configuration
st.set_page_config(
    page_title="Databricks Streamlit Template",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def generate_sample_data():
    """Generate sample data for demonstration purposes."""
    np.random.seed(42)
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')

    data = pd.DataFrame({
        'date': dates,
        'sales': np.random.randint(100, 1000, size=len(dates)),
        'revenue': np.random.uniform(1000, 10000, size=len(dates)),
        'customers': np.random.randint(10, 100, size=len(dates)),
        'region': np.random.choice(['North', 'South', 'East', 'West'], size=len(dates))
    })

    return data


def load_data_from_databricks():
    """
    Load data from Databricks SQL warehouse or Unity Catalog.
    Uncomment and configure when deploying to Databricks.
    """
    # Example connection to Databricks SQL warehouse
    # connection = sql.connect(
    #     server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
    #     http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    #     access_token=os.getenv("DATABRICKS_TOKEN")
    # )
    #
    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM your_catalog.your_schema.your_table")
    # df = cursor.fetchall_arrow().to_pandas()
    # cursor.close()
    # connection.close()
    # return df

    # For now, return sample data
    return generate_sample_data()


def main():
    """Main application logic."""

    # Sidebar
    with st.sidebar:
        st.title("🎯 Configuration")
        st.markdown("---")

        # Data source selection
        data_source = st.selectbox(
            "Select Data Source",
            ["Sample Data", "Databricks SQL Warehouse", "Unity Catalog"]
        )

        # Date range filter
        st.subheader("Filters")
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now())
        )

        # Region filter
        regions = st.multiselect(
            "Select Regions",
            ["North", "South", "East", "West"],
            default=["North", "South", "East", "West"]
        )

        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # Main content
    st.title("📊 Databricks Streamlit Dashboard")
    st.markdown("A template application for visualizing data in Databricks Apps")

    # Load data
    with st.spinner("Loading data..."):
        df = load_data_from_databricks()

    # Filter data based on sidebar selections
    if len(date_range) == 2:
        df = df[(df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])]

    df = df[df['region'].isin(regions)]

    # Key metrics
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_sales = df['sales'].sum()
        st.metric("Total Sales", f"{total_sales:,}", delta=f"{int(total_sales * 0.1):,}")

    with col2:
        total_revenue = df['revenue'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}", delta=f"${total_revenue * 0.15:,.2f}")

    with col3:
        avg_customers = df['customers'].mean()
        st.metric("Avg Daily Customers", f"{avg_customers:.0f}", delta=f"{int(avg_customers * 0.05)}")

    with col4:
        avg_order_value = total_revenue / total_sales
        st.metric("Avg Order Value", f"${avg_order_value:.2f}", delta=f"${avg_order_value * 0.08:.2f}")

    st.markdown("---")

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sales Over Time")
        fig_sales = px.line(
            df,
            x='date',
            y='sales',
            title='Daily Sales Trend',
            labels={'sales': 'Sales', 'date': 'Date'}
        )
        fig_sales.update_layout(height=400)
        st.plotly_chart(fig_sales, use_container_width=True)

    with col2:
        st.subheader("Revenue by Region")
        region_revenue = df.groupby('region')['revenue'].sum().reset_index()
        fig_region = px.pie(
            region_revenue,
            values='revenue',
            names='region',
            title='Revenue Distribution by Region'
        )
        fig_region.update_layout(height=400)
        st.plotly_chart(fig_region, use_container_width=True)

    # Additional visualizations
    st.subheader("Revenue vs Customers Correlation")
    fig_scatter = px.scatter(
        df,
        x='customers',
        y='revenue',
        color='region',
        size='sales',
        title='Revenue vs Customer Count by Region',
        labels={'customers': 'Number of Customers', 'revenue': 'Revenue ($)'}
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Data table
    with st.expander("📋 View Raw Data"):
        st.dataframe(
            df.style.format({
                'revenue': '${:,.2f}',
                'sales': '{:,}',
                'customers': '{:,}'
            }),
            use_container_width=True
        )

    # Download data
    st.download_button(
        label="📥 Download Data as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=f'databricks_data_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
    )


if __name__ == "__main__":
    main()
