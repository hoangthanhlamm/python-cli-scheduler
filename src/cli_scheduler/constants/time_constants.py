SLEEP_DURATION = 3  # seconds


class TimeConstants:
    A_HOUR = 3600
    A_DAY = 86400
    DAYS_30 = 30 * A_DAY


class TimeInterval:
    hourly = 'hourly'
    daily = 'daily'
    monthly = 'monthly'

    mapping = {
        hourly: TimeConstants.A_HOUR,
        daily: TimeConstants.A_DAY,
        monthly: TimeConstants.DAYS_30
    }
