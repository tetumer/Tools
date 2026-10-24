import os, json
import numpy as np
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
SIM_THRESHOLD = 0.55   # channels closer than this = same cluster

def get_youtube():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def fetch_subscriptions(yt):
    subs, token = [], None
    while True:
        res = yt.subscriptions().list(part="snippet", mine=True,
                                      maxResults=50, pageToken=token).execute()
        subs += res["items"]
        token = res.get("nextPageToken")
        if not token: break
    return [(s["snippet"]["resourceId"]["channelId"], s["snippet"]["title"]) for s in subs]

def fetch_descriptions(yt, ids):
    info = {}
    for i in range(0, len(ids), 50):
        res = yt.channels().list(part="snippet", id=",".join(ids[i:i+50])).execute()
        for ch in res["items"]:
            info[ch["id"]] = ch["snippet"].get("description", "")
    return info

def clusterize(sim):
    n = sim.shape[0]
    assigned, clusters = -np.ones(n, dtype=int), []
    for i in range(n):
        if assigned[i] != -1: continue
        members = [j for j in range(n) if assigned[j] == -1 and sim[i, j] >= SIM_THRESHOLD]
        if not members: members = [i]
        cid = len(clusters)
        clusters.append(members)
        for m in members: assigned[m] = cid
    return assigned, clusters

def main():
    yt = get_youtube()
    subs = fetch_subscriptions(yt)
    print(f"{len(subs)} subscriptions found.")
    descs = fetch_descriptions(yt, [c[0] for c in subs])
    texts = [f"{t}. {descs.get(i,'')[:500]}" for i, t in subs]

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embs = model.encode(texts, show_progress_bar=True)
    sim = cosine_similarity(embs)
    np.fill_diagonal(sim, 1.0)

    labels, clusters = clusterize(sim)
    order = sorted(range(len(clusters)), key=lambda c: -len(clusters[c]))

    print(f"\n{len(clusters)} clusters formed. Label each: k=keep r=review x=kick s=skip\n")
    verdict_map = {}
    for rank, cid in enumerate(order, 1):
        members = clusters[cid]
        names = [subs[m][1] for m in members]
        print(f"[{rank}/{len(clusters)}] Cluster {cid} ({len(members)} channels)")
        for n in names[:6]: print(f"   - {n}")
        if len(names) > 6: print(f"   ... and {len(names)-6} more")
        v = input("   verdict (k/r/x/s): ").strip().lower()
        if v in ("k", "r", "x"):
            verdict_map[cid] = {"keep": "keep", "r": "review", "x": "kick"}[v]

    rows = []
    for m, (ch_id, title) in enumerate(subs):
        cid = labels[m]
        v = verdict_map.get(cid)
        rows.append({"channel": title,
                     "cluster": cid,
                     "cluster_size": len(clusters[cid]),
                     "verdict": v if v else "skipped"})
    df = pd.DataFrame(rows)
    df.to_csv("verdicts.csv", index=False)
    with open("cluster_labels.json", "w") as f:
        json.dump({str(k): v for k, v in verdict_map.items()}, f)
    print(f"\nSaved verdicts.csv and cluster_labels.json")
    print(df["verdict"].value_counts())

if __name__ == "__main__":
    main()