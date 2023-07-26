import pandas as pd
import numpy as np
import re
# import pysptools.distance.SAM
from pysptools.distance import SAM
# def match_seq(seq):


def get_ms2_dic():
    cnt = 0
    df_prosit = pd.read_csv("./prosit/prosit.csv")
    # df_prosit = df_prosit[2000:10000]
    # df_prosit.to_csv("sliced_prosit.csv")
    # exit()
    df_prosit= df_prosit[:70000000]
    # df_prosit = df_prosit[100000000:]
    ms_dict = {}
    for seq, precursor_mz, mz, intensity in zip(df_prosit["ModifiedPeptide"], df_prosit["PrecursorCharge"], df_prosit["FragmentMz"], df_prosit["RelativeIntensity"]):
        if (seq,precursor_mz) not in ms_dict:
            ms_dict[(seq,precursor_mz)] = [[mz,intensity]]
        elif (seq,precursor_mz) in ms_dict:
            ms_dict[(seq,precursor_mz)].append([mz,intensity])
    print("@@@@@@@@@@@@@dict made@@@@@@@@@@@@@@@@@@")
    # print(ms_dict)
    # for a in ms_dict:
    #     print(a)
    #     for b in ms_dict[a]:
    #         print(b)
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    # for a in ms_dict[('_KPAAAAGAK_', 2)]:
    #     print(a)

    df_input = pd.read_csv("./prosit/input_for_prosit2.pin")
    mgf = open("./conc_file.mgf")#concatted hek file
    sa_list = []
    mgf_info = mgf.readlines()
    mgf.close()
    idx = 0
    prev_idx = 0
    for sequence, charge, id in zip(df_input["modified_sequence"], df_input["precursor_charge"], df_input["id"]):
        title_idx = 0
        temp = []
        tolerance = 0.025
        idx = prev_idx
        # idx = 0
        lenth = len(mgf_info)
        while(idx < lenth):
            m = re.match(f".*{id}_.*", mgf_info[idx].replace(".","_"))
            if m:
                title_idx = idx
                prev_idx =idx
                # print(f"title idx= {title_idx}, title = {mgf_info[title_idx]} ")
                break
            if idx == lenth -1:
                prev_idx = 0
            idx += 1
        # for idx in range(len(mgf_info)):
        #     # print(f"id = {id}, mgf_idx = {mgf_info[idx+1].replace('.', '_')}")
        #     # exit()
        #     m = re.match(f".*{id}_.*", mgf_info[idx].replace(".","_"))
        #     if m:
        #         title_idx = idx
        #         # print(f"title idx= {title_idx}, title = {mgf_info[title_idx]} ")
        #         break

        for idx in range(title_idx+4, len(mgf_info)):
            if mgf_info[idx] == 'END IONS\n':
                break
            temp.append(mgf_info[idx].strip())
        # print(temp)
        # exit()
        sa_vector_prosit = []
        sa_vector_mgf = []
        # print(ms_dict)
        
        # for j, i in enumerate(ms_dict):
        #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #     print(i)
        #     print(ms_dict[i])
        #     if j == 3:
        #         break

        # print(f"seq,charge = {(sequence,charge)}")
        # exit()
        if (sequence, charge) not in ms_dict:
            cnt += 1
            # print(f"none exist = {sequence,charge}")
            sa_list.append((-1,id,sequence,mgf_info[title_idx][6:]))
            # if cnt == 4000:
            #     break
            if cnt % 10000 == 0 and cnt >1:
                with open(f"./prosit/output2/sa_scores_total{cnt}.csv", "w") as f:
                    f.write("SA,prosit_id,prosit_seq,ori_id\n")
                    for a in sa_list:
                        for i,b in enumerate(a):
                            if i == 3:
                                f.write(f"{b.strip()}")
                            else:
                                f.write(f"{b},") 
                        
                        f.write(f"\n")
                        sa_list = []
            continue
        # i = 0
        for mz, intensity in ms_dict[(sequence, charge)]:
            is_exist = 0
            # while(True):

            for i, info in enumerate(temp):
                mgf_mz, mgf_intensity = info.split(" ")
                mgf_mz = float(mgf_mz)
                mgf_intensity = float(mgf_intensity)
                if abs(mz - mgf_mz) < tolerance:
                    sa_vector_mgf.append(mgf_intensity)
                    sa_vector_prosit.append(intensity)
                    is_exist = 1
                    break
                # if i == len(temp)-1:
                #     sa_vector_mgf.append(0)
                #     sa_vector_prosit.append(intensity)
        # print(len(sa_vector_mgf), len(sa_vector_prosit))
        # print("@@@@@@@@@@@@@@@@")
        # print(sequence)
        # for a,b in zip(sa_vector_mgf, sa_vector_prosit):
        #     print(f"mgf = {a}, prosit = {b}")
        
        # if cnt > 20:
        #     break
        if not sa_vector_prosit:
            sa_list.append((0, id, sequence, mgf_info[title_idx][6:])) 
        else:
            sa_list.append((SAM(sa_vector_prosit, sa_vector_mgf),id,sequence,mgf_info[title_idx][6:]))
        # print(sa_list)
        # exit()
        # print(f"sa_list = {sa_list}, sa_vectors = {sa_vector_mgf}, {sa_vector_prosit}")
        # if cnt%100:
        #     print(f"cnt = {cnt}, len(SA) = {len(sa_list)}, seq = {sequence}, mgh_info = {mgf_info[title_idx][6:]}, prosit = {id}")
        cnt += 1
        if cnt % 1000 == 0:
            print(f"cnt = {cnt}, id = {id}")
        
        if cnt % 10000 == 0 and cnt >1:
            with open(f"./prosit/output2/sa_scores_total{cnt}.csv", "w") as f:
                f.write("SA,prosit_id,prosit_seq,ori_id\n")
                for a in sa_list:
                    for i,b in enumerate(a):
                        if i == 3:
                            f.write(f"{b.strip()}")
                        else:
                            f.write(f"{b},") 
                    
                    f.write(f"\n")
                    sa_list = []
        # if cnt == 4000:
        #     break

    with open("./prosit/output2/sa_scores_total1.csv", "w") as f:
        f.write("SA,prosit_id,prosit_seq,ori_id\n")
        for a in sa_list:
            for i,b in enumerate(a):
                if i == 3:
                    f.write(f"{b.strip()}")
                else:
                    f.write(f"{b},") 
            
            f.write(f"\n")
        # exit()

    return sa_list

# get_ms2_dic()       
# exit()
def merge_prosit_output():
    file = "./prosit/output3/sa_scores_total10000.csv"
    # r = (r",b1906.*,")
    df = pd.read_csv(file)
    print(df.shape)
    # exit()
    # exit()
    # df = pd.concat(df,df)
    for a in range(2,1093):
        file = f"./prosit/output3/sa_scores_total{a*10000}.csv"
        df_a = pd.read_csv(file)
        # print(df_a.shape)
        # exit()
        df = pd.concat([df,df_a])
    df_a = pd.read_csv("./prosit/output3/sa_scores_total1.csv")

    df = pd.concat([df,df_a])

    # df = df.sort_values(by="idx")
    print(df.shape)
    df.to_csv("SA_third_iter.pin", sep="\t", index=False)
    df_SA = df["SA"]
    df_SA.to_csv("./prosit/SA_only_third_iter1.pin")

    # mgf.close()
    
# merge_prosit_output()
# exit()

def concta_autort():
    df = pd.read_csv("./autoRT/test1.tsv", delimiter="\t")
    for a in range(2,5):
        file_name = f"./autoRT/test{a}.tsv"
        df_a = pd.read_csv(file_name, delimiter="\t")
        df = pd.concat([df, df_a])
    series = []
    for y, ypred in zip(df["y"], df["y_pred"]):
        series.append(abs(float(ypred) - float(y)))
    with open("./autoRT/delta_RT.tsv", "w") as f:
        f.write("deltaRT\n")
        for ele in series:
            f.write(f"{ele}\n")
    
    # df.to_csv("autoRT/read_RT.pin", sep="\t", index=False)
# concta_autort()
# exit()
def add_SA_to_input(file_name, output_file = "./SA_deltaRT_added.pin"):
    df_sa = pd.read_csv("./autoRT/delta_RT.tsv", delimiter="\t")

    df = pd.read_csv(file_name, delimiter="\t")
    # df_sa = pd.read_csv("./autoRT/delta_RT.tsv", delimiter="\t")
    # df= df.drop(["charge", "SA"], axis=1)
    # df.to_csv("output/temp_SA.pin")
    # exit()
    df.insert(7, "deltaRT", df_sa)
    # df.insert(19, "sequence", df_rt["x"])
    df.to_csv(output_file, sep='\t', index=False)
    return output_file

add_SA_to_input("SA_added.pin")
# exit()
# get_ms2_dic()
# exit()
def match_protein_name_prosit_input(inputfile):
    df = pd.read_csv("./reranked/reranked_finale1.pin", delimiter="\t")
    df_prosit = pd.read_csv("./prosit/myPrositLib_sliced.csv")
    df_prosit.drop_duplicates(subset=['RelativeIntensity', 'LabeledPeptide'])
    df_prosit.to_csv("./prosit/duplicated.csv", index=False, sep="\t")
    i = 2
    
    # exit()
    # for i, ele in enumerate(df):
    #     for j, ms in enumerate(df_prosit):
    #         pass
    i = 0 #
    j = 0 #3
    new_series = []
    for seq, id in zip(df["Peptide"], df["SpecId"]):
        pass


def drop():
    df = pd.read_csv("./prosit/input_for_prosit1.csv")
    df = df.drop_duplicates(subset=["modified_sequence", "precursor_charge"])
    df.to_csv("./prosit/input_prosit_dropped.csv", index=False)

# drop()

def fill_zeros_na():
    df = pd.read_csv("./prosit/SA_only_third_iter1.pin")
    series = []
    # df.fillna(method="ffill")
    df = df["SA"]
    # df.fillna(method="ffill")
    # df.fillna(method="ffill")
    mean_val = df.mean()
    # print(mean_val)
    # exit()
    # print(df.mean())
    for ele in df:
        if ele == 0:
            series.append(1.55)
            # print(df["idx"].loc(ele))
            # print(ele)
            # exit()
        elif ele == -1:
            series.append(mean_val)
        else:
            series.append(ele)

    with open("./prosit/real_SA.pin", "w") as f:
        f.write("SA\n")
        for a in series:
            f.write(f"{a}\n")

# fill_zeros_na()
# exit()

# print("asd")
def get_penalty():
    df = pd.read_csv("./output/real_final.pin", delimiter="\t")
    df =df["SA_new"]
    df.to_csv("./output/penalty_needed.pin")


# df = pd.read_csv("./reranked/reranked_finale1.pin", delimiter="\t")
# df_input = pd.read_csv("./output/real_real_final.pin", delimiter="\t")
# df_input = df_input.drop(["SA", "charge"], axis=1)
# # df_input
# # print(df.columns)
# # exit()
# # df_input.insert(7, "delta_rt", df["deltaRT"])
# df_input.to_csv("./output/real_real_final_with_no_SA.pin", index=False, sep="\t")
# get_penalty()
# print(SAM([1,2,31,9], [1,2,2,1]))
# print(SAM([1,1,1,1,1,0,0,0,1],[1,1,0,0,0,0,1,1,1,1]))
# print(SAM([200,210,0,12],[17,23,199,200]))
# print(SAM([1,0],[1,1]))