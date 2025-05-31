# PDF RAG Agent - Streamlit UI

## Overview

This Streamlit UI provides a user-friendly interface for the PDF RAG Agent project. It allows you to upload PDF documents, search for information within them, and retrieve relevant content from both the document and the web.

## Features

- **PDF Upload**: Upload any PDF document for analysis
- **Search Functionality**: Enter search queries to find relevant information
- **Web Integration**: Combines document search with web search for comprehensive results
- **Search History**: Keeps track of your previous searches for easy reference
- **Result Export**: Download results in Markdown or HTML format
- **Model Selection**: Choose between different OpenAI models for your searches

## Getting Started

### Prerequisites

Make sure you have all the required dependencies installed:

```bash
pip install -r requirements.txt
pip install streamlit PyPDF2 markdown
```

### Running the Application

To start the Streamlit application, run the following command in your terminal:

```bash
streamlit run app.py
```

This will launch the application in your default web browser.

## Using the Application

1. **Configure API Key**: Enter your OpenAI API key in the sidebar
2. **Upload a PDF**: Use the file uploader to select a PDF document
3. **Enter a Query**: Type your search topic in the search box
4. **Run the Search**: Click the "Run Search" button to start the process
5. **View Results**: Results will appear in the right panel
6. **Export Results**: Download results in your preferred format

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits
- **PDF Upload Errors**: Make sure your PDF is not corrupted and is readable
- **Search Failures**: Try simplifying your search query if you encounter errors

## Additional Information

This Streamlit UI is built on top of the CrewAI framework and uses the PDF RAG Agent to process documents and search queries. The application leverages OpenAI's models to generate comprehensive responses based on the content of your documents and relevant web information.

## Customization

You can customize the application by modifying the `app.py` file. Some potential customizations include:

- Changing the default model
- Adjusting the number of search iterations
- Modifying the UI layout and styling
- Adding additional export formats

---

Created with ❤️ using Streamlit and CrewAI
