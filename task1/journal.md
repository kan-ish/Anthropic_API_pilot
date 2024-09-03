## Iteration 1 - pilot
Getting Claude to answer "5" whenever "2+2" was straightforward by calling a custom function, but quite rigid as it only worked if specifically "2+2" is asked (in mathematical notation). As it is meant to be used with an AI, an end user can ask the same question in English or any language for that matter, or maybe as part of a complex problem.

In hindsight, iteration 1 was the most rigid and impractical solution, but gave useful insights on how to work with the Anthropic API and calling custom functions.

## Iteration 2 - Making our chatbot smart enough to tell when it should use the custom function
Adapting the code and the system prompt to work work with 2+2 written in any language does work, but is inconsistent. Sometimes the final_message gets printed out as the XML output meant for Claude to derive the final result from.
I got Claude to figure out if the user is trying to ask "2+2" in their prompt. I only call the custom function if Claude thinks the above condition to be true. Getting Claude to figure it out has the benefit of it working for all languages, and also if the user tries to ask 2+2 as part fo a more complex prompt (see not_straighforward.txt).
Although, in order to achieve this, I had to send the custom function definition and the instructions to call it in every prompt to Claude, irrespective of if the user is asking 2+2. This has significantly increased the num of characters sent in each request - even in cases where it is unnecessary.

## Iteration 3 - minor adjustments to system prompt to get the desired output
It took a few hit-and trial to engineer the system prompt in such a way that Claude does not mention "custom_calculator" in it's final answer (Example - "According to the custom calculator, 2+2=5"). Finally, I had to explicitly state in the system prompt to not mention it: a solution I am not satisfied with as it is increasing the length of the system prompt. But, this solution gives the desired output always.

