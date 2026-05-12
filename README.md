# ole-backend

Python pipeline + FastAPI for the OLE Analyzer module inside IE Pulse.

## Folder structure

```
ole-backend/
├── data/
│   ├── raw/          ← place SMH .xls files here
│   └── mart/         ← parquet outputs (auto-generated)
├── pipeline/
│   ├── ingest.py     ← normalise MES + eTMS CSVs + SMH files → parquet
│   ├── compute.py    ← DuckDB JOIN + OLE calculation → ole_computed.parquet
│   └── refresh.py    ← entry point: runs ingest then compute
├── api/
│   └── main.py       ← FastAPI app
├── config.py         ← all paths, workcell config, constants
├── requirements.txt
└── README.md
```

## Setup

```bash
cd C:\Users\4033375\Projects\OLE ANALYZER\ole-backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## SMH files

Place the SMH XLS files in `data/raw/`:

```
data/raw/
├── ASP_SMH.xls
├── AOP1_SMH.xls
├── KEYSIGHT_PCA_SMH.xls
└── KEYSIGHT_HLA_SMH.xls
```

## Run the pipeline

```bash
# From ole-backend root
python pipeline/refresh.py
```

This will:
1. Read CSVs from \\penhomev10\OLE (last 7 days)
2. Read SMH files from data/raw/
3. Normalise and write 3 parquet files to data/mart/
4. Run DuckDB JOINs and compute OLE
5. Write ole_computed.parquet to data/mart/

## Start the API

```bash
python api/main.py
```

API runs at http://localhost:8000

## API endpoints

| Method | Endpoint            | Description                        |
|--------|---------------------|------------------------------------|
| GET    | /api/health         | Check mart status                  |
| GET    | /api/workcells      | Workcell config reference          |
| GET    | /api/ole            | OLE results (filterable)           |
| GET    | /api/ole/summary    | Per-workcell OLE summary           |
| GET    | /api/production     | Raw MES production data            |
| GET    | /api/paid-hours     | Raw eTMS paid hours data           |
| GET    | /api/smh            | SMH lookup table                   |
| POST   | /api/refresh        | Trigger full pipeline refresh      |

Interactive docs: http://localhost:8000/docs

## Workcell config

Defined in `config.py`. Each workcell maps to its final scan stage:

| Workcell     | Final Scan Stage | SMH Column used     |
|--------------|------------------|---------------------|
| ASP          | Backend          | SMH/ Unit - Backend |
| AOP1         | SMT              | SMH/ Unit - SMT     |
| KEYSIGHT PCA | SMT              | SMH/ Unit - SMT     |
| KEYSIGHT HLA | BoxBuild         | SMH/ Unit - BoxBuild|

To add a new workcell, add one entry to `WORKCELL_CONFIG` and one entry
to `SMH_FILES` in config.py. No other changes needed.
