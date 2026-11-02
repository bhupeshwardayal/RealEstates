import re
from typing import Dict, Any, Optional, List

class QueryIntentExtractor:
    """
    Module 2: Natural Language Query Processing.
    Extracts hard filters (budget, BHK, locality, possession) and soft semantic preferences.
    """

    @staticmethod
    def extract_intent(query: str, previous_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        q = query.lower()
        extracted: Dict[str, Any] = {
            "max_budget_inr": None,
            "min_bhk": None,
            "target_locality": None,
            "target_city": None,
            "required_amenities": [],
            "possession_preference": None,
            "soft_preferences": []
        }

        # 1. Budget extraction (Lakhs, Cr, INR, numbers)
        # e.g., "under 85 Lakhs", "< 85L", "budget ₹1.2 Cr", "under 1.5 crore"
        cr_match = re.search(r'(?:under|below|budget|within|<|<=)?\s*(?:₹|inr|rs\.?)?\s*(\d+(?:\.\d+)?)\s*(?:cr|crore|crores)\b', q)
        if cr_match:
            extracted["max_budget_inr"] = float(cr_match.group(1)) * 10000000.0
        else:
            lakh_match = re.search(r'(?:under|below|budget|within|<|<=)?\s*(?:₹|inr|rs\.?)?\s*(\d+(?:\.\d+)?)\s*(?:l|lac|lakh|lakhs)\b', q)
            if lakh_match:
                extracted["max_budget_inr"] = float(lakh_match.group(1)) * 100000.0

        # 2. BHK count extraction
        # e.g., "3 BHK", "2 or 3 bhk", "4bhk", "1 bedroom"
        bhk_match = re.search(r'(\d+)\s*(?:bhk|bedroom|bed)\b', q)
        if bhk_match:
            extracted["min_bhk"] = int(bhk_match.group(1))

        # 3. City extraction
        for city in ["pune", "mumbai", "nagpur", "bangalore", "bengaluru", "hyderabad", "delhi"]:
            if city in q:
                extracted["target_city"] = "Bangalore" if city == "bengaluru" else city.capitalize()
                break

        # 4. Locality extraction
        localities = [
            "hinjawadi", "baner", "balewadi", "koregaon park", "kharadi", "wakad", "bavdhan", "kothrud",
            "wardha road", "mihan", "civil lines", "whitefield", "worli", "hitec city", "madhapur"
        ]
        for loc in localities:
            if loc in q:
                extracted["target_locality"] = loc.title()
                break

        # 5. Amenity extraction
        amenity_keywords = {
            "covered parking": "Covered Parking",
            "parking": "Covered Parking",
            "swimming pool": "Swimming Pool",
            "pool": "Swimming Pool",
            "gym": "Gymnasium",
            "clubhouse": "Clubhouse",
            "private lawn": "Private Lawn Garden",
            "lawn": "Private Lawn Garden",
            "terrace": "Private Terrace Deck",
            "balcony": "Balcony",
            "security": "24/7 Security",
            "power backup": "Power Backup"
        }
        for kw, canonical in amenity_keywords.items():
            if kw in q:
                if canonical not in extracted["required_amenities"]:
                    extracted["required_amenities"].append(canonical)

        # 6. Possession preference
        if "ready to move" in q or "immediate" in q or "ready" in q:
            extracted["possession_preference"] = "Ready to Move"
        elif "under construction" in q:
            extracted["possession_preference"] = "Under Construction"

        # 7. Soft preferences (commute, lifestyle, yield)
        if "it park" in q or "tech park" in q or "infosys" in q or "tcs" in q or "wipro" in q:
            extracted["soft_preferences"].append("proximity to IT/Tech corridors")
        if "school" in q or "transit" in q or "college" in q:
            extracted["soft_preferences"].append("reputed educational connectivity")
        if "rental yield" in q or "investment" in q or "roi" in q or "high yield" in q:
            extracted["soft_preferences"].append("high rental yield & investor appeal")
        if "luxury" in q or "penthouse" in q or "sea view" in q or "villa" in q:
            extracted["soft_preferences"].append("luxury lifestyle & premium amenities")

        # Conversational Memory inheritances (if user issued follow-up like "Show me only ones with covered parking")
        if previous_context:
            if extracted["max_budget_inr"] is None and previous_context.get("max_budget_inr"):
                extracted["max_budget_inr"] = previous_context["max_budget_inr"]
            if extracted["min_bhk"] is None and previous_context.get("min_bhk"):
                extracted["min_bhk"] = previous_context["min_bhk"]
            if extracted["target_locality"] is None and previous_context.get("target_locality"):
                extracted["target_locality"] = previous_context["target_locality"]
            if extracted["target_city"] is None and previous_context.get("target_city"):
                extracted["target_city"] = previous_context["target_city"]

        return extracted

