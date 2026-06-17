# Expert-calibrated taxonomy (LEAD model vs PDM-Lite expert) — Bench2Drive-220

Model clean-route mean DS: **93.36** over 202 cleanly-evaluated routes.  Expert routes scored so far: **220/220**.

## Bucket counts

- `a`: 12
- `a*`: 6
- `b`: 28
- `c`: 4
- `clean`: 170

## Calibration targets (model failed, DS<100) — the heart of the paper

| route | town | model DS | expert DS | bucket | note |
|---|---|---|---|---|---|
| 2127 | Town12 | 60.0 | 100.0 | b | model failed DS 60.0; expert clean -> fixable model gap |
| 2201 | Town12 | 42.0 | 100.0 | b | model failed DS 42.0; expert clean -> fixable model gap |
| 2204 | Town12 | 30.26 | 100.0 | b | model failed DS 30.26; expert clean -> fixable model gap |
| 2215 | Town12 | 70.0 | 100.0 | b | model failed DS 70.0; expert clean -> fixable model gap |
| 2790 | Town12 | 98.993457 | 96.980453 | c | model DS 98.993457 & expert DS 96.980453 both <100 -> structural ceiling candidate |
| 2903 | Town12 | 21.132 | 100.0 | b | model failed DS 21.132; expert clean -> fixable model gap |
| 2989 | Town12 | 32.56 | 100.0 | b | model failed DS 32.56; expert clean -> fixable model gap |
| 3093 | Town12 | 60.0 | 100.0 | b | model failed DS 60.0; expert clean -> fixable model gap |
| 3364 | Town13 | 70.0 | 100.0 | b | model failed DS 70.0; expert clean -> fixable model gap |
| 3373 | Town13 | 70.0 | 100.0 | b | model failed DS 70.0; expert clean -> fixable model gap |
| 3378 | Town13 | 70.0 | 100.0 | b | model failed DS 70.0; expert clean -> fixable model gap |
| 3380 | Town13 | 70.0 | 100.0 | b | model failed DS 70.0; expert clean -> fixable model gap |
| 3436 | Town13 | 21.6 | 100.0 | b | model failed DS 21.6; expert clean -> fixable model gap |
| 3905 | Town13 | 7.94 | 100.0 | b | model failed DS 7.94; expert clean -> fixable model gap |
| 11755 | Town12 | 29.628 | 100.0 | b | model failed DS 29.628; expert clean -> fixable model gap |
| 17563 | Town12 | 60.0 | 100.0 | b | model failed DS 60.0; expert clean -> fixable model gap |
| 17635 | Town12 | 60.0 | 100.0 | b | model failed DS 60.0; expert clean -> fixable model gap |
| 17655 | Town12 | 60.0 | 100.0 | b | model failed DS 60.0; expert clean -> fixable model gap |
| 18252 | Town12 | 50.0 | 100.0 | b | model failed DS 50.0; expert clean -> fixable model gap |
| 23659 | Town12 | 79.89 | 100.0 | b | model failed DS 79.89; expert clean -> fixable model gap |
| 23687 | Town12 | 96.770791 | 100.0 | b | model failed DS 96.770791; expert clean -> fixable model gap |
| 23695 | Town13 | 60.0 | 100.0 | b | model failed DS 60.0; expert clean -> fixable model gap |
| 23910 | Town12 | 96.08 | 17.68 | c | model DS 96.08 & expert DS 17.68 both <100 -> structural ceiling candidate |
| 24041 | Town13 | 55.628204 | 100.0 | b | model failed DS 55.628204; expert clean -> fixable model gap |
| 24078 | Town12 | 60.0 | 100.0 | b | model failed DS 60.0; expert clean -> fixable model gap |
| 24098 | Town12 | 96.08 | 65.0 | c | model DS 96.08 & expert DS 65.0 both <100 -> structural ceiling candidate |
| 24206 | Town03 | 0.0 | None | a | model+expert both crash -> shared infra/benchmark |
| 24224 | Town02 | 50.0 | 100.0 | b | model failed DS 50.0; expert clean -> fixable model gap |
| 24759 | Town05 | None | 100.0 | a* | model crashed but expert ran (DS 100.0) -> harness/model-specific, not benchmark |
| 24816 | Town03 | 0.0 | None | a | model+expert both crash -> shared infra/benchmark |
| 25378 | Town03 | None | None | a | model+expert both crash -> shared infra/benchmark |
| 25381 | Town05 | None | 100.0 | a* | model crashed but expert ran (DS 100.0) -> harness/model-specific, not benchmark |
| 25854 | Town03 | 0.0 | None | a | model+expert both crash -> shared infra/benchmark |
| 25857 | Town05 | None | 100.0 | a* | model crashed but expert ran (DS 100.0) -> harness/model-specific, not benchmark |
| 25896 | Town03 | 0.0 | None | a | model+expert both crash -> shared infra/benchmark |
| 25955 | Town05 | None | 100.0 | a* | model crashed but expert ran (DS 100.0) -> harness/model-specific, not benchmark |
| 26393 | Town03 | None | None | a | model+expert both crash -> shared infra/benchmark |
| 26401 | Town06 | 60.0 | 100.0 | b | model failed DS 60.0; expert clean -> fixable model gap |
| 26435 | Town03 | 0.0 | None | a | model+expert both crash -> shared infra/benchmark |
| 26456 | Town03 | 0.0 | None | a | model+expert both crash -> shared infra/benchmark |
| 26950 | Town03 | 0.0 | None | a | model+expert both crash -> shared infra/benchmark |
| 26956 | Town05 | None | 100.0 | a* | model crashed but expert ran (DS 100.0) -> harness/model-specific, not benchmark |
| 26966 | Town05 | None | None | a | model+expert both crash -> shared infra/benchmark |
| 26990 | Town03 | 0.0 | None | a | model+expert both crash -> shared infra/benchmark |
| 27018 | Town15 | 60.0 | 30.222 | c | model DS 60.0 & expert DS 30.222 both <100 -> structural ceiling candidate |
| 27515 | Town03 | 0.0 | None | a | model+expert both crash -> shared infra/benchmark |
| 28035 | Town01 | 70.0 | 100.0 | b | model failed DS 70.0; expert clean -> fixable model gap |
| 28048 | Town02 | None | 100.0 | a* | model crashed but expert ran (DS 100.0) -> harness/model-specific, not benchmark |
| 28093 | Town04 | 30.86 | 100.0 | b | model failed DS 30.86; expert clean -> fixable model gap |
| 28330 | Town12 | 60.0 | 100.0 | b | model failed DS 60.0; expert clean -> fixable model gap |
