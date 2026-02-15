# Trabalho Laboratório Prático: AI Code Reviewer com GitHub Actions

**Curso:** MBA Engenharia de Software
**Disciplina:** AI Driven Development
**Professor:** Luiz Gustavo dos Santos Real
**Aluno:** Alexandre Garcia Macedo
**RM:** 363454

---

## 1. Links

*   **Repositório:** https://github.com/alemacedo/gnews
*   **Pull Request com a Análise:** https://github.com/alemacedo/gnews/pull/1
*   **Workflow Run:** https://github.com/alemacedo/gnews/actions/runs/22039459859

---

## 2. Análise Crítica

### Precisão da IA
**A IA conseguiu detectar o SQL Injection?**
> Sim, a IA foi capaz de identificar exatamente o ponto de falha inserido no código e classificou corretamente o tipo. Ela apontou corretamente para a linha 126 do código em `ArticleService.java`.

### Didática
**O comentário explicou o risco e sugeriu correções?**
> Sim. Explicou que é um risco classificado com o TOP10 OWASP e citou o uso de PreparedStatement para aplicar uma correção.

### Falsos Positivos
**Ela criticou algo que na verdade estava correto?**
> Não.

---

## 3. Detalhes da Implementação Técnica

Para viabilizar este laboratório com o modelo **Gemini**, foram realizadas as seguintes adaptações no projeto original:

1.  **Script Customizado em Python**:
    *   Criação do script `.github/scripts/ai_reviewer.py` para substituir a Action de terceiros limitadas.
    *   O script utiliza a biblioteca oficial `google-generativeai` do Google.

2.  **Estratégia de Modelos (Fallback)**:
    *   Foi implementada uma lógica que tenta conectar em múltiplos modelos sequencialmente (`gemini-2.0-flash`, `gemini-2.5-flash`, `gemini-flash-latest`, etc.) para garantir que a revisão ocorra mesmo se uma versão específica estiver indisponível na chave de API.

3.  **Prompt de Segurança**:
    *   Foi configurado um prompt específico para atuar como *Engenheiro de DevSecOps*, focando estritamente no OWASP Top 10 e ignorando problemas menores de formatação.

---


## 2. Evidências da Análise

* Relatório da AI Review:





* Status de Pull Request



