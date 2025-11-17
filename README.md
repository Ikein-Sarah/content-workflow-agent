# 🎯 AI Content Workflow Agent

Transform one topic into complete, multi-platform content in 5 minutes.

**Live Demo:** [https://content-workflow-agent.streamlit.app](https://content-workflow-agent.streamlit.app/)  
**Password:** `undisclosed` **

---

##  What Does This Do?

This app takes **one topic** and automatically:

1. ✅ Researches it across the web
2. ✅ Writes a 1000-1500 word blog post
3. ✅ Creates a TikTok script
4. ✅ Creates a LinkedIn post
5. ✅ Creates an Instagram caption
6. ✅ Saves everything to Notion
7. ✅ Schedules posts to Google Calendar

**All in under 5 minutes.** No manual work required.

---

## 🎬 Demo Video

*(https://drive.google.com/file/d/1l8fgp7O1P7Br5zmDdGA2i8rxZ9YZ2AAF/view?usp=drive_link)*

---

## ⚡ Quick Start

### Option 1: Use the Live App (Easiest)

1. Visit: [https://content-workflow-agent.streamlit.app/](https://content-workflow-agent.streamlit.app/)
2. Enter password: ``
3. Type your topic (e.g., "How to learn coding fast with AI")
4. Click **Generate Content**
5. Wait 2-3 minutes
6. Download your content!

### Option 2: Run It Locally

**Step 1: Clone this repo**
```bash
git clone https://github.com/Ikein-Sarah/content-workflow-agent.git
cd content-workflow-agent
```

**Step 2: Install requirements**
```bash
pip install -r requirements.txt
```

**Step 3: Add your API keys**

Create a file called `.env` and add:
```
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
NOTION_API_KEY=your-notion-key
NOTION_DATABASE_ID=your-database-id
GOOGLE_CALENDAR_ID=your-email@gmail.com
APP_PASSWORD=your-password
```

Also add your Google service account file as `social-media-agent.json`

**Step 4: Run the app**
```bash
streamlit run streamlit_app.py
```

Open your browser to `http://localhost:8501`

---

##  API Keys You Need

You'll need accounts for these services:

| Service | What It's For | Where to Get It | Cost |
|---------|---------------|-----------------|------|
| **OpenAI** | AI content generation | [platform.openai.com](https://platform.openai.com) | ~$0.28 per run |
| **Tavily** | Web research | [tavily.com](https://tavily.com) | Free tier available |
| **Notion** | Save content | [notion.so/my-integrations](https://notion.so/my-integrations) | Free |
| **Google Calendar** | Schedule posts | [console.cloud.google.com](https://console.cloud.google.com) | Free |

<details>
<summary>📖 Click here for detailed setup instructions</summary>

### OpenAI Setup
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to API Keys
4. Create new key
5. Copy it to your `.env` file

### Tavily Setup
1. Go to [tavily.com](https://tavily.com)
2. Sign up for free
3. Get your API key
4. Copy it to your `.env` file

### Notion Setup
1. Go to [notion.so/my-integrations](https://notion.so/my-integrations)
2. Click "New integration"
3. Give it a name
4. Copy the "Internal Integration Token"
5. Create a new database in Notion
6. Click "..." → "Add connections" → Select your integration
7. Copy the database ID from the URL
8. Add both to your `.env` file

### Google Calendar Setup
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project
3. Enable "Google Calendar API"
4. Go to "Credentials" → "Create Credentials" → "Service Account"
5. Download the JSON key file
6. Rename it to `social-media-agent.json`
7. Put it in your project folder
8. Share your Google Calendar with the service account email

</details>

---

##  How It Works

The system uses **6 AI agents** that work together:
```
Your Topic
    ↓
[1. Research Agent] → Searches the web for information
    ↓
[2. Writer Agent] → Writes a blog post in your voice
    ↓
[3. Evaluator Agent] → Scores quality (needs 7/10 to pass)
    ↓ (if approved)
[4. Social Media Agent] → Creates TikTok, LinkedIn, Instagram versions
    ↓
[5. Storage Agent] → Saves to Notion
    ↓
[6. Scheduler Agent] → Adds to Google Calendar
    ↓
Done! ✅
```

**Total time: 2-3 minutes**

---

## 📸 Screenshots

**Main Interface:**

![Main Interface](https://github.com/user-attachments/assets/1d5d018a-d545-4fb4-b32b-c4e8ede19c34)



**Generated Content:**

![Content 1](https://github.com/user-attachments/assets/d99f3252-1952-44d8-843a-df85d2370be2)


![Content 2](https://github.com/user-attachments/assets/09a584fc-5b7c-47a5-b589-3e5b0ff993e0)


![Content 3](https://github.com/user-attachments/assets/7513eed4-c054-428e-86d4-fbc13c5d8f94)



**Evaluation Scores:**


![Evaluation](https://github.com/user-attachments/assets/dbae4c5d-d1f1-4d78-bb92-d83f96fb7fb4)

---

##  What's Inside
```
content-workflow-agent/
│
├── streamlit_app.py           ← Main web app
├── main.py                    ← Command-line version
├── requirements.txt           ← Python packages needed
│
├── ai_agents/                 ← The 6 AI agents
│   ├── research_agent.py      ← Does web research
│   ├── writer_agent.py        ← Writes blog posts
│   ├── evaluator_agent.py     ← Scores content quality
│   ├── social_media_agent.py  ← Creates social posts
│   ├── storage_agent.py       ← Saves to Notion
│   └── scheduler_agent.py     ← Schedules to calendar
│
└── writing_samples/           ← Your writing style examples
    └── creator_samples.txt
```

---

## 📊 Example Output

**Input:**
```
Topic: "How to learn anything fast with AI"
```

**Output:**

✅ **Blog Post**
- 1,083 words
- Quality Score: 7.7/10
- Includes research, examples, and actionable steps

✅ **TikTok Script**
- 60-second format
- Hook, script, and call-to-action

✅ **LinkedIn Post**
- Professional tone
- 5 relevant hashtags
- Engagement-focused

✅ **Instagram Caption**
- Conversational tone
- 10 relevant hashtags
- Story-driven

✅ **All saved to Notion** with links

✅ **All scheduled** to Google Calendar at optimal times

---

##  Features

### 🎯 What Makes This Special

- **Voice Matching:** Learns from your writing samples to sound like YOU
- **Self-Improving:** Tries up to 3 times with feedback until it's good enough
- **Multi-Platform:** One topic → 4 pieces of optimized content
- **Smart Scheduling:** Posts at the best times for each platform
- **Quality Control:** Won't publish bad content (needs 7/10 score minimum)

###  Optimal Posting Times

The scheduler automatically picks the best times:

- **TikTok:** Weekdays 8-10 AM or 6-8 PM
- **LinkedIn:** Weekdays 7-9 AM or 5-6 PM
- **Instagram:** Weekdays 11 AM-2 PM or 7-9 PM

*(All times in Lagos/Nigeria timezone)*

---

##  Tech Stack

Built with:
- **Python 3.11**
- **Streamlit** (web interface)
- **OpenAI GPT-4o** (AI brains)
- **Tavily API** (research)
- **Notion API** (storage)
- **Google Calendar API** (scheduling)

---

##  What I Learned

Building this project taught me:
- How to build multi-agent AI systems
- Working with multiple APIs
- Prompt engineering for consistent quality
- Deploying AI apps to production
- Managing API costs and rate limits

---

##  Known Issues

- Takes 2-3 minutes (not instant)
- Only works in English
- Requires paid OpenAI account ($0.28 per run)
- Only supports 3 social platforms (no Twitter/X yet)

---

##  Future Plans

Things I want to add:

- [ ] Twitter/X support
- [ ] Generate images with DALL-E
- [ ] Multiple languages
- [ ] Analytics dashboard
- [ ] A/B test different versions
- [ ] Direct publishing (not just scheduling)
- [ ] YouTube script generation
- [ ] Email newsletter format

---

##  Cost Breakdown

Per content generation:
- OpenAI API: ~$0.28
- Tavily API: Free
- Notion: Free
- Google Calendar: Free

**Total: ~$0.28 per topic**

*(Costs can vary based on content length and complexity)*

---

##  Contributing

Want to improve this? Here's how:

1. Fork this repo
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

##  License

This project is open source and available under the MIT License.

---

##  About Me

**Ikein Sarah**

I built this for [1M Celebration Hackathon] 2025 to solve my own problem: spending too much time creating content for multiple platforms.

- LinkedIn: [www.linkedin.com/in/ikein-sarah-51b664224
]
- Email: elosarah85@gmail.com
- GitHub: [https://github.com/Ikein-Sarah/]

---

##  Acknowledgments

Special thanks to:
- **OpenAI** for GPT-4 and the Agents SDK
- **Tavily** for the research API
- **Notion** for the storage integration
- **Streamlit** for making deployment easy
- **[1M Celebration Hackathon]** for the opportunity

---

## Support

If you found this helpful:
- ⭐ Star this repo
- 🍴 Fork it for your own use
- 📢 Share it with others
- 💬 Leave feedback in Issues

---

## 📞 Questions?

Have questions or found a bug?

- Open an [Issue](https://github.com/Ikein-Sarah/content-workflow-agent/issues)
- Email me: elosarah85@gmail.com
- DM me on [LinkedIn](www.linkedin.com/in/ikein-sarah-51b664224)

---

