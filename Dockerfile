FROM quay.io/centos-bootc/centos-bootc:stream9


RUN dnf -y install dnf-plugins-core && \
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
    dnf clean all

RUN bootc container lint
