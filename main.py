"""
Complete Workflow: Research → Write → Evaluate → Social Media → Store → Schedule
"""

import asyncio
import json
from agents import Runner
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


async def run_workflow(topic: str):
    """Run the complete workflow"""

    print(f"\n🚀 Creating content about: {topic}\n")

    # Step 1: Research
    print("🔍 Researching...")
    try:
        research_result = await run_with_retry(research_agent, f"Research this topic comprehensively: {topic}", timeout=180)
        if not research_result:
            return None
        research_data = json.loads(research_result.final_output)
        print(f"✅ Research complete ({len(research_data.get('sources', []))} sources)\n")
    except Exception as e:
        print(f"❌ Research failed: {e}")
        return None

    # Step 2 & 3: Write + Evaluate Loop
    print("✍️  Writing content...")
    best_content = None
    best_evaluation = None
    best_score = 0
    prompt = format_research_for_master_content(research_data)

    for attempt in range(1, 4):
        try:
            content_result = await run_with_retry(master_content_agent, prompt, timeout=150)
            if not content_result:
                continue
            master_content = content_result.final_output

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
                print(f"✅ Content approved (Score: {evaluation.overall_score}/10)\n")
                break
            else:
                print(f"📊 Attempt {attempt}: {evaluation.overall_score}/10 - Improving...")
                prompt = f"{prompt}\n\nPREVIOUS FEEDBACK:\n{evaluation.specific_feedback}\n\nRewrite addressing all issues."
        except Exception as e:
            print(f"⚠️  Attempt {attempt} failed: {e}")
            continue

    if not best_content:
        print("❌ Failed to generate content")
        return None

    print(f"✨ Final Score: {best_evaluation.overall_score}/10\n")

    # Step 4: Social Media
    print("📱 Repurposing for social media...")
    try:
        social_prompt = format_master_content_for_social(best_content, topic)
        social_result = await run_with_retry(social_media_agent, social_prompt, timeout=120)
        social_content = social_result.final_output if social_result else None
        if social_content:
            print("✅ Social media content created\n")
        else:
            print("⚠️  Social media failed, skipping storage/scheduling\n")
            return {"topic": topic, "master_content": best_content, "evaluation": best_evaluation, "social_media": None}
    except Exception as e:
        print(f"⚠️  Social media failed: {e}\n")
        return {"topic": topic, "master_content": best_content, "evaluation": best_evaluation, "social_media": None}

    # Step 5: Storage
    print("💾 Saving to Notion...")
    try:
        storage_prompt = format_content_for_storage(topic, best_content, social_content)
        storage_result = await run_with_retry(storage_agent, storage_prompt, timeout=120)
        storage_data = storage_result.final_output if storage_result else None
        if storage_data and storage_data.success:
            print("✅ Content saved to Notion\n")
        else:
            print("⚠️  Storage failed\n")
            storage_data = None
    except Exception as e:
        print(f"⚠️  Storage failed: {e}\n")
        storage_data = None

    # Step 6: Scheduling
    print("📅 Scheduling posts...")
    try:
        schedule_prompt = format_content_for_scheduling(topic, social_content)
        schedule_result = await run_with_retry(scheduler_agent, schedule_prompt, timeout=120)
        schedule_data = schedule_result.final_output if schedule_result else None
        if schedule_data and schedule_data.success:
            print("✅ Posts scheduled\n")
        else:
            print("⚠️  Scheduling failed\n")
            schedule_data = None
    except Exception as e:
        print(f"⚠️  Scheduling failed: {e}\n")
        schedule_data = None

    return {
        "topic": topic,
        "master_content": best_content,
        "evaluation": best_evaluation,
        "social_media": social_content,
        "storage": storage_data,
        "schedule": schedule_data
    }


async def main():
    """Main entry point"""

    topic = input("\nEnter your topic: ").strip()
    if not topic:
        print("❌ No topic provided")
        return

    try:
        result = await run_workflow(topic)
        if not result:
            print("\n❌ Workflow failed")
            return

        # Save master content
        with open("output_master_content.txt", "w", encoding="utf-8") as f:
            f.write(f"TOPIC: {result['topic']}\n{'=' * 60}\n\n")
            f.write(result['master_content'])
        print(f"\n💾 Master content: output_master_content.txt")

        # Save social media
        if result.get('social_media'):
            social = result['social_media']
            with open("output_social_media.txt", "w", encoding="utf-8") as f:
                f.write(f"SOCIAL MEDIA: {result['topic']}\n{'=' * 60}\n\n")
                f.write(
                    f"TIKTOK\n{'-' * 60}\n{social.tiktok_hook}\n\n{social.tiktok_script}\n\n{social.tiktok_cta}\n\n")
                f.write(
                    f"LINKEDIN\n{'-' * 60}\n{social.linkedin_hook}\n\n{social.linkedin_body}\n\n{social.linkedin_cta}\n\n{' '.join(social.linkedin_hashtags)}\n\n")
                f.write(
                    f"INSTAGRAM\n{'-' * 60}\n{social.instagram_hook}\n\n{social.instagram_body}\n\n{social.instagram_cta}\n\n{' '.join(social.instagram_hashtags)}\n")
            print(f"💾 Social media: output_social_media.txt")

        # Save Notion links
        if result.get('storage') and result['storage'].success:
            with open("output_notion_links.txt", "w", encoding="utf-8") as f:
                f.write(f"NOTION LINKS: {result['topic']}\n{'=' * 60}\n\n")
                for post in result['storage'].stored_posts:
                    f.write(f"{post.platform}: {post.notion_link}\n")
            print(f"💾 Notion links: output_notion_links.txt")

            # Print links to console
            print(f"\n📎 Notion Links:")
            for post in result['storage'].stored_posts:
                print(f"   {post.platform}: {post.notion_link}")

        # Save Calendar links
        if result.get('schedule') and result['schedule'].success:
            with open("output_calendar_links.txt", "w", encoding="utf-8") as f:
                f.write(f"CALENDAR LINKS: {result['topic']}\n{'=' * 60}\n\n")
                for post in result['schedule'].scheduled_posts:
                    f.write(f"{post.platform} ({post.scheduled_time}): {post.calendar_link}\n")
            print(f"💾 Calendar links: output_calendar_links.txt")

            # Print links to console
            print(f"\n📅 Calendar Links:")
            for post in result['schedule'].scheduled_posts:
                print(f"   {post.platform} @ {post.scheduled_time}")
                print(f"   {post.calendar_link}")

        # Summary
        print(f"\n✨ Complete!")
        print(f"📊 Quality: {result['evaluation'].overall_score}/10")
        print(f"📝 Words: {len(result['master_content'].split())}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())