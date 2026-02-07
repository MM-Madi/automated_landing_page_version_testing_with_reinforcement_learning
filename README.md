# An Interactive Demo for automating A/B Testing with Multi-Armed Bandits

This repository showcases a multi-armed bandit RL agent for automating landing-page optimization through version testing. This simple demo illustrates how the agent learns through exploration and exploitation to favor the higher-converting variant, serving as an intuitive, practical introduction to RL concepts applied to real-world A/B testing scenarios.


## Definitions

**Landing page (LP) version testing** is the practice of comparing different designs or content layouts of a website’s landing page to see which one drives more conversions. This is traditionally done through A/B Testing. The business problem it addresses is uncertainty about which page layout will maximize customer actions—like sign-ups, purchases, or leads—so companies can invest confidently in the version that delivers the best results, allowing them to optimize their website on a target metric.

**Multi-Armed Bandit (MAB)** is a self-learning optimization algorithm that is able to compare different options on a specific metric and reach a decision as to which one gives the best results. MAB is a part of the broader field of Reinforcement Learning (RL), which, among other things, offers an automated way to optimize landing pages. Here the MAB continuously experiments online with the different LP versions, tracks user responses (such as conversion), and dynamically allocates traffic to the designs that are performing better in real time, learning and adapting as data comes in. It fully automates the process of A/B testing end-to-end, allowing businesses to maximize conversions faster while minimizing lost opportunities from underperforming pages.




## MAB for Landing Pages Demo
<img width="1238" height="520" alt="Image" src="https://github.com/user-attachments/assets/a694e396-2759-473a-841f-85bb9484fa3e" />

This repo contains a demonstration of an **Epsilon-Greedy Multi-Armed Bandit** used for version testing of a landing page. The frontend simulates visitors seeing different variants (sunset vs. day); the backend agent chooses which variant to show and learns which version is better from user actions (clicking on "Book" or "Not Interested").

### Setup
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app
From the project root, with the virtual environment activated:
```bash
cd backend && python app.py
```

Then open **http://127.0.0.1:5000** in your browser.


### How it works
- The **frontend** starts with a short explanation and a “Start the Demo” button. Once clicked, an image with one version of the landing page appears with the two buttons, **"Book"** and **"Not Interested"** and next to it a graph showing the learning process of the agent. 
- The LP image has two variants: Sunset and Daytime. Once the 'First Visitor' makes a choice by clicking the page is refreshed, the graph gets updated and the next version chosen by the agent appears representing what a second then third visitor see demonstrating the cumulative interaction and learning from multiple visitors.
- The **backend:** includes a single Epsilon-Greedy agent with **ε = 10%**. It compares two arms: `day` and `night` for the corresponding versions of the landing page. 
- The agent chooses a version to be presented to each visitor in accordance with its algorithm. The first 10 visitors will always see each version 5 times appearing randomly. Then the agent starts displaying the **version with the better conversion rate** 90% of the time and a random choice between the two versions 10% of the time.
- The counters for the versions get updated with each visitor. The conversion rate per version gets updated as well with a **Reward = 1** for a “Book” click and 0 for a “Not Interested” click.
- To get a good feeling of the agent's learning process, **it is recommended** to start with random clicks, then choose one version as the 'better one', to start clicking on it selectively, and see the effect on the agent's behavior.

## API
- `POST /api/visit` — New visitor; returns `{ "version": "day" | "night" }`.
- `POST /api/feedback` — Body: `{ "version": "day"|"night", "action": "book"|"not_interested" }`. Returns `{ "nextVersion", "agentState" }`.
