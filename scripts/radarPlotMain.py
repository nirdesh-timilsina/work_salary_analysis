import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from sklearn.preprocessing import StandardScaler

#to merge all datasets for visualization and comparision purpose
def plot(file_address1,file_address_2,file_address3,year):
    df1 = pd.read_csv(file_address1,header= None)
    df2 = pd.read_csv(file_address_2,header= None)
    df3 = pd.read_csv(file_address3,header= None)
    
# I encountered several errors regarding header 'occupation' so i implemented this code as final solution 
    df1.columns = df1.iloc[0]
    df1 = df1.drop(0).reset_index(drop=True)
    df1 = df1.rename(columns={df1.columns[0]: "Occupation"})  # Ensure first column is named "Occupation"

    # Repeat for df2 and df3
    df2.columns = df2.iloc[0]
    df2 = df2.drop(0).reset_index(drop=True)
    df2 = df2.rename(columns={df2.columns[0]: "Occupation"})

    df3.columns = df3.iloc[0]
    df3 = df3.drop(0).reset_index(drop=True)
    df3 = df3.rename(columns={df3.columns[0]: "Occupation"})

    # Merge
    merged_df = df1.merge(df2, on="Occupation", how="outer") \
                .merge(df3, on="Occupation", how="outer")
    #rename the columns for ease
    merged_df.columns = ['Occupation', 'total_ear', 'male_ear', 'female_ear',
                            'total_pop', 'male_pop', 'female_pop',
                            'total_wor', 'male_wor', 'female_wor']
    
    scalar = StandardScaler()
    col_to_normalize = ['total_ear', 'male_ear', 'female_ear', 'total_pop', 'male_pop', 'female_pop', 'total_wor', 'male_wor', 'female_wor']
    # for col in col_to_normalize:
    #     merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')
    normalized_df = merged_df
    normalized_df[col_to_normalize]= scalar.fit_transform(merged_df[col_to_normalize])

    radar_df = normalized_df
    # Sample Data (values for each attribute)
    labels = ["Salary","Population","Working Hours","Female Population","Male Population","Male Salary","Female Salary","Female Working Hours","Male Working Hours"]
    row = 0
    values = [radar_df['total_ear'][row], radar_df['total_pop'][row], radar_df['total_wor'][row], radar_df['female_pop'][row], radar_df['male_pop'][row],radar_df['male_ear'][row],radar_df['female_ear'][row],radar_df['female_wor'][row],radar_df['male_wor'][row]]  # Scores out of 110

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
    ax.set_ylim(-2.5, 2.5)
    ax.set_xticklabels(labels)

    # Show the plot
    plt.title(radar_df['Occupation'][row])
    plt.show()

#employee population of 2018 needs to be found for proper implementation 
plot('data/2018/Earning2018.csv','data/2018/employePopn2018.csv','data/2018/workinghr2018.csv','2018')
plot('data/2008/Earning2008.csv','data/2008/employePopn2008.csv','data/2008/workinghr2008.csv','2008')
plot('data/1998/Earning1998.csv','data/1998/employePopn1998.csv','data/1998/workinghr1998.csv','1998')