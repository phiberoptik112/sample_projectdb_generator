import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_room_volume_comparison():
    """Compare room volumes across all projects"""
    conn = sqlite3.connect('project_management.db')
    
    query = """
    SELECT 
        p.project_name,
        p.client_name,
        es.space_name,
        es.space_type,
        es.volume_cubic_ft,
        es.nc_requirement,
        es.rt60_500hz,
        es.background_noise_dba
    FROM equipment_spaces es
    JOIN projects p ON es.project_id = p.project_id
    ORDER BY es.volume_cubic_ft DESC
    """
    
    df = pd.read_sql_query(query, conn)
    
    # Create a summary by project
    project_summary = df.groupby('project_name').agg({
        'volume_cubic_ft': ['sum', 'mean', 'count'],
        'nc_requirement': 'mean',
        'background_noise_dba': 'mean'
    }).round(2)
    
    project_summary.columns = ['Total Volume (ft³)', 'Avg Room Volume (ft³)', 
                             'Number of Rooms', 'Avg NC', 'Avg Background Noise (dBA)']
    
    return df, project_summary

def get_material_performance_comparison():
    """Compare material performance and costs across projects"""
    conn = sqlite3.connect('project_management.db')
    
    query = """
    SELECT 
        p.project_name,
        p.client_name,
        am.material_name,
        am.material_type,
        am.nrc_single_value,
        am.stc_rating,
        am.iic_rating,
        am.cost_per_sqft
    FROM acoustic_materials am
    JOIN projects p ON am.project_id = p.project_id
    """
    
    df = pd.read_sql_query(query, conn)
    
    # Create performance-cost summary
    performance_summary = df.groupby('material_type').agg({
        'nrc_single_value': 'mean',
        'stc_rating': 'mean',
        'iic_rating': 'mean',
        'cost_per_sqft': ['mean', 'min', 'max']
    }).round(2)
    
    return df, performance_summary

def plot_room_volumes(df):
    """Create visualizations for room volumes"""
    plt.figure(figsize=(12, 6))
    
    # Create box plot of room volumes by project
    sns.boxplot(data=df, x='project_name', y='volume_cubic_ft')
    plt.xticks(rotation=45)
    plt.title('Room Volume Distribution by Project')
    plt.xlabel('Project')
    plt.ylabel('Volume (cubic feet)')
    plt.tight_layout()
    plt.savefig('room_volumes.png')
    plt.close()

def plot_material_performance(df):
    """Create visualizations for material performance vs cost"""
    plt.figure(figsize=(12, 6))
    
    # Create scatter plot of NRC vs cost for room treatments
    room_treatments = df[df['material_type'] == 'Room Treatment']
    sns.scatterplot(data=room_treatments, 
                   x='cost_per_sqft', 
                   y='nrc_single_value',
                   hue='material_name',
                   s=100)
    plt.title('NRC vs Cost for Room Treatment Materials')
    plt.xlabel('Cost per Square Foot ($)')
    plt.ylabel('NRC Rating')
    plt.tight_layout()
    plt.savefig('material_performance.png')
    plt.close()

def main():
    # Get room volume analysis
    room_df, room_summary = get_room_volume_comparison()
    print("\nRoom Volume Analysis by Project:")
    print(room_summary)
    
    # Get material performance analysis
    material_df, material_summary = get_material_performance_comparison()
    print("\nMaterial Performance Summary:")
    print(material_summary)
    
    # Create visualizations
    plot_room_volumes(room_df)
    plot_material_performance(material_df)
    
    # Save detailed analysis to CSV
    room_df.to_csv('room_analysis.csv', index=False)
    material_df.to_csv('material_analysis.csv', index=False)

if __name__ == "__main__":
    main() 