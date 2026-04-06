# TrendPulse: HackerNews Data Pipeline

This repository contains a complete, 4-step automated data pipeline that extracts, cleans, analyzes, and visualizes trending stories from the HackerNews API. 

This project was built as a mini-project for an AI and Data Science Masai course.

## 📂 Project Structure

The pipeline is split into four modular Python scripts, designed to be run in sequence:

### 1. `task1_data_collection.py`
**Goal:** Fetch and categorize live data from a public API.
* Connects to the open HackerNews API using the `requests` library.
* Fetches the top 500 trending stories and categorizes them (Technology, World News, Sports, Science, Entertainment) based on title keywords.
* Implements robust error handling and uses a `requests.Session()` to maintain connection stability.
* Implements rate-limiting (`time.sleep(2)`) between categories.
* **Output:** Saves the raw, scraped data into the `data/` folder as a JSON file (e.g., `trends_YYYYMMDD.json`).

### 2. `task2_data_processing.py`
**Goal:** Clean and format raw JSON data.
* Loads the raw JSON data into a `pandas` DataFrame.
* Performs critical data cleaning: removes duplicate `post_id`s, drops rows with missing critical data, and enforces correct data types (integers for scores and comments).
* Filters out low-quality data (stories with a score of less than 5) and strips whitespace from text columns.
* **Output:** Exports the cleaned, structured data as `data/trends_clean.csv`.

### 3. `task3_analysis.py`
**Goal:** Perform statistical analysis and feature engineering.
* Loads the clean CSV and utilizes explicit `numpy` functions to calculate descriptive statistics (mean, median, standard deviation, min, max) of story scores.
* Identifies trends, such as the most commented story and the highest-performing category.
* Engineers two new features: 
  * `engagement`: A calculated metric of comments per upvote.
  * `is_popular`: A boolean flag for stories performing above the overall average score.
* **Output:** Saves the enriched dataset as `data/trends_analysed.csv`.

### 4. `task4_visualization.py`
**Goal:** Generate visual insights from the analyzed data.
* Uses `matplotlib` to generate insightful charts based on the final dataset.
* Creates a horizontal bar chart of the Top 10 stories by score.
* Creates a bar chart showing the distribution of stories across categories.
* Creates a scatter plot comparing Scores vs. Comments, color-coded by popularity.
* Combines all individual charts into a single, comprehensive `dashboard.png`.
* **Output:** Saves all `.png` visual assets into the `outputs/` folder.

## 🧠 Lessons Learned & Challenges Overcome

During the development of this pipeline, I encountered and solved a few real-world engineering challenges:

* **Handling Silent Execution (Developer UX):** Initially, the data collection script appeared "stuck" or frozen because it was silently making hundreds of API calls in the background. I learned how to use `end="\r"` and `flush=True` in Python's `print()` function to create a live, in-place progress indicator. This provided real-time feedback without flooding the terminal console.
* **Connection Pooling for API Limits (SSLEOFError):** When making 500 rapid, sequential HTTP requests, the HackerNews server occasionally dropped the connection, resulting in an `SSLEOFError`. I discovered that standard `requests.get()` opens a brand-new secure connection for every single loop. By upgrading the script to use a `requests.Session()`, I was able to pool and reuse a single connection. This not only prevented the server-side disconnects but also made the script run significantly faster.

trendpulse-project/
│
├── task1_data_collection.py
├── task2_data_processing.py
├── task3_analysis.py
├── task4_visualization.py
├── README.md
│
├── data/
│   ├── trends_20240115.json      # Raw data
│   ├── trends_clean.csv          # Cleaned data
│   └── trends_analysed.csv       # Data with new features
│
└── outputs/
    ├── chart1_top_stories.png
    ├── chart2_categories.png
    ├── chart3_scatter.png
    └── dashboard.png             # Combined visualization