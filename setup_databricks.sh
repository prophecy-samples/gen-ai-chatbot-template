#!/bin/bash

# Check if databricks-cli is installed
if ! command -v databricks &> /dev/null
then
    echo "databricks-cli could not be found"
    echo "Please install databricks-cli using the following command:"
    echo "pip install databricks-cli"
    exit
fi

# Sets variables
PROFILE=${1:-DEFAULT}
CATALOG=${2:-gen_ai}

# Loads the .env file
unamestr=$(uname)
if [ "$unamestr" = 'Linux' ]; then
  export $(grep -v '^#' .env | xargs -d '\n')
elif [ "$unamestr" = 'FreeBSD' ] || [ "$unamestr" = 'Darwin' ]; then
  export $(grep -v '^#' .env | xargs -0)
fi

# Create a default catalog
databricks --profile "$PROFILE" unity-catalog catalogs create --name "$CATALOG"

# Create schemas for the catalog
databricks --profile "$PROFILE" unity-catalog schemas create --catalog-name "$CATALOG" --name web_bronze
databricks --profile "$PROFILE" unity-catalog schemas create --catalog-name "$CATALOG" --name web_silver
databricks --profile "$PROFILE" unity-catalog schemas create --catalog-name "$CATALOG" --name operational

# Setup secrets for Slack
databricks --profile "$PROFILE" secrets create-scope --scope slack
databricks --profile "$PROFILE" secrets put --scope slack --key token --string-value "$SLACK_TOKEN"
databricks --profile "$PROFILE" secrets put --scope slack --key app_token --string-value "$SLACK_APP_TOKEN"

# Setup secrets for Open-AI
databricks --profile "$PROFILE" secrets create-scope --scope open_ai
databricks --profile "$PROFILE" secrets put --scope open_ai --key api_key --string-value "$OPEN_AI_API_KEY"

# Setup secrets for Pinecone
databricks --profile "$PROFILE" secrets create-scope --scope pinecone
databricks --profile "$PROFILE" secrets put --scope pinecone --key token --string-value "$PINECONE_TOKEN"
