# TMDB Trending: dynamic library matching and TV identity fix

## Why Doctor X did not appear

The Trending catalog is live: it fetches TMDB's current trending IDs, then queries the Telegram database on each catalog request for playable records with those IDs. The collection JSON does not store trending titles.

The supplied database record is currently identified as `Doctor White` (2022), TMDB ID `153751`, IMDb ID `tt17336482`. That identity does not match the newly added `Doctor X: Mafia in White` series (2026), which is listed as TMDB ID `293610`, IMDb ID `tt39328047`. Since Trending correctly matches canonical TMDB IDs, the record with ID `153751` cannot match the trending result for ID `293610`.

## Code fix

The TVDB and Cinemeta match thresholds were too permissive for series titles. A partial text overlap could match `Doctor X Mafia in White` to `Doctor White` and attach a new episode to the wrong parent series. Series-only matching now requires a score of at least `0.72`; movie matching thresholds are unchanged. The TMDB series search uses the same stricter threshold. TMDB trending IDs refresh every five minutes, while Telegram availability is rechecked on each catalog request.

## Correct the already-stored record

Deploy the updated project first, then use the existing metadata-rescan UI for the current record:

1. Open Media Management and edit the TV record with TMDB ID `153751` in `storage_1`.
2. Open **Rescan**, search for `Doctor X: Mafia in White`, and select the TMDB result with ID `293610` (IMDb `tt39328047`).
3. Apply the selection. The existing metadata-rescan implementation preserves the stored season/episode Telegram files while replacing the parent series metadata/identity. If the UI reports an existing target record, review that target before merging.
4. Open **Streaming Services → Trending Now → TMDB Trending (Series)** again. No collection JSON edit or re-import is needed; the catalog ID remains `trending_series`.

The back-end code cannot safely infer that an already-stored record with an incorrect TMDB/IMDb identity belongs to a different show. That existing record must be corrected once. Future uploads use the stricter series matching to prevent the same false match.
