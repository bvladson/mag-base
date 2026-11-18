"""Gera overlay/custom/Language/{pt-BR,en-US}.ini — textos sem a marca Leantime.

O Leantime carrega, nesta ordem: en-US.ini, custom/en-US.ini (vale para todos os idiomas
como complemento), <idioma>.ini e custom/<idioma>.ini. Aqui só entram as chaves alteradas.

Cada chave recebe um valor inteiro (str) ou uma lista de trocas exatas sobre o valor
original (tuplas antigo→novo), o que preserva o escape de aspas do INI. Ao final o script
falha se sobrar "leantime" em algum valor gerado.
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ORIGINAL = Path(r'C:\Users\VLADSON\Downloads\Leantime-v3.10.0\app\Language')
DESTINO = BASE / 'overlay' / 'custom' / 'Language'

BOTAO_ANTIGO = 'background: #006d9f;'
BOTAO_MAG = 'background: #A61915;'

PT = {
    'headlines.welcome': '"Bem-vindo!"',
    'headlines.welcome_to_leantime': '"Bem-vindo ao sistema MAG!"',
    'text.welcome_to_leantime': '"Você foi convidado para colaborar em um projeto no sistema MAG. Antes de começar, crie sua senha."',
    'text.here_are_news': '"Novidades dos seus projetos"',
    'text.my_timesheets_helper_content': [('Horas extras no leantime pode ajudar', 'Horas extras registradas no sistema podem ajudar')],
    'text.show_projects_helper_content': [('coração do seu negócio e do leantime!', 'coração do seu negócio!')],
    'text.new_db_version': [('Para usar o Leantime', 'Para usar o sistema')],
    'text.ical_export_description': [('seu calendário Leantime', 'seu calendário do sistema')],
    'text.helpful_resources': [('tornar o Leantime o mais simples', 'tornar o sistema o mais simples')],
    'text.documentation': [('o uso do Leantime', 'o uso do sistema')],
    'label.connect_calendar_description': [('reuniões do Leantime', 'reuniões do sistema')],
    'label.more_integrations_hint': '"Outras integrações de calendário poderão ser adicionadas ao sistema."',
    'label.send_telemetry': '"Envio de dados anônimos de uso"',
    'label.telemetry_background': '"O envio de dados de uso para fora da MAG está desativado neste servidor."',
    'label.open_in_leantime': '"Abrir no sistema"',
    'email_notifications.new_user_subject': '"Sua conta no sistema MAG está pronta"',
    'email_notifications.user_invite_subject': '"Você foi convidado para um projeto no sistema MAG"',
    'email_notifications.user_invite_message': [('um projeto no Leantime.', 'um projeto no sistema MAG.'), (BOTAO_ANTIGO, BOTAO_MAG)],
    'email_notifications.password_reset_subject': '"Redefinição de senha do sistema MAG"',
    'email_notifications.password_reset_message': [('redefinição da senha do Leantime.', 'redefinição da sua senha no sistema MAG.'), (BOTAO_ANTIGO, BOTAO_MAG)],
    'email_notifications.latest_updates_subject': '"MAG - Últimas atualizações"',
    'tour.congratulations_kanban_text': '"Você completou o tour!<br/>Se precisar de ajuda, fale com o administrador do sistema."',
    'description.valuecanvas': [('O Canvas de Valor do Projeto do Leantime permite', 'O Canvas de Valor do Projeto permite')],
    'headlines.connector': '"Integrações"',
    'text.logo_reset': '"Para voltar ao logotipo padrão, clique no botão abaixo"',
    'tooltip.link_milestones_tooltip': [('Marcos no Leantime agrupam', 'Marcos agrupam')],
    'checklist.timeline.tasks.createMilestones': [('Marcos no Leantime agrupam', 'Marcos agrupam')],
    'label.import_ical_content': '"Você pode importar qualquer calendário que suporte o formato iCal. Isso inclui Google Calendar, Outlook, Apple Calendar e muitos outros."',
    'menu.apps': '"<span class=\'fa fa-fw fa-puzzle-piece\'></span> Apps"',
    'menu.leantime_apps': '"<span class=\'fa fa-fw fa-puzzle-piece\'></span> Apps"',
    'menu.leantime_apps_tooltip': '"Apps"',
    'marketplace.certified_tooltip': '"Plugin com assinatura verificada"',
    'text.get_organized_with_projects': [('O Leantime gerencia seu trabalho', 'O sistema organiza seu trabalho')],
    'text.ical_title': '"Calendário MAG"',
    'text.ical.todo_is_due': '"Uma tarefa vence em breve."',
    'text.ical.todo_start_alert': '"Uma tarefa está agendada para começar em breve"',
    'widget.descriptions.implementation_intentions': [(re.compile(r" <a href='https://support\.leantime\.io[^']*' target='_blank'>[^<]*</a>"), '')],
    'text.milestone_helper_content': [('No Leantime, marcos são fases', 'Marcos são fases')],
    'text.not_found_helper_content_simple': '"<p>Ainda não há conteúdo de ajuda para esta página. Se tiver dificuldades, fale com o administrador do sistema.</p>"',
    'text.discordChat': '"Em caso de dúvidas, fale com o administrador do sistema."',
    'menu.support_us': '"<span class=\'fa-solid fa-heart\'></span> Suporte"',
    'menu.leantime_community': '"Comunidade"',
    'link.support_us': '"Suporte"',
    # Aba Tema do perfil (sem tradução no pt-BR original)
    'tabs.personal_access_tokens': '"Tokens de acesso pessoal"',
    'headlines.personal_access_tokens': '"Tokens de acesso pessoal"',
    # Formatos do Brasil: o pt-BR original vinha com 12 h (AM/PM) e semana a partir de domingo.
    # Vale para quem não escolheu outro formato no perfil (Perfil → Configurações).
    'language.timeformat': '"H:i"',
    'language.jstimeformat': '"HH:mm"',
    'language.firstDayOfWeek': '"1"',
    # Traduções que o pt-BR original deixou em inglês
    'labels.tags': '"Etiquetas"',
    'menu.project_value_canvas': '"<span class=\'fa-solid fa-ranking-star\'></span> Canvas de Valor do Projeto"',
}

EN = {
    'headlines.welcome': '"Welcome!"',
    'headlines.welcome_to_leantime': '"Welcome to MAG!"',
    'text.welcome_to_leantime': '"You were invited to collaborate on a MAG project. Before you can get started please create your password."',
    'text.here_are_news': '"News from your projects"',
    'text.choose_access_for_users': '"Check or uncheck the users you want to add/remove."',
    'text.these_are_system_wide_settings': [('your leantime experience', 'the system')],
    'text.my_timesheets_helper_content': [('Overtime leantime', 'Overtime')],
    'text.show_projects_helper_content': [('heart of your business and leantime!', 'heart of your business!')],
    'text.new_db_version': [('To use Leantime', 'To use the system')],
    'text.ical_export_description': [('your Leantime calendar', 'your calendar')],
    'text.helpful_resources': [('make Leantime as simple', 'make the system as simple')],
    'text.documentation': [('usage of Leantime', 'usage of the system')],
    'label.open_in_leantime': '"Open in MAG"',
    'label.send_telemetry': '"Anonymous usage data"',
    'label.telemetry_background': '"Sending usage data outside MAG is disabled on this server."',
    'email_notifications.new_user_subject': '"Your MAG account is ready"',
    'email_notifications.user_invite_subject': '"You have been invited to join a project on MAG"',
    'email_notifications.user_invite_message': [('a project on Leantime.', 'a project on MAG.'), (BOTAO_ANTIGO, BOTAO_MAG)],
    'email_notifications.password_reset_subject': '"MAG Password Reset"',
    'email_notifications.password_reset_message': [('your Leantime password', 'your MAG password'), (BOTAO_ANTIGO, BOTAO_MAG)],
    'email_notifications.latest_updates_subject': '"MAG - Latest updates"',
    'tour.congratulations_kanban_text': '"You have completed the tour!<br/>If you need more help, please contact your system administrator."',
    'description.valuecanvas': [("Leantime's Project Value Canvas", 'The Project Value Canvas')],
    'headlines.connector': '"Integrations"',
    'text.logo_reset': '"To reset to the default logo, please click the button below"',
    'tooltip.link_milestones_tooltip': [('Milestones in Leantime take', 'Milestones take')],
    'checklist.timeline.tasks.createMilestones': [('Milestones in Leantime take', 'Milestones take')],
    'label.import_ical_content': '"You can import any calendar that supports the iCal format. This includes Google Calendar, Outlook, Apple Calendar and many more."',
    'label.connect_calendar_description': [('your Leantime tasks', 'your tasks')],
    'label.more_integrations_hint': '"More calendar integrations may be added to the system."',
    'menu.apps': '"<span class=\'fa fa-fw fa-puzzle-piece\'></span> Apps"',
    'menu.leantime_apps': '"<span class=\'fa fa-fw fa-puzzle-piece\'></span> Apps"',
    'menu.leantime_apps_tooltip': '"Apps"',
    'marketplace.certified_tooltip': '"Signature verified plugin"',
    'text.get_organized_with_projects': [('Leantime manages your work', 'The system manages your work')],
    'text.ical_title': '"MAG Calendar"',
    'text.ical.todo_is_due': '"A To-Do is due soon."',
    'text.ical.todo_start_alert': '"A To-Do is scheduled to be worked on soon"',
    'widget.descriptions.implementation_intentions': [(re.compile(r" <a href='https://support\.leantime\.io[^']*' target='_blank'>[^<]*</a>"), '')],
    'text.milestone_helper_content': [('Milestones in Leantime are considered', 'Milestones are considered')],
    'text.not_found_helper_content_simple': '"<p>We don\'t have help content for this page yet. If you have trouble navigating, please contact your system administrator.</p>"',
    'text.discordChat': '"If you have questions, please contact your system administrator."',
    'menu.support_us': '"<span class=\'fa-solid fa-heart\'></span> Support"',
    'menu.leantime_community': '"Community"',
    'link.support_us': '"Support"',
}


def carregar(arquivo: Path) -> dict:
    valores = {}
    for linha in arquivo.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^\s*([^;#=\s][^=]*?)\s*=\s*(.*)$', linha)
        if m:
            valores[m.group(1)] = m.group(2)
    return valores


TRADUCOES = Path(__file__).resolve().parent / 'traducoes'


def traducoes_em_arquivo(idioma: str) -> dict:
    """Traduções das chaves que o Leantime deixou sem tradução (tools/traducoes/*.<idioma>.ini)."""
    valores = {}
    for arquivo in sorted(TRADUCOES.glob(f'*.{idioma}.ini')):
        valores.update(carregar(arquivo))
    return valores


def gerar(idioma: str, regras: dict) -> None:
    # Arquivos de tradução primeiro; as regras deste script (marca, formatos) prevalecem
    regras = {**traducoes_em_arquivo(idioma), **regras}
    original = carregar(ORIGINAL / f'{idioma}.ini')
    base_en = carregar(ORIGINAL / 'en-US.ini')
    linhas = [
        f'; MAG — textos sem a marca Leantime, traduções faltantes e formatos do Brasil ({idioma}). Gerado por tools/gerar_idiomas.py.',
        '; Só contém as chaves alteradas; o restante vem de app/Language.',
        '',
    ]
    for chave, regra in regras.items():
        if isinstance(regra, str):
            valor = regra
        else:
            valor = original.get(chave, base_en.get(chave))
            if valor is None:
                raise SystemExit(f'{idioma}: chave inexistente {chave}')
            for antigo, novo in regra:
                if isinstance(antigo, re.Pattern):
                    valor, n = antigo.subn(novo, valor)
                else:
                    n = valor.count(antigo)
                    valor = valor.replace(antigo, novo)
                if n != 1:
                    raise SystemExit(f'{idioma}: {chave}: trecho encontrado {n} vezes: {antigo!r}')
        if re.search('leantime', valor, re.I):
            raise SystemExit(f'{idioma}: {chave} ainda cita Leantime: {valor[:120]}')
        linhas.append(f'{chave}={valor}')

    # Toda chave do idioma que cita Leantime precisa estar coberta
    faltando = [k for k, v in original.items() if re.search('leantime', v, re.I) and k not in regras]
    if faltando:
        raise SystemExit(f'{idioma}: chaves sem tratamento: {faltando}')

    DESTINO.mkdir(parents=True, exist_ok=True)
    (DESTINO / f'{idioma}.ini').write_bytes(('\n'.join(linhas) + '\n').encode('utf-8'))
    print(f'{idioma}: {len(regras)} chaves')


if __name__ == '__main__':
    gerar('pt-BR', PT)
    gerar('en-US', EN)
