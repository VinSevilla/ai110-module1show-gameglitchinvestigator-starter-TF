# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

> When I first ran the game it kinda worked but stuff was acting weird and not how a guessing game should. The number guessing part showed up fine but the state was getting messed up as I played. After messing with it for a while I found two main bugs:

The first bug was that the "New Game" button only resets the secret number to guess, but it doesnt clear out the rest of the stuff like the history or the attempts, so it never really felt like a fresh game. The second bug was that the history records were always behind by one, so every time I typed in a new guess the history would show my previous guess instead of the one I just made. That delay made it super confusing to tell if my guess was actually being recorded right.

**Bug Reproduction Log**

Here are all the bugs i found while testing, i tried to sort them by category.

**Code / Debug Window bugs**

1. New game only resets the number to guess

- Input: click the "New Game" button
- Expected behavior: everything should reset like the history, attempts, score and the new secret number
- Actual behavior: only the secret number gets reset, the rest of the state stays the same so it dont feel like a new game

2. History records delayed by 1

- Input: type in a guess
- Expected behavior: the history should show the guess i just made right away
- Actual behavior: the history is always one behind, so it shows my previous guess instead of the current one

3. Number generated before a difficulty is picked

- Input: open the game and switch the difficulty after
- Expected behavior: the secret number should only be generated after a difficulty is selected so its inside the right range
- Actual behavior: a number already gets made before you pick a difficulty, so the number can be outside the range once you change difficulty

4. Wrong / incorrect hints being given

- Input: make a guess and read the hint
- Expected behavior: the hint should point you the right direction (like "go higher" or "go lower")
- Actual behavior: the hints are incorrect and give you the reverse direction.

5. UI: Attempts left does not equal attempts allowed

- Input: start a game and look at the attempts counter
- Expected behavior: attempts left should match the attempts allowed for that difficulty
- Actual behavior: the attempts left number doesnt line up with the attempts allowed shown

**Program logical errors**

6. Score going into negatives

- Input: keep guessing wrong
- Expected behavior: the score should stop at 0 and not keep dropping
- Actual behavior: the score keeps going down into negative numbers

7. Hard difficulty is arguably easier than normal

- Input: play on Hard vs Normal
- Expected behavior: Hard should actually be harder than Normal
- Actual behavior: Hard gives the least attempts allowed but the range is only half of normal, so its kinda easier than normal which dont make sense

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
