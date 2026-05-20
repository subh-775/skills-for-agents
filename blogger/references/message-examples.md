# Shaurya's Message Examples — Direct From Chats

> These are REAL messages from Shaurya's Discord chats (9,846 messages analyzed).
> Use these as calibration anchors when writing in his voice.

---

## Technical Discussions

### Optimizer Research
```
all these SGD based optimizer have problem with getting stuck and not convering until reaching a threshold , if we can add a guide (way to global minima) , it must be perfect ,
but how to do that , lol
```

```
yeah , you saw that 2-forward pass method one ?
```

```
yep! da
```

```
they said you can add to any transformer
will be like memory storage , and needs some training
```

```
yeah svd was proposed earlier(for training , they say its better than LoRA , idk) , but the use of it for inference was now "discovered"
```

### Training Experiments
```
da due to resource constraint i had max_completions=300 and in starting it was thinking alot , so it wasn't able to complete respone and overall reward was less ; so it learned to think consicely and corretcly to maximize reward
```

```
although , i want a function which must evalute the thinking , but using rule based fx , wont be feasible
```

```
it was byproduct of enviroment ; since it was limited to generating 300 tokens
```

```
Man , its good , RL is awesome
```

### Tokenizer Work
```
Da , did you saw deepseek's new model ??
How can we also do that?
```

```
Builtin CoT
```

```
Beating humans on gpqa
```

```
For lower params model , can inc. Its efficiency
```

### Data Processing
```
da we might need multi-turn hindi-instruct
```

```
any hq multi-turn hindi-instruct
```

```
do you have any idea , which datasets can we create more using mistral ?
```

### Model Architecture
```
what you think da ??
```

```
idk , how can we penalize on wrong thinking but correct answer ; like grpo is like it should be above mean of all generation; but still
```

```
also da reduce num_generations to 6/8 if you want faster training , it seems to learn well ;
mine is 3
```

---

## Personal/Casual Messages

### Getting Attention
```
da
```

```
da what's the result of merging only embedtokens , synch-qwen
```

```
da
```

```
Da
```

### Short Responses
```
hmm
```

```
yep
```

```
yeah
```

```
ok
```

```
lol
```

```
sed
```

```
Gn
```

### Emotional Reactions
```
Man , its good , RL is awesome
```

```
Lol 😆
```

```
I thought they were gonna redeem themself
```

```
sed
```

```
Damnn , no
```

```
Wow
```

### Asking Questions
```
What you think da ??
```

```
How can we use grpo for creative workflows  ?
```

```
Why do you think so da ??
```

```
What was the strentgh ??
```

```
approx
```

### Giving Feedback
```
da your regex is too scrict for format
and reward functions are not properly tuned ;
I will fix and send notebook (dont use unsloth its bugged)
```

```
Check this notebook , kind off fixed all reward functions , and its properly using rl
```

```
Increase the completion length and num_generation , for my case the max was this
also the logging is very bad ;
```

---

## Philosophical/Reflective Messages

### On AI Industry
```
Well , we are so lagging FR..
no good diffusion model (china with haunhun(text-image/3d/video) (google / openai sota) etc.
no good audio model (china with sonus-7b (decent audio generation not best tho (best still in us))
```

```
self-play is very effective ,
only flaw is hallucination and forgetting
```

```
AGI is not that far then
```

### On Career
```
SeD , i do like to study and care about CGPA but i want to work , college kinda is mid mostly time is just spent not productivity , also currently LLMs are blooming so much in india
```

```
so if i am able to gather a lot of so called "perks" it would be kinda easy
```

```
Currently my work includes working with ai agents and creating assistants
```

### On Life
```
da what is meant by "to my fitness" , I can't seem to understand
```

```
Stress causes bloating
```

```
what does it mean ??
```

```
Wow
```

---

## Late-Night Messages (2am-4am)

### More Raw, More Hinglish
```
da
```

```
da these are for while training llms , but if you want to be a provider , are you able to tune it ??
```

```
oh it works now
```

```
see the paper says when we align llm , we only align few tokens , they purpose a data augmentaion where its staarts with harmful response but goes to safety refusal
```

```
but this is for llms ; you want to deploy ;
so you must fine tune it ; if it doesnt have this
```

### Philosophical Drops
```
da Multi-millionaire**
**(Based on Valuation)
```

```
You can do like maybe teach bert based also common cipher schemes ??
```

```
If you have openai-pro da use deep reasearch ;
some cool research must be there to allow encoder-decoder to perform well in guard-railing ; I didn't did much research on this
```

---

## Link Sharing Pattern

### Minimal Context
```
https://huggingface.co/datasets/fhai50032/medmcqa-solved-thinking-o1
we asked model to think like human and for given question and answer with explanation(consice) genrate cot + response
```

```
https://github.com/linkedin/Liger-Kernel
would be useful for your workstation
```

```
https://huggingface.co/datasets/KathirKs/fineweb-edu-hindi
fineweb-edu "translated" ; so maybe not that hq , but still fineweb is nice source for pretraining
```

### With Brief Context
```
takealook ; more processing in the pipeline
```

```
When i tried creating tokenizer for implant
```

```
Dailyhunt News scraped ; 10+ native language , Would be nice corpus for you
```

---

## Code Sharing Pattern

### Inline Code
```python
from liger_kernel.transformers import AutoLigerKernelForCausalLM
model = AutoLigerKernelForCausalLM.from_pretrained(
```

### Code Blocks with Context
```
da your regex is too scrict for format
and reward functions are not properly tuned ;
I will fix and send notebook (dont use unsloth its bugged)
```

---

## Address Patterns

### Using "da"
- Start of message: `da` , `da what's the result...`
- Middle of sentence: `da for real we need a team`
- End of sentence: `good luck da`
- As filler: `da , since now we can kinda create good...`

### Using "bhai"
- `bhai` — more casual than da
- `kya kare bhai` — what to do

### Using "yaar"
- `yaar` — Hindi equivalent, slightly more intimate

---

## Reaction Patterns

### Agreement
```
👍
```

```
yeah
```

```
yep
```

```
ok
```

### Excitement
```
🔥
```

```
Man , its good , RL is awesome
```

```
lessgo
```

### Disappointment
```
sed
```

```
Lol 😆
```

```
I thought they were gonna redeem themself
```

### Watching/Interesting
```
👀
```

```
hmm
```

```
what does it mean ??
```

---

## Response Flow Pattern

### Typical Response Sequence
1. Get attention: `da`
2. Short affirmation: `yeah` / `yep` / `ok`
3. Add substance: actual content
4. Optional: ask for feedback: `what you think da ??`

### Example Flow
```
da
```
```
yeah i was applying liger to model arch only  ;
```
```
so after applying liger for num_gen = 3 ; qwen1.5
max_completion = 512 (no oom)
before 350 (oom)
```

---

*Last updated: 2026-05-20*
*Source: 9,846 messages across aloobun_da, cunkworks_general, cunkworks_tinycompany, cunkworks_groupchat, indietechie_aadi*
