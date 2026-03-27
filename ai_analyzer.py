import os
from openai import OpenAI

def analyze_product(product_name):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Analyze this Amazon product:

                    {product_name}

                    Give:
                    - Why it's trending
                    - Opportunity level (Low/Medium/High)
                    - Improvement idea
                    """
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI error: {str(e)}"
