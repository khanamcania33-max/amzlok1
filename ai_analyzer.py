from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def analyze_product(product_name):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Analyze this Amazon product:

                    {product_name}

                    Return:
                    - Why it's trending
                    - Opportunity level
                    - Improvement idea
                    """
                }
            ]
        )

        return response.choices[0].message.content

    except:
        return "AI analysis unavailable (API key missing or error)"
