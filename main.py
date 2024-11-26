import streamlit as st
import folium
from streamlit_folium import folium_static
from data import scenic_routes
from utils import create_base_map, add_route_to_map, get_route_color, create_legend
from styles import apply_custom_styles

# Page configuration
st.set_page_config(
    page_title="Bay Area Scenic Drives",
    page_icon="🚗",
    layout="wide"
)

# Apply custom styles
st.markdown(apply_custom_styles(), unsafe_allow_html=True)

# Title and introduction
st.title("🚗 Bay Area Scenic Drives")
st.markdown("""
Explore the most beautiful driving routes in the San Francisco Bay Area. 
Select routes to view details and plan your next scenic adventure.
""")

# Sidebar filters
st.sidebar.title("Route Filters")

# Category filter
categories = list(set(route["category"] for route in scenic_routes.values()))
selected_categories = st.sidebar.multiselect(
    "Filter by Category",
    categories,
    default=categories
)

# Distance filter
distance_ranges = {
    "All": (0, 100),
    "Short (< 15 miles)": (0, 15),
    "Medium (15-30 miles)": (15, 30),
    "Long (> 30 miles)": (30, 100)
}
selected_distance = st.sidebar.selectbox("Filter by Distance", list(distance_ranges.keys()))

# Create the base map
m = create_base_map()

# Filter and display routes
filtered_routes = {}
for name, route in scenic_routes.items():
    distance = float(route["distance"].split()[0])
    distance_range = distance_ranges[selected_distance]
    
    if (route["category"] in selected_categories and 
        distance_range[0] <= distance <= distance_range[1]):
        filtered_routes[name] = route
        add_route_to_map(
            m, 
            route["coordinates"], 
            name, 
            get_route_color(route["category"])
        )

# Add legend to map
legend_html = create_legend(categories)
m.get_root().html.add_child(folium.Element(legend_html))

# Start content container
st.markdown('<div class="content-container">', unsafe_allow_html=True)

# Display map section
st.markdown("### Interactive Map")
st.markdown('<div class="map-container">', unsafe_allow_html=True)
folium_static(m)
st.markdown('</div>', unsafe_allow_html=True)

# Display route details section
st.markdown("### Route Details")

if not filtered_routes:
    st.warning("No routes match the selected filters.")
else:
    for name, route in filtered_routes.items():
        st.markdown(f"""
        <div class="route-info">
            <div class="route-title">{name}</div>
            <div class="metrics">
                <span class="metric">🛣️ {route['distance']}</span>
                <span class="metric">⏱️ {route['duration']}</span>
            </div>
            <p>{route['description']}</p>
            <strong>Highlights:</strong>
            <ul class="highlight-list">
                {''.join([f'<li class="highlight-item">• {h}</li>' for h in route['highlights']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style='text-align: center; color: #666;'>
    <small>Data is for demonstration purposes. Always verify route conditions before travel.</small>
</div>
""", unsafe_allow_html=True)

# Close content container
st.markdown('</div>', unsafe_allow_html=True)
