# Rock Paper Scissors Engine

A modular, extensible Rock–Paper–Scissors engine featuring five AI bots and a Markov Chain–based predictive model.
This project is an enhanced and customizable version of the freeCodeCamp RPS Machine Learning challenge.

It supports both:

* Web-based deployment (HTML + JavaScript)
* Desktop deployment (Pygame)

---

## Markov Chain Prediction (ML Bot)

The Markov bot uses a first-order Markov Chain to predict the opponent's next move based on observed patterns.

### How It Works

A Markov Chain assumes that the next state depends only on the current state.

In this project:

* State = opponent's previous move
* Prediction = most likely next move

The bot builds a transition table:

| Previous Move | Next Move | Count |
| ------------- | --------- | ----- |
| R             | P         | 18    |
| R             | S         | 9     |
| R             | R         | 5     |

From this data, probabilities are calculated for each possible next move.
The bot selects the most probable move and plays the counter to it.

### Why It Works

* Learns patterns dynamically during gameplay
* Improves accuracy over time
* Performs well against predictable opponents
* Outperforms static and random strategies in long matches

---

## Deployment Options

This project supports two runtime environments.

---

### 1. Web Deployment (HTML + JavaScript)

#### Features

* Runs directly in the browser
* No installation required
* Easy deployment on platforms like Vercel
* Uses Canvas or DOM for rendering

#### How to Run Locally

1. Open the project folder
2. Locate `index.html`
3. Open it in a browser

Optional (recommended):
Use a local development server such as Live Server.

#### How to Deploy

```bash
vercel deploy
```

#### Implementation Details

* Game loop handled using `requestAnimationFrame`
* Input handled via browser events
* Bots implemented in JavaScript
* Markov logic adapted from Python

---

### 2. Desktop Deployment (Pygame)

#### Features

* Native desktop execution
* Real-time rendering using Pygame
* Suitable for simulations and testing

#### Requirements

* Python 3.x
* Pygame library

#### Installation

```bash
pip install pygame
```

#### How to Run

```bash
cd pygame_version
python main.py
```

---

## Key Differences Between Deployments

| Feature     | Web Version (JS) | Pygame Version (Python) |
| ----------- | ---------------- | ----------------------- |
| Platform    | Browser          | Desktop                 |
| Rendering   | Canvas / DOM     | Pygame window           |
| Deployment  | Static hosting   | Local execution         |
| Performance | Moderate         | High                    |
| Setup       | None             | Requires installation   |

---

## Bots Included

* Random Bot
* Cycle Bot
* Frequency Analysis Bot
* Pattern Bot
* Markov Chain Bot

---

## Customization

The engine is modular and allows:

* Changing match length
* Adding new bots
* Modifying prediction logic
* Tracking performance statistics

---

## Project Goal

This project demonstrates:

* Practical use of Markov Chains
* Strategy optimization in games
* Differences between web and desktop execution environments

---

## Future Improvements

* Higher-order Markov models
* Neural network-based prediction
* Multiplayer support
* Data visualization tools

---

## Notes

This project shows how the same core logic can be implemented across:

* A browser-based environment using JavaScript
* A desktop application using Pygame

It highlights differences in rendering, input handling, and execution models.
