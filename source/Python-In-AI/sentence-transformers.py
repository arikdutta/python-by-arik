from sentence_transformers import SentenceTransformer, util
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

script_dir = os.path.dirname(os.path.abspath(__file__))

job_desc_path = os.path.join(script_dir, "job_description.txt")
resume_path = os.path.join(script_dir, "resume.txt")

if not os.path.exists(job_desc_path):
    raise FileNotFoundError(f"Missing file: {job_desc_path}")
if not os.path.exists(resume_path):
    raise FileNotFoundError(f"Missing file: {resume_path}")

with open(job_desc_path) as f:
    job_desc = f.read()

with open(resume_path) as f:
    resume = f.read()

emb_job = model.encode(job_desc, convert_to_tensor=True)
emb_resume = model.encode(resume, convert_to_tensor=True)

similarity = util.cos_sim(emb_job, emb_resume)
print("Match score:", similarity.item())
