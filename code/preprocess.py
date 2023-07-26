import pandas as pd
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

# df = pd.read_csv("output/reranked_original.pin", delimiter="\t")
# df = df.drop(["absdMppm"], axis = 1)
# df.to_csv("./output/real_with_no_ez.pin", sep="\t", index=False)
preprocess("./big_size/original_hek.pin", "./input_percolator/original_hek.pin.pin")
exit()
def preprocess_mod(file_name, out_file_name = "input_mod.tsv"):

    df = pd.read_csv(file_name, delimiter= '\t')
    cnt = 0
    new_series = []
    for sequence in df["Peptide"]:
        # print(sequence)
        new_sequence = sequence.replace("M+15.99", "1")
        new_sequence = new_sequence.replace("C+57.02", "C")
        new_series.append(new_sequence)
        # if cnt == 53:
        #     break
        # cnt += 1
    # df["Peptide"][:54] = new_series
    # df.to_csv(out_file_name, sep= "\t")
    with open("input_for_auto_rt.tsv", "w") as f:
        f.write("x\ty")
        f.write("\n")
        for seq, y in zip(new_series, df["rt_file1_experimental"]):
            f.write(f"{seq}\t{y/60}\n")
    # sequence_series = pd.Series(new_series)
    # print(sequence_series)
    # sequence_series.to_csv("sequence_list.pin")
    return out_file_name
# preprocess_mod("./prosit/output/SA_added.pin")
# exit()

def preprocess_mod_alphapep(file_name, out_file_name = "input_mod.pin"):

    df = pd.read_csv(file_name, delimiter= '\t')
    cnt = 0
    new_series = []
    modifi_series = []
    mod_type = []
    # df = df[:100]
    cnt = 0
    for i,sequence in enumerate(df["Peptide"]):
        # print(sequence)
        temp = sequence
        if cnt%100000 == 0:
            print(cnt)
        modifi_series.append("")
        mod_type.append("")
        # print(sequence)
        while("M+15.99" in temp or "C+57.02" in temp):
            mod_cnt = 0
            for idx in range(len(temp)-6):
                if temp[idx: idx + 7] == "M+15.99":
                    # temp.replace("M+15.99", "M")
                    modifi_series[i] += str((idx-mod_cnt*6 + 1))
                    modifi_series[i] += str(';')
                    mod_type[i] += "Oxidation@M;"
                    mod_cnt += 1
                    # break
                elif temp[idx: idx + 7] == "C+57.02":
                    # temp.replace("C+57.02", "C")
                    modifi_series[i] += str(idx-mod_cnt*6 + 1)
                    modifi_series[i] += str(';')
                    mod_type[i] += "Carbamidomethyl@C;"
                    mod_cnt += 1
                    # break

            modifi_series[i] = modifi_series[i][:-1]
            mod_type[i] = mod_type[i][:-1]
            temp = temp.replace("C+57.02", "C")
            temp = temp.replace("M+15.99", "M")
    
        new_series.append(temp)
            
                
        cnt += 1
        # new_sequence = sequence.replace("M+15.99", "1")
        # new_sequence = new_sequence.replace("C+57.02", "C")
        # new_series.append(new_sequence)
        # if cnt == 53:
        #     break
        # cnt += 1
    # df["Peptide"][:54] = new_series
    # df.to_csv(out_file_name, sep= "\t")
    with open("./alphapep/sequence.pin", "w") as f:
        f.write("sequence,mods,mod_sites,charge")
        f.write("\n")
        for seq, modi, typemod, charge in zip(new_series, modifi_series,mod_type,df["charge"]):
            f.write(f"{seq},{typemod},{modi},{charge}\n")
    # sequence_series = pd.Series(new_series)
    # print(sequence_series)
    # sequence_series.to_csv("sequence_list.pin")
    return out_file_name

# preprocess_mod_alphapep("./finale_deltaRT_5head/finale_deltaRT_5head.tsv")
# exit()

def feature_selection(file_name, exclusion, out_file_name = "feature_input"): #feature exclusion
    # file = open(file_name, "r")
    df = pd.read_csv(file_name, delimiter='\t')
    # print(df.shape)
    # print(df.columns[exclusion[1]])
    # for column in exclusion:
    #     df.drop([df.columns[column]], axis=1)
    column_list = []
    for a in exclusion:
        column_list.append(df.columns[a])
    # print(column_list)
    df = df.drop(column_list, axis=1)
    # print(df.shape)
    df.to_csv(out_file_name, sep="\t", index=False)
    return out_file_name
# preprocess("test_percolator.pin")
def feature_exclusion():
    df = pd.read_csv("./output/real_real_final.pin", delimiter="\t")
    print(df.columns)
    # df = df.drop(["idx","charge", "rt_file1_experimental","rt_file2_input", "deltaRT"], axis=1)
    df = df.drop(["charge"], axis=1)
    print(df.columns)
    df.to_csv("./output/real.pin", sep="\t", index=False)


# feature_exclusion()
# exit()
# input_file = "test_percolator.pin"
# preprocess_mod(input_file)
# feature_selection(input_file, [3,4])
# output_file = preprocess(input_file)

def get_delta_rt():
    df_rt = pd.read_csv("autoRT/real_rt.tsv", delimiter='\t')
    series = []
    for y, ypred in zip(df_rt["y"], df_rt["y_pred"]):
        series.append(abs(float(ypred) - float(y)))
    with open("./autoRT/delta_RT.tsv", "w") as f:
        f.write("deltaRT\n")
        for ele in series:
            f.write(f"{ele}\n")

# get_delta_rt()
# exit()
# percolator = ''
def add_RT_to_input(file_name, output_file = "./output/real_real_RT.pin"):
    df = pd.read_csv(file_name, delimiter="\t")
    df_rt = pd.read_csv("./autoRT/delta_RT.tsv", delimiter='\t')
    df = df.drop(["charge", "delta_rt_new"], axis=1)
    df.insert(7, "delta_rt", df_rt["deltaRT"])
    # df.insert(19, "sequence", df_rt["x"])
    df.to_csv(output_file, sep='\t', index=False)
    return output_file

# add_RT_to_input("./output/real_real_final.pin")
# exit()
def add_charge_to_input(file_name = "RT_added.pin", output_file = "RT_charge_added.pin"):
    df = pd.read_csv(file_name, delimiter="\t")
    df_rt = pd.read_csv("experimental_charge.pin", names=["charge", "title"])

    # df.insert(7, "charge", df_rt["charge"])
    df.insert(7, "charge")
    # df.insert(19, "sequence", df_rt["x"])
    df.to_csv(output_file, sep='\t', index=False)
    return output_file

# add_charge_to_input()
# exit()



def find_charge_with_ScanNum(msf_file):
    # temp = []
    title_idx = 0
    msf = open(msf_file, 'r')
    msfs = msf.readlines()
    charge_list = []
    scan_num_list = []
    for idx in range(len(msfs)):
        m = re.match(f'.*\.[0-9]*\.[0-9]*.*', msfs[idx]) #정규표현식을 이용해서 scanNum 찾음.
        
        if m:
            title_idx = idx
            charge_list.append(msfs[title_idx+3][7:8].strip())
            scan_num = msfs[title_idx].replace(".","_")[6:].strip()
            scan_num = re.findall(f".*_.*_.*_.*_.*_.*_.*_", scan_num)
            # print(scan_num[0])
            # exit()
            scan_num_list.append(scan_num[0])
            
    
    # for idx in range(title_idx+4,len(msfs)):
    #     if msfs[idx] == 'END IONS\n':
    #         break
    #     temp.append(msfs[idx].strip())
    
    msf.close()
    with open("experimental_charge.pin", "w") as f:
        for charge,scan_num in zip(charge_list, scan_num_list):
            f.write(f"{charge},{scan_num}\n")

    return

# find_charge_with_ScanNum("./20100614_Velos1_TaGe_SA_K562_123456.mgf")
# exit()
import matplotlib.pyplot as plt
import seaborn as sns
def draw_distribution(inputfile):
    df = pd.read_csv(inputfile, delimiter="\t")
    # target_rt = df[df["Label"]==1]
    # decoy_rt = df[df["Label"]==-1]
    df = df.loc[df.groupby(["SpecId"])['Xcorr'].idxmax()]
    # target_rt = df["y_pred"] - df["y"]
    target_rt = df[df["Label"]==1]
    decoy_rt = df[df["Label"]==-1]
    # df.loc[df.groupby(["sp", "mt"])["count"].idxmax()]
    # target_rt = target_rt.loc[target_rt.groupby(["SpecId"])['Xcorr'].idxmax()]
    # decoy_rt = decoy_rt.groupby(["SpecId"])['Xcorr'].max()
    # decoy_rt = decoy_rt.loc[decoy_rt.groupby(["SpecId"])['Xcorr'].idxmax()]
    # print(target_rt[:5])
    # exit()
    # decoy_rt = decoy_rt.groupby(["SpecId"])
    print(len(target_rt))
    print(target_rt[:5])
    # print(len(decoy_rt))
    # plt.hist(target_rt, color="black", bins = 100)
    plt.hist([decoy_rt["delta_rt"],target_rt["delta_rt"]], color=['lightgreen', 'red'], ec='black', bins=30)
    plt.xlabel('delta RT')
    plt.ylabel('intensity')
    plt.legend()
    plt.show()
    # sns.displot(target_rt['deltaRT'])


# draw_distribution("./output/real_real_RT.pin")
# exit()
# draw_distribution("./deltaRT_5head/deltaRT_5head.pin")
# draw_distribution("./output/final_preprocessed.pin")
# # draw_distribution("./prosit/output/SA_added.pin")
# exit()


# exit()
def read_myscv(input_file):
    # file = open(input_file, 'r')
    df = pd.read_csv(input_file)

    # print(f"duplicted len(df) = {len(df)}")
    # df = df.drop_duplicates(subset='LabeledPeptide')
    # df = df[:10000]
    df.drop_duplicates(subset=["ModifiedPeptide"])
    # print(f"duplicted len(df) = {len(df)}")
    df.to_csv("./prosit/myPrositLib_final_sliced.csv", index= False)

    # contents = file.readlines()
    # for i,line in enumerate(contents):
    #     if i == 100:
    #         break
    #     print(line)
# with open("./alphapept/predict.speclib.hdf", "rb") as f:
#     lines = f.readlines()
#     for i, c in enumerate(lines):
#         if i ==1000:
#             break
#         print(c)

# read_myscv("./prosit/myPrositLib_drop_dup_final.csv")
# exit()

def match_protein_name_prosit_input(inputfile):
    df = pd.read_csv("./reranked/reranked_finale1.pin", delimiter="\t")
    df_prosit = pd.read_csv("./prosit/myPrositLib_sliced.csv")
    df_prosit.drop_duplicates(subset=['RelativeIntensity', 'LabeledPeptide'])
    df_prosit.to_csv("./prosit/duplicated.csv", index=False, sep="\t")
    i = 2
    
    # exit()
    for i, ele in enumerate(df):
        for j, ms in enumerate(df_prosit):
            pass
    i = 0 #
    j = 0 #3
    new_series = []
    for seq, id in zip(df["Peptide"], df["SpecId"]):
        pass
    # while(i < len(df)):
# match_protein_name_prosit_input(1)
# exit()
import numpy as np
import warnings

# def get_SA_score(mgf_file, prosit_file):


warnings.filterwarnings(action='ignore') 
#slice rank by rank5 -> get half dataset
def rerank(inputfile):
    df = pd.read_csv(inputfile, delimiter="\t")
    # df = df[:4000]
    df.to_csv("big_size/reranked/test1.pin", sep="\t", index_label='idx')
    df = pd.read_csv("big_size/reranked/test1.pin", delimiter="\t")
    # print(df["idx"])
    # exit()
    asd = df.groupby("SpecId")
    new_df = np.array([])
    temp = []
    # print(asd.shape)
    # new_df = pd.DataFrame(new_df)
    # df.to_csv("reranked/test.pin" sep="\t")
    cnt = 0
    for i,ele in enumerate(asd):
        # print(ele)
        
        ele = np.array(ele)
        ele[1] = ele[1][:5]
        # print(len(ele[1]))
        # print(ele[1])
        # exit()
        if i == 0:
            temp = ele[1]
            continue
        elif i % 10000 == 0:
            column = ["idx", "SpecId",	"rt_file1_experimental","Label","deltaRT","charge","ScanNr","ExpMass","dM","absdM","dMppm","rt_file2_input","absdMppm","FracBMatchInt","FracYMatchInt","SeqCoverBion","SeqCoverYion","ConsecutiveBion","ConsecutiveYion","Xcorr","PepLen","enzInt","NumofAnnoPeaks","Peptide","Proteins"]
            temp = pd.DataFrame(temp, columns=column)
            temp = temp.sort_values(by="idx")
            temp.to_csv(f"reranked/reranked{i}.pin",index=False, sep="\t")
            temp = ele[1]
            continue
        # ele = np.array(ele)
        # print(ele)
        # exit()
        # temp += ele[1]
        temp = np.append(temp, ele[1] ,axis=0)
        # print(f"ele.shape = {ele.shape}, temp = {temp.shape}")
        # ele = pd.DataFrame(ele[1])
        # print(ele)
        # print(type(ele))
        # new_df.append(ele.nlargest(5,"Xcorr",keep="first"))
        # temp = np.append(new_df, ele ,axis = 0)
        # print(new_df.shape)
        if cnt % 1000 ==0:
            # print(temp)
            print(f"cnt = {cnt} temp = {len(temp)}")

        cnt += 1

    # print(temp)
    # df = pd.DataFrame(temp)
    # print(df.shape)
    # df.to_csv("./reranked/ouput1.pin")
    # out_file = open("./reranked/output.pin", "w")
    # for a in temp:
    #     for b in a:
    #         out_file.write(b)
    # out_file.close()
    # exit()
    column = ["idx", "SpecId",	"rt_file1_experimental","Label","deltaRT","charge","ScanNr","ExpMass","dM","absdM","dMppm","rt_file2_input","absdMppm","FracBMatchInt","FracYMatchInt","SeqCoverBion","SeqCoverYion","ConsecutiveBion","ConsecutiveYion","Xcorr","PepLen","enzInt","NumofAnnoPeaks","Peptide","Proteins"]
    temp = pd.DataFrame(temp, columns=column)
    temp = temp.sort_values(by="idx")
    temp.to_csv("big_size/reranked/reranked.pin",index=False, sep="\t")
    # with open("reranked/reranked.pin", "w") as f:
        
    # print(new_df)
    # for a in temp:
    #     print(a.shape)
    # print(new_df[0].shape)
    # df = df.loc[df.groupby(["SpecId"])["Xcorr"].idxmax()]
    # print(pd.DataFrame(df.groupby("SpecId")))
    exit()
    print(df_spec.shape)
    df_new = []
    for df in df_spec:
        df_new.append(df.nlargest(5,'Xcorr',keep='first'))
    # .nlargest(5, 'Xcorr', keep='first')
    print(df_new[:100])
    print(df.shape)


# rerank("./finale_deltaRT_5head/finale_deltaRT_5head.tsv")
# exit()
def merge_ranked_input():
    file = "./test/reranked10000.pin"
    df = pd.read_csv(file, delimiter="\t")
    print(df.shape)
    # exit()
    # df = pd.concat(df,df)
    for a in range(2,17):
        file = f"./test/reranked{a*10000}.pin"
        df_a = pd.read_csv(file, delimiter="\t")
        print(df_a.shape)
        # exit()
        df = pd.concat([df,df_a])
    df_a = pd.read_csv("./test/reranked_final.pin", delimiter="\t")

    df = pd.concat([df,df_a])
    df = df.sort_values(by="idx")
    print(df.shape)
    df.to_csv("reranked/reranked_finale1.pin", sep="\t", index=False)

# merge_ranked_input()
# exit()

#input file = prosit result with ms2 spec


def find_msf_with_ScanNum(msf_file):
    # temp = []
    title_idx = 0
    msf = open(msf_file, 'r')
    msfs = msf.readlines()
    rt_list = []
    scan_num_list = []
    for idx in range(len(msfs)):
        m = re.match(f'.*\.[0-9]*\.[0-9]*.*', msfs[idx]) #정규표현식을 이용해서 scanNum 찾음.
        
        if m:
            title_idx = idx
            rt_list.append(msfs[title_idx+1][12:].strip())
            scan_num = msfs[title_idx].replace(".","_")[6:].strip()
            scan_num = re.findall(f".*_.*_.*_.*_.*_.*_.*_", scan_num)
            # print(scan_num[0])
            # exit()
            scan_num_list.append(scan_num[0])
            
    
    # for idx in range(title_idx+4,len(msfs)):
    #     if msfs[idx] == 'END IONS\n':
    #         break
    #     temp.append(msfs[idx].strip())
    
    msf.close()
    with open("experimental_rt.pin2", "w") as f:
        for rt,scan_num in zip(rt_list, scan_num_list):
            f.write(f"{rt},{scan_num}\n")

    return

# find_msf_with_ScanNum("./20100614_Velos1_TaGe_SA_K562_123456.mgf")
# exit()


def get_SA(ori_mgf, prediced_ms2_file):
    pass


def get_delta_rt(input_file):
    df_rt = pd.read_csv("experimental_rt.pin", names=['rt', 'title'])
    df_input = pd.read_csv(input_file, delimiter="\t")
    # df_input.insert(7,"deltaRT", 0)
    cnt = 0
    delta_rt_list = []
    for i, input_title in enumerate(df_input["SpecId"]):
        if cnt == 100:
            
            break
        for j,rt_title in enumerate(df_rt["title"]):
            if re.match(f"{rt_title}.*", input_title):
                delta_rt_list.append(abs(df_input.loc[i]["rt"] - df_rt.loc[j]['rt']))
                # df_input.loc[i]["deltaRT"] = abs(df_input.loc[i]["rt"] - df_rt.loc[j]['rt'])
        cnt +=1          
    delta_rt = pd.DataFrame(delta_rt_list, columns=["deltaRT"])
    df_input.insert(7,"deltaRT", delta_rt["deltaRT"])
    print(df_input.head())
    df_input.to_csv("rt_5head.pin ", sep="\t")
    # cnt += 1
    
# get_delta_rt("rt_added.pin")
# exit()

def preprocess_for_prosit(file_name, out_file_name = "./prosit/input_for_prosit1.pin"):

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
        
        f.write("modified_sequence,collision_energy,precursor_charge,fragmentation")

        f.write("\n")
        
        for seq, charge, id in zip(new_series, df["charge"], df["SpecId"]):
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

# preprocess_for_prosit("reranked/reranked_finale1.pin")
# exit()
import subprocess

def get_input_file_for_auto_rt(input_file = "experimental_rt.pin"):
    df = pd.read_csv(input_file, names = ["rt", "title"])


def FDR(inputfile, threshhold, output_file = "FDR_file.pin"):
    
    df = pd.read_csv(inputfile, delimiter="\t")
    df.drop(df[(df['q-value'] < 0.01)], inplace=True)
    df.to_csv(output_file, sep="\t")

def get_FDR():
    df = pd.read_csv("./prosit/output/SAfilled_RT_added.pin", delimiter="\t")
    df = df.loc[df.groupby(["SpecId"])['Xcorr'].idxmax()]
    df = df.sort_values(by="Xcorr", ascending=False)
    # idx = 0
    fitted_idx = 0
    target = 0
    decoy = 0
    for idx, label in enumerate(df["Label"]):
        if label == 1:
            target += 1
        else:
            decoy += 1

        if decoy == 0:
            fitted_idx = idx
        if decoy/target <= 0.01:
            fitted_idx = idx
    df.to_csv("sorted_with_rank1.pin", index=False, sep="\t")

    return fitted_idx

print(get_FDR())
exit()

def call_percolator(call):
    try:
        output = subprocess.check_output(call, universal_newlines=True)
        
        with open('new_output.psm','w') as file:
            file.write(output)

        print("Rescoring Successfull! File saved as \'new_output.psm\'")
        return output
    
    except subprocess.CalledProcessError as e:
        print("RESCORING FAILED!: ", e)
    
ori_file_name = "test_percolator.pin"
file_name = add_RT_to_input(ori_file_name, "rt_added.pin")
# exit()
#feature 1~15 까지 하나씩 뻬봄.
max_psms = 0
# with open("comet1.psms", "r") as f:
#     lenth = f.readlines()
#     print(len(lenth))
# for i in range(3,18):
#     file_name = feature_selection(ori_file_name, [i])
#     file_name = preprocess(file_name)
#     command = ['percolator', file_name, ">", f"output_feature_{i}_excluded.psms" ]
#     out_put = call_percolator(command)
#     if max_psms < len(out_put):
#         max_psms = len(out_put)
#         with open(f"output_feature_{i}_excluded.psms", "w") as f:
#             f.write(out_put)
result = []
# file_name = feature_selection(file_name, [4,5,6,7])
preprocess(file_name, "rt_added2.pin")

# print(file_name)
# command = ['percolator', file_name]
# out_put = call_percolator(command)
# result.append((len(out_put), 3))
# for a in result:
#     print(len(a))

# with open(f"output_a{2}", "w") as f:
#         f.write(out_put)


# print(result)
# if max_psms < len(out_put):
#     max_psms = len(out_put)
#     with open(f"output_feature_{5}_excluded.psms", "w") as f:
#         f.write(out_put)