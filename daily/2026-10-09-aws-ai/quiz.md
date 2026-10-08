# 🧠 Quiz — AI Architecture on AWS (5 min)

**1. You need a chatbot over company docs, live next week, no ML team. Pick one:**
A. Train a model on SageMaker
B. Bedrock + RAG (S3 + OpenSearch + Lambda)
C. Rekognition
D. Self-host Llama on EC2 GPUs

<details><summary>Answer</summary>B — RAG on Bedrock needs no training and ships in days. A/D are weeks of work; C is image analysis, wrong tool.</details>

**2. In the RAG pattern, what does OpenSearch Serverless actually store?**
A. The PDF files
B. Chat history
C. Vector embeddings of chunked documents
D. Model weights

<details><summary>Answer</summary>C — S3 keeps the source files, DynamoDB keeps chat history, Bedrock hosts the model. OpenSearch holds the vectors for semantic retrieval.</details>

**3. Your SageMaker endpoint costs $400/month but only serves traffic 9-to-5. Cheapest fix?**
A. Bigger instance
B. Switch to Serverless Inference or scheduled autoscaling to zero
C. Add CloudFront
D. Move to Bedrock

<details><summary>Answer</summary>B — Endpoints bill per instance-hour even idle. Serverless Inference (or scale-to-zero) kills the idle cost. D changes the architecture entirely — valid but not the cheapest fix.</details>

**4. A Lambda needs Bedrock access. Best IAM practice?**
A. One shared admin role for all Lambdas
B. `bedrock:InvokeModel` scoped to specific model ARNs, per-function role
C. Hardcode access keys in the Lambda env vars
D. `bedrock:*` on `*`

<details><summary>Answer</summary>B — Least privilege per function. A/D are incident generators; C is a security horror story.</details>

**5. Which combo handles "process 10,000 invoices overnight" best?**
A. API Gateway → Lambda → Bedrock, synchronous
B. S3 → EventBridge → Lambda → Textract → Comprehend → DynamoDB, with SQS buffers + DLQs
C. SageMaker real-time endpoint
D. Polly

<details><summary>Answer</summary>B — Async, event-driven pipeline with queues absorbs the burst and survives flaky steps. A would time out; C is for real-time; D turns text into speech.</details>

---

_Score: 5/5 — ship it. 3-4 — re-read section 5. Below 3 — re-read the whole guide, it's only 15 minutes._ ☁️
