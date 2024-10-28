import pandas as pd

df = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/recipes_data_2024-10-22.csv')
df.columns = df.iloc[0]