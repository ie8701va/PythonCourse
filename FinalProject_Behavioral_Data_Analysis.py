# -*- coding: utf-8 -*-
"""
Created on Mon May  1 14:46:09 2023

@author: Ieva

THE FOLLOWING SCRIPT COMPLETES DATA WRANGLING PROCEDURES, VISUALISES SEPARATE DATASETS OF INTEREST, 
RUNS SOME MIXED EFFECTS MODELS AND COMPLETES OTHER INFERENTIAL STATISTICS ANALYSES.

"""


#%% IMPORTING LIBRARIES AND FUNCTIONS
# Importing the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # change the import statement here
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm
import seaborn as sns
from scipy.stats import chi2_contingency

sns.set_palette("Set2") # Set the color palette

# Function for extracting retrieval data in future datasets. I could save this in a separate file in the future. 
def extract_retrieval(raw_data):
    retrieval_data = raw_data.loc[(raw_data['ProcedureSubtrial'] == 'TestACProc') | (raw_data['ProcedureSubtrial'] == 'DATestProc')]
    retrieval_data = retrieval_data.reset_index(drop=True)
    return retrieval_data

#%% RAW DATA MANAGEMENT
raw_data = pd.read_excel(r'C:\Users\Leva\Documents\NewComputer\MasterProgramme\Thesis\Data\RawData.xlsx')
raw_data.info()




# Creating new empty columns which I will need later
raw_data["ConditionsFinal"] = " "
raw_data["IndoorOutdoor"] = " "
raw_data["Congruency"] = " "
raw_data["AssociationType"] = " "
raw_data["DetailedMem"] = " " # Empty new column for detailed memory. 
raw_data["NoMemory"] = " " # Empty new column for no memory. 
raw_data["CoarseMem"] = " " # Empty new column for coarse memory. 
raw_data["Accuracy_Associations"] = ''
raw_data["RT_Associations"] = ''



# Renaming the column to more appropriate names to be able to pull certain values from it and python would not mix .(dot) with a command. 
raw_data.columns = raw_data.columns.str.replace('.', '_') # The new way I found to rename columns with one line of code.
raw_data = raw_data.rename(columns={raw_data.columns[2]: 'ProcedureSubtrial'})




# Creating Retrieval Conditions column with values based on other columns

raw_data.loc[raw_data['Trigger_Inf'] == 141, 'ConditionsFinal'] = 'AC_Cong'
raw_data.loc[raw_data['Trigger_Inf'] == 142, 'ConditionsFinal'] = 'AC_Incong'

raw_data.loc[(raw_data['Trigger_DA'] == 131) & ((raw_data['Condition'] == 'ABC_Incong_Out') | (raw_data['Condition'] == 'ABC_Incong_In')), 'ConditionsFinal'] = 'AB_Incong'
raw_data.loc[(raw_data['Trigger_DA'] == 131) & ((raw_data['Condition'] == 'ABC_Cong_Out') | (raw_data['Condition'] == 'ABC_Cong_In')), 'ConditionsFinal'] = 'AB_Cong'
raw_data.loc[(raw_data['Trigger_DA'] == 132) & ((raw_data['Condition'] == 'ABC_Incong_Out') | (raw_data['Condition'] == 'ABC_Incong_In')), 'ConditionsFinal'] = 'BC_Incong'
raw_data.loc[(raw_data['Trigger_DA'] == 132) & ((raw_data['Condition'] == 'ABC_Cong_Out') | (raw_data['Condition'] == 'ABC_Cong_In')), 'ConditionsFinal'] = 'BC_Cong'
raw_data.loc[(raw_data['Trigger_DA'] == 133) & ((raw_data['Condition'] == 'XY_Incong_Out') | (raw_data['Condition'] == 'XY_Incong_In')), 'ConditionsFinal'] = 'XY_Incong'
raw_data.loc[(raw_data['Trigger_DA'] == 133) & ((raw_data['Condition'] == 'XY_Cong_Out') | (raw_data['Condition'] == 'XY_Cong_In')), 'ConditionsFinal'] = 'XY_Cong'




# Creating Indoor/Outdoor column with values based on other column
raw_data.loc[raw_data['Condition'].str.contains('_In'), 'IndoorOutdoor'] = 'Indoor'
raw_data.loc[raw_data['Condition'].str.contains('_Out'), 'IndoorOutdoor'] = 'Outdoor'



# Creating Congruency column with values based on other column
raw_data.loc[raw_data['ConditionsFinal'].str.contains('_Cong'), 'Congruency'] = 'Cong'
raw_data.loc[raw_data['ConditionsFinal'].str.contains('_Incong'), 'Congruency'] = 'Incong'



# Creating Association Type column with values based on other column
raw_data.loc[raw_data['ConditionsFinal'].str.contains('AB'), 'AssociationType'] = 'AB'
raw_data.loc[raw_data['ConditionsFinal'].str.contains('AC'), 'AssociationType'] = 'AC'
raw_data.loc[raw_data['ConditionsFinal'].str.contains('BC'), 'AssociationType'] = 'BC'
raw_data.loc[raw_data['ConditionsFinal'].str.contains('XY'), 'AssociationType'] = 'XY'



# FIXING STUDY DESIGN MISTAKES: Originally, in column TestDAProbe_ACC, the data was coded the opposite. 
# Where 1 is meant to be 0 and where 0 is meant ot be 1. Hence correcting this column.
# Same goes for column TestDAProve_Resp, where 1s should be 2s and 2s should be 1s. 3s remain the same. 
raw_data['TestDAProbe_ACC'] = raw_data['TestDAProbe_ACC'].replace({1: 0, 0: 1})
raw_data['TestDAProbe_RESP'] =  raw_data['TestDAProbe_RESP'].replace({1: 2, 2: 1})



# Exctacting what kind of memory people have based on asnwers in Context and Schema_ACC columns. 
raw_data['DetailedMem'] = np.where(raw_data['TestContext_ACC'] == 1, 1, np.where(raw_data['TestContext_ACC'] == 0, 0, raw_data['DetailedMem']))
raw_data['NoMemory'] = np.where(raw_data['TestSchema_ACC'] == 1, 0, np.where(raw_data['TestSchema_ACC'] == 0, 1, raw_data['NoMemory']))
raw_data['CoarseMem'] = np.where(raw_data['TestSchema_ACC'] == 1, 1, np.where(raw_data['TestSchema_ACC'] == 0, 0, raw_data['CoarseMem']))



# Creating another data frame that has only retrieval (and not encoding) data in it. 
# Using the custom function for that
retrieval_data = extract_retrieval(raw_data)

#%% RETRIEVAL DATA MANAGEMENT

# Code don't know's (answer 3) as 999. (In TestContext_RESP don't knows were #5) 
retrieval_data['TestAC_ACC'] = [999 if retrieval_data.iloc[i]['TestAC_RESP'] == 3 else retrieval_data.iloc[i]['TestAC_ACC'] for i in range(len(retrieval_data))]
retrieval_data['TestDAProbe_ACC'] = [999 if retrieval_data.iloc[i]['TestDAProbe_RESP'] == 3 else retrieval_data.iloc[i]['TestDAProbe_ACC'] for i in range(len(retrieval_data))]
retrieval_data['TestSchema_ACC'] = [999 if retrieval_data.iloc[i]['TestSchema_RESP'] == 3 else retrieval_data.iloc[i]['TestSchema_ACC'] for i in range(len(retrieval_data))]
retrieval_data['TestContext_ACC'] = [999 if retrieval_data.iloc[i]['TestContext_RESP'] == 5 else retrieval_data.iloc[i]['TestContext_ACC'] for i in range(len(retrieval_data))]


 
# Code - 0 response times as 999 in _ACC columns as well. 
retrieval_data['TestAC_ACC'] = [999 if retrieval_data.iloc[i]['TestAC_RT'] == 0 else retrieval_data.iloc[i]['TestAC_ACC'] for i in range(len(retrieval_data))]
retrieval_data['TestDAProbe_ACC'] = [999 if retrieval_data.iloc[i]['TestDAProbe_RT'] == 0 else retrieval_data.iloc[i]['TestDAProbe_ACC'] for i in range(len(retrieval_data))]
retrieval_data['TestSchema_ACC'] = [999 if retrieval_data.iloc[i]['TestSchema_RT'] == 0 else retrieval_data.iloc[i]['TestSchema_ACC'] for i in range(len(retrieval_data))]
retrieval_data['TestContext_ACC'] = [999 if retrieval_data.iloc[i]['TestContext_RT'] == 0 else retrieval_data.iloc[i]['TestContext_ACC'] for i in range(len(retrieval_data))]



# Code - 0 RTs as 999999 their own column, as that migth affect further calculations.
retrieval_data['TestAC_RT'] = retrieval_data['TestAC_RT'].replace(0, 999999) 
retrieval_data['TestDAProbe_RT'] = retrieval_data['TestDAProbe_RT'].replace(0, 999999)
retrieval_data['TestSchema_RT'] = retrieval_data['TestSchema_RT'].replace(0, 999999)
retrieval_data['TestContext_RT'] = retrieval_data['TestContext_RT'].replace(0, 999999)



# Concatenating some columns    
retrieval_data['Accuracy_Associations'] = retrieval_data['TestAC_ACC'].combine_first(retrieval_data['TestDAProbe_ACC'])
retrieval_data['RT_Associations'] = retrieval_data['TestAC_RT'].combine_first(retrieval_data['TestDAProbe_RT'])


#%% CREATING SMALLER DATASETS

# Selecting specific columns and create smaller datasets for specific calculations. 
associations_data = retrieval_data.loc[:, ['Subject', 'ConditionsFinal','AssociationType','Congruency','Accuracy_Associations', 'RT_Associations']]
memory_spec_data = retrieval_data.loc[retrieval_data['ProcedureSubtrial'] == 'TestACProc', ['Subject', 'ConditionsFinal','AssociationType','Congruency','CoarseMem', 'DetailedMem', 'NoMemory']]
coarse_mem_data = retrieval_data.loc[retrieval_data['ProcedureSubtrial'] == 'TestACProc', ['Subject', 'ConditionsFinal','AssociationType','Congruency','IndoorOutdoor', 'CoarseMem']]
detailed_mem_data = retrieval_data.loc[retrieval_data['ProcedureSubtrial'] == 'TestACProc', ['Subject', 'ConditionsFinal','AssociationType','Congruency','IndoorOutdoor', 'DetailedMem']]




# Answer 3 (in column TestContext_Resp it was a 5) in our study was a 'don't know' option. We will not be including those values into our analyses.
# Thus, I want to create a separate dataframe with all the excluded data with don't knows.
excluded_associations_dontknow_data = retrieval_data.loc[(retrieval_data['TestAC_RESP'] == 3) | (retrieval_data['TestDAProbe_RESP'] == 3), ['Subject', 'ConditionsFinal','AssociationType','Congruency', 'TestAC_RESP','TestDAProbe_RESP']]
excluded_coarsemem_dontknow_data = retrieval_data.loc[(retrieval_data['TestSchema_RESP'] == 3), ['Subject', 'ConditionsFinal','AssociationType','Congruency', 'TestSchema_RESP']]
excluded_detailedmem_dontknow_data = retrieval_data.loc[(retrieval_data['TestContext_RESP'] == 5), ['Subject', 'ConditionsFinal','AssociationType','Congruency', 'TestContext_RESP']]




# Sometimes people ran out of time to answer therefore their RTs were 0s. I had previously changed them to 999999. We will not be including those values into our analyses.
# Thus, I want to create a separate dataframe with all the excluded data points for where people ran out of time.
excluded_associations_noanswer_data = retrieval_data.loc[(retrieval_data['TestAC_RT'] == 999999) | (retrieval_data['TestDAProbe_RT'] == 999999), ['Subject', 'ConditionsFinal','AssociationType','Congruency', 'TestAC_RT','TestDAProbe_RT']]
excluded_coarse_noanswer_data = retrieval_data.loc[(retrieval_data['TestSchema_RT'] == 999999), ['Subject', 'ConditionsFinal','AssociationType','Congruency', 'TestSchema_RT']]
excluded_detailedmem_noanswer_data = retrieval_data.loc[(retrieval_data['TestContext_RT'] == 999999), ['Subject', 'ConditionsFinal','AssociationType','Congruency', 'TestContext_RT']]


#%% ASSOCIATION_DATA ACCURACY
associations_data['Accuracy_Associations'] = pd.to_numeric(associations_data['Accuracy_Associations'], errors='coerce').astype('Int64')
associations_data['RT_Associations'] = pd.to_numeric(associations_data['RT_Associations'], errors='coerce').astype('Int64')
print(associations_data)



# Deleting rows that were don't knows and where RTs were 0. We are not including them in the analysis.
associations_data = associations_data.loc[associations_data['Accuracy_Associations'] != 999]
associations_data = associations_data.loc[associations_data['RT_Associations'] != 999999]




# Creating a table with which displays the percentage of correct trials out of all attempted per condition. 
sums_associations_acc = pd.pivot_table(associations_data, values='Accuracy_Associations', index='Subject', columns='ConditionsFinal', aggfunc=np.sum)
counts_assocations_acc = pd.pivot_table(associations_data, values='Accuracy_Associations', index='Subject', columns='ConditionsFinal', aggfunc='count')
associations_percentage_table = (sums_associations_acc / counts_assocations_acc) * 100
print(associations_percentage_table)



# Plotting to see the general trend
associations_percentage_table.mean().plot(kind='bar')



# Reshaping the dataframe from wide to long format for the repeated measures ANOVA
associations_percentage_table = associations_percentage_table.reset_index()
associations_percentage_table_long = pd.melt(associations_percentage_table, id_vars=['Subject'], value_vars=['AB_Cong', 'AB_Incong', 'AC_Cong', 'AC_Incong', 'BC_Cong', 'BC_Incong', 'XY_Cong', 'XY_Incong'])
associations_percentage_table_long.info()


from matplotlib import rcParams
# Set the font to Times New Roman and font size to 12
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 14

# Boxplot to see data distributions
custom_palette = ["#2ca02c", "#9467bd"]
plt.figure(figsize=(12, 6))
plt.subplots_adjust(bottom=0.15)
dodge = 0.4
ax = sns.boxplot(x = 'ConditionsFinal', y = 'value', data = associations_percentage_table_long, color = '#99c2a2', width=0.6, palette = custom_palette)
ax = sns.swarmplot(x = 'ConditionsFinal', y = 'value', data = associations_percentage_table_long, color = "#FFA500", size = 3)
ax.set_ylabel('Accuracy (%)')
ax.set_xlabel('')

# Modify the x-axis labels
labels = [str(label.get_text()).replace("_Cong", " Congruent").replace("_Incong", " Incongruent") for label in ax.get_xticklabels()]
ax.set_xticklabels(labels, rotation=45, ha='right')
plt.savefig(r'C:\Users\Leva\Documents\NewComputer\MasterProgramme\Thesis\Data\Figures\Accuracy_All_Association_Types.png', dpi=500)



associations_percentage_table_long['ExpGroup'] = associations_percentage_table_long['ConditionsFinal'].str[:2] # Adding a column for congruency
associations_percentage_table_long['Congruence'] = associations_percentage_table_long['ConditionsFinal'].str[3:] # Removing the first three characters from the column called group. 
associations_percentage_table_long = associations_percentage_table_long.rename(columns={"value": "Accuracy"}) # Renaming that column to accuracy
associations_percentage_table_long.info()



# Converting the Float to numeric format for the ANOVA
associations_percentage_table_long['AccuracyNumeric'] = associations_percentage_table_long['Accuracy'].astype('float')
associations_percentage_table_long.info()




# Boxplot to see whether congruent memories resulted in more accurace answers than incongruent
custom_palette = ["#99c2a2", "red", "#ffa500", "blue", "darkgreen"]
plt.figure(figsize=(12, 6))
plt.subplots_adjust(bottom=0.15)
ax = sns.boxplot(x = 'Congruence', y = 'Accuracy', data = associations_percentage_table_long, palette = custom_palette, width=0.6)
ax = sns.swarmplot(x = 'Congruence', y = 'Accuracy', data = associations_percentage_table_long, color = "#FFA500")
ax.set_xticklabels(ax.get_xticklabels(), rotation = 45, ha = 'right')




# performing a 2x4 repeatesd measures ANOVA
model1 = ols('AccuracyNumeric ~ C(ExpGroup) + C(Congruence) + C(ExpGroup):C(Congruence)', data=associations_percentage_table_long).fit()
sm.stats.anova_lm(model1, typ = 2)

#%% ASSOCIATION_DATA RESPONSE TIME 

# Creating a table with which displays the median RT for all trials in each condition. 
median_associations_RT_table = pd.pivot_table(associations_data, values='RT_Associations', index='Subject', columns='ConditionsFinal', aggfunc=np.median)
print(median_associations_RT_table)




# Plotting to see the general trend
plt.figure(figsize=(10, 6))
median_associations_RT_table.mean().plot(kind='bar')
plt.ylabel('Reaction time (ms)')
plt.xticks(rotation= 45 )  # Adjust the rotation angle as needed



# Reshaping the dataframe from wide to long format for the repeated measures ANOVA
median_associations_RT_table = median_associations_RT_table.reset_index()
median_associations_RT_table_long = pd.melt(median_associations_RT_table, id_vars=['Subject'], value_vars=['AB_Cong', 'AB_Incong', 'AC_Cong', 'AC_Incong', 'BC_Cong', 'BC_Incong', 'XY_Cong', 'XY_Incong'])
median_associations_RT_table_long.info()




# Boxplot to see data distributions
ax1 = sns.boxplot(x = 'ConditionsFinal', y = 'value', data = median_associations_RT_table_long, color = '#99c2a2')
ax1= sns.swarmplot(x = 'ConditionsFinal', y = 'value', data = median_associations_RT_table_long, palette= custom_palette)



median_associations_RT_table_long['ExpGroup'] = median_associations_RT_table_long['ConditionsFinal'].str[:2] # Adding a column for congruency
median_associations_RT_table_long['Congruence'] = median_associations_RT_table_long['ConditionsFinal'].str[3:] # Removing the frist three characters from the column called group. 
median_associations_RT_table_long = median_associations_RT_table_long.rename(columns={"value": "RT"}) # Renaming that column to accuracy



median_associations_RT_table_long.info()
median_associations_RT_table_long['RTNumeric'] = pd.to_numeric(median_associations_RT_table_long['RT'], errors='coerce')
median_associations_RT_table_long['RTNumeric'] = median_associations_RT_table_long['RT'].astype('float')
median_associations_RT_table_long.info()


# performing a 2x4 repeatesd measures ANOVA
model2 = ols('RTNumeric ~ C(ExpGroup) + C(Congruence) + C(ExpGroup):C(Congruence)', data = median_associations_RT_table_long).fit()
sm.stats.anova_lm(model2, typ = 2)


#%% MEMORY SPECIFICITY DATA (COARSE MEMORY)


# Creating a table with which displays the percentage of correct trials out of all attempted in Coarse Memory group. 
sums_detailed_acc = pd.pivot_table(memory_spec_data, values='CoarseMem', index='Subject', columns='ConditionsFinal', aggfunc=np.sum)
counts_coarse_acc = pd.pivot_table(memory_spec_data, values='CoarseMem', index='Subject', columns='ConditionsFinal', aggfunc='count')
coarse_percentage_table = (sums_detailed_acc / counts_coarse_acc) * 100
print(coarse_percentage_table)



# Fixing some column names 
coarse_percentage_table = coarse_percentage_table.rename(columns={"AC_Cong": "CongCoarse", "AC_Incong": "IncongCoarse"}) # Renaming that column to accuracy


# Plotting to see the general trend
coarse_percentage_table.mean().plot(kind = 'bar')



# Reshaping the dataframe from wide to long format for the repeated measures ANOVA
coarse_percentage_table = coarse_percentage_table.reset_index()
coarse_percentage_table_long = pd.melt(coarse_percentage_table, id_vars=['Subject'], value_vars=['CongCoarse', 'IncongCoarse'])
coarse_percentage_table_long.info()




# Boxplot to see data distributions
custom_palette =["#2ca02c", "#9467bd"]
plt.figure(figsize=(12, 6))
plt.subplots_adjust(bottom=0.15)
dodge = 0.4
ax = sns.boxplot(x = 'ConditionsFinal', y = 'value', data = coarse_percentage_table_long, palette = custom_palette, width=0.6)
ax = sns.swarmplot(x = 'ConditionsFinal', y = 'value', data = coarse_percentage_table_long,color = "#FFA500", size = 3)
ax.set_ylabel('Accuracy (%)')
ax.set_xlabel(' ')
# Modify the x-axis labels
labels = [str(label.get_text()).replace("CongCoarse", " Congruent Coarse").replace("IncongCoarse", " Incongruent Coarse") for label in ax.get_xticklabels()]
ax.set_xticklabels(labels, rotation=45, ha='right')






coarse_percentage_table_long.info()
coarse_percentage_table_long = coarse_percentage_table_long.rename(columns={"value": "Accuracy"}) # Renaming that column to accuracy
coarse_percentage_table_long.info()




# Converting the Float to numeric format and ConditionsFinal for a category for the mixed effects model
coarse_percentage_table_long['AccuracyNumeric'] = coarse_percentage_table_long['Accuracy'].astype('float')
coarse_percentage_table_long['ConditionsFinal'] = coarse_percentage_table_long['ConditionsFinal'].astype('category')
coarse_percentage_table_long.info()



# A mixed effects model for Coarse memory group where subject is a random intercept
model3 = smf.mixedlm("AccuracyNumeric ~ ConditionsFinal", coarse_percentage_table_long, groups=coarse_percentage_table_long['Subject'])
result1 = model3.fit()

# Print model summary
print(result1.summary())




# Random slope plot
random_slopes1 = result1.random_effects # Extract random slopes
fig, ax = plt.subplots(figsize=(12, 8)) # Create a single figure and axes
color_palette = sns.color_palette("Set2", len(random_slopes1)) # Define the pallette to be used


# Plot each subject's data on the same axes
for i, (subject, slope) in enumerate(random_slopes1.items()):
    subject_data = coarse_percentage_table_long.loc[coarse_percentage_table_long['Subject'] == subject]
    sns.pointplot(x='ConditionsFinal', y='AccuracyNumeric', data=subject_data, ax=ax, color=color_palette[i])
    
ax.set_xlabel('Coarse memory group' ) # Add labels 
ax.set_ylabel('Accuracy (%)') # Add labels
ax.set_title('Random slope model per subject for coarse memory group') # Add title
ax.set_xticklabels(['Congruent', 'Incongruent']) # Change x-tick labels


#%% MEMORY SPECIFICITY DATA (DETAILED MEMORY)


# Narrowing down the DF
detailed_mem_data = memory_spec_data.loc[:, ['Subject', 'ConditionsFinal','Congruency','DetailedMem']]
detailed_mem_data['DetailedMem'] = pd.to_numeric(detailed_mem_data['DetailedMem'])
detailed_mem_data.info()
detailed_mem_data = detailed_mem_data.dropna(subset=['DetailedMem'])





# Creating a table with which displays the percentage of correct trials out of all attempted in Coarse Memory group. 
sums_detailed_acc = pd.pivot_table(detailed_mem_data, values='DetailedMem', index='Subject', columns='ConditionsFinal', aggfunc=np.sum)
counts_detailed_acc = pd.pivot_table(detailed_mem_data, values='DetailedMem', index='Subject', columns='ConditionsFinal', aggfunc='count')
detailed_percentage_table = (sums_detailed_acc / counts_detailed_acc) * 100
print(detailed_percentage_table)



# Fixing some column names 
detailed_percentage_table = detailed_percentage_table.rename(columns={"AC_Cong": "CongDetailed", "AC_Incong": "IncongDetailed"}) # Renaming that column to accuracy







# Reshaping the dataframe from wide to long format for the repeated measures ANOVA
detailed_percentage_table = detailed_percentage_table.reset_index()
detailed_percentage_table_long = pd.melt(detailed_percentage_table, id_vars=['Subject'], value_vars=['CongDetailed', 'IncongDetailed'])
detailed_percentage_table_long.info()





# Boxplot to see data distributions
ax = sns.boxplot(x = 'ConditionsFinal', y = 'value', data = detailed_percentage_table_long, color = '#99c2a2')
ax = sns.swarmplot(x = 'ConditionsFinal', y = 'value', data = detailed_percentage_table_long, color = '#7d0013')


# Boxplot to see data distributions
custom_palette =["#2ca02c", "#9467bd"]
plt.figure(figsize=(12, 6))
plt.subplots_adjust(bottom=0.15)
dodge = 0.4
ax = sns.boxplot(x = 'ConditionsFinal', y = 'value', data = detailed_percentage_table_long, palette = custom_palette, width=0.6)
ax = sns.swarmplot(x = 'ConditionsFinal', y = 'value', data = detailed_percentage_table_long,color = "#FFA500", size = 3)
ax.set_ylabel('Accuracy (%)')
ax.set_xlabel(' ')
# Modify the x-axis labels
labels = [str(label.get_text()).replace("CongDetailed", " Congruent Detailed").replace("IncongDetailed", " Incongruent Detailed") for label in ax.get_xticklabels()]
ax.set_xticklabels(labels, rotation=45, ha='right')







detailed_percentage_table_long.info()
detailed_percentage_table_long = detailed_percentage_table_long.rename(columns={"value": "Accuracy"}) # Renaming that column to accuracy




# Converting the Float to numeric format and ConditionsFinal for a catefory for the mixed effects model
detailed_percentage_table_long['AccuracyNumeric'] = detailed_percentage_table_long['Accuracy'].astype('float')
detailed_percentage_table_long['ConditionsFinal'] = detailed_percentage_table_long['ConditionsFinal'].astype('category')
detailed_percentage_table_long.info()




# Convert 'ConditionsFinal' to a numerical format
detailed_percentage_table_long['ConditionsNumeric'] = pd.Categorical(detailed_percentage_table_long['ConditionsFinal'])
detailed_percentage_table_long['ConditionsNumeric'] = detailed_percentage_table_long['ConditionsFinal'].cat.codes



# Convert columns to appropriate types
detailed_percentage_table_long['AccuracyNumeric'] = detailed_percentage_table_long['Accuracy'].astype('float')
detailed_percentage_table_long['ConditionsNumeric'] = detailed_percentage_table_long['ConditionsNumeric'].astype('category')





# # A mixed effects model for Coarse memory group where subject is a random intercept
model4 = smf.mixedlm("AccuracyNumeric ~ ConditionsNumeric", detailed_percentage_table_long, groups=detailed_percentage_table_long['Subject'])
result2 = model4.fit()



# Random slopes plot
random_slopes2 = result2.random_effects # Extract random slopes
fig, ax = plt.subplots(figsize=(12, 8)) # Create a single figure and axes
color_palette = sns.color_palette("Set2", len(random_slopes2)) # Define the custom pallette to be used


# Plot each subject's data on the same axes
for i, (subject, slope) in enumerate(random_slopes2.items()):
    subject_data = detailed_percentage_table_long.loc[detailed_percentage_table_long['Subject'] == subject]
    sns.pointplot(x='ConditionsNumeric', y='AccuracyNumeric', data=subject_data, ax=ax, color=color_palette[i])

# Add labels and title
ax.set_xlabel('Conditions')
ax.set_ylabel('Accuracy')
ax.set_title('Random slope model per subject for detailed memory group')
ax.set_xticklabels(['Congruent', 'Incongruent']) # Change x-tick labels





# # Plotting to see the general trend with both memory types combined
# combined_table = pd.concat([detailed_percentage_table_long.mean(), coarse_percentage_table_long.mean()], axis=1)
# combined_table.columns = ['Detailed', 'Coarse']
# combined_table = combined_table.drop('Subject', axis=0, errors='ignore')
# combined_table = combined_table.drop('index', axis=0, errors='ignore')
# plt.figure(figsize=(10, 6)) # Create a larger figure
# colors = plt.cm.viridis(np.linspace(0, 1, len(combined_table)))
# combined_table.plot(kind='bar', width = 1.8, color = colors, align = 'center') # Plot the bar chart
# x_positions = np.arange(len(combined_table)) # Adjust the x-axis tick positions
# plt.xlabel('') # Add labels and titles
# plt.ylabel('Accuracy %')
# labels = [str(label.get_text()).replace("CongCoarse", " Congruent").replace("IncongCoarse", " Incongruent").replace("IncongDetailed", " Incongruent").replace("CongDetailed", " Congruent") for label in ax.get_xticklabels()]
# ax.set_xticklabels(labels, rotation=45, ha='right')





#%% EXPLORATORY MIXED EFFECTS MODEL FOR CONGRUENCY AND MEMORY TYPE

exploratory_mixed_effects_data = detailed_mem_data = memory_spec_data.loc[:, ['Subject', 'Congruency','DetailedMem', 'CoarseMem']]


mem_spec_long = pd.melt(memory_spec_data, id_vars=['Subject', 'Congruency'], value_vars=['DetailedMem', 'CoarseMem'])
mem_spec_long.info()
mem_spec_long = mem_spec_long.rename(columns={"value": "Accuracy"}) # Renaming that column to accuracy
mem_spec_long = mem_spec_long.rename(columns={"variable": "MemType"}) # Renaming that column to accuracy


mem_spec_long['Accuracy'] = pd.to_numeric(mem_spec_long['Accuracy'])
mem_spec_long = mem_spec_long.dropna(subset=['Accuracy'])
mem_spec_long.info()


# Creating a table with which displays the percentage of correct trials out of all attempted in Coarse Memory group. 
sums_mem_spec_long_acc = pd.pivot_table(mem_spec_long, values='Accuracy', index=['Subject', 'Congruency'], columns='MemType', aggfunc=np.sum)
counts_mem_spec_long_acc = pd.pivot_table(mem_spec_long, values='Accuracy', index=['Subject', 'Congruency'], columns='MemType', aggfunc='count')
mem_spec_long_percentage_table = (sums_mem_spec_long_acc / counts_mem_spec_long_acc) * 100
print(mem_spec_long_percentage_table)



mem_spec_long_percentage_table = mem_spec_long_percentage_table.reset_index()
mem_spec_long_percentage_table_long = pd.melt(mem_spec_long_percentage_table, id_vars=['Subject', 'Congruency'], value_vars=['CoarseMem', 'DetailedMem']) # Long format


# Running a mixed effects model 
model5 = smf.mixedlm("value ~ Congruency * MemType", mem_spec_long_percentage_table_long, groups=mem_spec_long_percentage_table_long['Subject'])
result3 = model5.fit()
# Print model summary
print(result3.summary()) # Everything apart from congruency is sinificant.
# We clearly knew there was a diff betw coarse and detailed memory.
# But the interaction effect i of interest. 




#Let's conduct sosme post-hoc analsyses for the interaction effect to see what exactly is having an interaction effect. 
mem_spec_long_percentage_table_long['Interaction'] = mem_spec_long_percentage_table_long['Congruency'] + ' x ' + mem_spec_long_percentage_table_long['MemType']
interaction = mem_spec_long_percentage_table_long.groupby(['Congruency', 'MemType']).mean()['value'].unstack(level=1) # Error?



# Perform Tukey post-hoc analysis
tukey_results = pairwise_tukeyhsd(endog=mem_spec_long_percentage_table_long['value'], groups=mem_spec_long_percentage_table_long['Interaction'], alpha=0.05) # No diff in Coarse Cong and Incong. The rest is significantly different. There are 5 interaction effects to explain. 
print(tukey_results) # No diff in Coarse Cong and Incong. The rest is significantly different. There are 5 interaction effects to explain. 
 


# Create the bar plot
plt.figure(figsize=(8, 6))
plt.bar(x= mem_spec_long_percentage_table_long['Congruency'],
        height=mem_spec_long_percentage_table_long['value'],
        color=mem_spec_long_percentage_table_long['MemType'],
        alpha=0.8)

# Set labels and title
plt.xlabel('')
plt.ylabel('Accuracy (%)')


# Create the legend
legend_labels = mem_spec_long_percentage_table_long['MemType'].unique()
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=label) for label in legend_labels]
plt.legend(legend_handles, legend_labels)

# Show the plot
plt.show()



#%% EXCLUDED ASSOCIATIONS DONT KNOW DATA
# We want to ensure there are no significant differences between the groups for data that we excluded.

excluded_associations_dontknow_data.info()


# To test for statistically significant differences between two categorical data groups, i.e. congruence and association type,I will use the chi-square test of independence. 
# Creating a contingency table
contingency_table_assoc_dontknow = pd.crosstab(excluded_associations_dontknow_data['Congruency'], excluded_associations_dontknow_data['AssociationType'])
contingency_table_assoc_dontknow = contingency_table_assoc_dontknow.rename(index={"Cong": "CongDontKnow", "Incong": "InongDontKnow"})

# Perform chi-square test of independence
chi2, p, dof, expected = chi2_contingency(contingency_table_assoc_dontknow)

# Print results
print("Chi-square statistic:", chi2)
print("p-value:", p) 
print("degrees of freedom:", dof)# No significant differences between those groups. Safe to remove them from final analysis. 


# Plot the bar plot
ax = contingency_table_assoc_dontknow.sum().plot(kind='bar')
# Add a title to the plot
plt.title("Excluded data points for 'do not know' option")
# Rotate the tick labels by 45 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_xlabel('') # Add x-axis labels
# Display the plot
plt.show()

#%% EXCLUDED MEMORY SPECIFICITY DATA

# count the instances of each category in the Congruency column
counts_coarse_excluded = excluded_coarsemem_dontknow_data['Congruency'].value_counts()
counts_detailed_excluded = excluded_detailedmem_dontknow_data['Congruency'].value_counts()

# Run the following two graphs together to better visualise the differences

bar_width = 0.35 # Set the width of the bars
x = np.arange(len(counts_coarse_excluded)) # Calculate the center positions for the bars

fig, ax = plt.subplots() # Create a figure and axes
ax.bar(x, counts_coarse_excluded.values, width=bar_width, label='Coarse memory group') # Plot the first bar plot
ax.bar(x + bar_width, counts_detailed_excluded.values, width=bar_width, label='Detailed memory group') # Plot the second bar plot with adjusted positions
ax.set_xticks(x + bar_width / 2) # Set the x-axis ticks
ax.set_xticklabels(counts_coarse_excluded.index)# Set the x-axis labels
ax.set_xlabel('Congruency') # Add x-axis labels
ax.set_ylabel('Count of excluded answers') # Add  y-axis labels
ax.set_title('Excluded "Do not know" data points') # Set the title
ax.legend() # Add a legend

# We can see that there were more congruent points were excluded in detailed memory group while more incongruent answers received a dont know in coarse memory group. 

#%% NO ANSWER DATA

excluded_associations_noanswer_data.info()
excluded_coarse_noanswer_data.info()
excluded_detailedmem_noanswer_data.info()


contingency_table_assoc_noanswer = pd.crosstab(excluded_associations_noanswer_data['Congruency'], excluded_associations_noanswer_data['AssociationType'])
# Perform chi-square test of independence
chi3, p, dof, expected = chi2_contingency(contingency_table_assoc_noanswer)
print("Chi-square statistic:", chi3)# Print results
print("p-value:", p) # No significant differences between those groups. Safe to remove them from final analysis. 
contingency_table_assoc_noanswer = contingency_table_assoc_noanswer.rename(index={"Cong": "CongNoAnswer", "Incong": "InongNoAnswer"})


# Plot the bar plot
ax = contingency_table_assoc_noanswer.sum().plot(kind='bar')
# Add a title to the plot
plt.title("Excluded data points where no answer was recorded")
# Rotate the tick labels by 45 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_xlabel('') # Add x-axis labels
# Display the plot
plt.show()

# count the instances of each category in the Congruency column
counts_coarse_noanswer_excluded = excluded_coarse_noanswer_data['Congruency'].value_counts()
counts_detailed_noanswer_excluded = excluded_detailedmem_noanswer_data['Congruency'].value_counts()


bar_width = 0.35 # Set the width of the bars
x2 = np.arange(len(counts_coarse_noanswer_excluded)) # Calculate the center positions for the bars

fig2, ax = plt.subplots() # Create a figure and axes
ax.bar(x2, counts_coarse_noanswer_excluded.values, width=bar_width, label='Coarse memory group') # Plot the first bar plot
ax.bar(x2 + bar_width, counts_detailed_noanswer_excluded.values, width=bar_width, label='Detailed memory group') # Plot the second bar plot with adjusted positions
ax.set_xticks(x2 + bar_width / 2) # Set the x-axis ticks
ax.set_xticklabels(counts_coarse_noanswer_excluded.index)# Set the x-axis labels
ax.set_xlabel('Congruency') # Add x-axis labels
ax.set_ylabel('Count of excluded answers') # Add  y-axis labels
ax.set_title('Excluded "no-answer" data points') # Set the title
ax.legend(loc='upper right', bbox_to_anchor=(1.5, 1)) # Add a legend

stacked_table = pd.concat([contingency_table_assoc_noanswer, contingency_table_assoc_dontknow], axis=0)
print(stacked_table)

stacked_table1 = (stacked_table / 1184) * 100



