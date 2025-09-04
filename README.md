# AI-data-navigator

This repository contains a Streamlit-based application developed as part of a coding challenge. The app allows users to upload CSV or Excel files, analyze data, ask questions using AI, and provide feedback on the responses.

## Features
- **File Upload**: Upload one or more CSV/XLS files (e.g., the Titanic dataset for testing).
- **Top N Rows Display**: View the top N rows of any uploaded sheet, where N is user-defined.
- **AI-Powered Questions**: Ask questions or provide prompts to get answers from the uploaded CSV/Excel files.
- **Prompt History**: Maintain a history of prompts for reuse.
- **Feedback System**: Users can provide feedback on whether answers are useful or not, with a summary of feedback statistics.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation
1. Clone the repository
2. Create a virtual environment (optional but recommended)
3. Install the required dependencies


### Running the App
1. Ensure you have a temporary OpenAI API key (provided separately for the challenge).
2. Run the app
3. Open your browser and go to `http://localhost:8501`.
4. Enter the OpenAI API key when prompted in the app interface.

### Usage
- **Upload Files**: Use the file uploader to add CSV or Excel files.
- **View Data**: Select a file and enter a number (N) to display the top N rows.
- **Ask Questions**: Select a file, enter a prompt (e.g., "What is the survival rate?"), and click "Get Answer".
- **Review History**: Check the "Prompt History" section for past questions and answers.
- **Provide Feedback**: Use "👍 Useful" or "👎 Not Useful" buttons to rate answers, and view the "Feedback Summary".

## Future Improvements
- Add support for multiple sheets in Excel files.
- Implement environment variable configuration for the API key.
- Enhance the UI with additional visualizations for data analysis.

## License
This project is for challenge purposes only and does not include a formal license.
