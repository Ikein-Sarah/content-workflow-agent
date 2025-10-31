"""
AI Content Workflow Agent - Streamlit App
Modern/Minimalist Design with Green/Teal Theme
"""


# Import your agents
from ai_agents import (
    research_agent,
    master_content_agent,
    format_research_for_master_content,
    evaluator_agent,
    format_content_for_evaluation,
    social_media_agent,
    format_master_content_for_social,
    storage_agent,
    format_content_for_storage,
    scheduler_agent,
    format_content_for_scheduling
)


import streamlit as st
import asyncio
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import hashlib
from agents import Runner

load_dotenv()

# ============================================
# PASSWORD CONFIGURATION
# ============================================

# Set your password here (or in Streamlit secrets)
APP_PASSWORD = os.getenv("APP_PASSWORD", "Tina2025")


def check_password():
    """Returns True if user entered correct password"""

    def password_entered():
        """Checks whether password entered is correct"""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == hashlib.sha256(
                APP_PASSWORD.encode()).hexdigest():
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # First run, show input for password
    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <h1 style="color: #10b981; font-size: 3rem;">🎯 AI Content Workflow Agent</h1>
            <p style="color: #64748b; font-size: 1.2rem; margin-top: 1rem;">
                This app is password protected for hackathon judges.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Enter Password",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Enter hackathon password"
            )
            st.info("💡 Password provided to hackathon judges only")
        return False

    # Password incorrect, show input + error
    elif not st.session_state["password_correct"]:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <h1 style="color: #10b981; font-size: 3rem;">🎯 AI Content Workflow Agent</h1>
            <p style="color: #64748b; font-size: 1.2rem; margin-top: 1rem;">
                This app is password protected for hackathon judges.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Enter Password",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Enter hackathon password"
            )
            st.error("❌ Incorrect password. Please try again.")
        return False
    else:
        # Password correct
        return True


# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="AI Content Workflow Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary: #10b981;
        --secondary: #14b8a6;
        --background: #f8fafc;
        --card: #ffffff;
        --text: #1e293b;
        --text-light: #64748b;
        --border: #e2e8f0;
        --success: #22c55e;
        --error: #ef4444;
        --warning: #f59e0b;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container */
    .main {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 100%);
        padding: 2rem;
    }

    /* Header */
    .app-header {
        background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .app-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }

    .app-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }

    /* Cards */
    .content-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }

    .card-title {
        color: var(--primary);
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #10b981 0%, #14b8a6 100%);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--primary);
        font-size: 2rem;
        font-weight: 700;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        background: white;
        border: 1px solid var(--border);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
        color: white;
    }

    /* Text area */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid var(--border);
        padding: 1rem;
    }

    .stTextArea textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }

    /* Score badge */
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
    }

    .score-high {
        background: #d1fae5;
        color: #065f46;
    }

    .score-medium {
        background: #fef3c7;
        color: #92400e;
    }

    .score-low {
        background: #fee2e2;
        color: #991b1b;
    }

    /* Success/Error messages */
    .stSuccess {
        background: #d1fae5;
        color: #065f46;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
    }

    .stError {
        background: #fee2e2;
        color: #991b1b;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
    }

    /* Text input */
    .stTextInput input {
        border-radius: 8px;
        border: 2px solid var(--border);
        padding: 0.75rem;
    }

    .stTextInput input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# HELPER FUNCTIONS
# ============================================

async def run_with_retry(agent, input_text, timeout=180):
    """Run agent with retry logic"""
    for attempt in range(3):
        try:
            result = await asyncio.wait_for(
                Runner.run(agent, input=input_text),
                timeout=timeout
            )
            if result and hasattr(result, 'final_output'):
                return result
        except asyncio.TimeoutError:
            if attempt < 2:
                await asyncio.sleep(2 ** attempt)
            else:
                raise
        except Exception as e:
            if attempt < 2:
                await asyncio.sleep(2 ** attempt)
            else:
                raise
    return None


def get_score_class(score):
    """Get CSS class based on score"""
    if score >= 7:
        return "score-high"
    elif score >= 5:
        return "score-medium"
    else:
        return "score-low"


# ============================================
# MAIN WORKFLOW
# ============================================

async def run_workflow(topic: str, progress_callback):
    """Run the complete workflow with progress updates"""

    # Step 1: Research
    progress_callback(0.1, "🔍 Researching topic...")
    try:
        research_result = await run_with_retry(
            research_agent,
            f"Research this topic comprehensively: {topic}",
            timeout=180
        )
        if not research_result:
            return None, "Research failed"

        raw_output = research_result.final_output.strip()
        if raw_output.startswith('```json'):
            raw_output = raw_output.replace('```json', '').replace('```', '').strip()

        research_data = json.loads(raw_output)
        progress_callback(0.25, f"✅ Research complete ({len(research_data.get('sources', []))} sources)")
    except Exception as e:
        return None, f"Research failed: {str(e)}"

    # Step 2 & 3: Write + Evaluate
    progress_callback(0.3, "✍️ Writing master content...")
    best_content = None
    best_evaluation = None
    best_score = 0
    prompt = format_research_for_master_content(research_data)

    for attempt in range(1, 4):
        try:
            progress_callback(0.3 + (attempt * 0.1), f"✍️ Writing attempt {attempt}/3...")

            content_result = await run_with_retry(master_content_agent, prompt, timeout=150)
            if not content_result:
                continue
            master_content = content_result.final_output

            progress_callback(0.4 + (attempt * 0.1), f"📊 Evaluating attempt {attempt}/3...")

            eval_prompt = format_content_for_evaluation(master_content, research_data)
            eval_result = await run_with_retry(evaluator_agent, eval_prompt, timeout=120)
            if not eval_result:
                continue
            evaluation = eval_result.final_output

            if evaluation.overall_score > best_score:
                best_score = evaluation.overall_score
                best_content = master_content
                best_evaluation = evaluation

            if evaluation.approved:
                break
            else:
                prompt = f"{prompt}\n\nPREVIOUS FEEDBACK:\n{evaluation.specific_feedback}\n\nRewrite addressing all issues."

        except Exception as e:
            continue

    if not best_content:
        return None, "Failed to generate content"

    progress_callback(0.65, f"✨ Content approved (Score: {best_evaluation.overall_score}/10)")

    # Step 4: Social Media
    progress_callback(0.7, "📱 Creating social media content...")
    try:
        social_prompt = format_master_content_for_social(best_content, topic)
        social_result = await run_with_retry(social_media_agent, social_prompt, timeout=120)
        social_content = social_result.final_output if social_result else None
    except Exception as e:
        social_content = None

    progress_callback(0.8, "✅ Social media content created")

    # Step 5: Storage
    storage_data = None
    if social_content:
        progress_callback(0.85, "💾 Saving to Notion...")
        try:
            storage_prompt = format_content_for_storage(topic, best_content, social_content)
            storage_result = await run_with_retry(storage_agent, storage_prompt, timeout=120)
            storage_data = storage_result.final_output if storage_result else None
        except Exception as e:
            storage_data = None

    # Step 6: Scheduling
    schedule_data = None
    if social_content:
        progress_callback(0.92, "📅 Scheduling posts...")
        try:
            schedule_prompt = format_content_for_scheduling(topic, social_content)
            schedule_result = await run_with_retry(scheduler_agent, schedule_prompt, timeout=120)
            schedule_data = schedule_result.final_output if schedule_result else None
        except Exception as e:
            schedule_data = None

    progress_callback(1.0, "✅ Workflow complete!")

    return {
        "topic": topic,
        "research": research_data,
        "master_content": best_content,
        "evaluation": best_evaluation,
        "social_media": social_content,
        "storage": storage_data,
        "schedule": schedule_data
    }, None


async def regenerate_social_media(master_content: str, topic: str):
    """Regenerate social media content only"""
    try:
        social_prompt = format_master_content_for_social(master_content, topic)
        social_result = await run_with_retry(social_media_agent, social_prompt, timeout=120)
        return social_result.final_output if social_result else None
    except Exception as e:
        return None


# ============================================
# STREAMLIT APP
# ============================================

def main():
    # Check password first
    if not check_password():
        return

    # Header
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">🎯 AI Content Workflow Agent</h1>
        <p class="app-subtitle">From Idea to Published Content in 5 Minutes</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'generating' not in st.session_state:
        st.session_state.generating = False

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ App Info")

        # API Status
        st.markdown("**API Status:**")
        apis = {
            "OpenAI": os.getenv("OPENAI_API_KEY"),
            "Tavily": os.getenv("TAVILY_API_KEY"),
            "Notion": os.getenv("NOTION_API_KEY"),
            "Google Calendar": os.path.exists("social-media-agent.json")
        }

        for api, status in apis.items():
            if status:
                st.success(f"✅ {api}")
            else:
                st.error(f"❌ {api}")

        st.markdown("---")
        st.markdown("### 📊 Features")
        st.markdown("""
        - ✅ AI-Powered Research
        - ✅ Smart Content Writing
        - ✅ Quality Evaluation
        - ✅ Social Media Adaptation
        - ✅ Notion Integration
        - ✅ Calendar Scheduling
        """)

        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Be specific with your topic
        - Include target audience if relevant
        - Let the AI work through 3 attempts
        - Review and edit before publishing
        """)

        st.markdown("---")
        st.markdown("### 🔒 Security")
        st.info("This app is password-protected and will be taken down after the hackathon.")

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📝 Enter Your Content Topic")
        topic = st.text_input(
            "Enter your topic",
            placeholder="E.g., How to use AI to automate your content workflow",
            label_visibility="collapsed"
        )

        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            generate_button = st.button("🚀 Generate Content", use_container_width=True,
                                        disabled=st.session_state.generating)
        with col_btn2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)

    with col2:
        st.markdown("### 📈 Quick Stats")
        if st.session_state.result:
            score = st.session_state.result['evaluation'].overall_score
            st.metric("Quality Score", f"{score}/10")
            st.metric("Word Count", len(st.session_state.result['master_content'].split()))
        else:
            st.info("Generate content to see stats")

    # Clear button logic
    if clear_button:
        st.session_state.result = None
        st.rerun()

    # Generate button logic
    if generate_button and topic:
        st.session_state.generating = True

        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(value, message):
            progress_bar.progress(value)
            status_text.info(message)

        # Run workflow
        try:
            result, error = asyncio.run(run_workflow(topic, update_progress))

            if error:
                st.error(f"❌ {error}")
            elif result:
                st.session_state.result = result
                st.success("✅ Content generated successfully!")
                progress_bar.empty()
                status_text.empty()
                st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        finally:
            st.session_state.generating = False

    # Display results
    if st.session_state.result:
        result = st.session_state.result

        st.markdown("---")

        # Evaluation Summary
        st.markdown("### 📊 Evaluation Summary")
        eval_data = result['evaluation']

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Authenticity", f"{eval_data.authenticity_score}/10")
        col2.metric("Quality", f"{eval_data.quality_score}/10")
        col3.metric("Completeness", f"{eval_data.completeness_score}/10")
        col4.metric("Depth", f"{eval_data.depth_score}/10")

        # Overall score badge
        score_class = get_score_class(eval_data.overall_score)
        st.markdown(f"""
        <div style="text-align: center; margin: 1rem 0;">
            <span class="score-badge {score_class}">
                Overall Score: {eval_data.overall_score}/10
                {'✅ APPROVED' if eval_data.approved else '⚠️ NEEDS WORK'}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Strengths and Weaknesses
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("✅ Strengths"):
                for strength in eval_data.strengths:
                    st.write(f"• {strength}")
        with col2:
            with st.expander("⚠️ Areas for Improvement"):
                for weakness in eval_data.weaknesses:
                    st.write(f"• {weakness}")

        st.markdown("---")

        # Content Tabs
        tabs = st.tabs(["📄 Master Content", "📱 Social Media", "💾 Storage", "📅 Schedule"])

        # Tab 1: Master Content
        with tabs[0]:
            st.markdown("### Master Content (Blog Post)")

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**Word Count:** {len(result['master_content'].split())} words")
            with col2:
                if st.button("📋 Copy to Clipboard"):
                    st.code(result['master_content'])
                    st.success("Copied!")
            with col3:
                st.download_button(
                    label="⬇️ Download",
                    data=result['master_content'],
                    file_name=f"{result['topic'][:30]}_master_content.txt",
                    mime="text/plain"
                )

            st.text_area(
                "Master content",
                value=result['master_content'],
                height=400,
                label_visibility="collapsed"
            )

        # Tab 2: Social Media
        with tabs[1]:
            st.markdown("### Social Media Content")

            if result['social_media']:
                social = result['social_media']

                # Regenerate button
                if st.button("🔄 Regenerate Social Media Content", use_container_width=True):
                    with st.spinner("Regenerating..."):
                        new_social = asyncio.run(regenerate_social_media(
                            result['master_content'],
                            result['topic']
                        ))
                        if new_social:
                            st.session_state.result['social_media'] = new_social
                            st.success("✅ Regenerated!")
                            st.rerun()
                        else:
                            st.error("❌ Regeneration failed")

                st.markdown("---")

                # TikTok
                with st.expander("🎥 TikTok/Reels Script", expanded=True):
                    st.markdown(f"**Hook:** {social.tiktok_hook}")
                    st.markdown("**Script:**")
                    st.write(social.tiktok_script)
                    st.markdown(f"**CTA:** {social.tiktok_cta}")

                    st.download_button(
                        "Download TikTok Script",
                        data=f"Hook: {social.tiktok_hook}\n\n{social.tiktok_script}\n\nCTA: {social.tiktok_cta}",
                        file_name="tiktok_script.txt"
                    )

                # LinkedIn
                with st.expander("💼 LinkedIn Post", expanded=True):
                    st.markdown(f"**Hook:** {social.linkedin_hook}")
                    st.write(social.linkedin_body)
                    st.markdown(f"**CTA:** {social.linkedin_cta}")
                    st.markdown(f"**Hashtags:** {' '.join(social.linkedin_hashtags)}")

                    st.download_button(
                        "Download LinkedIn Post",
                        data=f"{social.linkedin_hook}\n\n{social.linkedin_body}\n\n{social.linkedin_cta}\n\n{' '.join(social.linkedin_hashtags)}",
                        file_name="linkedin_post.txt"
                    )

                # Instagram
                with st.expander("📸 Instagram Caption", expanded=True):
                    st.markdown(f"**Hook:** {social.instagram_hook}")
                    st.write(social.instagram_body)
                    st.markdown(f"**CTA:** {social.instagram_cta}")
                    st.markdown(f"**Hashtags:**")
                    st.write(' '.join(social.instagram_hashtags))

                    st.download_button(
                        "Download Instagram Caption",
                        data=f"{social.instagram_hook}\n\n{social.instagram_body}\n\n{social.instagram_cta}\n\n{' '.join(social.instagram_hashtags)}",
                        file_name="instagram_caption.txt"
                    )
            else:
                st.warning("Social media content not available")

        # Tab 3: Storage
        with tabs[2]:
            st.markdown("### Notion Storage")

            if result.get('storage') and result['storage'].success:
                st.success("✅ Content saved to Notion!")

                # Master content link
                st.markdown("**📄 Blog Post:**")
                st.markdown(f"[Open in Notion]({result['storage'].master_content_link})")

                st.markdown("**📱 Social Media Posts:**")
                for post in result['storage'].stored_posts:
                    st.markdown(f"• {post.platform}: [Open in Notion]({post.notion_link})")
            else:
                st.warning("Content not saved to Notion (check API credentials)")

        # Tab 4: Schedule
        with tabs[3]:
            st.markdown("### Calendar Schedule")

            if result.get('schedule') and result['schedule'].success:
                st.success("✅ Posts scheduled to Google Calendar!")

                for post in result['schedule'].scheduled_posts:
                    with st.expander(f"📅 {post.platform} - {post.scheduled_time}"):
                        st.markdown(f"**Title:** {post.title}")
                        st.markdown(f"**Scheduled:** {post.scheduled_time}")
                        st.markdown(f"[Open in Calendar]({post.calendar_link})")
            else:
                st.warning("Posts not scheduled (check Google Calendar credentials)")


if __name__ == "__main__":
    main()