"""
bedrock_rag.py — Minimal RAG loop on Amazon Bedrock.

Flow: retrieve context from a Bedrock Knowledge Base, then call a
foundation model with the retrieved context (converse API).

Prereqs:
    pip install boto3
    aws configure            # credentials with bedrock:InvokeModel + Retrieve

Usage:
    python bedrock_rag.py --kb-id ABC123XYZ --query "What is our refund policy?"
    python bedrock_rag.py --query "Hello!"   # no KB -> plain Bedrock call
"""

import argparse
import boto3

REGION = "us-east-1"
MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"  # swap freely on Bedrock

SYSTEM_PROMPT = (
    "You are a helpful support assistant. Answer ONLY from the provided "
    "context. If the answer is not in the context, say you don't know."
)


def retrieve(kb_id: str, query: str, n: int = 4) -> str:
    """Pull top-n chunks from a Bedrock Knowledge Base."""
    agent = boto3.client("bedrock-agent-runtime", region_name=REGION)
    resp = agent.retrieve(
        knowledgeBaseId=kb_id,
        retrievalQuery={"text": query},
        retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": n}},
    )
    chunks = [r["content"]["text"] for r in resp.get("retrievalResults", [])]
    return "\n\n---\n\n".join(chunks)


def ask(question: str, context: str = "") -> str:
    """Call Bedrock with optional RAG context."""
    bedrock = boto3.client("bedrock-runtime", region_name=REGION)
    user_msg = f"Context:\n{context}\n\nQuestion: {question}" if context else question
    resp = bedrock.converse(
        modelId=MODEL_ID,
        system=[{"text": SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": [{"text": user_msg}]}],
        inferenceConfig={"maxTokens": 512, "temperature": 0.2},
    )
    out = resp["output"]["message"]["content"]
    usage = resp.get("usage", {})
    print(f"[tokens in={usage.get('inputTokens')} out={usage.get('outputTokens')}]")
    return "".join(b.get("text", "") for b in out)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--kb-id", default="", help="Bedrock Knowledge Base ID")
    p.add_argument("--query", required=True)
    args = p.parse_args()

    context = ""
    if args.kb_id:
        print("Retrieving context…")
        context = retrieve(args.kb_id, args.query)
        print(f"Got {len(context)} chars of context.\n")

    print(ask(args.query, context))


if __name__ == "__main__":
    main()
