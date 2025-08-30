FROM quay.io/centos-bootc/centos-bootc:stream9


RUN dnf remove subscription-manager -y && \
    dnf install -y dnf-plugins-core && \
    dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo && \
    dnf config-manager -y --add-repo=https://netdevops.fury.site/yum/ && \
    echo "gpgcheck=0" | tee -a /etc/yum.repos.d/netdevops.fury.site_yum_.repo && \
    dnf -y install \
      git \
      make \
      docker-ce \
      docker-ce-cli \
      containerd.io \
      docker-buildx-plugin \
      docker-compose-plugin \
      containerlab && \
    systemctl enable docker.service && \
    dnf clean all && rm -rf /var/cache/dnf/*

RUN rm -rf /var/log/*.log /var/log/*/*.log /var/log/rhsm/rhsm.log
RUN mkdir -p /usr/lib/sysusers.d/ && \
    echo 'g clab_admins - - -' > /usr/lib/sysusers.d/clab_admins.conf && \
    echo 'g docker - - -' > /usr/lib/sysusers.d/docker.conf

RUN bootc container lint

