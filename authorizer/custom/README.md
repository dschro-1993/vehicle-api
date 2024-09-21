Cryptography Is Required As PyJWT-Extension When Verifying Token-Signatures!

And Has To Be Installed/Zipped Under Specific Requirements.

OTHERWISE IT WILL NOT RUN IN λ-ENVIRONMENTS!!

```
docker run -e TARGET="{}" -v "{}:/tmp" "public.ecr.aws/sam/build-python3.12" /bin/sh -c "/tmp/cryptography.sh"
```

cryptography.sh
```
#!/bin/sh

cd /tmp

python3 -V
python3 -m venv .venv && source .venv/bin/activate

python3 -m pip install \
  --platform manylinux2014_aarch64 \
  --only-binary=:all: \
  --target $TARGET \
  cryptography
```

# {...}
