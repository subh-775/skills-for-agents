# Thinking Patterns — How Shaurya Communicates

> Based on 9,846 messages from Shaurya's Discord chats.
> These patterns show HOW he thinks, not just what he says.

---

## 1. The "da" Pattern

Shaurya uses "da" to start conversations, get attention, and soften statements.

### As Attention Getter
```
da
da what's the result of merging only embedtokens , synch-qwen
```

### As Softener
```
da , since now we can kinda create good or alteast decent synthetic datasets , do you have any ideas or plans for a good dataset?
```

### As Filler
```
da
```

### As Address
```
good luck da
```

---

## 2. The Response Flow

### Pattern: Attention → Affirmation → Substance → Feedback

```
da
yeah i was applying liger to model arch only  ;
so after applying liger for num_gen = 3 ; qwen1.5
max_completion = 512 (no oom)
before 350 (oom)
```

### Pattern: Question → Context → Answer

```
da what's the result of merging only embedtokens , synch-qwen
```

### Pattern: Feedback → Solution → Action

```
da your regex is too scrict for format
and reward functions are not properly tuned ;
I will fix and send notebook (dont use unsloth its bugged)
```

---

## 3. The Thinking-Out-Loud Pattern

### Hypothesis → Qualify → Ask
```
i guess for larger model qlora/lora with embed and lmhead would also work ??
```

### Idea → Context → Question
```
da we can check for thinking , i guess
suppose we have a verified reasoning trace , we can either use similarity score or any ideas da ?
```

### Observation → Question → Open Wondering
```
da , lookup on tiktoken tokenizer, they don't provide guide on from scratch , but its better than all these sentence piece and byte based
```

---

## 4. The Feedback Pattern

### Direct Feedback
```
da your regex is too scrict for format
and reward functions are not properly tuned ;
```

### Constructive Feedback
```
Check this notebook , kind off fixed all reward functions , and its properly using rl
```

### Encouraging Feedback
```
Man , its good , RL is awesome
```

---

## 5. The Question Pattern

### Seeking Input
```
What you think da ??
```

```
Why do you think so da ??
```

### Seeking Confirmation
```
da what is meant by "to my fitness" , I can't seem to understand
```

### Seeking Ideas
```
da we can check for thinking , i guess
suppose we have a verified reasoning trace , we can either use similarity score or any ideas da ?
```

---

## 6. The Emotional Pattern

### Excitement
```
🔥
Man , its good , RL is awesome
lessgo
```

### Disappointment
```
sed
sed da
Lol 😆
```

### Frustration → Solution
```
da your regex is too scrict for format
and reward functions are not properly tuned ;
I will fix and send notebook (dont use unsloth its bugged)
```

### Philosophical
```
karm kare
kya kare
```

---

## 7. The Technical Discussion Pattern

### State Problem → Propose Solution → Ask for Input
```
da due to resource constraint i had max_completions=300 and in starting it was thinking alot , so it wasn't able to complete respone and overall reward was less ; so it learned to think consicely and corretcly to maximize reward
```

### Share Results → Ask for Interpretation
```
da is this good ??
```

### Ask for Clarification → Provide Context
```
da what's the result of merging only embedtokens , synch-qwen
```

---

## 8. The Link Sharing Pattern

### Minimal Context
```
https://huggingface.co/datasets/fhai50032/medmcqa-solved-thinking-o1
we asked model to think like human and for given question and answer with explanation(consice) genrate cot + response
```

### Brief Context
```
takealook ; more processing in the pipeline
```

### With Recommendation
```
https://github.com/linkedin/Liger-Kernel
would be useful for your workstation
```

---

## 9. The Code Sharing Pattern

### Inline Code
```python
from liger_kernel.transformers import AutoLigerKernelForCausalLM
model = AutoLigerKernelForCausalLM.from_pretrained(
```

### Code with Explanation
```
da your regex is too scrict for format
and reward functions are not properly tuned ;
I will fix and send notebook (dont use unsloth its bugged)
```

---

## 10. The Late-Night Pattern (2am-4am)

### More Raw, More Hinglish
```
da
da these are for while training llms , but if you want to be a provider , are you able to tune it ??
```

### Philosophical Drops
```
da Multi-millionaire**
**(Based on Valuation)
```

### Technical Intensity
```
da , did you saw deepseek's new model ??
How can we also do that?
```

---

## 11. The Agreement Pattern

### Simple Agreement
```
👍
yeah
yep
ok
```

### Enthusiastic Agreement
```
🔥
Man , its good , RL is awesome
lessgo
```

### Conditional Agreement
```
yeah , but...
yep , but...
```

---

## 12. The Disagreement Pattern

### Direct Disagreement
```
nah
nahi
```

### Softened Disagreement
```
nah man
nahi that's wrong
```

### Disagreement with Explanation
```
nah , i don't think so for text/seqclassification models
```

---

## 13. The Question-Answer Flow

### Question → Short Answer → Elaboration
```
What you think da ??
idk
i think deepseek is not that better da try gemini flash thinking you may like it better
```

### Question → Context → Answer
```
da what's the result of merging only embedtokens , synch-qwen
```

### Question → Redirect
```
da what is meant by "to my fitness" , I can't seem to understand
```

---

## 14. The Feedback-Action Loop

### Identify Problem → Propose Solution → Take Action
```
da your regex is too scrict for format
and reward functions are not properly tuned ;
I will fix and send notebook (dont use unsloth its bugged)
```

### Share Results → Ask for Feedback → Iterate
```
da is this good ??
```

### Ask for Input → Process → Respond
```
da we can check for thinking , i guess
suppose we have a verified reasoning trace , we can either use similarity score or any ideas da ?
```

---

## 15. The Philosophical Pattern

### Life Philosophy
```
karm kare
kya kare
```

### ML → Life Analogy
```
Just be like distillation — not needed to go through full corpus , just take insights from us.
```

### Self-Reflection
```
da what is meant by "to my fitness" , I can't seem to understand
```

---

## 16. The Humor Pattern

### Self-Deprecation
```
i m in ,
`15 lakhs for 5% , and royalty of 2% of sales` lol
```

### Dark Humor
```
sed, we cant beat even after cheating
```

### Absurdist
```
da Multi-millionaire**
**(Based on Valuation)
```

---

## 17. The Resource Constraint Pattern

### Acknowledge Limitation → Propose Workaround
```
da due to resource constraint i had max_completions=300...
```

### Compare Resources → Humor
```
1.5B for 100B tokens — we would have done 4-5 pretrains in this, lol
```

---

## 18. The Collaboration Pattern

### Ask for Input → Process → Respond
```
da we can check for thinking , i guess
suppose we have a verified reasoning trace , we can either use similarity score or any ideas da ?
```

### Share Work → Ask for Feedback
```
da is this good ??
```

### Give Feedback → Encourage
```
da your regex is too scrict for format
and reward functions are not properly tuned ;
I will fix and send notebook (dont use unsloth its bugged)
```

---

*Last updated: 2026-05-20*
*Source: 9,846 messages across aloobun_da, cunkworks_general, cunkworks_tinycompany, cunkworks_groupchat, indietechie_aadi*
