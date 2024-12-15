SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

SELECT COUNT(*) AS row_count FROM table_name;
SELECT COUNT(*) AS row_count FROM tokens;

CREATE INDEX ON passages USING hnsw (embedding vector_l2_ops);

SELECT ndims(embedding) AS vector_length FROM passages LIMIT 10;

SELECT extname FROM pg_extension;

\d passages

SELECT passages.id,passages.user_id,passages.text,passages.doc_id,passages.agent_id,passages.source_id,passages.embedding_config,passages.metadata_,passages.created_at FROM passages LIMIT 1;

SELECT passages.id,passages.user_id,passages.doc_id,passages.agent_id,passages.source_id,passages.embedding_config,passages.metadata_ FROM passages LIMIT 1;

SELECT passages.text, passages.created_at FROM passages LIMIT 1;

Updated record with id passage-40b384f4-bcfb-fb6f-d3ff-7487315e217e
SELECT passages.id, passages.text FROM passages WHERE passages.id='passage-40b384f4-bcfb-fb6f-d3ff-7487315e217e';
DELETE FROM passages WHERE passages.id='passage-40b384f4-bcfb-fb6f-d3ff-7487315e217e';

SELECT messages.id, messages.text FROM messages WHERE messages.id='message-4182638a-5767-42dd-ae94-ce07b62aef51';
DELETE FROM messages WHERE messages.id='message-4182638a-5767-42dd-ae94-ce07b62aef51';

SELECT messages.text, messages.created_at FROM messages ORDER BY created_at DESC LIMIT 3;

DELETE FROM passages;
DELETE FROM messages;

SELECT passages.id FROM passages;

psql -h localhost -p 8888 -U yzhao862 -d doc_qa
curl -X GET "http://localhost:8080/question" -H "Content-Type: application/json"   -d '{"q": "实习生协议"}'
curl -X POST "http://0.0.0.0:8080/uploadfiles/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "files=@/home/yzhao862/MemGPT/paper_experiments/doc_qa_task/test_files/1.txt"

{\"object\":\"page\",\"data\":[{\"object\": \"bucket\",\"start_time\": 1730419200,\"end_time\": 1730505600,\"results\": [{\"object\": \"organization.usage.embeddings.result\",\"input_tokens\": 16,\"num_model_requests\": 2,\"project_id\": null,\"user_id\": null,\"api_key_id\": null,\"model\": null}]}],\"has_more\": false,\"next_page\":null}
