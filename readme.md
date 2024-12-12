# Contoso Gaming Sample Audio

A sample application utilizing the cutting-edge GPT-4o-audio-preview API. This application showcases the following capabilities:
- **Interactive AI Assistant**: Engage with the AI Assistant using your microphone for input, and receive responses played out as audio.
- **Seamless Audio Processing**: The GPT-4o-audio-preview API handles both audio input and output, eliminating the need for separate Speech-to-Text (STT) and Text-to-Speech (TTS) services.
- **Dynamic Tool Integration**: Automatically translate user requests into database queries, Jira API calls, or AI Search operations based on the detected intent.

To see a demo of this in action, check out our [YouTube video](https://youtu.be/2skyRF-_ZD0).

<img width="485" alt="image" src="https://github.com/user-attachments/assets/80c96e24-80c4-4eea-b7f7-13bd040c1c18" />


**Note The demo is based on OpenAI's GPT-4o audio-preview API, and not using the equivalent on Azure OpenAI. It is not available in Azure as of this writing**

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)


## Introduction
Welcome to the Contoso Gaming Sample Audio application. This project showcases the capabilities of the GPT-4o-audio-preview API by providing an AI Assistant that helps customers with their queries and grievances related to gaming services.

## Features
- AI Assistant for customer support
- Audio input and output for user interaction
- Integration with OpenAI and Azure AI Search
- Jira integration for grievance registration
- Real-time game status summary retrieval

## Installation
To get started with this project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/contoso-gaming-sample-audio.git
    cd contoso-gaming-sample-audio
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables by creating a [.env](http://_vscodecontentref_/1) file in the root directory and adding the following:
    ```env
    api_key=your_openai_api_key
    model=your_openai_model
    attlassian_api_key=your_attlassian_api_key
    attlassian_user_name=your_attlassian_user_name
    attlassian_url=your_attlassian_url
    grievance_project_key=your_grievance_project_key
    grievance_type=your_grievance_type
    grievance_project_name=your_grievance_project_name
    ai_search_url=your_ai_search_url
    ai_search_key=your_ai_search_key
    ai_index_name=your_ai_index_name
    ai_semantic_config=your_ai_semantic_config
    ai_assistant_organization_name=your_ai_assistant_organization_name
    ```

## Usage
To run the application, use the following command:
```sh
streamlit run bot-app.py


This will start the Streamlit application, and you can interact with the AI Assistant through the web interface.

Configuration
The configuration for the application is managed through environment variables defined in the .env file. The config.py file loads these variables and makes them available to the application.

Project Structure

contoso-gaming-sample-audio/
├── __pycache__/
├── data/
│   ├── jira-account.txt
│   ├── qna_manual/
│   │   ├── FAQ - Part1.txt
│   │   ├── FAQ - Part2.txt
│   │   ├── FAQ - Part3.txt
│   │   ├── FAQ - Part4.txt
│   └── script.sql
├── .env
├── .gitignore
├── bot-app.py
├── config.py
├── readme.md
├── requirements.txt
├── tools.py
└── tools_st.py


bot-app.py: Main application file that runs the Streamlit app.
config.py: Configuration file that loads environment variables.
tools.py: Contains the ConnectionManager class and various utility functions.
tools_st.py: An alternative to tools.py file, with static responses to the function calls. Use this if you do not want to worry about integrating with Jira, sql database, AI Search. You will need to make minor changes in bot-app.py to use this class
data: Directory containing data files and manuals. Use this if you want to recreate the same content as in the Youtube video above, to run the sample.
requirements.txt: List of dependencies required for the project.
.env: Environment variables file (not included in the repository for security reasons).
