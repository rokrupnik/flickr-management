# flickr-management
A collection of a few simple python scripts for managing you flickr account.

# Requirements
* python 2.7
* [`flickrapi` library](https://github.com/sybrenstuvel/flickrapi) -> `pip install flickrapi`

# Usage
1. Rename `flickr_account.example.py` to `flickr_account.py` and insert your API key, secret and user id.  
2. In terminal, run any desired script (e.g.: `python sort_albums.py`). On the first time, the authorization process should happen in the browser.. When the process is finished, add `user_id`, `access_token` and `access_token_secret` to `flickr_account.py` file. See more detailed instructions in the [flickr_api package docs].
3. Usage for any of the scripts is included in their comments.
