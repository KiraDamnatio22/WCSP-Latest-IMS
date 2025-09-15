import pandas as pd

df = pd.read_excel("C://Users//mrenz//OneDrive//Documents//Python Repo//Python Space//My Projects//Inventory Management System//EXECUTABLE//testing folder//Inventory-Records.xlsx")

# Clean column names: remove line breaks, strip spaces, replace multiple spaces with one
df.columns = (
    df.columns
    .str.replace(r"\n", " ", regex=True)   # replace line breaks
    .str.replace(r"\s+", " ", regex=True)  # collapse multiple spaces
    .str.strip()                           # trim spaces
    .str.replace('-', ' ', regex=False)    # treat hyphens as word separators
    .str.replace(r'[^\w\s]', '', regex=True) # remove punctuation
    .str.lower()
    .str.replace(r'\s+', '_', regex=True)  # spaces -> underscores
)

""" Display first 5 rows """
# print(df.head())

""" View all column names """
# print(df.columns)

""" View all column names (list-format) """
# print("columns:", df.columns.tolist())

""" Access single column """
# print(df["product_id"])

""" Access multiple column """
# print(df[["product_id", "product_name", "opening_stock"]])

""" Iterate through rows """
# for index, row in df.iterrows():
#     print(row["product_id"], row["product_name"])

""" Read from a specific sheet """
# df2 = pd.read_excel("your_file.xlsx", sheet_name="Sheet2")


product_ids = df["product_id"].tolist()
product_names = df["product_name"].tolist()
product_total_price = df["cost_price_total_usd"].tolist()
print(product_ids)
print(product_names)
print(product_total_price)
