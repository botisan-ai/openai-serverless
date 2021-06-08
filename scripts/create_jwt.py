from jwcrypto import jwk

key = jwk.JWK.generate(kty='RSA', size=2048)

print(key.export(private_key=True))
print(key.export(private_key=False))
