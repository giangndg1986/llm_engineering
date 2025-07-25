"""
Project: Web Content Summarizer using Ollama's llama3.2 model
- Developed a Python tool to extract and summarize website content using Ollama's llama3.2 model and BeautifulSoup.
- Implemented secure API integration and HTTP requests with custom headers to mimic browser behavior.
"""

import os
import requests
from bs4 import BeautifulSoup
import ollama

# Constants

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

# Define the Website class to fetch and parse website content
class Website:
    def __init__(self, url):
        """
        Initialize a Website object by fetching and parsing the given URL.
        Uses BeautifulSoup to extract the title and text content of the page.
        """
        self.url = url
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title of the website
        self.title = soup.title.string if soup.title else "No title found"
        
        # Remove irrelevant elements like scripts, styles, images, and inputs
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        
        # Extract the main text content of the website
        self.text = soup.body.get_text(separator="\n", strip=True)

# Define the system prompt for the OpenAI model
system_prompt = (
    "You are an assistant that analyzes the contents of a website "
    "and provides a short summary, ignoring text that might be navigation related. "
    "Respond in markdown."
)

# Function to generate the user prompt based on the website content
def user_prompt_for(website):
    """
    Generate a user prompt for the llama3.2 model based on the website's title and content.
    """
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; summarize these.\n\n"
    user_prompt += website.text
    return user_prompt

# Function to create the messages list for the OpenAI API
def messages_for(website):
    """
    Create a list of messages for the ollama, including the system and user prompts.
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# Function to summarize the content of a given URL
def summarize(url):
    """
    Summarize the content of the given URL using the OpenAI API.
    """
    # Create a Website object to fetch and parse the URL
    website = Website(url)
    
    # Call the llama3.2 using ollama with the generated messages
    response = ollama.chat(
        model= MODEL,
        messages=messages_for(website)
    )
    
    # Return the summary generated by ollama
    print(response.message.content)

# Example usage: Summarize the content of a specific URL
summarize("https://sruthianem.com")