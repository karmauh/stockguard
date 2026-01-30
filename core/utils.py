from datetime import datetime, timedelta

def get_lookback_date(date_str: str, days: int = 365) -> str:
    """
    Returns a date string subtracted by 'days'.
    Args:
        date_str: 'YYYY-MM-DD'
        days: number of days to look back
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    lookback_dt = dt - timedelta(days=days)
    return lookback_dt.strftime("%Y-%m-%d")
