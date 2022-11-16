# %%

import pandas as pd
import os

# %%

files = [f for f in os.listdir("results/")]

# %%

files

# %%

n_dict = {}
for data_t in ["u", "w", "s"]:
    for ep in [100, 250, 500]:
        n_dict[data_t + str(ep)] = []

# %%

for f in files:
    params = f.split("-")
    n_dict[params[0][0] + str(params[1])].append(f)


# %%

def get_penalty(params):
    if "PBIL" in params:
        return params[5]
    else:
        return ""


def get_lr(params):
    if "PBIL" in params:
        return params[-1]
    else:
        return ""


def get_best(results):
    if results.empty:
        return 0
    else:
        return results.head(1).iloc[0, 1]


def get_best_w(results):
    if results.empty:
        return 0
    else:
        return results.head(1).iloc[0, 0]


def get_mean(results):
    if results.empty:
        return 0
    else:
        return round(results["profit"].mean(), 2)


def get_std(results):
    if results.empty:
        return 0
    else:
        return round(results["profit"].std(), 2)


def get_time(df_):
    if df_.empty:
        return 0
    else:
        return round(df_["time"].mean(), 2)


i = 1
df_data = []
for key_ in n_dict.keys():
    df_data.append([])
    for f in n_dict[key_]:
        in_f = pd.read_csv("results/" + f)
        valid_res = in_f[in_f["weight"] <= int(params[2])].sort_values("profit",
                                                                       ascending=False)
        params = f.split("-")
        i += 1
        tmp_dict = {"algorithm": params[4],
                    "penalty": get_penalty(params),
                    "lr": get_lr(params),
                    "best": get_best(valid_res),
                    "mean": get_mean(valid_res),
                    "time": get_time(in_f),
                    "zzzz": get_best_w(valid_res),
                    "zzzzz": get_std(valid_res),
                    "zzzzzzzzz": valid_res.shape[0] / int(params[3])}
        df_data[-1].append(tmp_dict)

# %%

for name, data_lst in zip(n_dict.keys(), df_data):
    tmp_df = pd.DataFrame(data_lst)
    tmp_df = tmp_df.sort_values(by=["algorithm", "penalty", "lr"])
    tmp_df.to_csv(name + ".csv")
