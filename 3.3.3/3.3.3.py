import pandas as pd
import requests

url_intervals = []
for i in range(1, 23):
    url_intervals.append(f"https://api.hh.ru/vacancies?specialization=1&date_from=2022-12-20T{str(i).zfill(2)}:00:00&date_to=2022-12-20T{str(i + 1).zfill(2)}:00:00&")

df = pd.DataFrame(columns=["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"])

for url in url_intervals:
    json_for_pages = requests.get(url).json()
    for p in range(json_for_pages["pages"] + 1):
        if json_for_pages["per_page"] < 100:
            params = {'page': p}
        else:
            params = {'per_page': '100', 'page': p}
        items = requests.get(url, params=params).json()["items"]
        for item in items:
            try:
                df.loc[len(df)] = [item["name"], item["salary"]["from"], item["salary"]["to"],
                                   item["salary"]["currency"], item["area"]["name"], item["published_at"]]
            except TypeError:
                continue

df.to_csv("vacancies_head_hunter_2022_12_20.csv", index=False)
