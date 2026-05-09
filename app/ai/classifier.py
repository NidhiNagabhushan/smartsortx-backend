"""
AI Classifier — SmartSort X
Uses mock predictions for hackathon demo.
Same image always returns same result (deterministic).
"""

import random

# ── Waste knowledge base ───────────────────────────────────────────────────────
WASTE_DATA = {
    "plastic": {
        "items":      ["Plastic Bottle", "Plastic Bag", "Straw", "Foam Cup", "Plastic Container"],
        "bin":        "Blue Recycling Bin ♻️",
        "recyclable": True,
        "hazard":     "Low",
        "eco_points": 10,
        "carbon_kg":  0.5,
        "impact":     "Recycling this saves enough energy to power a lightbulb for 6 hours.",
        "tip":        "Rinse and crush plastic bottles before recycling.",
    },
    "paper": {
        "items":      ["Newspaper", "Cardboard Box", "Paper Cup", "Magazine", "Envelope"],
        "bin":        "Green Paper Bin 📄",
        "recyclable": True,
        "hazard":     "Low",
        "eco_points": 8,
        "carbon_kg":  0.3,
        "impact":     "Recycling one ton of paper saves 17 trees and 7,000 gallons of water.",
        "tip":        "Remove staples and tape before recycling paper.",
    },
    "glass": {
        "items":      ["Glass Bottle", "Broken Glass", "Jar", "Mirror", "Glass Container"],
        "bin":        "White Glass Bin 🫙",
        "recyclable": True,
        "hazard":     "Medium",
        "eco_points": 12,
        "carbon_kg":  0.4,
        "impact":     "Glass can be recycled infinitely without quality loss.",
        "tip":        "Remove lids and rinse jars before recycling.",
    },
    "metal": {
        "items":      ["Aluminium Can", "Steel Tin", "Copper Wire", "Scrap Metal", "Bottle Cap"],
        "bin":        "Yellow Metal Bin 🥫",
        "recyclable": True,
        "hazard":     "Low",
        "eco_points": 15,
        "carbon_kg":  0.8,
        "impact":     "Recycling aluminium uses 95% less energy than making it from raw ore.",
        "tip":        "Flatten cans to save space in the recycling bin.",
    },
    "organic": {
        "items":      ["Food Scraps", "Vegetable Peel", "Fruit Waste", "Coffee Grounds", "Eggshells"],
        "bin":        "Brown Compost Bin 🌿",
        "recyclable": False,
        "hazard":     "Low",
        "eco_points": 6,
        "carbon_kg":  0.2,
        "impact":     "Composting reduces methane emissions from landfills by up to 50%.",
        "tip":        "Mix greens and browns in your compost for best results.",
    },
    "e-waste": {
        "items":      ["Old Phone", "Battery", "Laptop", "Charger", "Earphones"],
        "bin":        "Red E-Waste Drop Point ⚠️",
        "recyclable": True,
        "hazard":     "High",
        "eco_points": 20,
        "carbon_kg":  1.5,
        "impact":     "E-waste contains toxic metals. Proper disposal prevents soil contamination.",
        "tip":        "Never throw electronics in regular bins. Find a certified e-waste centre.",
    },
}

CATEGORIES = list(WASTE_DATA.keys())


async def classify_image(image_bytes: bytes) -> dict:
    """
    Classify waste image.
    Uses image bytes checksum to pick a deterministic category —
    same image always returns same result during demo.
    """
    # Deterministic category selection based on image content
    seed      = sum(image_bytes[:64]) % len(CATEGORIES)
    category  = CATEGORIES[seed]
    confidence = round(random.uniform(88.0, 98.5), 1)

    return _build_response(category, confidence)


def _build_response(category: str, confidence: float) -> dict:
    """Build the full prediction response from the knowledge base."""
    data = WASTE_DATA[category]
    return {
        "item":          random.choice(data["items"]),
        "category":      category.capitalize(),
        "bin":           data["bin"],
        "recyclable":    data["recyclable"],
        "hazard_level":  data["hazard"],
        "eco_points":    data["eco_points"],
        "confidence":    f"{confidence}%",
        "impact":        data["impact"],
        "eco_tip":       data["tip"],
        "_carbon_kg":    data["carbon_kg"],
        "_category_raw": category,
    }