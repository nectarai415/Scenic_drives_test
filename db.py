import os
import psycopg2
from psycopg2.extras import DictCursor
from data import scenic_routes

def get_db_connection():
    """Create a database connection"""
    try:
        return psycopg2.connect(os.environ['DATABASE_URL'])
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def migrate_routes():
    """Migrate routes from data.py to the database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Insert routes
        for name, route in scenic_routes.items():
            # Extract distance value (remove 'miles' and convert to float)
            distance = float(route['distance'].split()[0])
            
            # Insert route
            cur.execute("""
                INSERT INTO routes (name, description, distance, duration, category)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
            """, (name, route['description'], distance, route['duration'], route['category']))
            
            route_id = cur.fetchone()[0]
            
            # Insert highlights
            for highlight in route['highlights']:
                cur.execute("""
                    INSERT INTO highlights (route_id, highlight_name)
                    VALUES (%s, %s)
                """, (route_id, highlight))
            
            # Insert coordinates
            for position, coord in enumerate(route['coordinates']):
                cur.execute("""
                    INSERT INTO coordinates (route_id, latitude, longitude, position)
                    VALUES (%s, %s, %s, %s)
                """, (route_id, coord[0], coord[1], position))
        
        conn.commit()
        print("Routes migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        
    finally:
        cur.close()
        conn.close()

def get_all_routes():
    """Retrieve all routes with their highlights and coordinates"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    
    try:
        # Get all routes
        cur.execute("""
            SELECT id, name, description, distance, duration, category
            FROM routes
        """)
        routes = dict()
        
        for route in cur.fetchall():
            route_id = route['id']
            routes[route['name']] = {
                'description': route['description'],
                'distance': f"{route['distance']} miles",
                'duration': route['duration'],
                'category': route['category'],
                'highlights': [],
                'coordinates': []
            }
            
            # Get highlights for each route
            cur.execute("""
                SELECT highlight_name
                FROM highlights
                WHERE route_id = %s
                ORDER BY id
            """, (route_id,))
            routes[route['name']]['highlights'] = [h['highlight_name'] for h in cur.fetchall()]
            
            # Get coordinates for each route
            cur.execute("""
                SELECT latitude, longitude
                FROM coordinates
                WHERE route_id = %s
                ORDER BY position
            """, (route_id,))
            routes[route['name']]['coordinates'] = [[c['latitude'], c['longitude']] for c in cur.fetchall()]
            
        return routes
        
    finally:
        cur.close()
        conn.close()
