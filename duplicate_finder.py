import pandas as pd
from rapidfuzz import fuzz
import sys

def find_duplicates(file_path):
    cols = [
        "Company Name",
        "First Name",
        "Last Name",
        "Status",
        "Delivery Status",
        "Email",
        "LinkedIn/Lead Validation Url"
    ]

    df = pd.read_excel(file_path)

    def clean(x):
        if pd.isna(x):
            return ""
        return str(x).lower().strip()

    df["company_clean"] = df["Company Name"].apply(clean)
    df["name_clean"] = (
        df["First Name"].apply(clean) + " " + df["Last Name"].apply(clean)
    )

    output_rows = []
    pair_id = 1
    assigned = set()

    idxs = df.index.tolist()

    for x in range(len(idxs)):
        i = idxs[x]
        if i in assigned:
            continue

        ci = df.at[i, "company_clean"]
        ni = df.at[i, "name_clean"]

        group = [i]

        for y in range(x + 1, len(idxs)):
            j = idxs[y]
            if j in assigned:
                continue

            if abs(len(ci) - len(df.at[j, "company_clean"])) > 12:
                continue

            company_score = fuzz.token_sort_ratio(
                ci, df.at[j, "company_clean"]
            )
            if company_score < 50:
                continue

            name_score = fuzz.token_sort_ratio(
                ni, df.at[j, "name_clean"]
            )
            if name_score >= 80:
                group.append(j)

        # Only create a duplicate group if more than 1 row
        if len(group) > 1:
            pid = f"DUP_{pair_id}"
            for idx in group:
                row = df.loc[idx, cols].copy()
                row["Pair_ID"] = pid
                row["Excel_Row"] = idx + 2
                row["Company_Score"] = company_score
                row["Name_Score"] = name_score
                output_rows.append(row)
                assigned.add(idx)

            pair_id += 1

    final_df = pd.DataFrame(output_rows)
    if not final_df.empty:
        final_df = final_df.sort_values(by=["Pair_ID", "Excel_Row"])

    return final_df


if __name__ == "__main__":
    file_path = sys.argv[1]
    df = find_duplicates(file_path)
    print(df)
