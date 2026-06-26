"""
AI Diet Plan Generator using LangChain
--------------------------------------
Collects user inputs (age, weight, goals, preferences, etc.)
and generates a personalized diet plan using an LLM.

Setup:
    pip install langchain-core langchain-anthropic python-dotenv
    export ANTHROPIC_API_KEY="your-key-here"

Run:
    python diet_plan_generator.py
"""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
api_key=os.environ.get("ANTHROPIC_API_KEY")


# ----------------------------
# 1. Collect user inputs
# ----------------------------
def get_user_inputs():
    print("=" * 50)
    print("  🥗  AI DIET PLAN GENERATOR")
    print("=" * 50)

    def ask(prompt, default=None, cast=str):
        while True:
            raw = input(prompt).strip()
            if not raw and default is not None:
                return default
            if not raw:
                print("  ⚠️  This field is required.")
                continue
            try:
                return cast(raw)
            except ValueError:
                print("  ⚠️  Invalid value, try again.")

    data = {}
    data["age"] = ask("Age: ", cast=int)
    data["gender"] = ask("Gender (male/female/other): ")
    data["weight_kg"] = ask("Weight (kg): ", cast=float)
    data["height_cm"] = ask("Height (cm): ", cast=float)
    data["activity"] = ask(
        "Activity level (sedentary/light/moderate/active/very active): ",
        default="moderate",
    )
    data["goal"] = ask(
        "Goal (lose weight/maintain/gain muscle): ", default="maintain"
    )
    data["diet_type"] = ask(
        "Diet preference (omnivore/vegetarian/vegan/keto/etc.): ",
        default="omnivore",
    )
    data["allergies"] = ask(
        "Allergies/foods to avoid (comma-separated, or 'none'): ", default="none"
    )
    data["meals_per_day"] = ask("Meals per day: ", default=3, cast=int)
    data["budget"] = ask("Budget level (low/medium/high): ", default="medium")
    data["cuisine"] = ask(
        "Preferred cuisine (e.g. Mediterranean, Indian, any): ", default="any"
    )
    return data


# ----------------------------
# 2. Build the LangChain chain
# ----------------------------
def build_chain():
    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        temperature=0.7,
        max_tokens=2000,
        api_key=api_key
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a certified nutritionist and dietitian. "
                "Create safe, balanced, and personalized diet plans. "
                "Always include a brief disclaimer that this is general "
                "guidance and not a substitute for professional medical advice.",
            ),
            (
                "human",
                """Create a personalized one-day diet plan for the following person:

- Age: {age}
- Gender: {gender}
- Weight: {weight_kg} kg
- Height: {height_cm} cm
- Activity level: {activity}
- Goal: {goal}
- Diet preference: {diet_type}
- Allergies / avoid: {allergies}
- Meals per day: {meals_per_day}
- Budget: {budget}
- Preferred cuisine: {cuisine}

Please provide:
1. Estimated daily calorie target and macronutrient split (protein/carbs/fats).
2. A full meal-by-meal plan ({meals_per_day} meals) with portion sizes.
3. Approximate calories per meal.
4. 3 quick snack ideas that fit the goal.
5. 3 practical tips to stay on track.

Format the output clearly with headings.""",
            ),
        ]
    )

    return prompt | llm | StrOutputParser()


# ----------------------------
# 3. Main
# ----------------------------
def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Please set the ANTHROPIC_API_KEY environment variable.")
        return

    user_data = get_user_inputs()
    chain = build_chain()

    print("\n⏳ Generating your personalized diet plan...\n")
    plan = chain.invoke(user_data)

    print("=" * 50)
    print("  YOUR PERSONALIZED DIET PLAN")
    print("=" * 50)
    print(plan)



if __name__ == "__main__":
    main()