# docker 安装

## odoo conf
``` conf

inside_gateway_link=http://172.17.0.1:9000/gateway

# workers

workers = 8
proxy_mode = True
longpolling_port = 8072
max_cron_threads = 2

```

# online
``` shell
docker run -v /etc/chuanmoon/:/etc/odoo/ \
-v /data/docker/chuanmoon/addons:/mnt/extra-addons/ \
-v /data/docker/chuanmoon/log/:/var/log/odoo/ \
-v /data/docker/chuanmoon/odoo:/var/lib/odoo/ \
-p 7069:8069 -p 7072:8072 -p 7071:8071 \
--name odoo_chuanmoon -t odoo:14
```

## windows 11

``` shell
docker run \
-v //d/etc/chuanmoon/:/etc/odoo/ \
-v //d/workspace/chuanmoon/admin/addons/:/mnt/extra-addons/ \
-p 8069:8069 \
--name odoo_chuanmoon -t odoo:14
```

## macos

``` shell
docker run -v /etc/chuanmoon/:/etc/odoo/ \
-v /data/workspace/chuanmoon/admin/addons:/mnt/extra-addons/ \
-v /data/workspace/chuanmoon/admin/log/:/var/log/odoo/ \
-v /data/workspace/chuanmoon/admin/odoo:/var/lib/odoo/ \
-p 8069:8069 \
--link postgres:db \
--name odoo_chuanmoon -t odoo:14
```


## nginx

``` conf
server {
        listen 80;
        listen 443 ssl;
        server_name admin.your_domin.com;

        ssl_certificate      /etc/nginx/ssl/1_admin_your_domin_com_bundle.crt;
        ssl_certificate_key  /etc/nginx/ssl/2_admin_your_domin_com.key;
        ssl_session_timeout 5m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers AESGCM:ALL:!DH:!EXPORT:!RC4:+HIGH:!MEDIUM:!LOW:!aNULL:!eNULL;
        ssl_prefer_server_ciphers on;

        proxy_set_header           Host $host;
        proxy_set_header           X-Real-IP $remote_addr;
        proxy_set_header           X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header           X-Forwarded-Proto https;
        proxy_set_header           X-Forwarded-Host $host;

        gzip                       on;
        gzip_min_length            1k;
        gzip_buffers               4 32k;
        gzip_types                 text/plain application/x-javascript text/xml text/css application/xml text/javascript application/javascript application/json image/jpeg image/gif image/png;
        gzip_vary                  on;

        # HTTP to HTTPS
        if ($scheme = http) {
            return 301 https://$host$request_uri;
        } 

        location / {
                client_max_body_size    10m;
                proxy_pass              http://localhost:7069;
        }

        location ~* /web/static/ {
                proxy_cache_valid       200 60m;
                proxy_buffering         on;
                expires                 864000;
                proxy_pass              http://localhost:7069;
        }
        
        location /longpolling/ {
                proxy_pass        http://localhost:7072/longpolling/;
                proxy_redirect    off;
        }
        
        location ~ ^/web/database/(manager|selector) {
                deny    all;
        }

}
```

