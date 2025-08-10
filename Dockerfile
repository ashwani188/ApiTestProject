# Start from official Jenkins LTS image
FROM jenkins/jenkins:lts

# Switch to root to install packages
USER root

# Install Git and Docker CLI, then clean up
RUN apt-get update && \
    apt-get install -y git docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to Jenkins user
USER jenkins