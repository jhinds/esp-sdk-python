= Example
```
secretKey = '[Secret Key]'
publicKey = '[Public Key]'
evidentApi = EvidentApi(secretKey, publicKey)
evidentApi.ListSignatures()
evidentApi.ListSeppressions()
evidentApi.ShowSeppression(id = '3715')
evidentApi.CreateSignatureSeppression(signature_ids = ['26'], resource = 'i-dce5491a', external_account_ids = ['1968'])
```
