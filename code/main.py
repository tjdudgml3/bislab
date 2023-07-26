import pandas as pd
import numpy as np
# import preprocess
import warnings
import re

def preprocess(file_name, out_file_name = "new_input.pin"): #substring "" in protein name
    
    file = open(file_name, "r")
    file_write = open(out_file_name, "w")
    lines = file.readlines()
    cnt = 0
    for a in lines:
        a = a.replace("\"", '')

        file_write.write(a)
    file.close()
    file_write.close()
    return out_file_name

# df = pd.read_csv("SA_deltaRT_added.pin", delimiter="\t")
# df = df.drop(["RT","Charge"], axis = 1)
# df.to_csv("./final_ouput.pin", sep="\t", index=False)
preprocess("./final_ouput.pin", "./input_percolator/final_output.pin")
exit()

def preprocess_for_prosit(file_name, out_file_name = "./prosit/input_for_prosit2.pin"):

    df = pd.read_csv(file_name, delimiter= '\t')
    # cnt = 0
    new_series = []
    for sequence in df["Peptide"]:
        # print(sequence)
        new_sequence = sequence.replace("M+15.99", "M[Oxidation (O)]")
        new_sequence = new_sequence.replace("C+57.02", "C[Carbamidomethyl (C)]")
        new_series.append("_"+new_sequence+"_")
        # if cnt == 53:
        #     break
        # cnt += 1
    # df["Peptide"][:54] = new_series
    # df.to_csv(out_file_name, sep= "\t")
    # cnt = 0
    with open(out_file_name, "w") as f:
        
        f.write("modified_sequence,collision_energy,precursor_charge,fragmentation,id")

        f.write("\n")
        
        for seq, charge, id in zip(new_series, df["Charge"], df["SpecId"]):
            # cnt += 1
            # if cnt == 6:
            #     break
            # if charge < 1 or charge > 10:
            #     print(seq)
            #     break
             
            f.write(f"{seq},25,{charge},CID,{id}\n")

    # sequence_series = pd.Series(new_series)
    # print(sequence_series)
    # sequence_series.to_csv("sequence_list.pin")
    return out_file_name    

preprocess_for_prosit("ex_rt_charge_added.pin")
exit()
# def get_delta_RT()

#id 맞추기



def find_msf_with_ScanNum(msf_file):
    # temp = []
    title_idx = 0
    msf = open(msf_file, 'r')
    msfs = msf.readlines()
    rt_list = []
    scan_num_list = []
    cnt = 0
    for idx in range(len(msfs)):
        if cnt % 100000 ==0:
            print(cnt)
        cnt += 1
        m = re.match(f'.*\.[0-9]*\.[0-9]*.*', msfs[idx]) #정규표현식을 이용해서 scanNum 찾음.
        
        if m:
            title_idx = idx
            rt_list.append(msfs[title_idx+1][12:].strip())
            # title = msfs[title_idx].replace(".","_")[6:].strip()
            # title = re.sub(r"",", title" )
            scan_num = msfs[title_idx].replace(".","_")[6:].strip()
            scan_num = re.findall(f".*_.*_.*_.*_.*_.*_.*_", scan_num)
            # print(scan_num[0])
            # exit()
            title = str(scan_num[0])
            title = title.split("_")[:7]
            temp = ""
            for a in title:
                temp += a
                temp += "_"
            scan_num_list.append(temp[:-1])
            
    
    # for idx in range(title_idx+4,len(msfs)):
    #     if msfs[idx] == 'END IONS\n':
    #         break
    #     temp.append(msfs[idx].strip())
    
    msf.close()
    with open("experimental_rt1.pin", "w") as f:
        for rt,scan_num in zip(rt_list, scan_num_list):
            f.write(f"{rt},{scan_num}\n")

    return

# find_msf_with_ScanNum("./conc_file.mgf")
# exit()
df1 = pd.read_csv("ex_rt_charge_added.pin", delimiter="\t")
df1 = df1.drop("RT", axis=1)
df2 = pd.read_csv("experimental_rt1.pin", names=["RT", "SpecId"])
df = pd.merge(df1,df2, how = "inner", on = "SpecId")
df.to_csv("new_rt_added.pin")
exit()
import os

#The folder containing the 24 mgf files & ouput file name
folder_path = 'mgf_files'
conc_file = 'conc_file.pin'

file_list = os.listdir(folder_path)
file_list.sort() #little sorting

#start the concata...
with open(conc_file, 'w') as final_file:
    #Iterating through each file in the folder
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        #Checking if the item in the folder is a file or not
        if os.path.isfile(file_path):
            with open(file_path, 'r') as current_file:
                #Reading the content of the file
                file_content = current_file.read()

                #Write the content to the final_mgf file
                final_file.write(file_content)

exit()
def make_ids_same():
    # filename = open("./hek293_feature_for_DL.pin", "r")
    df = pd.read_csv('./hek293_feature_for_DL.pin', sep='\t')

    # Modifying the "SpecId" column - removing ranking at end
    df['SpecId'] = df['SpecId'].str.replace(r'(_[0-9]+){2}$', '', regex=True)
    df.to_csv("original_hek", index=False, sep="\t")




# make_ids_same()

# warnings.filterwarnings(action='ignore') 
# #slice rank by rank5 -> get half dataset
# def rerank(inputfile):
#     df = pd.read_csv(inputfile, delimiter="\t")
#     # df = df[:4000]
#     df.to_csv("reranked/original1.pin", sep="\t", index_label='idx')
#     df = pd.read_csv("reranked/original1.pin", delimiter="\t")
#     # print(df["idx"])
#     # exit()
#     asd = df.groupby("SpecId")
#     new_df = np.array([])
#     temp = []
#     # print(asd.shape)
#     # new_df = pd.DataFrame(new_df)
#     # df.to_csv("reranked/test.pin" sep="\t")
#     cnt = 0
#     for i,ele in enumerate(asd):
#         # print(ele)
        
#         ele = np.array(ele)
#         ele[1] = ele[1][:5]
#         # print(len(ele[1]))
#         # print(ele[1])
#         # exit()
#         if i == 0:
#             temp = ele[1]
#             continue
#         elif i % 10000 == 0:
#             column = ["idx", "SpecId","Label","ScanNr","ExpMass","dM","absdM","dMppm","absdMppm","FracBMatchInt","FracYMatchInt","SeqCoverBion","SeqCoverYion","ConsecutiveBion","ConsecutiveYion","Xcorr","PepLen","enzInt","NumofAnnoPeaks","Peptide","Proteins"]
#             temp = pd.DataFrame(temp, columns=column)
#             temp = temp.sort_values(by="idx")
#             temp.to_csv(f"reranked/reranked{i}.pin",index=False, sep="\t")
#             temp = ele[1]
#             continue
#         # ele = np.array(ele)
#         # print(ele)
#         # exit()
#         # temp += ele[1]
#         temp = np.append(temp, ele[1] ,axis=0)
#         # print(f"ele.shape = {ele.shape}, temp = {temp.shape}")
#         # ele = pd.DataFrame(ele[1])
#         # print(ele)
#         # print(type(ele))
#         # new_df.append(ele.nlargest(5,"Xcorr",keep="first"))
#         # temp = np.append(new_df, ele ,axis = 0)
#         # print(new_df.shape)
#         if cnt % 1000 ==0:
#             # print(temp)
#             print(f"cnt = {cnt} temp = {len(temp)}")

#         cnt += 1

#     # print(temp)
#     # df = pd.DataFrame(temp)
#     # print(df.shape)
#     # df.to_csv("./reranked/ouput1.pin")
#     # out_file = open("./reranked/output.pin", "w")
#     # for a in temp:
#     #     for b in a:
#     #         out_file.write(b)
#     # out_file.close()
#     # exit()
#     column = ["idx", "SpecId",	"rt_file1_experimental","Label","deltaRT","charge","ScanNr","ExpMass","dM","absdM","dMppm","rt_file2_input","absdMppm","FracBMatchInt","FracYMatchInt","SeqCoverBion","SeqCoverYion","ConsecutiveBion","ConsecutiveYion","Xcorr","PepLen","enzInt","NumofAnnoPeaks","Peptide","Proteins"]
#     temp = pd.DataFrame(temp, columns=column)
#     temp = temp.sort_values(by="idx")
#     temp.to_csv("reranked/reranked_final.pin",index=False, sep="\t")

# rerank("./original_hek")

# def merge_ranked_input():
#     file = "./test/reranked10000.pin"
#     df = pd.read_csv(file, delimiter="\t")
#     print(df.shape)
#     # exit()
#     # df = pd.concat(df,df)
#     for a in range(2,17):
#         file = f"./test/reranked{a*10000}.pin"
#         df_a = pd.read_csv(file, delimiter="\t")
#         print(df_a.shape)
#         # exit()
#         df = pd.concat([df,df_a])
#     df_a = pd.read_csv("./test/reranked_final.pin", delimiter="\t")

#     df = pd.concat([df,df_a])
#     df = df.sort_values(by="idx")
#     print(df.shape)
#     df.to_csv("reranked/reranked_finale1.pin", sep="\t", index=False)