Engineering Knowledge AI Agent Test

1.Describe differences between REST API, MCP in the context of AI.
    Answer : 
    REST API is the way a service exposes its functionality to other service through HTTP. Usually support methods such as GET, POST, PUT, PATCH, and DELETE to interact with the service.
    MCP is a standarized way so that an AI application can discover and call tools which is exposed to them. Which can be in form of REST API endpoints.

2. How REST API, MCP, can improve the AI use case
    Answer : 
    REST API enables AI use case to be more diverse by allowing them to interact with external systems. While MCP provides AI application a standarized way so it can discover and invoke the tools which can be a REST API. 
    Without having REST API and MCP, An AI application capabilites is limited to the training data of the LLM.
    When an AI application is connected to a MCP it have much more capabilites. It can do live data verification by calling the tool to browse through the internet or invoke other tools for example writting to docs, make a gsheet and much more. This is also meant that we dont need to manually make a custom AI application connector to each tool, we can just reuse the already available MCP tools. 

3. How do you ensure that your AI agent answers correctly?
    Answer : 
    By building a evaluation system. If I were to break it down step by steps it would be something like this : 
        1. Make a golden dataset for the test case, with some example of prompt that this agent supposed to handle and the expected answer and what defines a correct answer. For example if an agent supposed to handle a task that calls a specific tool, then we will need to check if the agent actually calls the correct tool.
        2. Then run the AI agent everytime before every release via CI against the dataset. If the evaluation pass a certain threshold then the release can be made, vice versa. 
        3. Prod monitoring and reiteration based on failed real cases. If we can find some failure in the prod, we can just reiterate the AI agent to cover that cases better, and to ensure the answer will be correct this time, we will be adding the cases to the test dataset too.

4. Describe what can you do with Docker / Containerize environment in the context of AI
    Answer : 
    By using Docker we can package an AI application with the dependencies into a container, so it can run consistently across different environment. This will minimize dependencies mismatch issue, so what I have tested in my local supposedly will behave the same in stg or prod or even someone else local.

5. How do you finetune the LLM model from raw ?
    Answer :
    Here I will assume that finetune LLM model from raw means fine tuning an existing LLM / pretrained model for our specific task or use case.

    First we will need to make a dataset for the LLM on the specific task that we want to do. Like some relevant example and what the expected behaviour / response of the LLM model. Then we can tokenize the example and fit in the dataset into the model. After the model retraining is completed, we can do a evaluation by comparing the non-tuned version of the LLM vs the tuned version against a evaluation set. If the result have satisfied the requirements, we can save the weights then redeploy the LLM model. 


Coding Test Result Video Recording can be found here : 
https://drive.google.com/drive/folders/1qy78-eaydBq2lIrep1YPYfKyvtXW_DjQ?usp=sharing