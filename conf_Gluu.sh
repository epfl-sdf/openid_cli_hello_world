echo "Configuration file 1:"
read -p "Enter Your license id: "  license_id
while [ -z "$license_id" ]
do
  read -p "Enter Your license id: "  license_id
done
read -p "Enter Your public key: "  public_key
while [ -z "$public_key" ]
do
  read -p "Enter Your license id: "  public_key
done
read -p "Enter Your public password: "  public_password
while [ -z "$public_password" ]
do
  read -p "Enter Your license id: "  public_password
done
read -p "Enter Your license password: "  license_password
while [ -z "$license_password" ]
do
  read -p "Enter Your license id: "  license_password
done

echo "oxd-conf.json:"
sudo echo "{
    \"port\":8099,
    \"localhost_only\":true,
    \"time_out_in_seconds\":0,
    \"use_client_authentication_for_pat\":true,
    \"use_client_authentication_for_aat\":true,
    \"trust_all_certs\":true,
    \"trust_store_path\":\"\",
    \"trust_store_password\":\"\",
    \"license_id\":\"$license_id\",
    \"public_key\":\"$public_key\",
    \"public_password\":\"$public_password\",   
    \"license_password\":\"$license_password\",
    \"support-google-logout\": true,
    \"state_expiration_in_minutes\":5,
    \"nonce_expiration_in_minutes\":5
}" | sudo tee /opt/oxd-server/conf/oxd-conf.json 

echo "Configuration file 2:"
read -p "Enter Your op_host: "  op_host
while [ -z "$op_host" ]
do
  read -p "Enter Your op_host: "  op_host
done
read -p "Enter Your authorization_redirect_uri: "  authorization_redirect_uri
while [ -z "$authorization_redirect_uri" ]
do
  read -p "Enter Your authorization_redirect_uri: "  authorization_redirect_uri
done
read -p "Enter Your post_logout_redirect_uri: " post_logout_redirect_uri
while [ -z "$post_logout_redirect_uri" ]
do
  read -p "Enter Your post_logout_redirect_uri: "  post_logout_redirect_uri
done

echo "oxd-default-site-config.json:"
sudo echo "{
    \"op_host\":\"$op_host\",
    \"authorization_redirect_uri\":\"$authorization_redirect_uri\",
    \"post_logout_redirect_uri\":\"$post_logout_redirect_uri\",
    \"response_types\":[\"code\"],
    \"grant_type\":[\"authorization_code\"],
    \"acr_values\":[\"basic\"],
    \"scope\":[\"openid\", \"profile\"],
    \"ui_locales\":[\"en\"],
    \"claims_locales\":[\"en\"],
    \"client_jwks_uri\":\"\",
    \"contacts\":[]
}" | sudo tee /opt/oxd-server/conf/oxd-default-site-config.json
