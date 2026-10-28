#!/usr/bin/env python3
"""W3 - a program outside the cluster that uses HDFS only as storage.

It talks to HDFS over HTTP (WebHDFS), the way the W1 scripts talked to MinIO.
Every request goes in two steps, as on the read diagram: first the NameNode,
which answers with the address of a DataNode (HTTP 307), then that DataNode,
which sends or receives the bytes.

Run it in the `client` container, which sits in the cluster network:
    docker compose -f compose-hdfs.yml run --rm client python /scripts/hdfs_client.py get /taxi/yellow_tripdata_2024-01.parquet
    docker compose -f compose-hdfs.yml run --rm client python /scripts/hdfs_client.py put /data/yellow_tripdata_2024-01.parquet /external/january.parquet
    docker compose -f compose-hdfs.yml run --rm client python /scripts/hdfs_client.py year

get and put are ready. The extra task fills in year(), marked TODO.
"""
import io
import sys
import urllib.error
import urllib.request

import pyarrow.parquet as pq

NAMENODE = "http://namenode:9870/webhdfs/v1"
USER = "hadoop"  # without it WebHDFS acts as the anonymous user dr.who, who may not write
YEAR = [f"/taxi/yellow_tripdata_2024-{m:02d}.parquet" for m in range(1, 13)]


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # we want to SEE the redirect, not follow it silently


_opener = urllib.request.build_opener(_NoRedirect)


def ask_namenode(path: str, op: str, method: str, extra: str = "") -> str:
    """Step 1: ask the NameNode. It answers with the address of a DataNode, not with data."""
    url = f"{NAMENODE}{path}?op={op}&user.name={USER}{extra}"
    try:
        _opener.open(urllib.request.Request(url, method=method))
    except urllib.error.HTTPError as e:
        if e.code == 307:
            location = e.headers["Location"]
            print("NameNode sent me to:", location.split("/webhdfs")[0])
            return location
        raise
    raise RuntimeError("expected a redirect to a DataNode")


def get(path: str) -> bytes:
    location = ask_namenode(path, "OPEN", "GET")
    with urllib.request.urlopen(location) as r:  # step 2: the bytes come from the DataNode
        return r.read()


def put(local_path: str, path: str) -> None:
    location = ask_namenode(path, "CREATE", "PUT", "&overwrite=true")
    with open(local_path, "rb") as f:
        body = f.read()
    req = urllib.request.Request(location, data=body, method="PUT")  # step 2
    with urllib.request.urlopen(req) as r:
        print(f"HTTP {r.status}, {len(body):,} B written to {path}")


def trip_distance(data: bytes):
    """Read one column of a Parquet file held in memory (column projection, as in W2)."""
    table = pq.read_table(io.BytesIO(data), columns=["trip_distance"])
    return table.column(0).to_pandas()


def year() -> None:
    """Mean trip distance of the whole year, one file at a time (the chunks of W2)."""
    # TODO (extra task): for each path in YEAR fetch the file with get(), take its column
    #       with trip_distance(), and add up the sum, the number of rows and the bytes.
    #       Print the three totals and the mean: total / rows, to 4 decimal places.
    #       Do not average the twelve monthly means: the months have different numbers of rows.
    raise NotImplementedError


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "get" and len(sys.argv) == 3:
        data = get(sys.argv[2])
        print(f"{len(data):,} B, mean trip_distance {trip_distance(data).mean():.4f}")
    elif cmd == "put" and len(sys.argv) == 4:
        put(sys.argv[2], sys.argv[3])
    elif cmd == "year":
        year()
    else:
        sys.exit(__doc__)
