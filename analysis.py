"""
EPU Indonesia Data Analysis
Author: Made Gde
Website: madegde.github.io/epuindonesia
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Load EPU data
def load_epu_data():
    """Load EPU data from Excel file"""
    df = pd.read_excel('EPU_Indo_Monthly.xlsx')
    
    # Create date column
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
    df['Date_String'] = df['Date'].dt.strftime('%Y-%m')
    
    return df

# Create Figure 1: Article Coverage
def create_article_coverage_plot(data):
    """Create scatter plot for article coverage per publisher"""
    fig = px.scatter(
        data, 
        x='Date', 
        y='Publisher Code', 
        color='Publisher', 
        title='Article Coverages per Publisher Over Time',
        labels={'Date': 'Date', 'Publisher': 'Publisher'},
        height=500
    )
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title='Publisher Code',
        xaxis=dict(tickangle=0),
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

# Create Figure 2: EPU Index with annotations
def create_epu_index_plot(df):
    """Create EPU index line chart with event annotations"""
    
    # Create base figure
    fig = go.Figure()
    
    # Add main EPU line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Indonesia'],
        mode='lines',
        name='EPU Index',
        line=dict(color='rgb(102, 126, 234)', width=2),
        hovertemplate='%{x|%b %Y}<br>EPU: %{y:.2f}<extra></extra>'
    ))
    
    # Define major events with their dates
    events = [
        {'date': '1998-06-01', 'text': 'Asian Financial\nCrisis', 'y_offset': -30},
        {'date': '2001-05-01', 'text': 'Wahid Scandal', 'y_offset': -40},
        {'date': '2002-08-01', 'text': 'Constitutional\nAmendments', 'y_offset': -25},
        {'date': '2003-12-01', 'text': 'Iraq War &\nSARS', 'y_offset': -35},
        {'date': '2004-09-01', 'text': 'Bomb Attacks', 'y_offset': -30},
        {'date': '2008-05-01', 'text': 'Global Financial\nCrisis', 'y_offset': -30},
        {'date': '2010-05-01', 'text': 'Eurozone\nDebt Crisis', 'y_offset': -25},
        {'date': '2011-12-01', 'text': 'US Debt\nCeiling', 'y_offset': -35},
        {'date': '2014-12-01', 'text': 'Fuel Subsidies\nCut', 'y_offset': -30},
        {'date': '2015-10-01', 'text': 'China Economic\nTurmoil', 'y_offset': -35},
        {'date': '2016-11-01', 'text': 'Trump Election', 'y_offset': -25},
        {'date': '2020-09-01', 'text': 'COVID-19\nPandemic', 'y_offset': -40},
        {'date': '2022-08-01', 'text': 'Ukraine War', 'y_offset': -35},
        {'date': '2024-11-01', 'text': 'US Election', 'y_offset': -25}
    ]
    
    # Add annotations for each event
    for event in events:
        event_date = pd.to_datetime(event['date'])
        # Find the EPU value for this date
        epu_value = df[df['Date'] == event_date]['Indonesia'].values
        if len(epu_value) > 0:
            fig.add_annotation(
                x=event_date,
                y=epu_value[0],
                text=event['text'],
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor="gray",
                ax=0,
                ay=event['y_offset'],
                font=dict(size=10),
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor="gray",
                borderwidth=1
            )
    
    # Update layout
    fig.update_layout(
        title='Economic Policy Uncertainty (EPU) Index for Indonesia',
        xaxis_title='',
        yaxis_title='EPU Index',
        template='plotly_white',
        height=600,
        hovermode='x unified',
        showlegend=False,
        xaxis=dict(
            rangeslider=dict(visible=True, thickness=0.05),
            type='date'
        )
    )
    
    return fig

# Export data for web
def export_for_web(df):
    """Export data in formats suitable for web visualization"""
    
    # Prepare data for JSON export
    web_data = {
        'data': df[['Year', 'Month', 'Indonesia']].to_dict('records'),
        'statistics': {
            'total_points': len(df),
            'max_value': float(df['Indonesia'].max()),
            'min_value': float(df['Indonesia'].min()),
            'mean_value': float(df['Indonesia'].mean()),
            'median_value': float(df['Indonesia'].median()),
            'std_dev': float(df['Indonesia'].std())
        },
        'date_range': {
            'start': df['Date'].min().strftime('%Y-%m'),
            'end': df['Date'].max().strftime('%Y-%m')
        }
    }
    
    # Save as JSON
    with open('epu_data.json', 'w') as f:
        json.dump(web_data, f, indent=2)
    
    # Save as CSV
    df[['Date_String', 'Indonesia']].rename(
        columns={'Date_String': 'Date', 'Indonesia': 'EPU_Index'}
    ).to_csv('epu_indonesia.csv', index=False)
    
    print("Data exported successfully!")
    print(f"Total data points: {len(df)}")
    print(f"Date range: {web_data['date_range']['start']} to {web_data['date_range']['end']}")
    print(f"EPU range: {web_data['statistics']['min_value']:.2f} to {web_data['statistics']['max_value']:.2f}")

# Main execution
if __name__ == "__main__":
    # Load data
    df = load_epu_data()
    
    # Create and show EPU index plot
    fig = create_epu_index_plot(df)
    fig.show()
    
    # Export for web
    export_for_web(df)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Mean EPU: {df['Indonesia'].mean():.2f}")
    print(f"Median EPU: {df['Indonesia'].median():.2f}")
    print(f"Max EPU: {df['Indonesia'].max():.2f} in {df.loc[df['Indonesia'].idxmax(), 'Date_String']}")
    print(f"Min EPU: {df['Indonesia'].min():.2f} in {df.loc[df['Indonesia'].idxmin(), 'Date_String']}")
