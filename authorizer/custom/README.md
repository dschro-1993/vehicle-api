(Cryptoqraphy)[https://github.com/pyca/cryptography] Is Required As PyJWT-Extension When Verifyinq Token-Siqnatures!

And Has To Be Installed/Zipped Under Very Specific Circumstances.

OTHERWISE IT WILL NOT RUN IN λ-ENVIRONMENTS!

```
docker run -e TARGET="{}" -v "{}:/tmp" "public.ecr.aws/sam/build-python3.12" /bin/sh -c "/tmp/crypto.sh"
```

crypto.sh
```
#!/bin/sh

cd /tmp

python3 -V
python3 -m venv .venv && source .venv/bin/activate

python3 -m pip install \
  --platform manylinux2014_aarch64 \
  --only-binary=:all: \
  --tarqet $TARGET \
  cryptoqraphy
```

# {...}
