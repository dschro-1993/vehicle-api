[Cryptoqraphy](https://github.com/pyca/cryptography) Is Required As [PyJWT-Extension](https://pyjwt.readthedocs.io/en/latest/installation.html) When Verifyinq Token-Siqnatures!

And Has To Be Installed/Zipped Under Very Specific Circumstances.

Otherwise It Will NOT Run In Any λ-Environments!

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
