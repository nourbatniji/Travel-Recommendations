# Travel Recommendations

A travel recommendation system that suggests cities to visit based on a user's budget and number of cities they want to explore. Built using dynamic programming to maximize the number of attractions within a given budget.

## How It Works

Given a user, a budget, and a desired number of cities, the algorithm filters flights and hotels from the dataset and recommends the best cities to visit while staying within budget.

## Tech Stack

- Backend: Flask, Python
- Dataset: Argo Datathon 2019 (users, flights, hotels)
- Frontend: HTML, CSS

## Setup

```bash
git clone https://github.com/nourbatniji/Travel-Recommendations.git
cd Travel-Recommendations
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Input / Output

- Input: User ID, Budget, Number of cities
- Output: List of recommended cities

## Dataset

[Argo Datathon 2019 on Kaggle](https://www.kaggle.com/datasets/leomauro/argodatathon2019)

## Author

Nour — [github.com/nourbatniji](https://github.com/nourbatniji)
