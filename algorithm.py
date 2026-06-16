import pandas as pd

def load_data():
    # reads as tables
    users   = pd.read_csv("datasets/users.csv")
    flights = pd.read_csv("datasets/flights.csv")
    hotels  = pd.read_csv("datasets/hotels.csv")
    return users, flights, hotels


# data cleaning: how much each city will cost
def prepare_city_costs(flights, hotels, user_code):
    user_flights = flights[flights["userCode"] == user_code]
    user_hotels  = hotels[hotels["userCode"]  == user_code]

    # create a table
    merged = pd.merge(user_flights, user_hotels, on="travelCode", suffixes=("_flight", "_hotel"))
    # created new column with total price of city
    merged["total_cost"] = merged["price_flight"] + merged["total"]
    trips = merged[["to", "total_cost"]].copy()  # keep only city, total cost, skip the rest
    trips.columns = ["city", "cost"]
    # Keep all trips (no groupby) so the DP can pick multiple trips per city
    # and make better use of the full budget
    trips = trips.reset_index(drop=True)
    return trips


def dp_recommend(trips, budget, max_cities):
    cities = trips["city"].tolist()
    costs  = [int(c) for c in trips["cost"].tolist()]
    n      = len(cities)

    # dp[i][b] = (max_cities_count, max_spend) as a tuple
    NEG = (-1, -1)
    dp = [[NEG] * (budget + 1) for _ in range(n + 1)]
    for b in range(budget + 1):
        dp[0][b] = (0, 0)

    for i in range(1, n + 1):
        cost = costs[i - 1]
        for b in range(budget + 1):
            # Option 1: skip this city
            skip = dp[i - 1][b]

            # Option 2: take this city (if affordable and cities limit not hit)
            take = NEG
            if cost <= b and dp[i - 1][b - cost] != NEG:
                prev_count, prev_spend = dp[i - 1][b - cost]
                if prev_count < max_cities:
                    take = (prev_count + 1, prev_spend + cost)

            # Pick the better option: more cities first, then more spend
            if take == NEG:
                dp[i][b] = skip
            elif skip == NEG:
                dp[i][b] = take
            else:
                # Prefer more cities; tie-break by higher spend
                dp[i][b] = take if (take[0] > skip[0] or
                                    (take[0] == skip[0] and take[1] > skip[1])) else skip

    # Traceback
    chosen = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(cities[i - 1])
            b -= costs[i - 1]

    return chosen, len(chosen)


def get_user(users, user_code):
    user = users[users["code"] == user_code]
    if user.empty:
        return None
    return user.iloc[0]

def run_recommendation(user_code, budget, max_cities):
    users, flights, hotels = load_data()
    user = get_user(users, user_code)
    if user is None:
        return {"error": "User not found"}

    trips = prepare_city_costs(flights, hotels, user_code)
    if trips.empty:
        return {"error": "No trips found for this user"}

    recommended_cities, count = dp_recommend(trips, budget, max_cities)
    if not recommended_cities:
        return {"error": "No cities fit within your budget"}

    result_cities = []
    total_spent = 0
    # Track index to correctly match cost for repeated cities
    city_cost_map = dict(zip(trips["city"], trips["cost"]))
    remaining_cities = list(recommended_cities)

    for city in recommended_cities:
        cost = float(trips[trips["city"] == city]["cost"].values[0])
        total_spent += cost
        result_cities.append({"city": city, "cost": round(cost, 2)})

    return {
        "user_name": user["name"],
        "cities": result_cities,
        "total_spent": round(total_spent, 2),
        "remaining": round(budget - total_spent, 2),
        "count": count
    }

