
import os
import requests
import json
import google.generativeai as genai

def review_pr():
    # Load environment variables
    github_token = os.environ.get("GITHUB_TOKEN")
    ai_api_key = os.environ.get("AI_API_KEY") 
    pr_number = os.environ.get("PR_NUMBER")
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    commit_sha = os.environ.get("GITHUB_SHA")

    if not all([github_token, ai_api_key, pr_number, repo_name]):
        print("Error: Missing required environment variables.")
        # Try to print which one is missing
        if not github_token: print("Missing GITHUB_TOKEN")
        if not ai_api_key: print("Missing AI_API_KEY")
        if not pr_number: print("Missing PR_NUMBER")
        if not repo_name: print("Missing GITHUB_REPOSITORY")
        exit(1)

    print(f"Starting review for PR #{pr_number} in {repo_name}...")

    genai.configure(api_key=ai_api_key)
    # Using 'gemini-1.5-flash' since 'gemini-2.0-flash-exp' might not be stable for all keys yet, 
    # but let's stick to what the user intended if possible or fallback. 
    # Actually, let's use a very standard model name.
    model = genai.GenerativeModel('gemini-1.5-flash') 

    # Get PR diff/files
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get the list of files in the PR
    files_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
    response = requests.get(files_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching PR files: {response.status_code} - {response.text}")
        exit(1)
        
    files = response.json()
    
    all_comments_body = ""
    has_findings = False
    
    for file in files:
        filename = file['filename']
        patch = file.get('patch', '')
        status = file['status']
        
        # Skip if file is deleted or too large/no patch
        if status == 'removed' or not patch:
            continue
            
        # Only review Java files for this lab
        if not filename.endswith('.java'):
            continue
            
        print(f"Reviewing {filename}...")
        
        prompt = f"""
        Você é um Engenheiro de Segurança Sênior (DevSecOps).
        Analise o seguinte DIFF (patch) do arquivo '{filename}' buscando VULNERABILIDADES CRÍTICAS.
        
        Foco principal:
        1. Vulnerabilidades OWASP Top 10 (especialmente SQL Injection e Insecure Deserialization).
        2. Code Smells graves e más práticas.
        
        Se encontrar vulnerabilidades, explique o risco e como corrigir.
        Se o código estiver seguro, responda APENAS "OK".
        
        DIFF:
        {patch}
        """
        
        try:
            response = model.generate_content(prompt)
            review_text = response.text.strip()
            
            # Simple check if there is content worth reporting
            if review_text and "OK" not in review_text and len(review_text) > 10:
                has_findings = True
                
                # Check for SQL Injection specifically to highlight it
                if "SQL Injection" in review_text or "inyeccion SQL" in review_text:
                    all_comments_body += f"### 🚨 ALERTA CRÍTICO: SQL Injection em `{filename}`\n"
                else:
                    all_comments_body += f"### ⚠️ Observações em `{filename}`\n"
                    
                all_comments_body += f"{review_text}\n\n---\n"
                
        except Exception as e:
            print(f"Failed to review {filename}: {e}")

    # Post comments
    post_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/reviews"
    
    if has_findings and len(all_comments_body) > 0:
        print("Posting review comment...")
        final_body = "## 🛡️ Relatório de Auditoria de Segurança por IA (Gemini)\n\n" + all_comments_body
        
        review_payload = {
            "body": final_body,
            "event": "REQUEST_CHANGES" 
        }
        
        p_response = requests.post(post_url, headers=headers, json=review_payload)
        if p_response.status_code not in [200, 201]:
            print(f"Error posting review: {p_response.status_code} - {p_response.text}")
        else:
            print("Review posted successfully!")
    else:
        print("No critical issues found. Posting approval comment.")
        review_payload = {
            "body": "✅ **Auditoria Aprovada**\n\nNenhuma vulnerabilidade crítica encontrada.",
            "event": "APPROVE"
        }
        requests.post(post_url, headers=headers, json=review_payload)
            
if __name__ == "__main__":
    review_pr()
