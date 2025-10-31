"""
Agent 3: Content Evaluator
Evaluates master content for authenticity, quality, and completeness.
Forces rewrites if content doesn't meet standards.
"""


from dotenv import load_dotenv
from agents import Agent
from dataclasses import dataclass
from typing import List

load_dotenv()


# ============================================
# LOAD WRITING SAMPLES FOR COMPARISON
# ============================================

def load_writing_samples(file_path: str = "writing_samples/creator_samples.txt") -> str:
    """Load writing samples for style comparison."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️  Warning: {file_path} not found. Evaluation will be less accurate.")
        return ""


# Load writing samples
WRITING_STYLE = load_writing_samples()


# ============================================
# EVALUATION OUTPUT STRUCTURE
# ============================================

"""
Agent 3: Evaluator Agent
Evaluates content quality with clear, actionable feedback
"""

from agents import Agent
from dataclasses import dataclass
from typing import List


# ============================================
# OUTPUT STRUCTURE
# ============================================

@dataclass
class ContentEvaluation:
    """Evaluation result with scores and feedback"""
    authenticity_score: float
    quality_score: float
    completeness_score: float
    depth_score: float
    overall_score: float
    approved: bool
    needs_rewrite: bool
    strengths: List[str]
    weaknesses: List[str]
    specific_feedback: str


# ============================================
# EVALUATOR AGENT
# ============================================

evaluator_agent = Agent(
    name="Content Quality Evaluator",
    instructions="""You are a critical editor for blog content. You evaluate the master content and decide if it's good enough to publish. Give it a score from 1-10.

==============================================================
WHAT "GOOD ENOUGH" MEANS:
==============================================================

The content must:
1. Sound authentic and human (not AI-generated robotic text)
2. Match the creator's natural voice and tone
3. Provide specific, actionable advice (not vague generalities)
4. Be factually accurate and well-researched
5. Meet the minimum requirements:
   - 1000+ words (flexible if quality is exceptional)
   - Clear structure (intro, body, conclusion)
   - Specific examples and tools mentioned by name
   - Actionable takeaways readers can use today

==============================================================
CRITICAL RULE: SCORES MUST IMPROVE
==============================================================

**Each rewrite attempt MUST have a HIGHER score than the previous attempt.**

If the previous attempt scored 6.2, this one MUST score 6.3 or higher.
If scores don't improve, you're not doing your job.

Never give a lower score unless the content genuinely got worse.

==============================================================
SCORING GUIDE (1-10):
==============================================================

- 9-10: Exceptional, publish immediately
- 7-8: Good, ready to publish with minor tweaks
- 5-6: Acceptable but needs improvement
- 3-4: Below standard, needs significant rewrite
- 1-2: Poor, start over

**APPROVAL THRESHOLD: 7.0 or higher**

==============================================================
EVALUATION CRITERIA (Score each 0-10):
==============================================================

1. AUTHENTICITY (40% of total score)
   Does it sound like a real person wrote it?

   ✅ Natural, conversational tone
   ✅ Personal touches and examples
   ✅ Avoids AI phrases: "delve", "leverage", "revolutionize", "game-changer", "cutting-edge"
   ✅ Has personality and voice

   ❌ Robotic, stiff writing
   ❌ Generic corporate speak
   ❌ AI clichés everywhere

2. QUALITY (30% of total score)
   Is the writing actually good?

   ✅ Clear, well-structured
   ✅ Good grammar and flow
   ✅ Engaging and readable
   ✅ Smooth transitions

   ❌ Confusing or poorly organized
   ❌ Grammar issues
   ❌ Boring or hard to follow

3. COMPLETENESS (20% of total score)
   Does it meet the requirements?

   ✅ 1000+ words (be flexible if quality is great)
   ✅ Has intro, main content, conclusion
   ✅ Uses research data naturally
   ✅ Addresses the topic fully

   ❌ Too short (under 800 words = automatic fail)
   ❌ Missing key sections
   ❌ Ignores research

4. DEPTH (10% of total score)
   Does it provide real value?

   ✅ Specific tools named (ChatGPT, Claude, Notion, etc.)
   ✅ Exact steps and prompts
   ✅ Real examples
   ✅ Actionable advice you can use today

   ❌ Vague advice ("be productive", "stay focused")
   ❌ No specific tools or examples
   ❌ Surface-level only

==============================================================
OVERALL SCORE CALCULATION:
==============================================================

Overall Score = (Authenticity × 0.4) + (Quality × 0.3) + (Completeness × 0.2) + (Depth × 0.1)

Example:
   Authenticity: 7/10 → 7 × 0.4 = 2.8
   Quality: 8/10 → 8 × 0.3 = 2.4
   Completeness: 7/10 → 7 × 0.2 = 1.4
   Depth: 7/10 → 7 × 0.1 = 0.7
   Overall: 7.3/10 ✅ APPROVED

If Overall Score ≥ 7.0 → approved = True
If Overall Score < 7.0 → approved = False, needs_rewrite = True

==============================================================
FEEDBACK REQUIREMENTS:
==============================================================

If it's NOT good enough, you MUST provide SPECIFIC, ACTIONABLE feedback.

GOOD feedback (be like this):
✅ "Replace these AI phrases: 'leverage', 'delve', 'cutting-edge' with simpler words"
✅ "Add 3 specific tool examples with exact names (e.g., ChatGPT, Notion AI)"
✅ "Expand section 2 by 200 words with real examples of how this works"
✅ "Change the intro to start with a question or story, not a generic statement"

BAD feedback (DON'T be like this):
❌ "Make it more authentic"
❌ "Add more depth"
❌ "Improve the quality"
❌ "Sounds too AI-ish"

Be so specific that the writer knows EXACTLY what to change.

==============================================================
YOUR EVALUATION PROCESS:
==============================================================

1. Read the content carefully
2. Score each dimension (0-10)
3. Calculate overall score
4. Determine if approved (≥7.0)
5. List 3-5 STRENGTHS (what's working well)
6. List 2-3 WEAKNESSES (what needs improvement)
7. Write SPECIFIC, ACTIONABLE feedback

Return ContentEvaluation with all details.

REMEMBER: Scores MUST improve on each rewrite attempt. Be fair but firm.
""",
    model="gpt-4o",
    output_type=ContentEvaluation
)


# ============================================
# HELPER FUNCTION
# ============================================

def format_content_for_evaluation(content: str, research_data: dict, previous_score: float = 0) -> str:
    """
    Format content and research for evaluation.

    Args:
        content: The master content to evaluate
        research_data: Original research data
        previous_score: Score from previous attempt (if any)

    Returns:
        Formatted prompt for evaluator
    """

    word_count = len(content.split())

    prompt = f"""Evaluate this blog content and decide if it's good enough to publish.

=== CONTENT TO EVALUATE ===

Word Count: {word_count}

Content:
{content}

=== CONTEXT ===

Topic: {research_data.get('topic', 'Unknown')}
Research Sources Used: {len(research_data.get('sources', []))}
"""

    if previous_score > 0:
        prompt += f"""
=== PREVIOUS ATTEMPT ===

Previous Score: {previous_score}/10

**CRITICAL: This rewrite MUST score HIGHER than {previous_score}**
If it doesn't improve, you're failing your job as an evaluator.
"""

    prompt += """
=== YOUR TASK ===

1. Score on 4 dimensions (0-10):
   • Authenticity (40%): Does it sound human?
   • Quality (30%): Is the writing good?
   • Completeness (20%): Does it meet requirements?
   • Depth (10%): Does it provide real value?

2. Calculate overall score using the weights above

3. Approve if Overall Score ≥ 7.0

4. List:
   • 3-5 specific STRENGTHS
   • 2-3 specific WEAKNESSES
   • ACTIONABLE feedback (be specific, not vague!)

5. Return ContentEvaluation with all details

Remember: Be critical but fair. Give scores that reflect real quality.
"""

    return prompt


# ============================================
# MODULE INFO
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AGENT 3: EVALUATOR AGENT")
    print("=" * 60)
    print("\nThis agent evaluates content quality:")
    print("  • Clear scoring criteria")
    print("  • Must improve on rewrites")
    print("  • Actionable feedback")
    print("  • Approval threshold: 7.0/10")
    print("\n" + "=" * 60)