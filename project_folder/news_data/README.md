# news_data (Shared News Layer)

This folder is the single shared source for stock news used by all tasks.

## One-time fetch workflow
1. Run `project_folder/news_data/implementation/01_News_Data_Ingestion.ipynb`.
2. It writes one canonical file:
   - `project_folder/news_data/data/news_headlines_raw.csv`
3. Other notebooks should only read this canonical CSV.

## Date window behavior
- Default window in `price_aligned` mode:
  - start date = `min(price_date) - NEWS_BUFFER_DAYS`
  - end date = `max(price_date)`
- Default `NEWS_BUFFER_DAYS = 30`.
- You can change to `10` if needed.

## Notes
- Shared-only mode is enabled in ingestion:
  - no local cache fallback from task folders
  - no synthetic proxy fallback rows
- If the canonical CSV is missing, rerun the ingestion notebook once.
