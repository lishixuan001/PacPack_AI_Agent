# CS188-PacPack

*For the most up-to-date version of the instructions, refer to the PacPack website*

## Condensed instructions

**Phase 1**:

Run `python capture.py -p phase1Team`. This will run a match using:
- v0.0 of `PickyStaffAgent`, a P1 staff bot (`p1StaffBot.py`)
- A baseline solution student bot that works reasonably well (`p1StudentBotSol.py`)

**Phase 2**:

Run `python capture.py -p phase2Team`. This will run a match using:
- A full release version of P1 staff bot (`p1StaffBot.py`)
- A baseline greedy student bot that works (not very) well (`p2StudentBotSol.py`)

**Phase 3:**

Run `python capture.py -p phase3Team -g P3oneGhostTeam` or `python capture.py -p phase3Team -g P3twoGhostTeam` (against one or two ghosts). This will run a match using:
- The (very poor) baseline team bots as the 'cooperative' bots
- A baselineTeam bot as the opponent ghost


# Student Instructions
## Challenge: PacPack

## Logistics intro (as seen in lecture and on Piazza):

Hello everyone!

This summer, we're trying out an improvement for the course. Please bear with us as we're offering this for the first time. You may have heard about CS188 Contests. This is a special type of assignment that CS188 has historically had where you build bots to compete against other student bots for extra credit. It has had many issues though, and our big project for the summer is to iterate on it and improve it! We've redesigned the contest to hopefully make it a better learning experience, more collaborative, and give you the chance to explore AI algorithms in a more open-ended way.

The results of our efforts is a new assignment called PacPack! (You'll get the pun soon enough...) In this assignment, we'll be moving away from the competitive agents we used for topics like minimax game trees. We want to flip the script a little, and challenge you with a much more realistic, and interesting, task: you will be building bots to cooperate with each other!

This assignment is a more open-ended project, and will draw on some of the techniques you have learned in the first half of the class while simultaneously requiring you to refine those techniques to develop a bot that can work together with other bots to solve our task. As always, our setting is Pacman!

The details of this game will be in the specs, but first, here are some logistics.

First and foremost, this assignment will be replacing Project 4, and will be worth the same amount of points that project 4 would have been worth (i.e. it is worth 5% of your grade). The result of this is that PacPack is the ONLY project-level assignment you will have to be working on for the next week (though you will have 1.5 weeks to complete the whole thing).

Second, we have not finalized exactly how this will be graded. Now, while this sounds pretty scary when considering the point above, we promise that given how experimental this assignment is, that we will absolutely stay on the generous side here. More details about that to follow.

### Now for important dates and deadlines:

**Saturday, July 21st:** 
*The first 2 out of the 3 parts of the assignment will be due at this time.* If you have a submission for the third part, then submitting a non-trivial bot before this deadline will give you **2 extra credit points** on the assignment! You CAN resubmit your refined bot after the deadline, so if you have made decent progress then there is literally nothing to lose by submitting your draft early.

**Sunday, July 22nd:**
We will be processing the bots we got from early submissions so that we can give a more robust grading breakdown for phase 3. We'll be using this early scoring data to determine fair grading thresholds. Keep in mind that our definition of a fair threshold will be based on what results constitute fair effort, *not* on curving around a normal-looking distribution.

**Monday, July 23rd:**
This is when we will release the final phase of the PacPack: our website. Here, all teams will upload their bots, and can request to see how well they cooperate with other bots. This is also the only place where you can try to cooperate with the final staff bot with whom you will be graded on when the assignment is finished.

**Thursday, July 26th:**
The final phase of PacPack will be due.

### Grading:
PacPack has 3 main parts, for a total of 25 points. The first 2 will be due this Saturday.

For parts one and two, we will be determining grade boundaries over the next few days after getting student feedback. We will make a Piazza thread for this purpose. For part three, we have included guideline times in the preliminary autograder, but keep in mind that the final goal times we decide on may be easier to attain. We will make these boundaries using the data we collect on Saturday.

In the pursuit of both effort-based grading, and of collecting feedback, we will be requiring that students fill out a **"diary"** of their progress. Aside from being worth a few points itself, we reserve the right to give points to students who don't meet the goal thresholds if they have demonstrated satisfactory efforts. We are leaving this vague on purpose, but keep in mind that maintaining this diary is very important both for your grade, but also for our getting to know how this assignment goes and improving it in the future. An example diary is [here](https://docs.google.com/document/d/1E0AMHInD8ts9O08E1A0chbD7gwhrEKvjR16jX4SRhhw). We know this is quite a lot to ask, but it is very valuable to us. Also, writing a log (if you are not used to doing so) can be useful to you to self-analyse how you approach problems and what your main difficulties and time-sinks are. Just to clarify, this *will* be part of your submission.

Again, this is an experimental assignment and there is a good chance that some things could go wrong. Please keep in mind that we have no intention to screw up anyone's grades or worsen the experience of the class, so we would greatly appreciate any feedback as we go.

On behalf of the entire staff this summer who has been working tirelessly to bring you something fresh, we wish y'all the best and hope that we all find success in this endeavor!

- CS188Su18 Staff


## Introduction
PacPack involves a multi-player variant of Pacman, where each agent controls a Pacman in coordinated team-based strategies. The PacPack code is available as a [zip archive](https://drive.google.com/uc?export=download&id=1aMeKrZjK8VOPS4HZAKSvCjdvBpTnXV_B).

#### Key Files to Read:
| File name | Content |
---|---|
| `capture.py`   | The main file that runs games locally. This file also describes the gameState type and rules.  |
| `captureAgents.py`  |  Specification and helper methods for capture agents.  |
| `myAgentP1.py`, `myAgentP2.py`, `myAgentP3.py` |   This is where you will define your own agents for submission. (These are the only files that you will submit.)   |


#### Supporting Files (Do not Modify):
| File name | Content |
|---|---|
| `game.py` |   The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid. This is probably the only supporting file that you might want to read |
| `util.py`  |  Useful data structures for implementing search algorithms.  |
| `distanceCalculator.py` |   Computes shortest paths between all maze positions.  |
| `graphicsDisplay.py` |   Graphics for Pacman  |
| `graphicsUtils.py`  |  Support for Pacman graphics  |
| `textDisplay.py`  |  ASCII graphics for Pacman  |
| `keyboardAgents.py`  |  Keyboard interfaces to control Pacman  |
| `layout.py`  |  Code for reading layout files and storing their contents  |

### Academic Dishonesty
Although the spirit of PacPack is cooperative, we expect you to share code **only with your partner** and submit your own code to the best of your ability. Please don't let us down.

* * *

## Rules of PacPack
------
#### Layout
The Pacman agents' goal is to try to eat the food in as few timesteps as possible; A ghost agent (in Phase 3) will try to stop the Pacman agents from doing so.

#### Scoring 
There are two numbers you want to pay attention to: the "score" displayed in the game GUI is just the number of pellets eaten, and the total number of timesteps taken to eat all pellets (but 2). The latter is what will be used for grading, and will be printed out in the console at the end of the game. Any game that does not finish in time (the pacman team doesn't eat the pellets in time) will be assigned a value of `1200` timesteps taken.

#### Computation Time
We will run your submissions on an [Amazon EC2 Large Instance](http://aws.amazon.com/ec2/instance-types/). Each agent has 1 second to return each action. Each move which does not return within one second will incur a warning. After three warnings, or any single move taking more than 3 seconds, the game is forfeit. There will be an initial start-up allowance of 15 seconds (use the `registerInitialState` function). If your agent times out or otherwise throws an exception, an error message will be present in the terminal output. Each game is limited to a maximum time of 1 minute.

* * *


## Overview of the Phases
There are **three** phases in this challenge. You agent will receive progressively more information from the teammate, which will enable better cooperation:
1. In Phase 1, your agent will try cooperate with a selfish agent who does not communicate.
2. In Phase 2, your agent will try cooperate with a selfish agent who lays out the plan for its first 400 moves, and will send you a list of actions they intend to take through the broadcast channel.
3. In Phase 3, your agent will try to cooperate with a **cooperative teammate**. Now, your agent can send broadcasts as well, and the teammate will take your plan into account. Your agent will receive a broadcast from its teammate every turn, and will broadcast back to it.

## Designing Agents
------
Unlike in projects, the agent now has to work with a partner when completing the task. The behaviour and predictability of the other agent varies across different phases. Finally, the time limit on computation introduces new challenges.

#### File Format

You should include your agent in a file of the same format as `myAgentP_.py`. Your agent must be completely contained in this one file. **Please include a comment block describing the algorithms your agents use at the top of the file. The course staff reserves the right to penalize solutions without a description.**

#### Interface

The `GameState` in `capture.py` should look familiar, but contains new methods like `getFood`, which returns a grid of all food on the board. Also, note that you can list a team's indices with `getPacmanTeamIndices`, or test membership with `isOnPacmanTeam`. This will mainly be relevant for Phase 3, when there will be a Ghost team.

#### Distance Calculation

To facilitate agent development, we provide code in `distanceCalculator.py` to supply shortest path maze distances.

#### CaptureAgent Methods

To get started designing your own agent, we recommend subclassing the `CaptureAgent` class. We have already done so in the starter code. This provides access to several convenience methods. Some useful methods are:

* * *

`def chooseAction(self, gameState):`

Override this method to make a good agent. It should return a legal action within the time limit (otherwise a random legal action will be chosen for you).

* * *

`def getFood(self, gameState):`

Returns a matrix where `m[x][y]=True` if there is food you can eat in that square.

* * *

`def getOpponents(self, gameState):`

Returns agent indices of your opponents (this is only useful for phase 3, in which your opponents are the ghosts). This is the list of the numbers of the agents (e.g., ghosts might be `[1,3]`).

* * *

`def getTeam(self, gameState):`

Returns agent indices of your team. This is the list of the numbers of the agents (e.g., for the pacman team it might be `[1,3]`).

* * *

`def getScore(self, gameState):`

Returns the score of the agent's team for a specific state

* * *

`def getMazeDistance(self, pos1, pos2):`

Returns the distance between two points; These are calculated using the provided distancer object. If `distancer.getMazeDistances()` has been called, then maze distances are available. Otherwise, this just returns Manhattan distance.

* * *

#### Restrictions

You are free to design any agent you want. However, you will need to respect the provided APIs. Agents which compute during another agent's turn will be disqualified. In particular, any form of multi-threading is disallowed, because we have found it very hard to ensure that no computation takes place on the opponent's turn.

<!-- TO BE ADDED WHEN WEBSITE IS UP

#### Warning About Output

If one of your agents produces any stderr output during its games in an online match, that output will be included in the results posted on the website. Additionally, in some cases a stack trace may be shown among this output in the event that one of your agents throws an exception. You should design your code in such a way that this does not expose any information that you wish to keep confidential. -->

* * *

### Getting Started

By default, you can run a game with (this will run phase 1 with default settings):

`python capture.py`

A wealth of options are available to you:

`python capture.py --help`

To run a phase 3 game (with a ghost), try

`python capture.py -p phase3Team -g P3oneGhostTeam`

which specifies that the Pacman team `-p`  is created from the `phase3Team.py` file and the Ghost team `-g` is created from the `P3oneGhostTeam` file. To control one of the four agents with the keyboard, pass the appropriate option:

`python capture.py --keys0`

The arrow keys control your character. (This might not work on Windows machines. Contact us if this is the case).

#### Agent Teams

As you might have noticed above, when starting a match with `python capture.py ...` we usually specify a pacman team (and potentially a ghost team).

There are 3 team files, `phase1Team.py`, `phase2Team.py`, `phase3Team.py`.

Each pacman team has two members, specified as default values in the signature of the function `createTeam`. If you want to create other agent classes for testing purposes, just change the signatures in the team files. *Something to note is that your agent will not necessarily have index 0* (except for phase 2 where it will always be index 1). Try to keep your code flexible.

Note: you might have to first import your agent class at the top of the `*Team.py` file you are using.

#### Layouts

By default, all games are run on the `defaultcapture` layout. To test your agent on other layouts, use the `-l` option. In particular, you can generate random layouts by specifying `RANDOM[seed]`. For example, `-l RANDOM13` will use a map randomly generated with seed 13.

<!-- #### Recordings 

You can record local games using the `--record` option, which will write the game history to a file named by the time the game was played. You can replay these histories using the `--replay` option and specifying the file to replay. 
All online matches should be automatically recorded and the most recent ones can be viewed on the PacPack website. You will also able to download the history associated with each replay. -->

#### Submission Instructions

For phases 1 and 2, we will be providing a script that you can run to test your agent against a staff bot of ours. To submit for these phases, you will be submitting your files to Gradescope. The final autograders and Gradescope assignments will be released in the coming days. In the meantime, try to hit the metrics we provide in the section specifics down below (through the preliminary autograders).
For phase 3, we recommend you test out your agent with the bot we provide and with itself, though more details about submission for phase 3 will be provided Monday July 23rd when the website launches.

To enter into the online challenge in phase 3, your agent must be defined as myAgentP3 in myAgentP3.py. Due to the way the matches are run, your code must not rely on any additional files that we have not provided. You may not modify the code we provide, except for testing purposes.

To enter your bot into the online challenge, you should visit [the official PacPack site](https://www.pacpack.org) once we announce that it is ready.
 
<!-- To log in, **(FIXME: verify with website team)**. Once you're logged in, you can form teams by requesting that your teammates join your team. Note that you'll need their **(FIXME: verify with website team)** to send a request, and that your teammate will need to accept the request.

You can upload bots by entering a bot name and selecting a file of same format as myAgent.py. After uploading the bot, you can then request to pair up with another bot in the next match, and see the results and statuses of all matches on the Matches page. (**FIXME: verify with website team**) -->

### PacPack Details

#### Teams

You may work in teams of up to 2 people.

#### Acknowledgements

Thanks to Barak Michener and Ed Karuna for providing improved graphics and debugging help.

Have fun! Phase 3 is especially open ended, so make sure to just spend time appreciating and exploring the problem and its possible solutions. 

Again, this will be the first offering of this project. If you find any infrastructural bugs, please report them to the staff. This will ensure they are fixed promptly.


*****


# Phase 1: Cooperate with the uncooperative [5 points]
-------------------------

**At the top of your file, you MUST include the following comment, with the fields filled in appropriately:**

```
"""  
Students' Names: (name your team members here)  
Phase Number: 1  
Description of Bot: (a DETAILED description of your bot and it's strategy including any algorithms, heuristics, etc...)  
"""
```

If you have not read the [general instructions](http://pacpack.org/docs/general), you should do that first. This page simply contains a subset of that information that is particularly relevant to Phase 1 for faster reference. 

The goal for this challenge is for your agent to work together with an uncooperative agent and eat all but two of the pellets as quickly as possible. **You will only be able to observe your teammate's actions as they take place. No other information will be available, as the broadcast channel is inactive in Phase 1.**

### A few things to note about Phase 1 staff bots (which will be your agent's teammate):
1. Uncooperative
2. Not guaranteed to take the shortest route to get to the next food
3. Does not plan to finish all the food on its own

### Local Testing

The staffbot that you will be running against in the final autograder is the same as the one in `p1StaffBot.py`, except it will be using a different `_RANDOMSEED` parameter. You can change this value by editing the `p1StaffBot.py` file if you want to have more certainty of your bot's performance.

Run `python capture.py -p phase1Team`. This will run a match using:
- PickyStaffAgent, a basic P1 staff bot (`p1StaffBot.py`)
- Your agent (`myAgentP1.py`)

### Preliminary Autograder
Run `python autograderP1.py`. This will run 10 games on 10 different layouts, each with a target time. 
If struggling with a specific layout, please feel free to run  `python capture.py -p phase1Team -l RANDOMxxxx` to only test on that layout.
To disable graphics, please use the `-q` option as in `python autograderP1.py -q`

**At submission time, your final bot should be defined in a class called `myAgentP1` in the `myAgentP1.py` file.** The starter code provides a guideline for the structure you should expect to use in your own implementation. You should be able to achieve to reasonable performance with the features we provide you, but you are free to modify and augment the features.


*Don't forget to fill in your diary as you go*

-------

# Phase 2: You Know Me [10 points]
-------------------------

**At the top of your file, you MUST include the following comment, with the fields filled in appropriately:**

```
"""
Students' Names: (name your team members here)  
Phase Number: 2
Description of Bot: (a DETAILED description of your bot and it's strategy including any algorithms, heuristics, etc...)  
"""
```

If you have not read the [general instructions](http://pacpack.org/docs/general), you should do that first. This page simply contains a subset of that information that is particularly relevant to Phase 2 for faster reference. 

The goal for this challenge is for your agent to work together with an uncooperative agent effectively and eat all but two of the pellets as quickly as possible. **The primary difference from Phase 1 is that your agent now has perfect information about their teammate's plan**. This will be provided to your agent as a list of actions your teammate will take, from which its positions can be extracted. In other words, with some calculation, your bot will have access exactly where its teammate is going to be at any time step.

To allow communication, we need to introduce a broadcasting system. In Phase 2, the staff bot teammate will plan all of its actions before the game starts and broadcast the plan to your agent. **Your agent will receive the broadcast during your agent's initialization (in the method `registerInitialState`)**.

Just as a reminder, you have a cap of 15 seconds of computation in the `registerInitialState` method, while you have a cap of 1 second of computation for normal turns. Depending on how you tackle the problem, you might want to do some computation at this stage. 
<!-- (Note: if you want to disable computation length checks for testing, ) -->

### A few things to note about Phase 2 staff bots (which will be your agent's teammate):
1. Uncooperative
2. Not guaranteed to be take the shortest path to the food pellets it is planning to eat
3. Does not plan to finish all the food on its own
4. Will broadcast it's first 400 actions to you before the beginning of the game

You can access your teammates broadcast from the `self.receivedInitialBroadcast` attribute of your agent during the execution of the method `registerInitialState`.

To enable local testing, `p2StaffBot.py` is released to you. This is the source file for the staff bot you will be working with during test time, **with different `_RANDOMSEED` and `_PERCENTAGE` values**. You can expect `_PERCENTAGE` to be s.t. $0.4 \leq p \leq 0.6$.

You should test your bot out with a few different `_RANDOMSEED` and `_PERCENTAGE` values, please do not modify anything else in the staff bot.

There are also some useful methods in the `GameState` class contained in `capture.py`. Please feel free to take a look.

### Local Testing

Run `python capture.py -p phase2Team`. This will run a match using:
- A full release version of P2 staff bot (`p2StaffBot.py`)
- Your agent (`myAgentP2.py`)

### Preliminary Autograder:
Run `python autograderP2.py`. This will run 10 games on 10 different layouts, each with a target time. 
If struggling with a specific layout, please feel free to run  `python capture.py -p phase2Team -l RANDOMxxxx` to only test on that layout.
To disable graphics, please use the `-q` option as in `python autograderP2.py -q`

**At submission time, your final bot should be defined in a class called `myAgentP2` in the `myAgentP2.py` file.** The starter code provides a guideline for the structure you should expect to use in your own implementation, including the broadcasting and some useful functions.


*Don't forget to fill in your diary as you go*

-----

# Phase 3: Co-op Raid [10 points]
-------------------------

**At the top of your file, you MUST include the following comment, with the fields filled in appropriately:**

```
"""  
Students' Names: (name your team members here)  
Phase Number: 3
Description of Bot: (a DETAILED description of your bot and it's strategy including any algorithms, heuristics, etc...)  
"""
```

If you have not read the [general instructions](http://pacpack.org/docs/general), you should do that first. This page simply contains a subset of that information that is particularly relevant to Phase 3 for faster reference. 

**The primary differences from the previous phrases is that your agent now has perfect communication with their teammate, and there is a ghost.** Your agent will receive a broadcast from their teammate every turn, and will send one to them – containing the actions it expects to be taking in **future** turns.

### Broadcasting Conventions 
On a high-level, broadcasting in phase 3 differs from that of phase 2 as it happens every turn, rather than just once before the start of the game. This enables each agent to update their plans in response to what the other agent is doing, and cooperate more effectively in collecting the food and avoiding the ghost.

Since your agent will not only work with cooperative staff bots, but also everyone else's cooperative agents, we need to establish some conventions for the communication channel.

1. The broadcast must be a list containing valid action strings (`"North", "West", "South", "East", "Stop"`) and nothing else.
2. You and your teammate agent can broadcast at every time step, but are not required to do so: in case you will not broadcast at a certain turn, you should set your broadcast for that turn to `None`.
3. You and your teammate can deviate from the your broadcasted plans any time, without notifying each other. Again, if doing this too much it will mainly be to your disadvantage, as you (or the other agent) will be operating under wrong assumptions.
4. Even though you are only allowed to broadcast valid action *strings*, when handling your teammates' broadcast, you should account for the possibility that the sequence of actions broadcasted to you might not be *legal actions* for your teammate. An example is if the agent is eaten by a ghost mid-way through executing it's broadcasted plan, and so the remaining actions in the plan might be illegal when conducted from the re-spawn point.

The above points should inform and guide how you decide to deal with incoming broadcasts from your teammate and choosing your own. In general, you want to try and **make design choices that are as robust as possible** to the choice of your actual teammate.

**IMPORTANT:** you will be setting your broadcast in `self.toBroadcast` within the method `chooseAction` while choosing the action for your turn (in addition to computing your current action, you can compute your expected *future actions*). Your teammate will receive your broadcast in their own turn. Therefore, **your broadcast should not include the action you will return from `chooseAction` – it will have already been performed by the time your teammate sees the broadcast**.

### The Ghost
The ghost finally found out that the Pacman team has been secretly stealing food 😠 so it decided to hunt them down.
The ghost is implemented in `P3oneGhostTeam.py`. However, please note that **the ghost agent may have a different randomness value in our final autograder**.

The ghost cannot see very well, and usually gets confused by other sounds, leading him to go the wrong direction a lot of the time (he has partially random actions). Moreover, he is scared of going to close to the Pacman team home base, so he will try to avoid it.

### Local Testing

We provide a very basic version of Phase 3 cooperative staff bot in `p3StaffBot.py`, please note that **this is not the staff bot on the PacPack site**. Feel free to generate more bots to test your agent's robustness

Run `python capture.py -p phase3Team -g P3oneGhostTeam` (against one ghost).

This will run a match using:
- A Pacman team comprised of:
    - A 'cooperative' teammate (`p3StaffBot.py`)
    - Your agent (`myAgentP3.py`)
- A ghost team consisting of a reflex ghost

### Preliminary Autograder:
Run `python autograder3.py`. This will run 20 games on 10 different layouts (in normal and reverse index), each with a target time. 
If struggling with a specific layout, please feel free to run  `python capture.py -p phase3Team -l RANDOMxxxx` to only test on that layout.
To disable graphics, please use the `-q` option, as in `python autograderP3.py -q`

**At submission time, your final bot should be defined in a class called `myAgentP3` in the myAgentP3.py file.** The starter code provides a guideline for the structure you should expect to use in your own implementation, including the broadcasting and some useful functions.

While you will be unable to test with our final staffbot until the website release, a good way of assessing your implementation is testing how your agent cooperates with itself (placing it as both agents for your team). You can also run the autograder to see how well you do in cooperating with the `simpleStaffBot` (Note: `simpleStaffBot` is *very* bad – it is mainly a sanity check that you are using the API correctly).

**FOR DEBUGGING:** `simpleStaffBot` will make a print something if illegal actions are broadcast to it. This is ok in certain situations (when a pacman dies), but if this happens regularly, this is an indication that your broadcast is incorrect.

### Online Testing

Once we announce the launching of the website, we encourage you to upload your agent to [the PacPack site](https://www.pacpack.org) once you are kind of satisfied with your bot. You may request to pair up with any bots listed.



*Don't forget to fill in your diary as you go*