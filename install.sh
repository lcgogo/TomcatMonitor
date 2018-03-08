#!/bin/sh

if [ ! -e /usr/lib/systemd/system/tomcat.service ];then
  yum install -y tomcat tomcat-webapps tomcat-admin-webapps git
else
  echo JAVA_OPTS=\"-Xms8m -Xmx16m\" >> /usr/share/tomcat/conf/tomcat.conf
  systemctl restart tomcat
fi

\cp -f ./tomcat_monitor.py /usr/bin
cat > /usr/lib/systemd/system/tomcat_monitor.service << EOF
[Unit]
Description=Tomcat Monitor service
After=syslog.target network.target
[Service]
ExecStart=/usr/bin/tomcat_monitor.py
Restart=always
RestartSec=10
[Install]
WantedBy=multi-user.target
EOF

chmod 644 /usr/lib/systemd/system/tomcat_monitor.service
systemctl daemon-reload
systemctl start tomcat_monitor.service
systemctl enable tomcat_monitor.service
