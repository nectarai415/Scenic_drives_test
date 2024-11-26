import folium
from folium import plugins
import streamlit as st

def create_base_map():
    """Create the base map centered on the Bay Area"""
    return folium.Map(
        location=[36.7783, -119.4179],  # California's center
        zoom_start=6,  # Zoom level to show whole state
        tiles='cartodbpositron'
    )

def add_route_to_map(m, coordinates, name, color="#2b7bf2"):
    """Add a route line to the map"""
    folium.PolyLine(
        coordinates,
        weight=4,
        color=color,
        opacity=0.8,
        popup=name
    ).add_to(m)
    
    # Add markers for start and end points
    folium.CircleMarker(
        coordinates[0],
        radius=8,
        color=color,
        fill=True,
        popup=f"{name} (Start)"
    ).add_to(m)
    
    folium.CircleMarker(
        coordinates[-1],
        radius=8,
        color=color,
        fill=True,
        popup=f"{name} (End)"
    ).add_to(m)

def get_route_color(category):
    """Return color based on route category"""
    colors = {
        "coastal": "#0066cc",
        "mountain": "#006600",
        "wine country": "#990033"
    }
    return colors.get(category, "#2b7bf2")

def create_legend(categories):
    """Create HTML legend for route categories"""
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white;
                padding: 10px; border-radius: 5px; border: 2px solid grey; opacity: 0.8;">
    <h4>Route Categories</h4>
    '''
    
    colors = {
        "coastal": "#0066cc",
        "mountain": "#006600",
        "wine country": "#990033"
    }
    
    for category in categories:
        legend_html += f'''
        <div>
            <span style="background-color: {colors[category]}; width: 20px; height: 20px; 
                        display: inline-block; margin-right: 5px; border-radius: 50%;"></span>
            <span>{category.title()}</span>
        </div>
        '''
    
    legend_html += '</div>'
    return legend_html
