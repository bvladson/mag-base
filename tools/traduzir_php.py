"""Traduz as mensagens fixas em inglês do PHP que chegam ao usuário (avisos e respostas).

Troca o literal entre aspas (simples ou duplas) nos arquivos indicados; ignora ferramentas de IA
(Tools/) e OIDC, que não são usadas. Idempotente. Uso: python traduzir_php.py
"""
import shutil
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
OVERLAY = TOOLS.parent / 'overlay'
ORIGINAL = Path(r'C:\Users\VLADSON\Downloads\Leantime-v3.10.0')

MENSAGENS = {
    'app/Domain/Calendar/Controllers/Export.php': {
        'There was a problem generating the ical hash': 'Houve um problema ao gerar o link do calendário',
        'Could not find ical URL': 'Não foi possível encontrar o link do calendário',
    },
    'app/Domain/Connector/Controllers/Integration.php': {
        'Entity not set': 'Entidade não definida',
        'There was a problem with the import ': 'Houve um problema na importação ',
    },
    'app/Domain/Install/Controllers/Update.php': {
        'There was a problem updating your database. Please check your error logs to verify your database is up to date.':
            'Houve um problema ao atualizar o banco de dados. Verifique os logs de erro para confirmar se ele está atualizado.',
    },
    'app/Domain/Sprints/Controllers/EditSprint.php': {
        'Sprint edited successfully': 'Sprint atualizada com sucesso',
        'There was a problem saving the sprint': 'Houve um problema ao salvar a sprint',
        'Sprint created successfully.': 'Sprint criada com sucesso.',
    },
    'app/Domain/Tickets/Controllers/ShowKanban.php': {
        'Task created: ': 'Tarefa criada: ',
    },
    'app/Domain/Tickets/Services/Tickets.php': {
        'Headline Missing': 'Título obrigatório',
        'You are not allowed to edit this milestone.': 'Você não tem permissão para editar este marco.',
        'You are not allowed to move this milestone to that project.': 'Você não tem permissão para mover este marco para esse projeto.',
        'Could not move milestone to the new project.': 'Não foi possível mover o marco para o novo projeto.',
    },
    'app/Domain/Timesheets/Controllers/ShowMy.php': {
        'Could not parse date': 'Data inválida',
    },
    'app/Domain/Timesheets/Services/Timesheets.php': {
        'Task ID is required for new entries': 'Informe a tarefa para novos lançamentos',
        'Timesheet saved successfully': 'Horas salvas com sucesso',
        'Error logging time: ': 'Erro ao registrar horas: ',
    },
    'app/Domain/Users/Controllers/PatchUserSettings.php': {
        'Not authorized': 'Não autorizado',
        'Invalid request': 'Requisição inválida',
    },
    'app/Domain/Wiki/Hxcontrollers/ArticleContent.php': {
        'Failed to save': 'Não foi possível salvar',
    },
}


def main():
    for rel, pares in MENSAGENS.items():
        destino = OVERLAY / rel
        if not destino.exists():
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ORIGINAL / rel, destino)
        s = destino.read_text(encoding='utf-8')
        original = s
        for en, pt in pares.items():
            trocou = False
            for q in ("'", '"'):
                if q + en + q in s:
                    novo = pt.replace("'", "\\'") if q == "'" else pt
                    s = s.replace(q + en + q, q + novo + q)
                    trocou = True
            if not trocou and pt not in s and pt.replace("'", "\\'") not in s:
                raise SystemExit(f'{rel}: mensagem não encontrada: {en!r}')
        if s != original:
            destino.write_bytes(s.encode('utf-8'))
        print(('alterado ' if s != original else 'sem mudanças ') + rel)


if __name__ == '__main__':
    main()
