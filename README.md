# [Geoip2Influx](https://github.com/leo15dev/geoip2influx)

***

A python script that will parse the nginx access.log and send geolocation metrics and log metrics to InfluxDB

![](https://i.imgur.com/w6kVRVW.jpeg)

Country: RFC 1918 for IPv4 Private Address (City: Lan)

Country: ULA for IPv6 Private Address (City: Lan)

***

## Usage

### Enviroment variables:

These are the **default** values for all envs. 
Add the ones that differ on your system. 

| Environment Variable | Example Value | Description |
| -------------------- | ------------- | ----------- |
| NGINX_LOG_PATH | /config/log/nginx/access.log | Container path for Nginx logfile , defaults to the example. |
| GEO_MEASUREMENT | geoip2influx | InfluxDB measurement name for geohashes. Optional, defaults to the example. |
| LOG_MEASUREMENT | nginx_access_logs | InfluxDB measurement name for nginx logs. Optional, defaults to the example. |
| SEND_NGINX_LOGS | true | Set to `false` to disable nginx logs. Optional, defaults to `true`. |
| GEOIP2INFLUX_LOG_LEVEL | info | Sets the log level in geoip2influx.log. Use `debug` for verbose logging Optional, defaults to info. |
| GEOIP2INFLUX_LOG_PATH | /config/log/geoip2influx/geoip2influx.log | Optional. Defaults to example. |
| GEOIP_DB_PATH | /config/geoip2db/GeoLite2-City.mmdb | Optional. Defaults to example. |
| MAXMINDDB_LICENSE_KEY | xxxxxxx | Add your Maxmind licence key |
| MAXMINDDB_USER_ID | xxxxxxx| Add your Maxmind account id |

**InfluxDB v1.8.x values**

| Environment Variable | Example Value | Description |
| -------------------- | ------------- | ----------- |
| INFLUX_HOST | localhost | Host running InfluxDB. |
| INFLUX_HOST_PORT | 8086 | Optional, defaults to 8086. |
| INFLUX_DATABASE | geoip2influx | Optional, defaults to geoip2influx. |
| INFLUX_USER | root | Optional, defaults to root. |
| INFLUX_PASS | root | Optional, defaults to root. |
| INFLUX_RETENTION | 7d | Sets the retention for the database. Optional, defaults to example.|
| INFLUX_SHARD | 1d | Set the shard for the database. Optional, defaults to example. |

**InfluxDB v2.x values**

| Environment Variable | Example Value | Description |
| -------------------- | ------------- | ----------- |
| USE_INFLUXDB_V2 | true | Required if using InfluxDB2. Defaults to false |
| INFLUXDB_V2_TOKEN | secret-token | Required |
| INFLUXDB_V2_URL | http://localhost:8086 | Optional, defaults to http://localhost:8086 |
| INFLUXDB_V2_ORG | geoip2influx | Optional, defaults to geoip2influx. Will be created if not exists. |
| INFLUXDB_V2_BUCKET | geoip2influx | Optional, defaults to geoip2influx. Will be created if not exists. |
| INFLUXDB_V2_RETENTION | 604800 | Optional, defaults to 604800. 7 days in seconds |
| INFLUXDB_V2_DEBUG | false | Optional, defaults to false. Enables the debug mode for the influxdb-client package. |
| INFLUXDB_V2_BATCHING | true | Optional, defaults to false. Enables batch writing of data. |
| INFLUXDB_V2_BATCH_SIZE | 100 | Optional, defaults to 10. |
| INFLUXDB_V2_FLUSH_INTERVAL | 30000 | Optional, defaults to 15000. How often in milliseconds to write a batch |

#### INFLUXDB_V2_TOKEN

If the organization or bucket does not exist, it will try and create them with the token.

> [!NOTE]
> The minimim level of rights needed is write access to the bucket.

### MaxMind Geolite2

Default download location is `/config/geoip2db/GeoLite2-City.mmdb`

Get your licence key here: https://www.maxmind.com/en/geolite2/signup

### InfluxDB 

#### InfluxDB v2.x and v1.8x is supported.

The InfluxDB database/bucket and retention rules will be created automatically with the name you choose.

### Docker compose

```yaml
services:
  geoip2influx:
    image: xcxxcxcxz/geoip2influx:test
    container_name: geoip2influx
    network_mode: bridge
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Taipei
      - INFLUX_HOST=<influxdb host>
      - INFLUX_HOST_PORT=<influxdb port>
      - MAXMINDDB_LICENSE_KEY=<license key>
      - MAXMINDDB_USER_ID=<account id>
      - SEND_NGINX_LOGS=true
    volumes:
      - /path/to/appdata/geoip2influx:/config
      - /var/log/nginx:/config/log/nginx   
    restart: unless-stopped
```

**InfluxDB2 examples** (Not yet tested, but it should be work)

```yaml
services:
  geoip2influx:
    image: xcxxcxcxz/geoip2influx:test
    container_name: geoip2influx
    network_mode: bridge
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Taipei
      - INFLUXDB_V2_URL=<influxdb url>
      - INFLUXDB_V2_TOKEN=<influxdb token>
      - USE_INFLUXDB_V2=true
      - MAXMINDDB_LICENSE_KEY=<license key>
      - MAXMINDDB_USER_ID=<account id>
      - SEND_NGINX_LOGS=true
    volumes:
      - /path/to/appdata/geoip2influx:/config
      - /var/log/nginx:/config/log/nginx    
    restart: unless-stopped
```

***

## Grafana dashboard: 





***

## Sending Nginx log metrics

Nginx needs to be compiled with the geoip2 module: https://github.com/leev/ngx_http_geoip2_module

1. Add the following to the http block in your `nginx.conf` file:

   The log format is compatible with fail2ban in my personal experience, but it should be slightly adjusted according to your specific needs.

```nginx
#geoip2 /config/geoip2db/GeoLite2-City.mmdb {
geoip2 /usr/share/GeoIP/GeoLite2-Country.mmdb {
auto_reload 60m;
$geoip2_metadata_country_build metadata build_epoch;
$geoip2_data_country_code default=TW country iso_code;
$geoip2_data_country_name country names en;
}

log_format main
#log_format custom
'$remote_addr - $remote_user [$time_local] '
'"$request" '
'$status $body_bytes_sent '
'"$http_referer" '
'"$host" '
'"$http_user_agent" '
'"$request_time" '
'"$upstream_connect_time" '
'"$geoip2_data_city_name" '
'"$geoip2_data_country_iso_code" '
'"$http_cf_ipcountry" '
'"$http_x_forwarded_for"';

access_log  /var/log/nginx/access.log  main;
 ```
 
 2. Or set the access log use the `custom` log format. 
 ```nginx
access_log /config/log/nginx/access.log custom;
 ```

### Multiple log files

If you separate your nginx log files but want this script to parse all of them you can do the following:

As nginx can have multiple `access log` directives in a block, just add another one in the server block. 

**Example**

```nginx
	access_log /config/log/nginx/technicalramblings/access.log custom;
	access_log /config/log/nginx/access.log custom;
```
This will log the same lines to both files.

Then use the `/config/log/nginx/access.log` file in the `NGINX_LOG_PATH` variable. 

***

## Updates 

**28.06.26** - New Style, Fixed Nginx Log Rotation Issue ( Previously, during Log Rotation, you needed to restart geoip2influx to continue reading new logs.) 
```
28/06/2026 00:08:01 | MainThread        | geoip2influx | INFO     | (logparser.follow_file|line:310) | Log rotation detected on /config/log/nginx/access.log (Inode changed from 5810116 to 5810130). Switching handles. |
28/06/2026 00:08:01 | MainThread        | geoip2influx | INFO     | (logparser.follow_file|line:281) | Successfully opened newly rotated file /config/log/nginx/access.log (Inode: 5810130). |
```

***

Adapted source: 

1. https://github.com/ratibor78/geostat

2. https://github.com/GilbN/geoip2influx 
