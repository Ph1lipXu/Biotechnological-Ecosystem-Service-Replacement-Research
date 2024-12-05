import openai
import os

# openai.api_key = os.getenv("OPENAI_API_KEY")

# Format Text
def formatText(text):
    cleanedText = text.replace("*", "").lower()
    return cleanedText

# Get AI Response
def askGPT(abstract):
    prompt = f"""Given this abstract for a research paper, would this article be suitable for biotechnological ecosystem service replacement research: {abstract}.

                Suitability is determined by whether the paper discusses technologies, methods, or approaches that could feasibly replace natural soil formation processes. 

                Please respond as follows:
                1. Reply with "Yes", "Maybe", or "No" based on the suitability.
                2. Provide a confidence score between 0 and 1 indicating how confident you are in your decision (1 is very confident, 0 is not confident).
                3. Summarize the abstract with a single keyword or short phrase that best represents its core topic. The summary should not contain special formatting and should focus on the main subject of the research.

                Example output:
                Yes
                0.85
                Biochar
                """

    try:
        # Make the request to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        # Extract and format the response
        return formatText(response['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Error: {e}")
        return None
