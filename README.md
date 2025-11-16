# Rock Paper Scissors
A modular, extensible Rock–Paper–Scissors engine featuring five AI bots and a Markov Chain–based predictive model.
Built as an enhanced, customizable version of the freeCodeCamp RPS Machine Learning challenge.

This project allows the player to run custom match lengths, analyze performance, and compare strategies across multiple bots.

This repository implements:

5 AI-controlled bot opponents

A Markov Pattern Prediction Model for adaptive gameplay

Customizable match lengths with detailed statistics

Modular and scalable architecture

A fully functional RPS game engine for simulation and testing

The Markov-powered bot observes the sequence of moves played by the opponent, learns transition probabilities, and predicts the next move using a first-order Markov chain.

# Markov Chain Prediction (ML Bot)

The Markov bot builds a transition table:

Previous Move → Next Move → Count


Example:

Prev	Next	Count
R	P	18
R	S	9
R	R	5

From these probabilities, the bot predicts the opponent’s next likely move and counters it.

This results in improving accuracy as the match progresses, outperforming naive bots significantly in long match sequences.
