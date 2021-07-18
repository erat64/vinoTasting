import pandas as pd

# Read the CSV into a pandas data frame (df)
#   With a df you can do many things
#   most important: visualize data with Seaborn
df = pd.read_csv('SliderAnswers.csv', sep=',')
guests=["Mum","Geo","Alf","Gab","Vee","Abe","All","Dav","Dyl","Sop"]
for i in range(len(guests)):
        df[guests[i]]=df[guests[i]]-df["Edm"]
        df[guests[i]]=abs(df[guests[i]])
df.to_csv(r'C:\Users\edmun\Documents\Programs\Python\Edmund\vinooootasting\vinoTasting\Sven CSV reader\SliderAnswers.csv', index = False)
