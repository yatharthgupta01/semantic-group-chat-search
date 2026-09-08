"""Evaluation Benchmark Script.
Evaluates the semantic search pipeline against data/evaluation_queries.json.
Computes Recall@1, Recall@5, Recall@10, and Mean Reciprocal Rank (MRR) across
Semantic, Attributed, Temporal, and Zero-Overlap retrieval categories.
"""

import json
import time
import sys
from pathlib import Path

# Add project root to sys.path for direct execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import EVALUATION_QUERIES_FILE, DATA_DIR
from app.search import search_messages


def evaluate_search_engine(queries_path: Path = EVALUATION_QUERIES_FILE) -> dict:
    if not queries_path.exists():
        raise FileNotFoundError(f"Missing {queries_path}")

    with open(queries_path, "r", encoding="utf-8") as f:
        queries = json.load(f)

    total_queries = len(queries)
    print(f"Running evaluation benchmark on {total_queries} queries...\n")

    # Metrics storage by category
    categories = ["semantic", "attributed", "temporal", "zero_overlap", "overall"]
    category_metrics = {
        cat: {
            "count": 0,
            "r1": 0.0,
            "r5": 0.0,
            "r10": 0.0,
            "mrr": 0.0,
            "details": []
        }
        for cat in categories
    }

    start_time = time.time()

    for item in queries:
        qid = item["id"]
        qtext = item["query"]
        qcat = item["category"]
        ground_truth = set(item["ground_truth_ids"])

        res = search_messages(qtext, limit=10)
        retrieved = [r["id"] for r in res.get("results", [])]

        # Calculate rank of first relevant hit
        hit_rank = None
        for rank, msg_id in enumerate(retrieved, start=1):
            if msg_id in ground_truth:
                hit_rank = rank
                break

        r1 = 1.0 if (hit_rank is not None and hit_rank == 1) else 0.0
        r5 = 1.0 if (hit_rank is not None and hit_rank <= 5) else 0.0
        r10 = 1.0 if (hit_rank is not None and hit_rank <= 10) else 0.0
        rr = (1.0 / hit_rank) if hit_rank is not None else 0.0

        query_record = {
            "id": qid,
            "query": qtext,
            "category": qcat,
            "ground_truth": list(ground_truth),
            "retrieved_top3": retrieved[:3],
            "hit_rank": hit_rank,
            "r1": r1,
            "r5": r5,
            "r10": r10,
            "rr": round(rr, 4)
        }

        # Update category metrics
        for target_cat in [qcat, "overall"]:
            m = category_metrics[target_cat]
            m["count"] += 1
            m["r1"] += r1
            m["r5"] += r5
            m["r10"] += r10
            m["mrr"] += rr
            m["details"].append(query_record)

    elapsed = time.time() - start_time

    # Normalize metrics to averages
    summary_table = {}
    for cat in categories:
        cnt = category_metrics[cat]["count"]
        if cnt > 0:
            summary_table[cat] = {
                "count": cnt,
                "recall@1": round(category_metrics[cat]["r1"] / cnt, 4),
                "recall@5": round(category_metrics[cat]["r5"] / cnt, 4),
                "recall@10": round(category_metrics[cat]["r10"] / cnt, 4),
                "mrr": round(category_metrics[cat]["mrr"] / cnt, 4)
            }

    # Print clean benchmark report
    print("=" * 72)
    print("           SEMANTIC GROUP CHAT SEARCH EVALUATION REPORT            ")
    print("=" * 72)
    print(f"{'Category':<16} | {'Count':<5} | {'Recall@1':<9} | {'Recall@5':<9} | {'Recall@10':<9} | {'MRR':<6}")
    print("-" * 72)

    for cat in ["semantic", "attributed", "temporal", "zero_overlap", "overall"]:
        s = summary_table[cat]
        title = cat.replace("_", " ").title() if cat != "overall" else "OVERALL"
        print(f"{title:<16} | {s['count']:<5} | {s['recall@1']*100:>7.1f}% | {s['recall@5']*100:>7.1f}% | {s['recall@10']*100:>8.1f}% | {s['mrr']:>6.3f}")

    print("=" * 72)
    print(f"Benchmark executed in {elapsed:.2f}s ({elapsed/total_queries:.3f}s per query)")

    # Save detailed evaluation report
    out_file = DATA_DIR / "evaluation_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "summary": summary_table,
            "total_queries": total_queries,
            "elapsed_seconds": round(elapsed, 2),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "details": category_metrics["overall"]["details"]
        }, f, indent=2, ensure_ascii=False)

    print(f"Detailed benchmark results saved to: {out_file}")
    return summary_table


if __name__ == "__main__":
    evaluate_search_engine()
