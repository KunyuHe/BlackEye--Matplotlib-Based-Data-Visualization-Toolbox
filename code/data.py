import seaborn as sns
from sklearn.preprocessing import StandardScaler

def get_mpg(target=None, scale=True):
    # Sample 50 observations from 'mpg' dataset
    sample = sns.load_dataset('mpg').sample(50, random_state=123)
    # Set name of the model as index, and keep the first row for rows with
    # duplicate index
    sample = sample.set_index(sample.name.apply(lambda x: x.title())).iloc[:,
             :-2]
    sample = sample.loc[sample.index.drop_duplicates(keep=False)]
    # Drop rows with missing values
    sample = sample[sample.isnull().sum(axis=1) == 0]

    if target:
        features = list(set(sample.columns) - {target})
    else:
        features = list(sample.columns)

    if scale:
        scaler = StandardScaler()
        sample[features] = scaler.fit_transform(sample[features])

    return sample
