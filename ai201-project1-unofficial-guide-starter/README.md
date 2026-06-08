# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
***The domain of my choice is information regarding the undergraduate experience at the University of California, Irvine. THe information from sources I've chosen span a range of topics from registration, housing resources, navigating difficult courses, etc. This knowledge isn't well known for students learning to live and study for the first time in their lives. A lot of the Reddit information is knowledge passed down from past students which alleviates a bit of the learning curve and builds a sense of community.***
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 |Reddit | Website|https://www.reddit.com/r/UCI/
| 2 |Reddit |Website |https://www.reddit.com/r/UCI/comments/1jckpkn/first_year_housing_scoop/
| 3 |Reddit |Website |https://www.reddit.com/r/UCI/comments/1jh388v/current_incoming_2029_students_faq_megathread/
| 4 |Reddit | Website|https://www.reddit.com/r/UCI/comments/w1ooph/how_to_request_assistance_in_a_time_of_crisis/
| 5 | Reddit| Website|https://www.reddit.com/r/UCI/comments/vfp0la/uci_housing_megathread_20222023/
| 6 |UCI Official Site|Website |https://www.admissions.uci.edu/study/majors-minors.php?type=Major
| 7 |Reddit | Website|https://www.reddit.com/r/UCI/comments/1d25n2j/
| 8 | Reddit|Website |https://www.reddit.com/r/UCI/comments/1d25n2j/comp_sci_majors_are_you_struggling_to_find_a_job/
| 9 | Reddit|Website |https://www.reddit.com/r/UCI/comments/194da57/why_are_cs_majors_so_gross/
| 10 |Reddit | Website|https://www.reddit.com/r/UCI/comments/1t57ayb/tips_for_prospective_undergraduate_cs_majors_at/
| 11 |Reddit |Website |https://www.reddit.com/r/UCI/comments/1sy66rb/uci_international_students_fall_2026_winter_2027/


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size: 200**

**Overlap 50**

**Why these choices fit your documents:Most of the information is extracted from medium to long length, opinion-based posts and a lot of the information to questions I garnered could be answered in about 1-3 sentences which approximately fits the size of 300 characters. I chose 50 as the overlap in case some sentences show connection or relevance to each other. 50 characters seems appropriate because it's approximately the size of a sentence so if it gets cut off or is related somehow to another chunk, any relevant information will not get lost.**

**Final chunk count: 163**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used: all-MiniLM-L6-v2**

**Production tradeoff reflection:In production, I would prioritize a balance between accuracy and latency. While all-MiniLM-L6-v2 is efficient for short to medium-length texts, I would consider a model with longer context length for better handling of long Reddit threads. If multilingual support is needed, I might explore alternatives like LaBSE. For niche communities, fine-tuning could be an option, but only if the performance gain justifies the additional cost and complexity.**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction: Prompt Template - You are an AI assistant. Answer the user's question using only the information in the provided documents. 
If the documents don't contain enough information to answer, say "I don't have enough information on that."**

**How source attribution is surfaced in the response: I included a list of URLS directly in the ingestion_pipeline.py**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Where can I find information regarding the majors and minors offered at UC Irvine? | You can find information regarding UCI's majors and minors offered at https://www.admissions.uci.edu/study/majors-minors.php?type=Major | You can find information regarding the majors and minors offered at UC Irvine on the Office of Undergraduate Admissions website, under the "Majors & Minors" section, or by using the filters on the UC Irvine website to explore 85-plus majors and 70-plus minors. Sources: https://www.a...(sources excluded for formatting purposes) | Relevant | Accurate |
| 2 | What are the differences between Middle Earth and Mesa Court Housing? | Middle Earth and Mesa Court are UC Irvine’s two primary first-year residential communities. While both provide excellent on-campus living experiences, they differ significantly in their vibe, social scene, dining halls, and location relative to classes. | The differences between Middle Earth and Mesa Court Housing are: 1. Room configuration: Mesa Court Towers have rooms for four people with a private bathroom, while the room configuration for Middle Earth Towers is not specified. 2. Student population: Middle Earth has more STEM majors. 3. Noise level: Middle Earth is quieter than Mesa Court. 4. Location: Middle Earth is located on the campus ring road and is close to the Engineering buildings. I don't have enough information on other potential differences, such as rates, floor plans, or community life. Sources: https://www.a...(sources excluded for formatting purposes) | Relevant | Accurate |
| 3 | What are some basic needs resources available to me at UCI? | Some basic needs resources available to UCI students include, but are not limited to, the UC Irvine Basic Needs Center, which offers a variety of services to UC Irvine students, regardless of immigration status, to help them meet their basic needs. From food pantry visits, CalFresh Application Assistance, to consultations with our social workers. We strive to offer support from a holistic approach.|I don't have enough information on that. | Relevant | Accurate | Relevant |
| 4 | [Insert question here] | I don't have enough information on that. | I don't have enough information on that. | Relevant | Accurate |
| 5 | [Insert question here] | I don't have enough information on that. | I don't have enough information on that. | Relevant | Accurate |


**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed: The last three failed because the retrieval failed due to Reddit sources being blocked by the server for requiring login.**

**What the system returned: The system correctly returned statements indicating the chatbot didn't know the answer as it was instructed to do so.**

**Root cause: Within the ingestion/chunking portion, the print statements in place showed that chunking was not successful because it could not access the URL**

**What you would change to fix it: I would choose easily accessible sources where scraping the text would be easier since a login was required or provide my own login credentials, which I chose not to do this time for security purposes.**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation: The specification helped me visualize the pipeline worked from ingestion and chunking to embedding and retrieval.**

**One way your implementation diverged from the spec, and why: Upon the first part of the chunking process, I realized quickly that the barriers to accessing the URLs I provided was a major issue so I provided new sources and altered the expected responses from questions.**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI: I started writing the skeleton of the ingestion pipeline based off my Lab 1 from Week 1 lecture then asked AI to help me debug. I was missing certain libraries and using the wrong method call for the Groq client.*
- *What it produced: I was instructed to install pip libraries such as BeautifulSoup4 to process the text and others as well as changed up my code for the generator which used the chat.completions.create method which I found from the API docs for the Groc API*
- *What I changed or overrode: I followed all the instructions/recommendations from the Copilot and Claude assistance so installing all the necessary libraries, using the API calls to generate a response, and ensuring all parts of the generation pipeline were connected.*

**Instance 2**

- *What I gave the AI: When I struggled with the chunking process, I realized I set it up to process PDFS like the Lab 1 as opposed to URLS so I asked Copilot to help me convert the existing code I had to scrape text from URLs I provided and clean up the text so the format was more readable.*
- *What it produced: See ingestion_pipeline.py for code reference*
- *What I changed or overrode: I kept almost all the code it provided and changed the chunk size from 300 -> 200 after seeing such a low number of chunks.*
