# Databricks Streamlit Template

A production-ready template for building and deploying Streamlit visualizations as Databricks Apps. This template provides a complete starting point with sample visualizations, Databricks integration utilities, and deployment configuration.

## Features

- 📊 Pre-built interactive dashboard with sample visualizations
- 🔌 Ready-to-use Databricks connectors (SQL Warehouse, Unity Catalog)
- 🎨 Clean, responsive UI with Plotly charts
- 🛠️ Utility modules for data generation and connections
- 📦 Complete deployment configuration for Databricks Apps
- 🔒 Secure credential management

## Project Structure

```
databricks-streamlit-template/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── databricks.yml                  # Databricks App configuration
├── .databrickscfg.template         # Authentication template
├── utils/
│   ├── __init__.py
│   ├── databricks_connector.py    # Databricks connection utilities
│   └── data_generator.py          # Sample data generation
└── README.md                       # This file
```

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd databricks-streamlit-template
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application locally**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

### Deploying to Databricks

#### Prerequisites

- Databricks workspace (AWS, Azure, or GCP)
- Databricks CLI installed (`pip install databricks-cli`)
- Personal access token from your Databricks workspace

#### Setup Authentication

1. **Create your Databricks configuration**
   ```bash
   cp .databrickscfg.template ~/.databrickscfg
   ```

2. **Edit `~/.databrickscfg` with your credentials**
   ```ini
   [DEFAULT]
   host = https://your-workspace.cloud.databricks.com
   token = dapi_your_personal_access_token
   ```

   To generate a personal access token:
   - Go to your Databricks workspace
   - Click your user profile (top right) → Settings
   - Navigate to Developer → Access tokens
   - Click "Generate new token"

3. **Update `databricks.yml`**
   - Edit the `host` field with your workspace URL
   - Adjust compute size based on your needs (2X-Small to 2X-Large)
   - Configure environment variables if connecting to SQL warehouses

#### Deploy the App

1. **Using Databricks CLI**
   ```bash
   databricks apps deploy
   ```

2. **Using Databricks Asset Bundles (recommended)**
   ```bash
   databricks bundle validate
   databricks bundle deploy
   ```

3. **Access your deployed app**
   - Navigate to your Databricks workspace
   - Go to Apps section
   - Find your app (streamlit-template)
   - Click to open the live application

## Connecting to Databricks Resources

### Using SQL Warehouse

Update your `databricks.yml` to include environment variables:

```yaml
env:
  - name: DATABRICKS_SERVER_HOSTNAME
    value: "your-workspace.cloud.databricks.com"
  - name: DATABRICKS_HTTP_PATH
    value: "/sql/1.0/warehouses/xxxxx"
  - name: DATABRICKS_TOKEN
    value: "{{secrets/scope/token}}"  # Use Databricks secrets
```

### Query Unity Catalog Tables

In your [app.py](app.py), use the provided utilities:

```python
from utils.databricks_connector import query_databricks_table

# Query a table
df = query_databricks_table(
    catalog="main",
    schema="default",
    table="sales_data",
    limit=10000,
    filters="date >= '2024-01-01'"
)
```

### Execute Custom SQL

```python
from utils.databricks_connector import execute_sql_query

query = """
    SELECT region, SUM(revenue) as total_revenue
    FROM main.default.sales_data
    GROUP BY region
    ORDER BY total_revenue DESC
"""

df = execute_sql_query(query)
```

## Customization

### Adding New Visualizations

Edit [app.py](app.py) and add your charts using Plotly, Matplotlib, or other libraries:

```python
import plotly.express as px

fig = px.bar(df, x='category', y='value', title='My Custom Chart')
st.plotly_chart(fig, use_container_width=True)
```

### Adding New Pages

Create a multi-page app structure:

```
pages/
├── 1_📊_Dashboard.py
├── 2_📈_Analytics.py
└── 3_⚙️_Settings.py
```

Streamlit will automatically create a navigation sidebar.

### Styling

Update the custom CSS in [app.py:30-38](app.py#L30-L38):

```python
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    /* Add your custom styles */
    </style>
    """, unsafe_allow_html=True)
```

## Configuration

### Compute Resources

Adjust the compute size in [databricks.yml](databricks.yml) based on your needs:

- **2X-Small / X-Small**: Light workloads, simple dashboards
- **Small / Medium**: Standard dashboards with moderate data
- **Large / X-Large**: Heavy computations, large datasets
- **2X-Large**: Very demanding workloads

### Dependencies

Add Python packages to [requirements.txt](requirements.txt):

```txt
# Your additional packages
scikit-learn>=1.3.0
pyspark>=3.5.0
```

## Sample Data

The template includes data generators in [utils/data_generator.py](utils/data_generator.py):

```python
from utils.data_generator import generate_sales_data, generate_time_series_data

# Generate sample sales data
sales_df = generate_sales_data(num_records=1000)

# Generate time series data
ts_df = generate_time_series_data(start_date=datetime(2024, 1, 1))
```

## Best Practices

### Performance

- **Cache data loading**: Use `@st.cache_data` for expensive operations
  ```python
  @st.cache_data(ttl=3600)
  def load_data():
      return query_databricks_table(...)
  ```

- **Limit query results**: Use LIMIT clauses or filters to reduce data transfer
- **Optimize compute size**: Start small and scale up as needed

### Security

- **Never commit credentials**: Use `.gitignore` to exclude sensitive files
- **Use Databricks secrets**: Store tokens in Databricks secret scopes
- **Validate user inputs**: Sanitize inputs to prevent SQL injection

### Development

- **Test locally first**: Use sample data generators for local development
- **Version control**: Commit your code regularly
- **Document changes**: Keep README updated with new features

## Troubleshooting

### App won't start
- Check [requirements.txt](requirements.txt) has all dependencies
- Verify compute resources are sufficient
- Check Databricks workspace logs

### Can't connect to SQL Warehouse
- Verify `DATABRICKS_SERVER_HOSTNAME` is correct
- Check `DATABRICKS_HTTP_PATH` points to valid warehouse
- Ensure token has proper permissions

### Deployment fails
- Validate [databricks.yml](databricks.yml) syntax
- Check Databricks CLI is authenticated
- Verify workspace has Apps feature enabled

## Resources

- [Databricks Apps Documentation](https://docs.databricks.com/apps/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Unity Catalog Guide](https://docs.databricks.com/data-governance/unity-catalog/)
- [Databricks SQL Connector](https://docs.databricks.com/dev-tools/python-sql-connector.html)

## License

This template is provided as-is for use in your Databricks projects.

## Contributing

Feel free to submit issues and enhancement requests!

---

Built with ❤️ for the Databricks community
