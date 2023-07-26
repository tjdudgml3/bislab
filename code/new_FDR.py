import pandas as pd
import re

def get_FDR(dataframe, path):
    df = dataframe
    fitted_idx = 0
    target = 0
    decoy = 0
    fitted_target = 0
    for idx, label in enumerate(df["label"]):
        if label == 1:
            target += 1
        else:
            decoy += 1

        if decoy == 0:
            fitted_idx = idx
            fitted_target = target
        if decoy/target <= 0.01:
            fitted_idx = idx
            fitted_target = target
    df.to_csv(f"{path}/original.pin")
    return fitted_target



# print(get_FDR())


def get_new_FDR(path):
    df_target = pd.read_csv(f"{path}/target.pin", delimiter="\t")
    df_decoy = pd.read_csv(f"{path}/decoy.pin", delimiter="\t")

    df_target.insert(4, "label", 1)
    df_decoy.insert(4, "label", -1)

    df=pd.concat([df_decoy,df_target])
    # df.to_csv("./temp/concat.pin")
    df = df.sort_values(by="score", ascending=False)
    # df.to_csv("./temp/sort.pin")
    df = df.drop_duplicates(subset=["PSMId"], keep="first")
    result = get_FDR(df, path)
    print(f"{path} = {result} psms")
    
get_new_FDR("./output_percolator/")
