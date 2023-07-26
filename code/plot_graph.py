import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.patches import Rectangle
def draw_distribution(inputfile):
    cmap = plt.get_cmap('jet')
    low = cmap(0.5)
    medium =cmap(0.25)
    high = cmap(0.8)
    df = pd.read_csv(inputfile, delimiter="\t")
    # target_rt = df[df["Label"]==1]
    # decoy_rt = df[df["Label"]==-1]
    # df = df.loc[df.groupby(["SpecId"])['Xcorr'].idxmax()]
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
    plt.hist([target_rt["SA"],decoy_rt["SA"]], color=[low, medium], ec='black', bins=30)
    plt.xlabel('SA')
    plt.ylabel('intensity')
    handles = [Rectangle((0,0),1,1,color=c,ec="k") for c in [low,medium]]
    labels= ["Target","Decoy"]
    plt.legend(handles, labels)
    # plt.legend()
    plt.show()
    # sns.displot(target_rt['deltaRT'])


draw_distribution("./SA_deltaRT_added.pin")
exit()