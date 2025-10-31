"""
Agent 1: Deep Research Agent with Tavily
This agent performs comprehensive research on any topic using Tavily AI.
"""

import os
from dotenv import load_dotenv
from tavily import TavilyClient
from agents import Agent, function_tool, WebSearchTool
from dataclasses import dataclass
from typing import List
import json

# Load environment variables
load_dotenv()

# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# ============================================
# DATA STRUCTURES
# ============================================

@dataclass
class ResearchData:
    """Structured output for research results"""
    topic: str
    facts_and_stats: List[str]
    controversies_and_debates: List[str]
    trending_angles: List[str]
    content_gaps: List[str]
    expert_quotes: List[str]
    sources: List[dict]  # [{"title": "...", "url": "..."}]
    research_summary: str


# ============================================
# HELPER FUNCTIONS
# ============================================

def extract_facts_and_stats(results: dict) -> List[str]:
    """
    Extract key facts, statistics, and data points from search results.

    How it works:
    - Looks through article content for numbers, percentages, dates
    - Identifies statements that sound factual
    - Returns list of concrete facts
    """
    facts = []

    for result in results.get("results", [])[:7]:  # Top 7 results
        content = result.get("content", "")

        # Look for sentences with numbers/percentages (likely facts/stats)
        sentences = content.split(". ")
        for sentence in sentences:
            # If sentence contains numbers or percentage signs
            if any(char.isdigit() for char in sentence) or "%" in sentence:
                facts.append(sentence.strip())
                if len(facts) >= 10:  # Limit to 10 facts
                    break
        if len(facts) >= 10:
            break

    return facts[:10]  # Return top 10 facts


def extract_controversies(results: dict) -> List[str]:
    """
    Find debates, criticisms, and different perspectives.

    How it works:
    - Looks for keywords like "however", "critics say", "debate"
    - Identifies contrasting viewpoints
    - Extracts controversial statements
    """
    controversies = []
    controversy_keywords = [
        "however", "critics", "criticism", "debate", "controversial",
        "disagree", "argue", "concern", "problem", "challenge"
    ]

    for result in results.get("results", []):
        content = result.get("content", "")
        sentences = content.split(". ")

        for sentence in sentences:
            # Check if sentence contains controversy keywords
            if any(keyword in sentence.lower() for keyword in controversy_keywords):
                controversies.append(sentence.strip())
                if len(controversies) >= 6:
                    break
        if len(controversies) >= 6:
            break

    return controversies[:6]


def extract_trends(results: dict) -> List[str]:
    """
    Identify trending angles and emerging discussions.

    How it works:
    - Looks for forward-looking statements
    - Finds mentions of "trend", "future", "emerging"
    - Captures what's new or growing
    """
    trends = []
    trend_keywords = [
        "trend", "emerging", "future", "growing", "increasing",
        "new", "innovation", "latest", "2025", "upcoming"
    ]

    for result in results.get("results", []):
        content = result.get("content", "")
        sentences = content.split(". ")

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in trend_keywords):
                trends.append(sentence.strip())
                if len(trends) >= 7:
                    break
        if len(trends) >= 7:
            break

    return trends[:7]


def extract_content_gaps(results: dict) -> List[str]:
    """
    Find what others aren't talking about - unique angles.

    How it works:
    - Looks for less common topics in results
    - Identifies underexplored areas
    - Finds niche perspectives
    """
    gaps = []
    gap_keywords = [
        "overlooked", "rarely", "often ignored", "underreported",
        "few discuss", "missing", "gap", "neglected"
    ]

    for result in results.get("results", []):
        content = result.get("content", "")
        sentences = content.split(". ")

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in gap_keywords):
                gaps.append(sentence.strip())
                if len(gaps) >= 5:
                    break
        if len(gaps) >= 5:
            break

    return gaps[:5]


def extract_expert_quotes(results: dict) -> List[str]:
    """
    Find expert opinions and authoritative statements.

    How it works:
    - Looks for quoted text
    - Finds mentions of experts, CEOs, researchers
    - Extracts credible opinions
    """
    quotes = []
    expert_indicators = [
        "according to", "expert", "researcher", "professor",
        "CEO", "founder", "analyst", "study shows"
    ]

    for result in results.get("results", []):
        content = result.get("content", "")
        sentences = content.split(". ")

        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in expert_indicators):
                quotes.append(sentence.strip())
                if len(quotes) >= 4:
                    break
        if len(quotes) >= 4:
            break

    return quotes[:4]


# ============================================
# MAIN RESEARCH FUNCTION (TOOL)
# ============================================

@function_tool
def deep_research(topic: str) -> str:
    """
    Performs comprehensive deep research on a given topic.

    This function:
    1. Searches for general information about the topic
    2. Searches specifically for controversies and debates
    3. Searches for trends and future perspectives
    4. Searches for unique angles and content gaps
    5. Combines all findings into structured research data

    Args:
        topic: The topic to research (e.g., "AI agents in content creation")

    Returns:
        JSON string with structured research data
    """

    print(f"\n🔍 Starting deep research on: {topic}\n")

    # ========================================
    # SEARCH 1: General Facts & Information
    # ========================================
    print(" Step 1: Gathering facts and statistics...")

    general_results = tavily_client.search(
        query=f"{topic} latest facts statistics data 2024 2025",
        search_depth="advanced",  # More thorough search
        max_results=10,
        include_answer=True  # Get AI-generated summary
    )

    facts = extract_facts_and_stats(general_results)
    print(f"   ✓ Found {len(facts)} facts")

    # ========================================
    # SEARCH 2: Controversies & Debates
    # ========================================
    print("  Step 2: Finding controversies and debates...")

    controversy_results = tavily_client.search(
        query=f"{topic} controversies debates criticisms challenges problems",
        search_depth="advanced",
        max_results=8
    )

    controversies = extract_controversies(controversy_results)
    print(f"   ✓ Found {len(controversies)} controversial points")

    # ========================================
    # SEARCH 3: Trends & Future Angles
    # ========================================
    print("📈 Step 3: Identifying trends and emerging angles...")

    trends_results = tavily_client.search(
        query=f"{topic} trends 2025 future emerging latest innovations",
        search_depth="advanced",
        max_results=8
    )

    trends = extract_trends(trends_results)
    print(f"   ✓ Found {len(trends)} trending angles")

    # ========================================
    # SEARCH 4: Content Gaps & Unique Angles
    # ========================================
    print("🔎 Step 4: Discovering content gaps...")

    gaps_results = tavily_client.search(
        query=f"{topic} overlooked underreported unique perspective niche angles",
        search_depth="advanced",
        max_results=8
    )

    gaps = extract_content_gaps(gaps_results)
    print(f"   ✓ Found {len(gaps)} content gaps")

    # ========================================
    # EXTRACT EXPERT QUOTES
    # ========================================
    print("💬 Step 5: Collecting expert opinions...")

    expert_results = tavily_client.search(
        query=f"{topic} expert opinion research study analysis report",
        search_depth="advanced",
        max_results=8
    )
    quotes = extract_expert_quotes(expert_results)
    print(f"   ✓ Found {len(quotes)} expert quotes")
    # ========================================
    # COMPILE SOURCES
    # ========================================
    print(" Step 6: Compiling sources...")

    sources = []
    seen_urls = set()

    # Combine all results and get unique sources
    all_results = (
            general_results.get("results", []) +
            controversy_results.get("results", []) +
            trends_results.get("results", []) +
            gaps_results.get("results", [])
    )

    for result in all_results:
        url = result.get("url", "")
        if url and url not in seen_urls:
            sources.append({
                "title": result.get("title", "Unknown"),
                "url": url,
                "published": result.get("published_date", "Unknown")
            })
            seen_urls.add(url)

        if len(sources) >= 10:  # Limit to 10 sources
            break

    print(f"   ✓ Compiled {len(sources)} unique sources")

    # ========================================
    # CREATE RESEARCH SUMMARY
    # ========================================
    print("📝 Step 7: Creating research summary...")

    # Use Tavily's AI-generated answer as base summary
    summary = general_results.get("answer", f"Comprehensive research on {topic}")

    # ========================================
    # STRUCTURE ALL DATA
    # ========================================
    research_data = ResearchData(
        topic=topic,
        facts_and_stats=facts,
        controversies_and_debates=controversies,
        trending_angles=trends,
        content_gaps=gaps,
        expert_quotes=quotes,
        sources=sources,
        research_summary=summary
    )

    print("\n✅ Research complete!\n")

    # Convert to JSON string for the agent
    return json.dumps({
        "topic": research_data.topic,
        "facts_and_stats": research_data.facts_and_stats,
        "controversies_and_debates": research_data.controversies_and_debates,
        "trending_angles": research_data.trending_angles,
        "content_gaps": research_data.content_gaps,
        "expert_quotes": research_data.expert_quotes,
        "sources": research_data.sources,
        "research_summary": research_data.research_summary
    }, indent=2)


# ============================================
# CREATE THE RESEARCH AGENT
# ============================================

research_agent = Agent(
    name="Deep Research Agent",
    instructions="""You are an expert research analyst...

    CRITICAL: When you use the deep_research tool, it returns a JSON string.
    Return that EXACT JSON string as your output.
    Do NOT add commentary, explanations, or modifications.
    Just return the raw JSON from the tool.
    Feel free to use the WebSearchTool fo make additional research when necessary to fill up information
    """,
    tools=[deep_research, WebSearchTool()],
    model="gpt-4o"
)

# ============================================
# EXAMPLE USAGE (for testing)
# ============================================

if __name__ == "__main__":
    """
    Test the research agent standalone
    """
    from agents import Runner
    import asyncio


    async def test_research():
        print("=" * 60)
        print("TESTING RESEARCH AGENT")
        print("=" * 60)

        # Get topic from user
        print("\n💡 What topic would you like to research?")
        topic = input("Enter your topic: ").strip()

        if not topic:
            print("❌ No topic provided. Exiting...")
            return

        print(f"\n🎯 Researching: {topic}")
        print("=" * 60)

        # Run the research agent
        result = await Runner.run(
            research_agent,
            input=f"Research this topic comprehensively: {topic}"
        )

        # The agent's response might be in different formats
        # Let's try to extract it properly
        research_json = None

        if hasattr(result, 'final_output'):
            output = result.final_output
            print(f"final_output type: {type(output)}")
            print(f"final_output preview: {str(output)[:200]}...")

            # If it's already a string, try to parse it
            if isinstance(output, str):
                try:
                    research_json = output
                    research_data = json.loads(output)
                except json.JSONDecodeError:
                    print("\n❌ Error: Could not parse JSON from final_output")
                    print("Raw output:")
                    print(output)
                    return
        else:
            print("\n❌ Error: Result doesn't have final_output attribute")
            print(f"Result attributes: {dir(result)}")
            return

        if not research_data:
            print("\n❌ Error: No research data found")
            return

        # Display results nicely
        print("\n" + "=" * 60)
        print("RESEARCH RESULTS")
        print("=" * 60)

        print(f"\n📌 TOPIC: {research_data['topic']}")

        print("\n📊 FACTS & STATISTICS:")
        for i, fact in enumerate(research_data['facts_and_stats'], 1):
            print(f"   {i}. {fact}")

        print("\n⚖️  CONTROVERSIES & DEBATES:")
        for i, controversy in enumerate(research_data['controversies_and_debates'], 1):
            print(f"   {i}. {controversy}")

        print("\n📈 TRENDING ANGLES:")
        for i, trend in enumerate(research_data['trending_angles'], 1):
            print(f"   {i}. {trend}")

        print("\n🔎 CONTENT GAPS:")
        for i, gap in enumerate(research_data['content_gaps'], 1):
            print(f"   {i}. {gap}")

        print("\n💬 EXPERT QUOTES:")
        for i, quote in enumerate(research_data['expert_quotes'], 1):
            print(f"   {i}. {quote}")

        print(f"\n📚 SOURCES ({len(research_data['sources'])}):")
        for i, source in enumerate(research_data['sources'][:5], 1):  # Show first 5
            print(f"   {i}. {source['title']}")
            print(f"      {source['url']}")

        print("\n📝 RESEARCH SUMMARY:")
        print(f"   {research_data['research_summary']}")

        print("\n" + "=" * 60)
        print("✅ TEST COMPLETE!")
        print("=" * 60)


    # Run the test
    asyncio.run(test_research())

