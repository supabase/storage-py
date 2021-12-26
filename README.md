# Storage-py

Python Client library to interact with Supabase Storage.



## How to use

As it takes some effort to get the headers. We suggest that you use the storage functionality through the main [Supabase Python Client](https://github.com/supabase-community/supabase-py)


```python3
from storage3 import storage_client

storage_client = storage_client.SupabaseStorageClient('https://<your_supabase_id>.supabase.co/storage/v1)', {'apiKey': '<your_api_key>', 'Authorization': 'Bearer <an_auth_token>'})

storage_client.list()
```
