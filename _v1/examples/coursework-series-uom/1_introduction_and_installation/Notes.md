## How ML/AI Development happens now?
- Data Scientists and ML Engineers work on Jupyter Notebooks, Python, Pytorch, Tensorflow, etc.
- Data Engineers work on Spark, Hadoop, etc.
- Data Analysts work on SQL, Tableau, etc.
- Backend Engineers work on Django, Flask, FastAPI, etc.
- Storage Engineers work on Cassandra, MongoDB, Redis, etc.
- DevOps/MLOps Engineers work on Kubernetes, Docker, etc.

From a company standpoint this is a huge problem, because it means that the company has to hire a lot of different people with different skillsets, and it's hard to find people with all of these skills. It also means that the company has to maintain a lot of different systems, which is expensive and time consuming.

and from developer standpoint, it means that you have to learn a lot of different things, and it's hard to keep up with all of these things.

## What is the Solution?
We need a single platform/framework that can do all of these things. Such that a single person can do all of these things. Such that a single company can do all of these things.

## Jaseci
Jaseci provides a new high level abstraction for creating sophisticated AI applications in micro-service/serverless environments. and its full-stack architecture and programming model enables developers to build, deploy, and manage AI applications with ease.

## What jaseci provides?
- Bleeding edge AI ready for use. No need to learn new frameworks. No prior ML knowledge required.
- Rapid backend development. requires zero backend development knowledge.
- Automatic API generation. No need to write API endpoints.
- Automatic Scaling. No need to worry about scaling or need devops knowledge.

## Language Level Abstraction
- Graph - A graph is a collection of nodes and edges. Nodes represent data and edges represent the relationship between the data.
- Node - A node is a collection of data. Nodes can be connected to other nodes using edges.
- Edge - An edge is a relationship between two nodes. Edges can be uni-directional or bi-directional.
- Walker - Walkers are used to traverse graphs.
- Abilities - functions that can be applied to nodes.
- Actions - External actions that can be used in walkers to perform certain tasks. Mainly AI related tasks.

## Setup and Installation
Pre-requisites:
- Python 3.6+ (3.9 recommended)
- Conda (optional) - https://docs.conda.io/en/latest/miniconda.html
- Docker, Kubernetes, or AWS Lambda (optional)

### Installation
```bash
pip install jaseci jaseci-serv
```
### Testing
```bash
jsctl -m
```

That's it! You're ready to go!

## Interfacing with Jaseci
Jaseci can be interfaced with in 3 ways:
- Local CLI - JSCTL
- Remote CLI - JSCTL
- JSSERV - Jaseci Server

## Running a Chatbot Example 0
Installing the Universal Sentence Encoder QA module for jaseci
```bash
pip install jac_nlp[use_qa]
```
Running a Jaseci Session in memory
```bash
jsctl -m
```
Loading the Universal Sentence Encoder QA module
```bash
actions load module jac_nlp.use_qa
```
Running the Chatbot Example
```bash
jac run main.jac
```

## Running a Chatbot Example 1
Installing the Biencoder
```bash
pip install jac_nlp[bi_enc]
```
Running a Jaseci Session in memory
```bash
jsctl -m
```
Loading the Biencoder module
```bash
actions load module jac_nlp.bi_enc
```
Train the Biencoder model with the training data
```bash
jac run bi_enc.jac -walk train -ctx '{"train_file": "training_data.json"}'
```
Try Inferecing with the trained Biencoder model
```bash
jac run bi_enc.jac -walk infer -ctx '{"labels": ["test_drive", "order a tesla"]}'
```
```bash
jaseci > jac run bi_enc.jac -walk infer -ctx "{\"labels\": [\"test drive\", \"order a tesla\"]}"
Enter input text (Ctrl-C to exit)> i want to order a tesla
{"label": "order a tesla", "score": 9.812651595405981}
Enter input text (Ctrl-C to exit)> i want to test drive
{"label": "test drive", "score": 6.931458692617463}
Enter input text (Ctrl-C to exit)>
```
Save the model
```bash
jac run bi_enc.jac -walk save_model -ctx '{"model_path": "dialogue_intent_model"}'
```
Load the model
```bash
jac run bi_enc.jac -walk load_model -ctx '{"model_path": "dialogue_intent_model"}'
```
Running the Chatbot Example
```bash
jac run main.jac
```

## Assignments
1. Go through the [Jaseci Documentation](docs.jaseci.org) and try to understand the concepts.
2. Build a simple chatbot using the Tfm_ner (Transformer based Named Entity Recognition) module. You can use the [Jaseci Documentation](docs.jaseci.org) to help you.
3. Add your own sass to the chatbot. Experiment with different things.
4. Present your chatbot to the class.