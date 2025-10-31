"""
Agent 6: Scheduler Agent
Schedules social media posts to Google Calendar at optimal times
"""

from agents import Agent, function_tool
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dataclasses import dataclass
from typing import List
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


# ============================================
# OUTPUT STRUCTURES
# ============================================

@dataclass
class ScheduledPost:
    """Single scheduled post information"""
    platform: str
    title: str
    scheduled_time: str
    calendar_link: str


@dataclass
class SchedulingResult:
    """Complete scheduling result for all posts"""
    scheduled_posts: List[ScheduledPost]
    success: bool
    message: str


# ============================================
# GOOGLE CALENDAR AUTHENTICATION
# ============================================

def authenticate_google_calendar():
    """Authenticate and return Google Calendar service"""
    SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "social-media-agent.json")
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        calendar_service = build("calendar", "v3", credentials=creds)
        return calendar_service
    except Exception as e:
        print(f"⚠️  Google Calendar authentication failed: {e}")
        return None


calendar_service = authenticate_google_calendar()


# ============================================
# CALENDAR TOOLS
# ============================================

@function_tool
def get_time_now_lagos():
    """
    Get the current time in Lagos, Nigeria timezone (Africa/Lagos, UTC+1)
    Returns datetime object in Lagos timezone
    """
    lagos_timezone = datetime.timezone(datetime.timedelta(hours=1))
    lagos_now = datetime.datetime.now(lagos_timezone)
    return lagos_now.isoformat()


@function_tool
def add_to_calendar(event_title: str, event_description: str, suggested_time: str):
    """
    Add event to Google Calendar at the specified time.

    Args:
        event_title: Title of the calendar event
        event_description: Full content/description
        suggested_time: ISO format datetime string

    Returns:
        Calendar event link or error message
    """
    if not calendar_service:
        return "Error: Google Calendar not authenticated"

    try:
        # Parse the suggested time
        suggested_time = datetime.datetime.fromisoformat(suggested_time)

        event = {
            'summary': event_title,
            'description': event_description,
            'start': {
                'dateTime': suggested_time.isoformat(),
                'timeZone': 'Africa/Lagos',
            },
            'end': {
                'dateTime': (suggested_time + datetime.timedelta(hours=1)).isoformat(),
                'timeZone': 'Africa/Lagos',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 60},
                    {'method': 'popup', 'minutes': 15},
                ],
            },
        }

        calendar_id = os.getenv("GOOGLE_CALENDAR_ID", "elosarah85@gmail.com")

        event_result = calendar_service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()

        event_link = event_result.get('htmlLink')
        print(f"   ✅ Scheduled {event_title}")
        return event_link

    except Exception as e:
        print(f"   ⚠️  Failed to schedule {event_title}: {e}")
        return f"Error: {str(e)[:100]}"


# ============================================
# SCHEDULER AGENT
# ============================================

scheduler_agent = Agent(
    name="Content Scheduling Agent",
    instructions="""You are a social media scheduling expert who schedules posts at optimal times.

PLATFORM-SPECIFIC BEST TIMES (Lagos Time, UTC+1):

- LinkedIn: Weekdays (Monday-Friday) 7-9 AM or 5-6 PM
- TikTok: Weekdays 8-10 AM or 6-8 PM; Weekends 10-11 AM
- Instagram: Weekdays 11 AM-2 PM or 7-9 PM; Weekends 10 AM-2 PM

YOUR TASK:

1. Get current Lagos time using get_time_now_lagos
2. For each platform, calculate the NEXT optimal posting time
3. Schedule each post using add_to_calendar

RULES:

- Schedule ONE event per platform
- Use optimal times for each platform
- If optimal time has passed today, schedule for tomorrow
- Space out posts (don't schedule all at same time)

EVENT FORMAT:

- Title: "[Platform] - [Topic]"
  Example: "LinkedIn Post - How to Learn with AI"

- Description: Include full content for easy copy-paste

Return a SchedulingResult with all scheduled posts and their calendar links.
""",
    model="gpt-4o-mini",
    tools=[get_time_now_lagos, add_to_calendar],
    output_type=SchedulingResult
)


# ============================================
# HELPER FUNCTION
# ============================================

def format_content_for_scheduling(topic: str, social_media: object) -> str:
    """
    Format social media content for scheduling.

    Args:
        topic: The content topic
        social_media: SocialMediaContent object

    Returns:
        Formatted prompt for scheduler agent
    """

    prompt = f"""Schedule these social media posts at optimal times: "{topic}"

=== POSTS TO SCHEDULE ===

1. TIKTOK POST
Platform: TikTok
Title: "TikTok - {topic}"
Content:
Hook: {social_media.tiktok_hook}

{social_media.tiktok_script}

CTA: {social_media.tiktok_cta}

---

2. LINKEDIN POST
Platform: LinkedIn
Title: "LinkedIn - {topic}"
Content:
{social_media.linkedin_hook}

{social_media.linkedin_body}

{social_media.linkedin_cta}

Hashtags: {' '.join(social_media.linkedin_hashtags)}

---

3. INSTAGRAM POST
Platform: Instagram
Title: "Instagram - {topic}"
Content:
{social_media.instagram_hook}

{social_media.instagram_body}

{social_media.instagram_cta}

Hashtags: {' '.join(social_media.instagram_hashtags)}

=== YOUR TASK ===

1. Get current Lagos time
2. Calculate next optimal posting time for each platform
3. Schedule each post to Google Calendar
4. Return SchedulingResult with all calendar links

Space out the posts appropriately - don't schedule all at once!
"""

    return prompt


# ============================================
# MODULE INFO
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AGENT 6: SCHEDULER AGENT")
    print("=" * 60)
    print("\nThis agent schedules posts to Google Calendar:")
    print("  • TikTok at optimal time")
    print("  • LinkedIn at optimal time")
    print("  • Instagram at optimal time")
    print("\nRequires:")
    print("  • social-media-agent.json (service account)")
    print("  • GOOGLE_CALENDAR_ID in .env")
    print("\nOptimal times (Lagos, UTC+1):")
    print("  • LinkedIn: 7-9 AM or 5-6 PM (weekdays)")
    print("  • TikTok: 8-10 AM or 6-8 PM (weekdays)")
    print("  • Instagram: 11 AM-2 PM or 7-9 PM (weekdays)")
    print("\nTo use this agent:")
    print("  from scheduler_agent import scheduler_agent")
    print("  from scheduler_agent import format_content_for_scheduling")
    print("\n" + "=" * 60)