import pandas as pd
import matplotlib.pyplot as plt
import os

def create_visualizations():
    file_path = "data/trends_analysed.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}. Please run Task 3 first.")
        return

    os.makedirs("outputs", exist_ok=True)

    # Get top 10, sort ascending so the highest score is at the top of the horizontal bar chart
    top_10 = df.nlargest(10, 'score').sort_values('score', ascending=True)
    short_titles = top_10['title'].apply(lambda x: x[:47] + "..." if len(x) > 50 else x)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(short_titles, top_10['score'], color='skyblue')
    ax.set_title('Top 10 Trending Stories by Score')
    ax.set_xlabel('Score (Upvotes)')
    ax.set_ylabel('Story Title')
    plt.tight_layout()
    plt.savefig('outputs/chart1_top_stories.png')
    plt.clf()

    # Count categories and sort descending
    category_counts = df['category'].value_counts()
    
    # Define a list of colors for the bars
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#C2C2F0']

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
    ax.set_title('Number of Stories per Category')
    ax.set_xlabel('Category')
    ax.set_ylabel('Number of Stories')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/chart2_categories.png')
    plt.clf()

    fig, ax = plt.subplots(figsize=(8, 6))
    
    popular = df[df['is_popular'] == True]
    not_popular = df[df['is_popular'] == False]

    ax.scatter(popular['score'], popular['num_comments'], color='gold', label='Popular (Above Avg)', alpha=0.7)
    ax.scatter(not_popular['score'], not_popular['num_comments'], color='grey', label='Standard', alpha=0.5)

    ax.set_title('Score vs Number of Comments')
    ax.set_xlabel('Score')
    ax.set_ylabel('Number of Comments')
    ax.legend()
    plt.tight_layout()
    plt.savefig('outputs/chart3_scatter.png')
    plt.clf()

    # Using a 2x2 grid. We will leave the bottom-right space empty.
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('TrendPulse Dashboard', fontsize=20, fontweight='bold')

    # Top-Left: Top 10 Stories
    axes[0, 0].barh(short_titles, top_10['score'], color='skyblue')
    axes[0, 0].set_title('Top 10 Trending Stories')
    axes[0, 0].set_xlabel('Score')

    # Top-Right: Categories
    axes[0, 1].bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
    axes[0, 1].set_title('Stories per Category')
    axes[0, 1].set_ylabel('Count')
    axes[0, 1].tick_params(axis='x', rotation=45)

    # Bottom-Left: Scatter Plot
    axes[1, 0].scatter(popular['score'], popular['num_comments'], color='gold', label='Popular', alpha=0.7)
    axes[1, 0].scatter(not_popular['score'], not_popular['num_comments'], color='grey', label='Standard', alpha=0.5)
    axes[1, 0].set_title('Score vs Comments')
    axes[1, 0].set_xlabel('Score')
    axes[1, 0].set_ylabel('Comments')
    axes[1, 0].legend()

    # Bottom-Right: Hide the 4th empty plot completely
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig('outputs/dashboard.png')
    plt.close('all')

    print("All charts generated successfully! Check the 'outputs/' folder.")

if __name__ == "__main__":
    create_visualizations()