# X-Automation

A bot that automatically fetches Weibo posts, translates them using GPT-4, and posts them to X (Twitter).

# Local Development Setup
## Create and activate virtual environment
- `python3 -m venv .venv`
- `source .venv/bin/activate`

## Install dependencies
- `pip install -r requirements.txt`

## Environment Variables
Create a `.env` file in the root directory with the following variables:
```
# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# X (Twitter) API
X_API_KEY=your_x_api_key
X_API_KEY_SECRET=your_x_api_key_secret
X_ACCESS_TOKEN=your_x_access_token
X_ACCESS_TOKEN_SECRET=your_x_access_token_secret
X_BEARER_TOKEN=your_x_bearer_token
X_CLIENT_ID=your_x_client_id
X_CLIENT_SECRET=your_x_client_secret
```

## Run the script locally
- `python main.py`

# GitHub Actions Setup
The repository is configured to run the script automatically using GitHub Actions.

## Directory Structure
- `data/posts_tweeted.json` - Tracks all posted tweets
- `.github/workflows/scheduled-run.yml` - GitHub Actions workflow configuration

## Setting up GitHub Actions
1. Push your code to GitHub repository

2. Add Repository Secrets
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add the following secrets:
     ```
     OPENAI_API_KEY
     X_API_KEY
     X_API_KEY_SECRET
     X_ACCESS_TOKEN
     X_ACCESS_TOKEN_SECRET
     X_BEARER_TOKEN
     X_CLIENT_ID
     X_CLIENT_SECRET
     ```

3. Schedule Configuration
   - The bot runs every 4 hours by default
   - You can modify the schedule in `.github/workflows/scheduled-run.yml`:
     ```yaml
     on:
       schedule:
         - cron: '0 */4 * * *'  # Every 4 hours
     ```
   - Common cron patterns:
     - Every 8 hours: `0 */8 * * *`
     - Three times a day: `0 8,16,24 * * *`
     - Twice a day: `0 0,12 * * *`

4. Manual Trigger
   - You can manually trigger the workflow:
     - Go to Actions tab
     - Select "Scheduled Twitter Bot"
     - Click "Run workflow"

## Monitoring
- Check the Actions tab in your repository for run history and logs
- Each run will show:
  - Setup steps
  - Dependencies installation
  - Script execution
  - Any errors or output

## Data Tracking
- All posted tweets are tracked in `data/posts_tweeted.json`
- The file is automatically updated and committed after each successful run
- Changes can be monitored through git history