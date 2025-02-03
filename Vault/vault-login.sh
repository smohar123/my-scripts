export VAULT_ADDR="http://localhost:9999"
pod=$(kubectl -n vault get pods -l app.kubernetes.io/name=vault --no-headers | awk '{print $1}' | head -n1)
token=$(kubectl -n vault exec -c vault $pod -- vault write auth/kubernetes/login role=admin jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token -format=json | jq -r .auth.client_token )
service=$(kubectl -n vault get svc --no-headers | awk '{print $1}' | grep "vault$")
while true
do
        kubectl -n vault port-forward svc/$service 9999:8200
done &
sleep 5s
vault login -no-print --address http://localhost:9999 token=$(echo $token)
