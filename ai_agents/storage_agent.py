"""
Agent 5: Storage Agent
Saves master content and social media posts to Notion
"""

from agents import Agent, function_tool
from typing import List
from dataclasses import dataclass
import requests
import os
from dotenv import load_dotenv

load_dotenv()


# ============================================
# OUTPUT STRUCTURES
# ============================================

@dataclass
class StoredPost:
    """Single stored post information"""
    platform: str
    title: str
    notion_link: str


@dataclass
class StorageResult:
    """Complete storage result for all content"""
    master_content_link: str
    stored_posts: List[StoredPost]
    success: bool
    message: str


def clean_markdown(text: str) -> str:
    """Remove Markdown formatting for Notion"""
    import re

    # Remove markdown headers (##, ###, etc.)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # Remove bold/italic markers
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*([^\*]+)\*', r'\1', text)  # *italic*
    text = re.sub(r'__([^_]+)__', r'\1', text)  # __bold__
    text = re.sub(r'_([^_]+)_', r'\1', text)  # _italic_

    return text


# ============================================
# NOTION SAVE FUNCTION (WITH CHUNKING)
# ============================================

@function_tool
def save_to_notion(content: str, title: str, platform: str) -> str:
    """
    Save content to Notion with automatic chunking for long content.
    Splits content into multiple blocks to handle Notion's 2000 char limit.
    """
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        return "Error: Notion credentials not found in .env file"
    content = clean_markdown(content)

    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Split content into chunks (Notion's limit is 2000 chars per block)
    def chunk_content(text, max_chars=1900):
        """Split text into chunks, respecting paragraph boundaries"""
        chunks = []
        paragraphs = text.split('\n\n')
        current_chunk = ""

        for para in paragraphs:
            # If adding this paragraph keeps us under limit
            if len(current_chunk) + len(para) + 2 < max_chars:
                current_chunk += para + "\n\n"
            else:
                # Save current chunk
                if current_chunk:
                    chunks.append(current_chunk.strip())

                # If paragraph itself is too long, split it
                if len(para) > max_chars:
                    # Split by sentences
                    sentences = para.replace('. ', '.|').split('|')
                    temp = ""
                    for sentence in sentences:
                        if len(temp) + len(sentence) < max_chars:
                            temp += sentence
                        else:
                            if temp:
                                chunks.append(temp.strip())
                            temp = sentence
                    if temp:
                        current_chunk = temp + "\n\n"
                else:
                    current_chunk = para + "\n\n"

        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    # Split content into chunks
    content_chunks = chunk_content(content)

    # Create paragraph blocks for each chunk
    children_blocks = []
    for chunk in content_chunks:
        children_blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": chunk
                        }
                    }
                ]
            }
        })

    # Notion max 100 blocks per request
    children_blocks = children_blocks[:100]

    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": title[:200]
                        }
                    }
                ]
            },
            "Platform": {
                "select": {
                    "name": platform
                }
            },
            "Status": {
                "select": {
                    "name": "Draft"
                }
            }
        },
        "children": children_blocks
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            page_id = response.json()["id"]
            notion_link = f"https://www.notion.so/{page_id.replace('-', '')}"
            print(f"   ✅ Saved {platform} to Notion ({len(content_chunks)} blocks)")
            return notion_link
        else:
            print(f"   ⚠️  Notion API error for {platform}: {response.status_code}")
            return f"Error: {response.text[:100]}"

    except Exception as e:
        print(f"   ⚠️  Notion connection failed for {platform}: {e}")
        return f"Connection failed: {str(e)[:100]}"


# ============================================
# STORAGE AGENT
# ============================================

storage_agent = Agent(
    name="Content Storage Agent",
    instructions="""You are a content storage specialist who saves content to Notion.

Your job:
1. Save the master content (blog post) to Notion
2. Save each social media post to Notion
3. Use clear, descriptive titles for each piece

Title Format:
- Master content: "[Topic] - Master Content"
- TikTok: "[Topic] - TikTok Script"
- LinkedIn: "[Topic] - LinkedIn Post"
- Instagram: "[Topic] - Instagram Caption"

For each piece of content:
1. Create a clear title
2. Use save_to_notion tool with the content, title, and platform
3. Return the Notion link

Be organized and confirm each save was successful.
Return a StorageResult with all the links.
""",
    model="gpt-4o-mini",
    tools=[save_to_notion],
    output_type=StorageResult
)


# ============================================
# HELPER FUNCTION
# ============================================

def format_content_for_storage(topic: str, master_content: str, social_media: object) -> str:
    """
    Format all content for storage agent.
    """

    prompt = f"""Save all content to Notion for topic: "{topic}"

=== CONTENT TO SAVE ===

1. MASTER CONTENT (Blog Post)
Platform: Blog
Title: "{topic} - Master Content"
Content:
{master_content}

---

2. TIKTOK SCRIPT
Platform: TikTok
Title: "{topic} - TikTok Script"
Content:
Hook: {social_media.tiktok_hook}

{social_media.tiktok_script}

CTA: {social_media.tiktok_cta}

---

3. LINKEDIN POST
Platform: LinkedIn
Title: "{topic} - LinkedIn Post"
Content:
{social_media.linkedin_hook}

{social_media.linkedin_body}

{social_media.linkedin_cta}

Hashtags: {' '.join(social_media.linkedin_hashtags)}

---

4. INSTAGRAM CAPTION
Platform: Instagram
Title: "{topic} - Instagram Caption"
Content:
{social_media.instagram_hook}

{social_media.instagram_body}

{social_media.instagram_cta}

Hashtags: {' '.join(social_media.instagram_hashtags)}

=== YOUR TASK ===

Use save_to_notion to save each piece:
1. Save master content with platform="Blog"
2. Save TikTok with platform="TikTok"
3. Save LinkedIn with platform="LinkedIn"
4. Save Instagram with platform="Instagram"

Return the StorageResult with all links.
"""

    return prompt


# ============================================
# MODULE INFO
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AGENT 5: STORAGE AGENT (WITH CHUNKING)")
    print("=" * 60)
    print("\nThis agent saves content to Notion:")
    print("  • Handles long content (splits into chunks)")
    print("  • No 2000 char limit issues")
    print("  • Saves complete blog posts")
    print("\n" + "=" * 60)

