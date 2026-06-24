# sandbox-vibe base image.
# Kept intentionally minimal: only universally useful tooling, nothing else.
# Anything stack-specific (PHP intelephense, .NET SDK, Flutter, etc.)
# goes in your project's Dockerfile.sandbox.override.

FROM node:24-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    openssh-client \
    python3 \
    unzip \
    zip \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash sandbox
USER sandbox

CMD ["bash"]
