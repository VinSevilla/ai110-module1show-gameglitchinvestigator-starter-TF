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
- Actual behavior: the history is always one behind when a new number is inputted, so it shows my previous guess instead of the current one.

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

  > For this project i mainly used Claude Code in agent mode inside VS Code. I would describe the bug i was seeing in plain english and it would go find the spot in the code and explain whats going on. I didnt really use ChatGPT or Copilot this time, i just stuck with the one tool so i wouldnt get a bunch of different answers that dont match.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  > When the history in the debug window was always one behind, the AI explained that Streamlit re-runs the whole script from top to bottom every time, so the debug window was drawing the history before my newest guess got added to the list. I verified this by running the app and submitting a few guesses, and now the history shows my newest guess right away instead of lagging behind.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  > The scoring was the tricky one. After we fixed a bunch of the other bugs, there was still this score bug where every guess would give you some points and then the very next guess would just take them right back, so the score kinda bounced around and never made sense. The misleading part was the original AI code tied the points to whether the attempt number was even or odd (attempt_number % 2), which looked like real scoring logic but was really what caused the give-then-take. I caught it by watching the score in the debug window after each guess, and we ended up scrapping that whole thing for a simple rule (closer = +5, farther = -5, and it cant go below 0). I also wrote a pytest test to make sure the score never goes negative.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  > I didnt just trust that changing the code fixed it, i actually had to see it behave right. For most of the bugs i would run the app and play it the way a normal person would, like switch difficulty, make a guess thats too high, click new game, and watch if it did what i expected.

- Describe at least one test you ran (manual or using pytest)  
   and what it showed you about your code.

  > Running pytest showed all 5 tests passing (the 3 starter ones plus my 2 new ones). The biggest thing it showed me was that my game logic actually lives in logic_utils.py now and can be checked without even opening Streamlit, which made me trust it way more.

- Did AI help you design or understand any tests? How?
  > Yeah, the AI helped me think about what to even test. It pointed out that a good test should target the exact bug i fixed, like testing that the score floors at 0 instead of just testing random stuff. It also helped me run the app in a headless way to drive it like a user, and thats actually how we caught a sneaky bug i wouldnt have found from the unit tests, the "attempts left" number was lagging one guess behind.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  > Ok so the weird thing about Streamlit is that every single time you do anything, like click a button or type in a box, it doesnt just update that one part, it literally re-runs your whole python file again from the very top to the bottom. So its not like a normal app that remembers where it was, its more like it reads the whole script fresh every time you touch something. So the way i'd explain it to a friend is: Streamlit forgets everything and re-reads your whole script on every click, and session_state is the one box where you stash the things you NEED it to remember, and the order your code runs in actually matters a lot because of that.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    > The biggest habit i want to keep is fixing one bug at a time and then actually testing it before moving on, instead of trying to fix everything at once and hoping it works. On this project we went bug by bug, and after each fix i either ran the app or ran pytest to make sure it actually worked and i didnt break something else.

- What is one thing you would do differently next time you work with AI on a coding task?

  > Next time i would test the code the AI gives me sooner instead of assuming its right because it sounds confident. There were a couple times the code looked totally fine and even had comments saying it was production ready, but it was still buggy (like the scoring). So i'd verify earlier and not let buggy code pile up before i actually run it.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  > This project really showed me that AI code can look clean and confident and still be full of bugs, so i cant just trust it blindly. Now i think of the AI as a teammate that gives me a fast first draft, but its still my job to test it and prove it actually works.
