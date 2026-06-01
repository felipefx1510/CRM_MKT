class SummaryAgent:
    def __init__(self, ollama_service):
        self.ollama_service = ollama_service

    def run(self, lead):
        prompt = self._build_prompt(lead)
        return self.ollama_service.generate_summary(prompt)

    def _build_prompt(self, lead):
        return (
            "Voce e um assistente de CRM. Gere um resumo executivo curto, "
            "em ate 3 frases, sem inventar informacoes.\n\n"
            f"Nome: {lead.nome}\n"
            f"Empresa: {lead.empresa or 'Nao informado'}\n"
            f"Origem: {lead.origem}\n"
            f"Segmento: {lead.segmento or 'Nao informado'}\n"
            f"Interesse (urgencia): {lead.interesse}\n"
            f"Mensagem: {lead.mensagem or 'Nao informado'}\n"
            f"Score: {lead.score}\n"
            f"Classificacao: {lead.classificacao_score}\n"
            f"Status: {lead.status}\n\n"
            "Responda em portugues do Brasil e apenas com o resumo."
        )
