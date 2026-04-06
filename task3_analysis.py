import pandas as pd
import numpy as np

def analyze_data():
    file_path = "data/trends_clean.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}. Please run Task 2 first.")
        return

    print(f"Loaded data: {df.shape}")
    print("First 5 rows:")
    print(df.head())
    print()

    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    
    print(f"Average score   : {avg_score:,.0f}")
    print(f"Average comments: {avg_comments:,.0f}")
    print()

    print("--- NumPy Stats ---")
    
    scores_array = df['score'].to_numpy()
    
    mean_score = np.mean(scores_array)
    median_score = np.median(scores_array)
    std_dev = np.std(scores_array)
    max_score = np.max(scores_array)
    min_score = np.min(scores_array)

    print(f"Mean score   : {mean_score:,.0f}")
    print(f"Median score : {median_score:,.0f}")
    print(f"Std deviation: {std_dev:,.0f}")
    print(f"Max score    : {max_score:,.0f}")
    print(f"Min score    : {min_score:,.0f}")

    # Which category has the most stories
    category_counts = df['category'].value_counts()
    top_category = category_counts.idxmax()
    top_category_count = category_counts.max()
    print(f"Most stories in: {top_category} ({top_category_count} stories)")

    most_comments_idx = df['num_comments'].idxmax()
    most_commented_title = df.loc[most_comments_idx, 'title']
    most_commented_count = df.loc[most_comments_idx, 'num_comments']
    print(f'Most commented story: "{most_commented_title}"  — {most_commented_count:,} comments')
    print()

    # engagement = num_comments / (score + 1)
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    df['is_popular'] = df['score'] > avg_score

    output_file = "data/trends_analysed.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    analyze_data()