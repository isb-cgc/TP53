export HOME=/home/circleci/${CIRCLE_PROJECT_REPONAME}
export HOMEROOT=/home/circleci/${CIRCLE_PROJECT_REPONAME}

# Remove .pyc files; these can sometimes stick around and if a
# model has changed names it will cause various load failures
find . -type f -name '*.pyc' -delete

# Install and update apt-get info
echo "Preparing System..."
apt-get -y --force-yes install software-properties-common
apt-get update -qq

# Install apt-get dependencies
echo "Installing Dependencies..."
apt-get install -y --force-yes unzip libffi-dev libssl-dev python3-dev libpython3-dev
echo "Dependencies Installed"

# Install PIP + Dependencies
echo "Installing pip3..."
curl --silent https://bootstrap.pypa.io/get-pip.py | python3

# Install our primary python libraries
# If we're not on CircleCI, or we are but the lib directory isn't there (cache miss), install lib
if [ ! -d "lib" ]; then
    echo "Installing Python Libraries..."
    pip3 install -r ${HOMEROOT}/requirements.txt -t ${HOMEROOT}/lib --upgrade --only-binary all
else
    echo "Using restored cache for Python Libraries"
fi

echo "Libraries Installed"

# Install Google Cloud SDK
# If we're not on CircleCI or we are but google-cloud-sdk isn't there, install it
if [ ! -d "/usr/lib/google-cloud-sdk" ]; then
    echo "Installing Google Cloud SDK..."
    export CLOUDSDK_CORE_DISABLE_PROMPTS=1
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    apt-get install apt-transport-https ca-certificates
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
    apt-get update && apt-get -y install google-cloud-sdk
    echo "Google Cloud SDK Installed"
fi
