def HA(df):
    df['HA_close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    df['HA_Open'] = (df['Open'] + df['Close']) / 2
    df['HA_low'] = df['Low']
    df['HA_high'] = df['High']
    return df