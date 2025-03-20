from itertools import combinations
from multiprocessing import Pool, cpu_count

import networkx as nx
import networkx.algorithms.community as nx_comm
import pandas as pd
from fuzzywuzzy import fuzz
from geopy.distance import geodesic

from util import get_csv_filepath


def compare_personal(u1, u2):
    similar = []
    points = 0
    sim_fn = fuzz.ratio(str(u1["first_name"]), str(u2["first_name"])) / 100.0
    if sim_fn >= 0.8:
        similar.append((u1["first_name"], sim_fn))
        points += 1

    sim_ln = fuzz.ratio(str(u1["last_name"]), str(u2["last_name"])) / 100.0
    if sim_ln >= 0.8:
        similar.append((u1["last_name"], sim_ln))
        points += 1

    if str(u1["gender"]).strip().lower() == str(u2["gender"]).strip().lower():
        similar.append((u1["gender"], 1.0))
        points += 1

    if str(u1["date_of_birth"]) == str(u2["date_of_birth"]):
        similar.append((u1["date_of_birth"], 1.0))
        points += 1

    return points, similar


def compare_address(u1, u2):
    similar = []
    points = 0
    sim_city = fuzz.ratio(str(u1["city"]), str(u2["city"])) / 100.0
    if sim_city >= 0.8:
        similar.append(("city", sim_city))
        points += 1

    sim_street = fuzz.ratio(str(u1["street_name"]), str(u2["street_name"])) / 100.0
    if sim_street >= 0.8:
        similar.append(("street_name", sim_street))
        points += 1

    sim_addr = fuzz.ratio(str(u1["street_address"]), str(u2["street_address"])) / 100.0
    if sim_addr >= 0.8:
        similar.append(("street_address", sim_addr))
        points += 1

    sim_zip = fuzz.ratio(str(u1["zip_code"]), str(u2["zip_code"])) / 100.0
    if sim_zip >= 0.8:
        similar.append(("zip_code", sim_zip))
        points += 1

    sim_state = fuzz.ratio(str(u1["state"]), str(u2["state"])) / 100.0
    if sim_state >= 0.8:
        similar.append(("state", sim_state))
        points += 1

    try:
        coord1 = (float(u1["latitude"]), float(u1["longitude"]))
        coord2 = (float(u2["latitude"]), float(u2["longitude"]))
        distance = geodesic(coord1, coord2).km
        if distance < 10:
            similar.append(("location", 1.0))
            points += 1
    except Exception as e:
        print("Error happened during comparing coordinates", e)
        pass

    return points, similar


def compare_employment(u1, u2):
    similar = []
    points = 0
    sim_title = (
        fuzz.ratio(str(u1["employment_title"]), str(u2["employment_title"])) / 100.0
    )
    if sim_title >= 0.8:
        similar.append(("employment_title", sim_title))
        points += 1

    sim_skill = fuzz.ratio(str(u1["key_skill"]), str(u2["key_skill"])) / 100.0
    if sim_skill >= 0.8:
        similar.append(("key_skill", sim_skill))
        points += 1

    return points, similar


def compare_subscription(u1, u2):
    similar = []
    points = 0
    for field in [
        "subscription_plan",
        "subscription_status",
        "payment_method",
        "subscription_term",
    ]:
        sim_val = fuzz.ratio(str(u1[field]), str(u2[field])) / 100.0
        if sim_val >= 0.8:
            similar.append((field, sim_val))
            points += 1
    return points, similar


def compare_users(u1, u2, strong_threshold=5):
    pers_pts, pers_sim = compare_personal(u1, u2)
    addr_pts, addr_sim = compare_address(u1, u2)
    emp_pts, emp_sim = compare_employment(u1, u2)
    subs_pts, subs_sim = compare_subscription(u1, u2)

    total_points = pers_pts + addr_pts + emp_pts + subs_pts
    result = {
        "User1": u1["uid"],
        "User2": u2["uid"],
        "Personal_Similar": "; ".join(
            [f"{field}:{score:.2f}" for field, score in pers_sim]
        ),
        "Personal_Points": pers_pts,
        "Address_Similar": "; ".join(
            [f"{field}:{score:.2f}" for field, score in addr_sim]
        ),
        "Address_Points": addr_pts,
        "Employment_Similar": "; ".join(
            [f"{field}:{score:.2f}" for field, score in emp_sim]
        ),
        "Employment_Points": emp_pts,
        "Subscription_Similar": "; ".join(
            [f"{field}:{score:.2f}" for field, score in subs_sim]
        ),
        "Subscription_Points": subs_pts,
        "Total_Points": total_points,
    }

    if total_points >= strong_threshold:
        result["Connection_Type"] = "Strong"
    elif total_points >= 2:
        result["Connection_Type"] = "Weak"
    else:
        return None

    return result


def compare_pair(pair):
    return compare_users(pair[0], pair[1])


def build_groups(pairs, type_filter):
    G = nx.Graph()
    for pair in pairs:
        if pair["Connection_Type"] == type_filter:
            G.add_edge(pair["User1"], pair["User2"])
    communities = list(nx_comm.greedy_modularity_communities(G))
    groups = [sorted(list(comm)) for comm in communities if len(comm) > 1]
    return groups


def find_similar_users(users_df):
    """
    Given a DataFrame of users, perform pairwise fuzzy matching.
    Note: For 1000 users, there are nearly 500,000 pairs.
    ##TODO Consider performance implications for larger datasets.
    """
    users = users_df.to_dict("records")
    user_pairs = list(combinations(users, 2))
    print(f"Comparing {len(user_pairs)} pairs using {cpu_count()} CPU cores...")

    with Pool(cpu_count()) as pool:
        comparisons = pool.map(compare_pair, user_pairs)
    comparisons = [comp for comp in comparisons if comp is not None]

    # Save pairwise similarities
    pair_df = pd.DataFrame(comparisons)
    pair_csv_path = get_csv_filepath("pairwise_similarities.csv")
    pair_df.to_csv(pair_csv_path, index=False)
    print("Pairwise similarities saved to pairwise_similarities.csv")

    # Build groups
    strong_groups = build_groups(comparisons, "Strong")
    weak_groups = build_groups(comparisons, "Weak")

    strong_df = pd.DataFrame(
        {
            "Group": range(1, len(strong_groups) + 1),
            "User_UIDs": [", ".join(map(str, grp)) for grp in strong_groups],
        }
    )
    weak_df = pd.DataFrame(
        {
            "Group": range(1, len(weak_groups) + 1),
            "User_UIDs": [", ".join(map(str, grp)) for grp in weak_groups],
        }
    )

    strong_csv_path = get_csv_filepath("strong_groups.csv")
    weak_csv_path = get_csv_filepath("weak_groups.csv")
    strong_df.to_csv(strong_csv_path, index=False)
    weak_df.to_csv(weak_csv_path, index=False)
    print("Strong groups saved to strong_groups.csv")
    print("Weak groups saved to weak_groups.csv")

    return pair_df, strong_groups, weak_groups


if __name__ == "__main__":
    try:
        users_df = pd.read_csv("random_users.csv")
    except Exception as e:
        print("Error loading CSV file:", e)
        exit(1)

    pair_df, strong_groups, weak_groups = find_similar_users(users_df)
