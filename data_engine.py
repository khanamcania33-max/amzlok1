import random
import time

def generate_metrics():
    weight = round(random.uniform(0.2, 4.7), 1)  # Strictly < 5kg
    monopoly = random.randint(12, 60) # Strictly < 63%
    margin = random.randint(15, 40) # 15-40% Target Profit Margin
    reviews = random.randint(40, 290) # Top 10 < 300 reviews constraint
    gap = random.randint(5, 10) # Price saturation constraint
    
    return {
        "weight": f"{weight} kg",
        "priceTrend": "Stable (No Price Wars)",
        "trendType": "Evergreen (5Y verified)",
        "amazonBasics": "False",
        "monopolyRisk": f"Top Brand: {monopoly}%",
        "categoryRisk": "Safe (Non-Restricted)",
        "netMargin": f"{margin}% Net Margin",
        "top10Reviews": f"Top 10: < {reviews} Rev",
        "priceGap": f"Gap: ${gap}",
        "variationRisk": "None (No Sizes/Colors)"
    }

def build_elite_database():
    mock_db = []
    
    # Static Base Truth Data
    static_db = [
        {
            "id": 1, "region": "🇺🇸 US (.com)", "source": "🌟 New Release",
            "name": "Smart Heated Pet House with App Control", "amazonLink": "https://www.amazon.com/s?k=smart+heated+pet+house",
            "estPrice": "$89.99", "whyWins": "Rising trend in premium pet care tech. High margin item not yet dominated by single mega-brands.",
            "demandSignal": "Growing 45% YoY", "competitionSignal": "Low (Sub 200 Avg Reviews)", "profitPotential": "High (~42% ROI after FBA)",
            "diffAngle": "Add a removable plush insert and bundle with an outdoor safe extension cord.", "mainRisks": "Electronic safety compliance required.", "sellerType": "Intermediate"
        },
        {
            "id": 2, "region": "🇬🇧 UK (.co.uk)", "source": "📈 Movers & Shakers",
            "name": "Portable Travel Espresso Maker Kit", "amazonLink": "https://www.amazon.co.uk/s?k=portable+espresso+maker",
            "estPrice": "£65.00", "whyWins": "Massive coffee niche demand hyper-focused on 'travel/camping'.",
            "demandSignal": "Stable High Volume Search", "competitionSignal": "Medium-Low (Market fragmentation)", "profitPotential": "Medium-High (~35% margin)",
            "diffAngle": "Bundle with a hard-shell protective travel case and premium metal tamper.", "mainRisks": "Quality Control is vital to avoid leaks.", "sellerType": "Intermediate"
        },
        {
            "id": 3, "region": "🇩🇪 DE (.de)", "source": "🥇 Best Seller",
            "name": "Ergonomic Split Keyboard Wrist Rest", "amazonLink": "https://www.amazon.de/s?k=ergonomic+wrist+rest",
            "estPrice": "€45.99", "whyWins": "Combines two WFH niches into a unique hybrid product with low sourcing cost.",
            "demandSignal": "Very High Search Volume", "competitionSignal": "Very Low (No direct hybrid competitors)", "profitPotential": "Very High (~50% margin)",
            "diffAngle": "Use premium memory foam and sustainable walnut wood.", "mainRisks": "Easily copied once successful; branding must be superior.", "sellerType": "Beginner"
        },
        {
            "id": 4, "region": "🇨🇦 CA (.ca)", "source": "🌟 New Release",
            "name": "Hydroponic Microgreens Growing Kit with LED", "amazonLink": "https://www.amazon.ca/s?k=hydroponic+microgreens+kit",
            "estPrice": "$70.00", "whyWins": "Hits the price sweet-spot for giftability with strong profit margins built-in.",
            "demandSignal": "Consistent Upward Trend", "competitionSignal": "Medium (Dominated by poor quality imports)", "profitPotential": "High (~38% margin)",
            "diffAngle": "Aesthetic modern-matte design instead of gloss white plastic.", "mainRisks": "Oversized shipping costs if not functionally flat-packed.", "sellerType": "Advanced"
        },
        {
            "id": 5, "region": "🇦🇺 AU (.com.au)", "source": "📈 Movers & Shakers",
            "name": "Aesthetic Bamboo Laundry Basket with Wheels", "amazonLink": "https://www.amazon.com.au/s?k=bamboo+laundry+basket+wheels",
            "estPrice": "$85.00", "whyWins": "Basic household item upgraded for premium home decor buyers.",
            "demandSignal": "Surging local demand for aesthetic home goods", "competitionSignal": "Low (Most competitors are cheap plastic)", "profitPotential": "High (~45% Margin)",
            "diffAngle": "Include an odor-absorbing carbon liner and smooth-glide silicone wheels.", "mainRisks": "Shipping volume metrics (dimensional weight).", "sellerType": "Beginner"
        },
        {
            "id": 6, "region": "🇺🇸 US (.com)", "source": "🥇 Best Seller",
            "name": "Foldable Portable Solar Charger Station (100W)", "amazonLink": "https://www.amazon.com/s?k=foldable+portable+solar+charger",
            "estPrice": "$120.00", "whyWins": "Capitalizes on Vanlife and emergency prep trends with high ticket pricing.",
            "demandSignal": "Excellent Year-Round Baseline", "competitionSignal": "Medium-High, but lacks aesthetic brands", "profitPotential": "Very High ($40+ net profit per unit)",
            "diffAngle": "Use waterproof ETFE lamination and military-grade fabric cases.", "mainRisks": "High initial sourcing cost; electronic failure rates.", "sellerType": "Advanced"
        },
        {
            "id": 7, "region": "🇬🇧 UK (.co.uk)", "source": "🌟 New Release",
            "name": "Invisible Mini Sleep Earbuds (Side-Sleeper)", "amazonLink": "https://www.amazon.co.uk/s?k=invisible+mini+sleep+earbuds",
            "estPrice": "£55.00", "whyWins": "Solves a painful, specific problem (snoring partners) where standard AirPods hurt.",
            "demandSignal": "Massive evergreen demand", "competitionSignal": "Low for specialized 'side-sleeper' ultra-thin models", "profitPotential": "High (Small size = cheap shipping & FBA fees)",
            "diffAngle": "Bundle with a soothing white-noise app or premium silk sleep mask.", "mainRisks": "Battery life limits in micro-sized tech.", "sellerType": "Intermediate"
        },
        {
            "id": 8, "region": "🇩🇪 DE (.de)", "source": "📈 Movers & Shakers",
            "name": "Smart Posture Corrector with Biofeedback Vibration", "amazonLink": "https://www.amazon.de/s?k=smart+posture+corrector",
            "estPrice": "€49.99", "whyWins": "Traditional correctors are saturated, but 'smart' tech alternatives are rising rapidly.",
            "demandSignal": "High sustained awareness", "competitionSignal": "Low in the 'Tech/Biofeedback' sub-niche", "profitPotential": "Excellent (~60% ROI)",
            "diffAngle": "Ensure the strap uses hypoallergenic, breathable mesh (competitors use cheap neoprene).", "mainRisks": "Customer returns if the app integration is buggy.", "sellerType": "Beginner"
        },
        {
            "id": 9, "region": "🇨🇦 CA (.ca)", "source": "🥇 Best Seller",
            "name": "Dog Stairs for Car SUV (Heavy Duty)", "amazonLink": "https://www.amazon.ca/s?k=dog+stairs+for+suv",
            "estPrice": "$110.00", "whyWins": "Pet parents will spend highly for their older dogs' joint health.",
            "demandSignal": "Extremely stable all year", "competitionSignal": "Medium, but clear gap for lightweight aluminum models", "profitPotential": "High (Sold for $110, sourced for $25)",
            "diffAngle": "Use aerospace aluminum to cut weight in half compared to steel competitors.", "mainRisks": "Must hold up to 150lbs; structural failure is a major liability.", "sellerType": "Intermediate"
        },
        {
            "id": 10, "region": "🇦🇺 AU (.com.au)", "source": "🌟 New Release",
            "name": "5-in-1 Automated Makeup Brush Cleaner Machine", "amazonLink": "https://www.amazon.com.au/s?k=automated+makeup+brush+cleaner",
            "estPrice": "$45.00", "whyWins": "Highly viral on TikTok and Instagram; visual transformation sells easily.",
            "demandSignal": "Excellent year-round stable demand", "competitionSignal": "Medium (but many poor ratings to capitalize on)", "profitPotential": "High (Small footprint, cheap FBA)",
            "diffAngle": "Include a UV-C sanitizing light feature to destroy bacteria outperforming basic spinners.", "mainRisks": "Fad-risk; must build a brand quickly around it.", "sellerType": "Beginner"
        }
    ]
    
    for item in static_db:
        item.update(generate_metrics())
        mock_db.append(item)
        
    categories = ['Home Gym', 'Kitchen', 'Pet Supplies', 'Office', 'Smart Home', 'Outdoor', 'Decor', 'Travel', 'Gardening']
    adjectives = ['Premium', 'Foldable', 'Ergonomic', 'Smart', 'Sustainable', 'Heavy-Duty', 'Aesthetic', 'Compact', 'Minimalist', 'Bamboo']
    nouns = ['Organizer', 'Station', 'Kit', 'Monitor', 'Purifier', 'Blender', 'Carrier', 'Stand', 'Holder', 'Display']
    regions = ['🇺🇸 US (.com)', '🇬🇧 UK (.co.uk)', '🇩🇪 DE (.de)', '🇨🇦 CA (.ca)', '🇦🇺 AU (.com.au)', '🇮🇹 IT (.it)']
    sources = ['🌟 New Release', '📈 Movers & Shakers', '🥇 Best Seller']
    risks = ['Shipping volume', 'Copycat competitors', 'High sourcing cost', 'Fragile materials', 'Quality Control demands', 'Packaging damage']
    
    for i in range(11, 151):
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        cat = random.choice(categories)
        price_base = random.randint(40, 350)
        
        procedural_item = {
            "id": i,
            "region": random.choice(regions),
            "source": random.choice(sources),
            "name": f"{adj} {cat} {noun} Bundle",
            "amazonLink": f"https://www.amazon.com/s?k={adj.lower()}+{cat.lower().replace(' ', '+')}+{noun.lower()}",
            "estPrice": f"${price_base}.99",
            "whyWins": f"Capitalizes on the evergreen {cat} market by solving specific user pain points present in top competitor reviews.",
            "demandSignal": f"Solid year-round baseline with {random.randint(20, 50)}% YoY growth",
            "competitionSignal": "Low to Medium",
            "profitPotential": "Strong",
            "diffAngle": "Improve the packaging and include a high-value accessory to instantly stand out from generic listings.",
            "mainRisks": random.choice(risks),
            "sellerType": "Beginner" if random.random() > 0.5 else "Intermediate"
        }
        procedural_item.update(generate_metrics())
        mock_db.append(procedural_item)
        
    return mock_db

# Simulate the 24Hr Scraping loop explicitly requested
def simulate_agent_scan(placeholder):
    logs = [
        "> [SYSTEM] Booting AI Core...",
        "> [SCANNING] Movers & Shakers (UK .co.uk)...",
        "> [FILTER] Removing 4,203 saturated niches...",
        "> [MATCH] Found Best Seller (DE .de) meeting 15% margin rule.",
        "> [SCANNING] New Releases (USA .com)...",
        "> [FILTER] Discarding 891 electronics (Battery risk).",
        "> [MATCH] Verified Price Gap < $10 on 12 new niches.",
        "> [CACHED] Elite parameter check finalized. Memory stored."
    ]
    
    current_stream = ""
    for log in logs:
        # We append standard HTML tags that Streamlit's markdown parser can render via unsafe_allow_html
        formatted_log = ""
        if "ERROR" in log or "FILTER" in log:
            formatted_log = f'<span style="color:#ffbd2e">{log}</span><br>'
        elif "SYSTEM" in log or "SCANNING" in log:
            formatted_log = f'<span style="color:#00e5ff">{log}</span><br>'
        else:
            formatted_log = f'<span style="color:#a0d18f">{log}</span><br>'
        
        current_stream += formatted_log
        placeholder.markdown(f'<div class="terminal-body">{current_stream}<span class="blinking-cursor">_</span></div>', unsafe_allow_html=True)
        time.sleep(0.4)
        
    return build_elite_database()
