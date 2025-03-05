import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

#to merge all datasets for visualization and comparision purpose
def plot(file_address1,file_address_2,file_address3,year):
    df1 = pd.read_csv(file_address1)
    df2 = pd.read_csv(file_address_2)
    df3 = pd.read_csv(file_address3)
    merged_df = df1.merge(df2,on='Occupation',suffixes=('_ear','_pop'))
    merged_df = merged_df.merge(df3, on='Occupation',suffixes=('','_wor'))
    merged_df.columns = ['Occupation', 'total_ear', 'male_ear', 'female_ear',
                        'total_pop', 'male_pop', 'female_pop',
                        'total_wor', 'male_wor', 'female_wor']
    merged_df.set_index('Occupation',inplace=True)

   
    def Zscore_normalize(df, columns):
        normalized_df = df.copy()
        for column in columns:
            min_value = df[column].min()
            max_value = df[column].max()
            
            normalized_df[column] = (df[column] - min_value) / (max_value - min_value)
        return normalized_df

    col_to_normalize = ['total_ear', 'total_pop', 'total_wor', 'female_pop', 'male_pop']
    normalized_df = Zscore_normalize(merged_df.drop('Total', axis=0), col_to_normalize)
    radar_df = normalized_df[col_to_normalize].head()

    radar_df

    # col_to_normalize = ['total_ear','total_pop','total_wor','female_pop','male_pop']
    # normalized_df = Zscore_normalize(merged_df,col_to_normalize)
    # radar_df = normalized_df[col_to_normalize]
    # radar_df.drop('Total', inplace=True,axis=0)
    # radar_df
    # Sample Data (values for each attribute)
    labels = ["total_ear",	"total_pop",	"total_wor",	"female_pop",	"male_pop"]
    row = 0
    values = [radar_df['total_ear'][row], radar_df['total_pop'][row], radar_df['total_wor'][row], radar_df['female_pop'][row], radar_df['male_pop'][row]]  # Scores out of 110

    # Convert to radians for the radar chart
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()

    # Close the shape by repeating first value
    values += values[:1]
    angles += angles[:1]

    # Plot radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.3)  # Fill area
    ax.plot(angles, values, color='blue', linewidth=2)  # Border line
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Show the plot
    plt.title("Employe Chat "+ year)
    plt.show()

#employee population of 2018 needs to be found for proper implementation 
#plot('data/2018/Earning2018.csv','data/2018/employePopn2018.csv','data/2018/workinghr2018.csv','2018')
plot('data/2008/Earning2008.csv','data/2008/employePopn2008.csv','data/2008/workinghr2008.csv','2008')
plot('data/1998/Earning1998.csv','data/1998/employePopn1998.csv','data/1998/workinghr1998.csv','1998')