import json
from datetime import date
from gemini_client import client, MODEL
from tools import TOOLS, DECLARATIONS

def ask(question: str) -> str:
    prompt = (
        f"Today's date is {date.today().isoformat()}. "
        "You answer questions about the user's food purchases using the tools. "
        "Always convert relative dates (yesterday, last 7 days) to YYYY-MM-DD. "
        "Amounts are in Indonesian Rupiah. If the tools return nothing, say so; never guess.\n\n"
        f"Question: {question}"
    )
    interaction = client.interactions.create(model=MODEL, input=prompt, tools=DECLARATIONS)

    for _ in range(5):   # safety cap on tool rounds
        calls = [s for s in interaction.steps if s.type == "function_call"]
        if not calls:
            return interaction.output_text          # final answer

        results = []
        for call in calls:
            output = TOOLS[call.name](**call.arguments)   # run YOUR function
            results.append({
                "type": "function_result",
                "name": call.name,
                "call_id": call.id,
                "result": [{"type": "text", "text": json.dumps(output)}],
            })

        interaction = client.interactions.create(
            model=MODEL, input=results, tools=DECLARATIONS,
            previous_interaction_id=interaction.id,
        )
    return "Sorry, I couldn't answer that."