import re
import pandas as pd
def pp(x):

    pattern = '\d{1,2}\/\d{1,2}\/\d{1,2}\,\s\d{1,2}\:\d{1,2}\s\w\w\s\-\s'

    messeges = re.split(pattern, x)[1:]


    dates = re.findall('\d{1,2}\/\d{1,2}\/\d{1,2}\,\s\d{1,2}\:\d{1,2}\s\w\w', x)

    df = pd.DataFrame({'user_messege': messeges, 'date': dates})

    df['date'] = pd.to_datetime(df['date'])

    df['user_messege'] = df['user_messege'].str.split(':')

    def user(x):
        if len(x) < 2:
            return 'Group notification'
        else:
            return x[0]

    df['messege'] = df['user_messege'].apply(lambda x: x[-1])

    df['user'] = df['user_messege'].apply(lambda x: user(x))

    df = df.drop(columns=['user_messege'])

    df['year'] = df['date'].dt.year

    df['month'] = df['date'].dt.month_name()

    df['hours'] = df['date'].dt.hour

    df['minute'] = df['date'].dt.minute
    df['messege'] = df['messege'].apply(lambda x: re.split('\n', x)[0])

    return df