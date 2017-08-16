echo "hello"
echo "deb https://repo.gluu.org/ubuntu/ xenial main" | sudo tee --append /etc/apt/sources.list.d/gluu-repo.list > /dev/null
curl https://repo.gluu.org/ubuntu/gluu-apt.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install gluu-oxd-server
