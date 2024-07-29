import pandas as pd

# Load the CSV file
file_path = 'rating_result_hpto1.1_hpto1.2_cogvlm2.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Filter rows where hptol1_rating is lower than cogvlm2_rating
filtered_df = df[df['hpto1.2_rating'] == df['hpto1.1_rating']]

result = filtered_df[['id', 'task', 'hpto1.1_rating', 'hpto1.2_rating', 'cogvlm2_rating']]

print(result)
print(f"total: {len(filtered_df)}")


# Optionally, save the filtered results to a new CSV file
#filtered_df.to_csv('/mnt/data/filtered_results.csv', index=False)
