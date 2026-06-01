import json
import logging


class ToolDefinition:
    def __init__(self, name, description, parameters, handler):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.handler = handler

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class SupervisorAgent:
    def __init__(
        self,
        ollama_service,
        lead_repository,
        summary_agent,
        followup_agent,
        max_steps=4,
    ):
        self.ollama_service = ollama_service
        self.lead_repository = lead_repository
        self.summary_agent = summary_agent
        self.followup_agent = followup_agent
        self.max_steps = max_steps
        self.logger = logging.getLogger(__name__)
        self.tools = self._build_tools()
        self.tool_map = {tool.name: tool for tool in self.tools}

    def run(self, user_message):
        history = []
        for _ in range(self.max_steps):
            prompt = self._build_prompt(user_message, history)
            raw = self.ollama_service.generate_text(prompt)
            data = self._parse_json(raw)
            if not isinstance(data, dict):
                return self._fallback_response()

            final = data.get("final")
            if isinstance(final, str) and final.strip():
                return final.strip()

            tool_calls = data.get("tool_calls", [])
            if not isinstance(tool_calls, list) or not tool_calls:
                return self._fallback_response()

            observations = []
            for call in tool_calls:
                observations.append(self._execute_tool_call(call))
            history.append({
                "tool_calls": tool_calls,
                "observations": observations,
            })

        return (
            "Nao consegui concluir a solicitacao dentro do limite de passos. "
            "Tente detalhar o pedido."
        )

    def _build_tools(self):
        return [
            ToolDefinition(
                name="buscar_lead_por_id",
                description="Busca um lead pelo ID e retorna os dados basicos.",
                parameters={
                    "type": "object",
                    "properties": {
                        "lead_id": {
                            "type": "integer",
                            "description": "ID do lead",
                        }
                    },
                    "required": ["lead_id"],
                },
                handler=self._tool_buscar_lead,
            ),
            ToolDefinition(
                name="gerar_resumo_lead",
                description="Gera um resumo executivo curto para um lead.",
                parameters={
                    "type": "object",
                    "properties": {
                        "lead_id": {
                            "type": "integer",
                            "description": "ID do lead",
                        }
                    },
                    "required": ["lead_id"],
                },
                handler=self._tool_gerar_resumo,
            ),
            ToolDefinition(
                name="gerar_followup_lead",
                description=(
                    "Cria uma mensagem de follow-up personalizada. "
                    "Use instrucoes para pedidos como desconto."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "lead_id": {
                            "type": "integer",
                            "description": "ID do lead",
                        },
                        "variacao": {
                            "type": "string",
                            "description": "Opcional. Ex: '1' ou 'A'",
                        },
                        "instrucoes": {
                            "type": "string",
                            "description": "Detalhes adicionais da mensagem",
                        },
                    },
                    "required": ["lead_id"],
                },
                handler=self._tool_gerar_followup,
            ),
        ]

    def _build_prompt(self, user_message, history):
        tools_json = json.dumps(
            [tool.to_dict() for tool in self.tools],
            ensure_ascii=True,
            indent=2,
        )
        history_json = json.dumps(history, ensure_ascii=True, indent=2)
        return (
            "Voce e o agente orquestrador do CRM."
            "\nSempre responda em portugues do Brasil."
            "\nNao revele raciocinio interno."
            "\nSe faltar informacao (ex: lead_id), responda pedindo o que falta."
            "\n\nFerramentas disponiveis (JSON):\n"
            f"{tools_json}"
            "\n\nFormato de resposta (apenas JSON):"
            "\n{\"tool_calls\":[{\"name\":\"NOME\",\"arguments\":{...}}]}"
            "\nou"
            "\n{\"final\":\"...\"}"
            "\n\nHistorico de execucao:\n"
            f"{history_json}"
            "\n\nPedido do usuario: "
            f"{user_message}"
        )

    def _execute_tool_call(self, call):
        if not isinstance(call, dict):
            return {"erro": "Chamada de ferramenta invalida."}

        name = call.get("name")
        args = call.get("arguments")
        if not isinstance(args, dict):
            args = {}

        tool = self.tool_map.get(name)
        if not tool:
            return {"erro": f"Ferramenta desconhecida: {name}"}

        try:
            result = tool.handler(args)
        except Exception:
            self.logger.exception("Tool execution failed: %s", name)
            return {"tool": name, "erro": "Falha ao executar ferramenta."}

        return {"tool": name, "result": result}

    def _tool_buscar_lead(self, args):
        lead, error = self._get_lead_from_args(args)
        if error:
            return {"erro": error}
        return lead.to_dict()

    def _tool_gerar_resumo(self, args):
        lead, error = self._get_lead_from_args(args)
        if error:
            return {"erro": error}
        resumo = self.summary_agent.run(lead)
        if not resumo:
            return {"erro": "Resumo vazio."}
        return {"resumo": resumo}

    def _tool_gerar_followup(self, args):
        lead, error = self._get_lead_from_args(args)
        if error:
            return {"erro": error}
        variacao = args.get("variacao")
        instrucoes = args.get("instrucoes")
        mensagem = self.followup_agent.run(
            lead,
            variation=variacao,
            extra_instruction=instrucoes,
        )
        if not mensagem:
            return {"erro": "Mensagem vazia."}
        return {"mensagem": mensagem}

    def _get_lead_from_args(self, args):
        lead_id = args.get("lead_id")
        if lead_id is None:
            return None, "lead_id obrigatorio."

        try:
            lead_id = int(lead_id)
        except (TypeError, ValueError):
            return None, "lead_id invalido."

        lead = self.lead_repository.get_by_id(lead_id)
        if not lead:
            return None, "Lead nao encontrado."

        return lead, None

    def _parse_json(self, text):
        if not text:
            return {}
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            extracted = self._extract_json(text)
            if extracted:
                try:
                    return json.loads(extracted)
                except json.JSONDecodeError:
                    return {}
            return {}

    def _extract_json(self, text):
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return ""
        return text[start:end + 1]

    def _fallback_response(self):
        return (
            "Nao consegui concluir a solicitacao. "
            "Tente reformular com mais detalhes (ex: inclua o ID do lead)."
        )
