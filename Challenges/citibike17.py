import pandas as pd
import matplotlib.pyplot as plt

# Loading zip file and asking pandas to infer datetime format
df = pd.read_csv("/Users/mohitsharma44/Downloads/201402-citibike-tripdata.zip",
                 compression='zip', infer_datetime_format=True,
                 parse_dates=['starttime', 'stoptime'])

# Average time in Timedelta format
average_time = (df['stoptime'] - df['starttime']).mean()

# gender based counts
gender_counts = df['gender'].value_counts()

# usertype based counts
usertype_counts = df['usertype'].value_counts()

# usage by gender for a month over 24 hours
citibike_usage = df.groupby([df['starttime'].dt.hour])['gender'].value_counts().unstack()
