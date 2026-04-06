import pandas as pd
import glob
import os

def process_data():
    # Automatically find the JSON file created in Task 1
    json_files = glob.glob("data/trends_*.json")
    if not json_files:
        print("Error: No JSON file found in the data/ folder. Please run Task 1 first.")
        return
    
    # Grab the most recently created file in case you ran Task 1 multiple times
    latest_file = max(json_files, key=os.path.getctime)
    
    # Load into Pandas DataFrame
    df = pd.read_json(latest_file)
    print(f"Loaded {len(df)} stories from {latest_file}")
    
    # Fix Duplicates: remove rows with the same post_id
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")
    
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")
    
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)
    df['score'] = df['score'].astype(int)
    
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")
    
    df['title'] = df['title'].astype(str).str.strip()
    
    output_file = "data/trends_clean.csv"
    
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} rows to {output_file}")
    
    print("Stories per category:")
    category_counts = df['category'].value_counts()
    
    for category, count in category_counts.items():
        print(f"  {category:<15} {count}")

if __name__ == "__main__":
    process_data()