# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  1. Pressing Enter does not apply the input.
  2. The number range of different difficulty level in the info section does not correspond with that in the side bar, so does the secrete number.
  3. When guessing a number, the number is not shown in the developer debug info history immediately after click submit, but only shown at nect click.
  4. The hints for guessing is converse – if the user inputs a lower number, it prompts the user to go hihger, and vice versa.
  5. The New Game button does not really refresh and starts a new game. All previous record persists.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - used Claude Code.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - Claude pointed out that the shown number of attemps is off by one. After Claude fixed it, I restarted the application and checked the number is corrected.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
    - Not this time.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - Through both unit tests and application behavior.
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
  - Used `pytest` to run all tests and all tests passed.
- Did AI help you design or understand any tests? How?
    - Yes, initially there were only three given tests and Claude notices that the return type for one method differs with the one used in app, and then it asked for clarification on which one to adapt. In addition, it added more comprehensive tests.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - The version I get did  not change the secret number, but it had other issues.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Rerun is triggered on every change (such as refresh, submit) and Streamlit reruns the scripts from top to bottom. The session state holds all the information of current session so the data can be shown in the web page.
- What change did you make that finally gave the game a stable secret number?
  - N/A
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    - This time I learn to add a fix point where there is a bug and create a subagent / open new sessions for specific tasks.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I would apply the new approach to future work.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - Nowadays AI tools have grown so much that I outperform junior software engineers and there is no need to worry much about the code quality of AI coding tools. Meanwhile, to grow faster, we need to embrace the benefit of AI instead of averting to it.