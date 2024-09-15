## Table of Contents
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [1. Data Collection and Preparation](#data-collection-and-preparation)
  - [2. Embedding and Recommendation Generation](#embedding-and-recommendation-generation)
- [Notes](#notes)
- [Acknowledgements](#acknowledgements)

## Project Structure

- **YouTube_analytics.py**: This script interacts with the YouTube Data API to fetch video analytics data. It retrieves various metrics like views, likes, comments, estimated minutes watched, subscribers gained, and subscribers lost, and stores this data in a CSV file.
- **generate_embeddings.py**: Processes the collected YouTube video data to generate embeddings using OpenAI's `text-embedding-ada-002` model. These embeddings capture the semantic meaning of the video content and performance.
- **process_embeddings.py**: Uses the precomputed embeddings to answer analytical questions and generate video recommendations. It employs OpenAI's GPT models to analyze the embeddings and provide insightful suggestions.
- **CSV Files**:  
  - **youtube_video_statistics_with_titles.csv**: Stores the fetched YouTube video statistics, including views, likes, comments, and other engagement metrics.
  - **youtube_video_statistics_embeddings.csv**: Contains the generated embeddings for each video entry, which are used to facilitate recommendations and analytics.

## How It Works

### Data Collection and Preparation
- **Data Collection:**  
  The system collects video analytics data using the YouTube Data API. The metrics include views, likes, comments, estimated minutes watched, subscribers gained, and subscribers lost.
- **Fetching and Storing Data:**  
  The `YouTube_analytics.py` script fetches this data from your YouTube channel and saves it into a CSV file (e.g., `youtube_video_statistics_with_titles.csv`). This data serves as the input for further processing and analysis.

### Embedding and Recommendation Generation
- **Generating Embeddings:**  
  The `generate_embeddings.py` script processes the collected video data using OpenAI's `text-embedding-ada-002` model to generate embeddings. These embeddings capture the semantic information related to each video's content and performance.
- **Processing and Recommendations:**  
  The `process_embeddings.py` script utilizes the precomputed embeddings to answer analytical questions about your videos and generate recommendations. It uses OpenAI's GPT models (such as `gpt-3.5-turbo`) to analyze the embeddings and provide suggestions for new video ideas tailored to your audience's preferences and engagement patterns.

## Notes

- **API Keys:**  
  Ensure you have your OpenAI API key and YouTube Data API key properly set up. The OpenAI API key should be set as an environment variable, while the YouTube Data API credentials should be stored securely in the `token.json` file. Do not share your API keys publicly or include them in your code.

- **Security Considerations:**  
  The `token.json` file contains sensitive information and is excluded from the repository for security reasons. Make sure to use a `.gitignore` file to prevent sensitive files from being tracked by Git. Always handle API keys and tokens with care to avoid security risks.

- **Environment Variables:**  
  Use environment variables to store sensitive information like API keys. For example, set your OpenAI API key using the following command:
  ```bash
  export OPENAI_API_KEY='your-openai-api-key'   # On Windows, use `set` instead of `export`
  ```

## Acknowledgements

- **[OpenAI](https://openai.com):**  
  For providing the powerful AI models used in this project, including `text-embedding-ada-002` and `gpt-3.5-turbo`. These models enable the analysis and recommendation generation based on YouTube video analytics data.

- **[YouTube Data API](https://developers.google.com/youtube/v3):**  
  For offering access to comprehensive analytics data for YouTube channels. This API allows the project to fetch and analyze video performance metrics crucial for generating content recommendations.

- **[Pandas](https://pandas.pydata.org):**  
  For being an essential library in data manipulation and analysis. Pandas was used to handle and process the YouTube video analytics data efficiently.

- **[NumPy](https://numpy.org):**  
  For providing support with numerical computations and array handling, which are fundamental in processing embeddings and calculating distances.

- **[SciPy](https://scipy.org):**  
  For offering functions to compute the cosine distance between embeddings, which helps in determining video similarity and recommendations.

- **[tiktoken](https://github.com/openai/tiktoken):**  
  For tokenizing prompts to ensure they fit within the token limits required by OpenAI models, ensuring smooth communication with the API.



