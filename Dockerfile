FROM debian:bullseye

ENV container docker
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive

LABEL mainainer="Emin Aktas<eminaktas34@gmail.com>"
LABEL version="2.0.0"
LABEL description="Get of Metrics Docker Image for get-of-metrics Python scipt, Node Exporter, Prometheus and Grafana"


COPY /get-of-metrics.deb /

RUN `# Updating Package List`                                                  && \
     apt update                                                            && \
                                                                               \
    `# Installing packages`                                                    && \
     apt install -y /get-of-metrics.deb                                    && \
                                                                                \
     apt-get install -y systemd systemd-sysv                                   && \
                                                                               \
     apt install -y curl wget libfontconfig1                               && \
                                                                               \
     `# Cleaning up after installation`                                        && \
     apt clean all                                                             && \
                                                                               \
     rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /get-of-metrics.deb

COPY /connection-parameters.json /home/get-of-metrics/

RUN `#Fixing permission error fir volume`                                                      && \
     chown -R 1000:1000 /home/get-of-metrics/connection-parameters.json                        && \
                                                                                               \
     chown -R 1000:1000 /var/log/get-of-metrics                                                && \
                                                                                               \
     chown -R 1000:1000 /etc/systemd/system/get-of-metrics.service                             && \
                                                                                               \
     chown -R 1000:1000 /home/get-of-metrics/prom-files

RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

RUN `#Node Exporter Setup` && \
    curl -s https://api.github.com/repos/prometheus/node_exporter/releases/latest \
    | grep browser_download_url \
    | grep linux-amd64 \
    | cut -d '"' -f 4 \
    | wget -qi - && \
    tar -xvf node_exporter*.tar.gz && \
    cd  node_exporter*/ && \
    cp node_exporter /usr/local/bin

COPY /node_exporter.service /etc/systemd/system/

RUN `#Prometheus Setup - 1`                               && \
    groupadd --system prometheus                          && \
    useradd -s /sbin/nologin --system -g prometheus prometheus                             && \
    mkdir /var/lib/prometheus                                           && \
    for i in rules rules.d files_sd; do mkdir -p /etc/prometheus/${i}; done                           && \
    mkdir -p /tmp/prometheus && cd /tmp/prometheus && \
    curl -s https://api.github.com/repos/prometheus/prometheus/releases/latest \
    | grep browser_download_url \
    | grep linux-amd64 \
    | cut -d '"' -f 4 \
    | wget -qi -    && \
    tar xvf prometheus*.tar.gz && \
    cd prometheus*/  && \
    mv prometheus promtool /usr/local/bin/ && \
    mv consoles/ console_libraries/ /etc/prometheus/ 

COPY /prometheus.yml /etc/prometheus/

COPY /prometheus.service /etc/systemd/system/

RUN `#Prometheus Setup - 2` && \
    cd ~/ && \
    rm -rf /tmp/prometheus && \
    for i in rules rules.d files_sd; do chown -R prometheus:prometheus /etc/prometheus/${i}; done && \
    for i in rules rules.d files_sd; do chmod -R 775 /etc/prometheus/${i}; done && \
    chown -R prometheus:prometheus /var/lib/prometheus/ && \
    `#Grafana Setup` && \
    wget https://dl.grafana.com/oss/release/grafana_7.1.3_amd64.deb && \
    dpkg -i grafana_7.1.3_amd64.deb && \
    apt remove -y curl wget && \
    rm -rf ~/* /node_exporter-1.0.1.linux-amd64 /node_exporter-1.0.1.linux-amd64.tar.gz

VOLUME [ "/sys/fs/cgroup" ]
VOLUME [ "/home/get-of-metrics" ]
VOLUME [ "/var/log/get-of-metrics" ]
VOLUME [ "/home/get-of-metrics/prom-files" ]

ENTRYPOINT [ "/lib/systemd/systemd" ]

RUN `#Enabling the service`                                                     && \
     systemctl enable get-of-metrics                                            && \
     systemctl enable prometheus                                                && \
     systemctl enable grafana-server                                            && \
     systemctl enable node_exporter

EXPOSE 9100
EXPOSE 9090
EXPOSE 3000