from influxdb import InfluxDBClient
import settings

client = InfluxDBClient(
    host=settings.INFLUX_HOST,
    port=settings.INFLUX_PORT,
    username=settings.INFLUX_USER,
    password=settings.INFLUX_PASS,
    database=settings.INFLUX_DATABASE
)
