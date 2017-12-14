from influxdb import InfluxDBClient
from CoinSpider import settings

if __name__ == '__main__':
    """
    clear database when startup
    """
    client = InfluxDBClient(
        host=settings.INFLUX_HOST,
        port=settings.INFLUX_PORT,
        username=settings.INFLUX_USER,
        password=settings.INFLUX_PASS,
        database=settings.INFLUX_DATABASE
    )
    client.query('drop measurement %s;' % settings.INFLUX_TABLE)
    client.close()