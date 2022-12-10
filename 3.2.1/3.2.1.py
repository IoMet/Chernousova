import pandas as pd

pd.set_option("expand_frame_repr", False)

file_name = input("Введите название файла: ")
df = pd.read_csv(file_name)

df["years"] = df["published_at"].apply(lambda date: int(".".join(date[:4].split("-"))))
years = df["years"].unique()

for year in years:
    data_to_insert = df[df["years"] == year]
    data_to_insert[["name", "salary_from", "salary_to",
                    "salary_currency", "area_name",
                    "published_at"]].to_csv(f"csv_files\part{year}.csv", index=False)