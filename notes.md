# chat piano with Teo
## Features to show?
- Retrieval
  - info about
    - direct metadata
    - indirect constraints (situation / demand)
  - info of
    - humming
    - playing
    - description of music constraints (e.g. instruments, chords)
  - Multi-round interaction!
- Performance eval with Clamp
- 自知之明 (just good to have. don't overdesign. As long as it doesn't harm the demo)
  - Gus: 这个曲子我有能力放，但我受版权限制不能给你放。
  - Gus: 这个曲子事实上在xxx数据集里，这个数据集我受版权限制不能给你放，但我更可以给你来个 piano cover. 
  - Gus: 自知之明 = 知道自己[有/知道]什么 + 知道自己能做什么
- [removed] Wraps MuseCoco (Is it really necessary with Teo?)
- [removed] Realtime accompany (only if it naturaly fits the rest of the demo)

## example scripts
### 0
user: "Find the piece in Disco Elysium OST that has [play piano] as the main melody"

### 1
user: "I'm selecting the background music for the commencement ceremony. I remember [vocal imitation]. Do you know what it is?"
piano cover...

### 2
user: "Help me locate a jazz arangement. It was performed at NYUSH, mostly 7/8, and many measures features the melody jumping around three unique notes."
TODO: make this multi-round interactive

### 3 Performance eval with Clamp
[Gus 太呆板，更多rubato]
user: [plays piano]
piano: "What style were you aiming for?"
user: "jazz".
piano: "Nice rhythm. next you can try more complex chords. For example, ... Need a practice proposal?"

## Gus feedback
[Gus: 可以串起来。1. 搜出曲子，2. eval发现问题，3. 进一步改进/教学]
[Gus: tech novelty 是 *agent*-based retrieval 可以多么丝滑。Demo 侧重点]

## jupiter
see "./script.md"
