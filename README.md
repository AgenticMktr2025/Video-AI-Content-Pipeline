# Video AI Content Pipeline

A Reflex-based application for automated video content processing and distribution.

## Features

- Video recording and cloud storage
- Automated transcription and topic extraction
- Long-form content generation from video transcripts
- Social media snippet creation
- Human-in-the-loop review workflow
- Multi-platform publishing integration

## Setup

1. Install dependencies:
bash
pip install -r requirements.txt


2. Set up environment variables:
bash
OPENAI_API_KEY=your_openai_key
GITHUB_TOKEN=your_github_token


3. Run the application:
bash
reflex run


## Tech Stack

- **Framework**: Reflex (Python web framework)
- **AI/ML**: OpenAI API for transcription and content generation
- **Version Control**: GitHub integration via PyGithub
- **Styling**: Tailwind CSS

## Project Structure


app/
  ├── __init__.py
  ├── app.py          # Main application file
assets/
  ├── favicon.ico
  ├── placeholder.svg
requirements.txt      # Python dependencies
rxconfig.py          # Reflex configuration


## Development

This project was built with Reflex Build. For more information on Reflex, visit:
https://reflex.dev/docs/

## License

MIT License
