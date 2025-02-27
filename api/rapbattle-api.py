from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import  SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import  TextMentionTermination

app = FastAPI()

def get_list_of_words() -> str:
    words = "apple, banana, cherry, date, elderberry, Christmas"
    return words

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/process-prompt/")
async def process_prompt(request: PromptRequest):
    prompt = request.prompt

    eminem_agent = AssistantAgent(
        name="eminem_agent",
        description="An agent that can rap using the style of Eminem",
        system_message="You are a rapper, and you rap in the style of Eminem. You are participating in a rap battle. You will be given a topic, and you will need to create the lyrics and rap about it, using all the words that the Rap_MC_Agent will share with you.",
        model_client=model_client
    )

    drake_agent = AssistantAgent(
        name="drake_agent",
        description="An agent that can rap using the style of Drake",
        system_message="You are a rapper, and you rap in the style of Drake. You are participating in a rap battle. You will be given a topic, and you will need to create the lyrics and rap about it, using all the words that the MC_Agent will share with you.",
        model_client=model_client
    )

    mc_agent = AssistantAgent(
        name="mc_agent",
        description="An agent that acts as an MC in a rap battle",
        system_message="You are a rap MC and your role is run a rap battle with two contestants, Eminem and Drake. The user will provide you the topic for the battle. Your main task is to be the master of ceremony and introduce the rap battle. You must share some words of encouragement and describe the topic for the battle that was given by the user. YOU MUST USE THE TOPIC GIVEN BY THE USER, you can't make up one on your own. You have access to a skill that gives you a list of words for rap lyrics. YOU MUST USE this skill to get a list of words. First, you're going to introduce the rap battle and then YOU MUST SHARE the list of words with the contenstants. The contestants will need to create lyrics for the given topic and they must use all the words in the list you have shared.",
        model_client=model_client,
        tools=[get_list_of_words]
    )
    
    judge_agent = AssistantAgent(
        name="judge_agent",
        description="An agent that acts as a judge in a rap battle",
        system_message="You are a judge in a rap battle. You will be given the lyrics of the rap battle and you must give a score to each contestant. You must give a score between 1 and 10 to each contestant. The rapper who gets the highest score wins. \\n You must ensure that the final score is given after all the other contestants have shared their lyrics. On top of the score, you need also to provide an explanation on why you assinged that score. YOUR FINAL RESPONSE MUST BE THE SCORE AND THE WINNER DECLARATION. When the plan is complete and the winner has been declared, you can respond with TERMINATE.",
        model_client=model_client
    )

    text_termination = TextMentionTermination("TERMINATE")

    # Define a team with a single agent and maximum auto-gen turns of 1.
    agent_team = SelectorGroupChat(
        participants=[mc_agent, eminem_agent, drake_agent, judge_agent], 
        max_turns=10, 
        termination_condition=text_termination,
        model_client=model_client,
        selector_prompt="""
            You are managing a dynamic, interactive rap battle with multiple AI agents. You must select an agent to perform the task:

            {roles}

            The workflow is the following one:

            - The rapmc_agent begins the battle by introducing th event, setting the topic, and providing a list of words that the rappers must use.
            - Once the introduction is complete, eminem_agent and drake_agent will take turns to generate lyrics based on the provided topic.
            - After eminem_agent and drake_agent have performed, the judge_agent will evaluate the lyrics and give a score to each rapper. If the battle is a tie or the score difference between the two rappers is only 1 point (for example, eminem_agent scores 8 while drage_agent scores 9), the judge must request another round, until a maximum of 3.
            The new round will start directly with the two rappers, without an introduction from the Rap MC agent.

            The battle continues until the Judge Agent explicitly states "TERMINATE" in their response.

            Current conversation context:
            {history}

            Read the above conversation, then select an agent from {participants} to perform the next task.
            Make sure the planner agent has assigned tasks before other agents start working.

            Only select one agent.
        """,
        allow_repeated_speaker=True
    )
    
    # Run the team and stream messages to the console.
    stream = await agent_team.run(task=prompt)
    
    return stream


# To run the FastAPI app, use the command: uvicorn filename:app --reload
# Replace 'filename' with the name of your Python file