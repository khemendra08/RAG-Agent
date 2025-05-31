#!/usr/bin/env python
import os
import sys
import subprocess
from dotenv import load_dotenv

# Explicitly load environment variables from .env file
load_dotenv(override=True)

# Print the loaded API key (masked for security)
api_key = os.environ.get('OPENAI_API_KEY', '')
masked_key = api_key[:7] + '*' * (len(api_key) - 11) + api_key[-4:] if api_key else ''
print(f"Using OpenAI API Key: {masked_key}")

# Run the test command with the loaded environment variables
cmd = ['crewai', 'test', '-n', '5', '-m', 'gpt-4o-mini']
result = subprocess.run(cmd, env=os.environ)

# Exit with the same code as the subprocess
sys.exit(result.returncode)
