# Storage-py

Python Client library to interact with Supabase Storage.



## How to use

As it takes some effort to get the headers. We suggest that you use the storage functionality through the main [Supabase Python Client](https://github.com/supabase-community/supabase-py)


```python3
from storage3 import create_client

url = "https://<your_supabase_id>.supabase.co/storage/v1"
key = "<your api key>"
headers = {"apiKey": key, "Authorization": f"Bearer {key}"}

# pass in is_async=True to create an async client
storage_client = create_client(url, headers, is_async=False)

storage_client.list_buckets()
```
