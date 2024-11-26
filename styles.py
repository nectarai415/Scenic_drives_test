def apply_custom_styles():
    return """
        <style>
        .content-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 1rem;
        }
        
        .map-container {
            width: 100%;
            margin-bottom: 2rem;
        }
        
        .route-info {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .route-title {
            color: #2b7bf2;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .highlight-list {
            list-style-type: none;
            padding-left: 0;
        }
        
        .highlight-item {
            margin: 0.2rem 0;
        }
        
        .metric {
            display: inline-block;
            background-color: #e1e5ee;
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            margin-right: 1rem;
        }
        </style>
    """
