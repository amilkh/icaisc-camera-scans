"""Consolidate code4fukui camera data at a pinned commit into parquet.

Reads the data repo with `git archive` (no checkout needed) and writes
data/{level}_{site}_{class}.parquet for level in {5min, daily}.
"""
import io, subprocess, sys, tarfile
from collections import defaultdict
from pathlib import Path
import pandas as pd

import os
COMMIT = "b89bc2ce26743f08e54468cbf33081dd30a3965f"
OUT = Path(__file__).resolve().parent.parent / "data"
URL = "https://github.com/code4fukui/fukui-kanko-people-flow-data.git"
# A local clone (PF_REPO or ~/active/...) is used if present; otherwise the repo is
# cloned bare into data/pf_repo so a fresh checkout can reproduce everything.
REPO = Path(os.environ.get("PF_REPO", Path.home() / "active/fukui-kanko-people-flow-data"))


def ensure_repo():
    global REPO
    if (REPO / ".git").exists() or (REPO / "HEAD").exists():
        return
    REPO = OUT / "pf_repo"
    if not (REPO / "HEAD").exists():
        subprocess.run(["git", "clone", "--bare", "--quiet", URL, str(REPO)], check=True)
    if subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", COMMIT], capture_output=True).returncode:
        subprocess.run(["git", "-C", str(REPO), "fetch", "--quiet", "origin"], check=True)


def main():
    OUT.mkdir(exist_ok=True)
    ensure_repo()
    proc = subprocess.Popen(["git", "-C", str(REPO), "archive", COMMIT, "full", "hourly"],
                            stdout=subprocess.PIPE)
    parts = defaultdict(list)
    with tarfile.open(fileobj=proc.stdout, mode="r|") as tar:
        for m in tar:
            if not m.isfile() or not m.name.endswith(".csv"):
                continue
            p = m.name.split("/")
            level = "daily" if p[0] == "full" else "5min"
            site = p[1]
            cls = p[2].removesuffix(".csv")
            parts[(level, site, cls)].append(tar.extractfile(m).read())
    for (level, site, cls), blobs in sorted(parts.items()):
        df = pd.concat([pd.read_csv(io.BytesIO(b)) for b in blobs], ignore_index=True)
        df = df.rename(columns={"aggregate from": "t0", "aggregate to": "t1", "total count": "count"})
        df["t0"] = pd.to_datetime(df["t0"]); df["t1"] = pd.to_datetime(df["t1"])
        df = df.drop(columns=["placement", "object class"]).sort_values("t0")
        dups = df.duplicated("t0").sum()
        df = df.drop_duplicates("t0", keep="last")
        df.to_parquet(OUT / f"{level}_{site}_{cls}.parquet", index=False)
        print(f"{level:6} {site:34} {cls:13} rows={len(df):7} dups={dups:5} "
              f"{df.t0.min():%Y-%m-%d} to {df.t0.max():%Y-%m-%d} total={df['count'].sum():,}")
    proc.wait()
    (OUT / "COMMIT").write_text(COMMIT + "\n")


if __name__ == "__main__":
    sys.exit(main())
