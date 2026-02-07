"""
Multi-Armed Bandit Demo — Backend with Epsilon-Greedy agent.
Two arms: "day" and "night" landing page versions.
Reward = 1 for "Book", 0 for "Not Interested"; both increment the arm's count.
"""
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

# Epsilon-Greedy MAB agent (epsilon = 10%)
EPSILON = 0.10
VERSIONS = ["day", "night"]
COLD_START_SIZE = 10  # first 10 displays: 5 of each version in random order


class EpsilonGreedyAgent:
    def __init__(self, epsilon: float = EPSILON, arms: list = None):
        self.epsilon = epsilon
        self.arms = arms or list(VERSIONS)
        self.q = {a: 0.0 for a in self.arms}   # value estimate Q(a)
        self.n = {a: 0 for a in self.arms}      # count N(a)
        # Cold start: first 10 displays are 5×day and 5×night in random order
        cold = list(self.arms) * (COLD_START_SIZE // 2)
        random.shuffle(cold)
        self._cold_start_queue = cold

    def choose(self) -> str:
        if self._cold_start_queue:
            return self._cold_start_queue.pop(0)
        # After cold start: epsilon-greedy (alpha = 10%)
        # Explore: pick randomly from arms
        if random.random() < self.epsilon:
            return random.choice(self.arms)
        # Exploit: pick arm with highest Q; break ties randomly
        best_q = max(self.q[a] for a in self.arms)
        tied = [a for a in self.arms if self.q[a] == best_q]
        return random.choice(tied)

    def update(self, arm: str, reward: float) -> None:
        self.n[arm] += 1
        # Incremental update: Q(a) <- Q(a) + (r - Q(a)) / N(a)
        self.q[arm] += (reward - self.q[arm]) / self.n[arm]

    def state(self):
        return {"q": dict(self.q), "n": dict(self.n)}


agent = EpsilonGreedyAgent()


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/visit", methods=["POST"])
def visit():
    """New visitor arrived — agent chooses which version to show."""
    version = agent.choose()
    return jsonify({"version": version})


@app.route("/api/feedback", methods=["POST"])
def feedback():
    """
    Frontend sends the version that was shown and the user's action.
    Reward = 1 for 'book', 0 for 'not_interested'. Both increment N(version).
    Returns the next version to display.
    """
    data = request.get_json() or {}
    version = data.get("version")
    action = (data.get("action") or "").strip().lower().replace(" ", "_")
    if version not in VERSIONS:
        return jsonify({"error": "invalid version"}), 400
    reward = 1.0 if action == "book" else 0.0
    agent.update(version, reward)
    next_version = agent.choose()
    return jsonify({
        "nextVersion": next_version,
        "agentState": agent.state(),
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
