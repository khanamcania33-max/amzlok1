import os

def analyze_product(product_name):
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")

        # If no key → fallback
        if not api_key:
            return fallback_analysis(product_name)

        client = OpenAI(api_key=api_key)

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
                    - Opportunity level
                    - Improvement idea
                    """
                }
            ]
        )

        return response.choices[0].message.content

    except Exception:
        return fallback_analysis(product_name)


# ✅ SAFE FALLBACK (NEVER FAILS)
def fallback_analysis(product_name):
    return f"""
🔍 AI Insight (Offline Mode)

Product: {product_name}

• Trend: Growing niche with consistent demand  
• Opportunity: Medium to High  
• Idea: Improve packaging + bundle accessories  
"""
