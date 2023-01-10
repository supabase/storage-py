# Changelog

<!--next-version-placeholder-->

## v0.4.0 (2023-01-10)
### Feature
* Add transform options to signed_url,download, and public_url ([`122b2a3`](https://github.com/supabase-community/storage-py/commit/122b2a3403dfa1fa33dd384b2a7c42e9f3094f9e))
* Add copy and transform option type ([`6be51ee`](https://github.com/supabase-community/storage-py/commit/6be51ee4a5bedabce6a25d05b9a38ae65f40efef))

### Fix
* Add stray / ([`27b6bcd`](https://github.com/supabase-community/storage-py/commit/27b6bcd85866a152a1804679cb27f726a50d2bf3))
* Remove stray / ([`216cf36`](https://github.com/supabase-community/storage-py/commit/216cf3667479380fb893e16b4bd47d31f5a2b641))
* Update render_path for get_public_url ([`0272f1b`](https://github.com/supabase-community/storage-py/commit/0272f1b5dd787b8a51727c1c9de3116c15b124b6))
* Run black ([`42a9ed3`](https://github.com/supabase-community/storage-py/commit/42a9ed3f8f4e3d8e66f065f2ec64936a95b422b5))
* Handle stray / ([`dd72fd6`](https://github.com/supabase-community/storage-py/commit/dd72fd6758f975e8d1f1ba56765c21ac846cf62c))
* Handle stray / ([`604e804`](https://github.com/supabase-community/storage-py/commit/604e804e73583cd396829d41ecb8f3baf789f754))
* Remove query params ([`1feb825`](https://github.com/supabase-community/storage-py/commit/1feb82590a9f3ca025da41da82e8089f7835783f))
* Add query string param ([`72d299d`](https://github.com/supabase-community/storage-py/commit/72d299d4257265099e44c6b9e821fa3ca86d19ab))
* Strip out transformation changes ([`686b7fa`](https://github.com/supabase-community/storage-py/commit/686b7fa03007ee6dddc2bd96492a171bddf7de82))
* Remove stray $ ([`f0c8fdc`](https://github.com/supabase-community/storage-py/commit/f0c8fdcf69cd397e31c24091ae10550d65e0cb97))
* Switch from | to Union ([`f4005fd`](https://github.com/supabase-community/storage-py/commit/f4005fd672bc86bb694f2ddf50e202be7beb6370))
* Import Union, Optional from typing instead of typing-extensions ([`c5e5aba`](https://github.com/supabase-community/storage-py/commit/c5e5abaa8f7830cbfcd1caeafcd5d3c2140f2f0d))
* Omit infra changes ([`9b967ce`](https://github.com/supabase-community/storage-py/commit/9b967ce41d3598a68b08cbad45435a26fc0d5f0b))
* Add transform options on public url and download ([`7352f61`](https://github.com/supabase-community/storage-py/commit/7352f6128a1bd52e863dea0cf8db6f53519e6c78))

**[See all commits in this version](https://github.com/supabase-community/storage-py/compare/v0.3.6...v0.4.0)**

## v0.3.6 (2023-01-05)
### Fix
* Datetime and upload file type ([#12](https://github.com/supabase-community/storage-py/issues/12)) ([`a926a06`](https://github.com/supabase-community/storage-py/commit/a926a068234e68afbf8039fc7f71565397dfea86))
* Remove trailing "/" in `get_public_url` ([`8bf407c`](https://github.com/supabase-community/storage-py/commit/8bf407c5fc2bca401a673d42d0f9a82b7b9e80bb))

**[See all commits in this version](https://github.com/supabase-community/storage-py/compare/v0.3.5...v0.3.6)**
## v0.3.5 (2022-06-07)
### Fix
* Justinbarak patch 1 by @justinbarak in https://github.com/supabase-community/storage-py/pull/14
* chore(deps-dev): bump pytest-asyncio from 0.18.3 to 0.19.0 by @dependabot in https://github.com/supabase-community/storage-py/pull/16
* chore: bump httpx to 0.23 by @J0 in https://github.com/supabase-community/storage-py/pull/21
* chore(deps): bump typing-extensions from 4.2.0 to 4.4.0 by @dependabot in https://github.com/supabase-community/storage-py/pull/18
* chore(deps-dev): bump python-dotenv from 0.20.0 to 0.21.0 by @dependabot in https://github.com/supabase-community/storage-py/pull/17
* chore(deps-dev): bump sphinx from 4.5.0 to 5.2.3 by @dependabot in https://github.com/supabase-community/storage-py/pull/15
* chore: bump storage version by @J0 in https://github.com/supabase-community/storage-py/pull/22

**[See all commits in this version](https://github.com/supabase-community/storage-py/compare/v0.3.4...v0.3.5)**

## v0.3.4 (2022-06-07)
### Fix
* Signed_url ([`c8cdf44`](https://github.com/supabase-community/storage-py/commit/c8cdf444090e7d9c6cd68ac4f31afb52921c3ea5))
* Try no timeout as fix instead of sleep ([`68026be`](https://github.com/supabase-community/storage-py/commit/68026be058a5e5a0684d7bc174da674dfc6a137c))
* Signed_url ([`bd2e09c`](https://github.com/supabase-community/storage-py/commit/bd2e09c28164b364ca919fd888019e837af3890f))

**[See all commits in this version](https://github.com/supabase-community/storage-py/compare/v0.3.3...v0.3.4)**

## v0.3.3 (2022-06-06)
### Fix
* Upload method ([`844561f`](https://github.com/supabase-community/storage-py/commit/844561f63d58ad869a4303941e7ef8194ae89154))
* Use ** to merge dicts ([`2965ae7`](https://github.com/supabase-community/storage-py/commit/2965ae79857fd3b264384b0fbe8c7172744a9f12))
* Poetry lock ([`4d2a73f`](https://github.com/supabase-community/storage-py/commit/4d2a73f7f8170ddeac5ef154fd3c14c7b7bfec71))

**[See all commits in this version](https://github.com/supabase-community/storage-py/compare/v0.3.2...v0.3.3)**

## v0.3.2 (2022-05-16)
### Fix
* Don't create virtualenv in CI ([#7](https://github.com/supabase-community/storage-py/issues/7)) ([`2a85860`](https://github.com/supabase-community/storage-py/commit/2a8586082ff667c7b525bccf01df2c0e890f2b66))

**[See all commits in this version](https://github.com/supabase-community/storage-py/compare/v0.3.1...v0.3.2)**

## v0.3.1 (2022-05-01)
### Fix
* Parity with js ([`19f1816`](https://github.com/supabase-community/storage-py/commit/19f1816d23671d576ddf23feab401d51aaf7b3e4))

**[See all commits in this version](https://github.com/supabase-community/storage-py/compare/v0.3.0...v0.3.1)**

## v0.3.0 (2022-04-30)
### Feature
* Force version bump ([`62556c0`](https://github.com/supabase-community/storage-py/commit/62556c00a064c691df90be6f8c8a46cc1b772ba4))
* Ignore unused imports in certain files ([`efebefe`](https://github.com/supabase-community/storage-py/commit/efebefed65a3adfa23ef4142600215bd1e6cff01))
* Add context manager ([`ec61c29`](https://github.com/supabase-community/storage-py/commit/ec61c29f72a1dae1148dbd15ab5cdad61eac835c))
* Add build_sync to makefile ([`b0a8665`](https://github.com/supabase-community/storage-py/commit/b0a86658678ce98a977cf67c07f07847003dcccf))
* Add statusCode to exception ([`6923975`](https://github.com/supabase-community/storage-py/commit/692397503f4a475168b92a8d5d8cda7719d2bf65))
* Add key to clients ([`838af7c`](https://github.com/supabase-community/storage-py/commit/838af7c0aded3c2e20df2ddd8e665da33d65106d))

### Fix
* **3.7 comp:** Import TypedDict from typing_extensions ([`dca5d6f`](https://github.com/supabase-community/storage-py/commit/dca5d6f716eb9624c4242a04e41e7b43f4e60ec6))
* Add AsyncClient ([`9522298`](https://github.com/supabase-community/storage-py/commit/9522298b9cb63531802984844287e7da3c996a93))
* Add storage to url ([`a33f9a3`](https://github.com/supabase-community/storage-py/commit/a33f9a398e43ef49d499b0685ff2557ca386c4fc))
* Async fixes ([`061cb15`](https://github.com/supabase-community/storage-py/commit/061cb15c4800117b71c4f3c50e3e1b9bd5989e7c))
* Typing.literal compatible w py3.7 ([`fcc21f1`](https://github.com/supabase-community/storage-py/commit/fcc21f16181a2127255edcf628e9f467a09874ca))

**[See all commits in this version](https://github.com/supabase-community/storage-py/compare/v0.2.0...v0.3.0)**

## v0.2.0 (2022-04-11)

### What's Changed

- Sync support by @anand2312 in https://github.com/supabase-community/storage-py/pull/1

### New Contributors

- @anand2312 made their first contribution in https://github.com/supabase-community/storage-py/pull/1

## v0.1.0 (2021-12-24)

### Refactor

- update test client imports
- change directory structure

### Feat

- initial commit
