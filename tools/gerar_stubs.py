"""Gera os controllers "vazios" que removem marketplace, apps, novidades e doação do Leantime.

As classes continuam existindo porque o classmap otimizado do Composer as referencia:
apagar o arquivo faria a rota responder 500. Sem métodos get/post/run, o Frontcontroller
não encontra método válido e responde 404.
"""
from pathlib import Path

OVERLAY = Path(__file__).resolve().parent.parent / 'overlay' / 'app'

STUBS = [
    # (arquivo, namespace, classe-base, classe, $view do HTMX ou None, o que era)
    ('Domain/Plugins/Controllers/Marketplace.php', r'Leantime\Domain\Plugins\Controllers', 'Controller', 'Marketplace', None,
     'loja de apps do Leantime (marketplace.leantime.io)'),
    ('Domain/Plugins/Controllers/Details.php', r'Leantime\Domain\Plugins\Controllers', 'Controller', 'Details', None,
     'página de detalhes de app da loja do Leantime'),
    ('Domain/Plugins/Controllers/Myapps.php', r'Leantime\Domain\Plugins\Controllers', 'Controller', 'Myapps', None,
     'tela "Meus Apps" (gestão de apps/extensões do Leantime)'),
    ('Domain/Plugins/Hxcontrollers/Marketplaceplugins.php', r'Leantime\Domain\Plugins\Hxcontrollers', 'HtmxController',
     'Marketplaceplugins', 'plugins::partials.pluginlist', 'listagem de apps da loja do Leantime'),
    ('Domain/Plugins/Hxcontrollers/Details.php', r'Leantime\Domain\Plugins\Hxcontrollers', 'HtmxController', 'Details',
     'plugins::plugindetails', 'instalação de apps da loja do Leantime'),
    ('Domain/Notifications/Hxcontrollers/News.php', r'Leantime\Domain\Notifications\Hxcontrollers', 'HtmxController', 'News',
     'notifications::partials.latestNews', 'feed de novidades do blog leantime.io'),
    ('Domain/Notifications/Hxcontrollers/NewsBadge.php', r'Leantime\Domain\Notifications\Hxcontrollers', 'HtmxController',
     'NewsBadge', 'notifications::partials.newsBadge', 'contador de novidades do blog leantime.io'),
    ('Domain/Help/Controllers/Support.php', r'Leantime\Domain\Help\Controllers', 'Controller', 'Support', None,
     'página "Apoie o Leantime" (doações ao projeto Leantime)'),
]

TEMPLATE = r'''<?php

namespace {ns};

use Leantime\Core\Controller\{base};

/**
 * MAG: removido da base — {what}.
 *
 * A classe continua existindo porque o classmap otimizado do Composer a referencia
 * (apagar o arquivo faria a rota responder 500). Sem métodos get/post/run, o
 * Frontcontroller não encontra método válido e qualquer acesso responde 404.
 */
class {cls} extends {base}
{{
{view}}}
'''

for path, ns, base, cls, view, what in STUBS:
    view_line = f"    protected static string $view = '{view}';\n" if view else ''
    content = TEMPLATE.format(ns=ns, base=base, cls=cls, what=what, view=view_line)
    target = OVERLAY / path
    target.write_text(content, encoding='utf-8', newline='\n')
    print('stub', path)
