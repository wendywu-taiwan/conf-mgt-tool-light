python3 -m venv venv
. venv/bin/activate

PROXY_HTTP=$http_proxy
PROXY_HTTPS=$https_proxy

export https_proxy=
export http_proxy=

git clone git@10.29.25.73:wendy_wu/ConfigManageTool.git
cd ConfigManageTool
git checkout -b region-apac origin/region-apac

https_proxy=$PROXY_HTTPS
http_proxy=$PROXY_HTTP

echo $https_proxy
echo $http_proxy

pip install -r requirements.txt
python3 manage.py makemigrations permission
python3 manage.py makemigrations common
python3 manage.py makemigrations RulesetComparer
python3 manage.py migrate permission
python3 manage.py migrate common
python3 manage.py migrate RulesetComparer
python3 manage.py migrate

https_proxy=
http_proxy=

cd RulesetComparer/rulesets
git submodule add git@10.29.25.73:axn/bre_ruleset.git Git
cd ..
cd ..