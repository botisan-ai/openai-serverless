from jwcrypto import jwk

key = jwk.JWK.generate(kty='oct', size=256)

print('Signing Key:')
print(key.export())
