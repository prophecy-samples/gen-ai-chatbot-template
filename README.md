# Generative-AI Chatbot

This project showcases how easy it is to ingest unstructured data from your applications, pre-process & vectorize it and store it within your vector database of choice. Based on those vectors, it builds a live chatbot application on Slack or Teams (coming soon).

Here's a quick video showcasing the result: [Demo here](https://www.loom.com/share/a89ee52de80e41abb9b5647c1da73e18?sid=6fcf0298-79e8-412b-8e48-f58c9d6d7f3b). 

<br>

![High-level Graphic](docs/images/training-inference-high-level-graphic.png)

<br>

## Requirements 

### External dependencies

Optional, but recommended for best results:

1. [**Pinecone**](https://www.pinecone.io/) - allows for efficient storage and retrieval of vectors. To simplify, it's possible to alternatively use Spark-ML cosine similarity - however, since that doesn't feature KNNs for more efficient lookup, it's only recommended for small datasets.
2. [**OpenAI**](https://openai.com/) - for creating text embeddings and formulating questions. Alternatively, one can use Spark's [word2vec](https://spark.apache.org/docs/2.2.0/mllib-feature-extraction.html#word2vec) for word embeddings and an [alternative LLM (e.g. Dolly)](https://github.com/prophecy-io/spark-ai/tree/main) for answer formulation based on context.
3. [**Slack**](https://slack.com/) or [**Teams**](https://teams.com/) (support coming soon) - for the chatbot interface. An example batch pipeline is present for fast debugging when that's not available.   

### Cluster dependencies

Required:

1. [**Spark-AI**](https://github.com/prophecy-io/spark-ai/tree/main) - Toolbox for building Generative AI applications on top of Apache Spark.

### Platform recommendations:

Below is a platform recommendation. The template is entirely code-based and runs on open-source projects like Spark. 

1. [**Prophecy Low-Code**](https://www.prophecy.io/) (version 3.1 and above) - for building the data pipelines. Free account is available.
2. [**Databricks**](https://databricks.com/) (DBR 12.2 ML and above) - for running the data pipelines. Free community edition is available or Prophecy provides Databricks' free trial. 

<br>

## Getting started

### 1. Dependencies setup

Ensure that above dependencies are satisfied. Create appropriate accounts on the services you want to use above and install required dependencies on your Spark cluster.

1. **Slack** - [quick video here](https://www.loom.com/share/2d7afeacd92e44809ab29b43665329dd?sid=c4e08d9d-bf86-4a6f-9e9d-fce9d7a12578) 

   1. [Setup Slack application](https://api.slack.com/reference/manifests#creating_apps) using the manifest file in [apps/slack/manifest.yml](apps/slack/manifest.yaml).
   2. Generate App-Level Token with `connections:write` permission. This token is going to be used for receiving messages from Slack.
   3. Find the Bot User OAuth Token. This token is going to be used for sending messages to Slack.<br><br>

### 2. Load the repository 

Fork this repository to your personal GitHub account. Afterwards, create new project in Prophecy pointing to the forked repository 

[gif here]

### 3. Setup credentials

Configure the credentials to your Pinecone, OpenAI, Slack and/or Teams accounts on Databricks secrets. 

 ```bash
 # Execute below commands one by one
 # Setup the scope credentials for Slack connection 
 databricks secrets create-scope --scope slack
 # The App-Level goes here
 databricks secrets put --scope slack --key app_token
 # The Bot user OAuth token goes here
 databricks secrets put --scope slack --key token

 # Setup the scope credentials for Pinecone connection
 databricks secrets create-scope --scope pinecone
 databricks secrets put --scope pincone --key api_key
 
 # Setup the scope credentials for OpenAI connection
 databricks secrets create-scope --scope openai
 databricks secrets put --scope openai --key token
 ```

### 4. Setup databases

This project runs on Databrick's Unity Catalog by default. However, you can also reconfigure Source & Target gems to use alternative sources.

For Databricks Unity Catalog, create the following catalog: `prophecy_data` and the following databases are required: `web_bronze`, `web_silver`. The tables are going to be created automatically on the first boot-up. 

### 5. Run your pipelines
   
1. Run the ingestion (web scraping) pipeline.
   <br><br>

2. Run the vectorization pipeline.
   <br><br>

3. Run the streaming inference pipeline. 
   <br><br>




